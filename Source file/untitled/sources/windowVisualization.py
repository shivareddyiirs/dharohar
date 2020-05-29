import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import QThread, SIGNAL, QString, QStringList
import PyQt4.uic as uic
import psycopg2, operator, io
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import numpy as np
import cv2, copy
import FileDialog
from skimage.feature import greycomatrix, greycoprops
from tableVisualization import tableVisualization
from figureViewDialog import figureViewDialog
from credits import credits
from contactus import contactUs
import webbrowser
import subprocess
import os
from skimage.measure import compare_ssim
import imutils
from skimage.filters import sobel, scharr, prewitt, laplace
from scipy import ndimage as ndi
from skimage import feature
uiFile = "forms/windowVisualization.ui"
windowVisualizationUI, QtBaseClass = uic.loadUiType(uiFile)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class MyTableModel(QtCore.QAbstractTableModel):

    def __init__(self, data_list, header_row, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.table_data = data_list
        self.header = header_row

    def rowCount(self, parent):
        return len(self.table_data)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(str(self.table_data[index.row()][index.column()]))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.header[col])
        return QtCore.QVariant()

    def sort(self, Ncol, order):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.table_data = sorted(self.table_data, key=operator.itemgetter(Ncol))
        if order == QtCore.Qt.DescendingOrder:
            self.table_data.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))


class texturethread(QThread):

    def __init__(self, d, a, sarraster):
        QThread.__init__(self)
        self.d = d
        self.a = a
        self.sarraster = sarraster
        self.stopFlag = False

    def stop(self):
        self.stopFlag = True
        self.terminate()

    def __del__(self):
        self.wait()

    def run(self):
        contrastraster = np.copy(self.sarraster)
        contrastraster[:] = 0
        k=1 # k is used to overcome memory management problem
        # print contrastraster
        dissimilarityraster = np.copy(self.sarraster)
        dissimilarityraster[:] = 0
        k=2
        homogeneityraster = np.copy(self.sarraster)
        homogeneityraster[:] = 0
        k=3
        energyraster = np.copy(self.sarraster)
        energyraster[:] = 0
        k=4
        correlationraster = np.copy(self.sarraster)
        correlationraster[:] = 0
        ASMraster = np.copy(self.sarraster)
        ASMraster[:] = 0
        k=5
        # Create figure to receive results
        for i in range(3,self.sarraster.shape[0]-4,1):  # returns the no of rows
            for j in range(3,self.sarraster.shape[1]-4,1):  # returns the no of columns
                # Define size of moving window
                glcm_window = self.sarraster[i: i + 4, j : j + 4]
                # Calculate GLCM and textures
                glcm = greycomatrix(glcm_window, [self.d], [self.a], symmetric=True,
                                    normed=True)
                # Calculate texture and write into raster where moving window is centered
                contrastraster[i, j] = greycoprops(glcm, 'contrast')
                dissimilarityraster[i, j] = greycoprops(glcm, 'dissimilarity')
                homogeneityraster[i, j] = greycoprops(glcm, 'homogeneity')
                energyraster[i, j] = greycoprops(glcm, 'energy')
                correlationraster[i, j] = greycoprops(glcm, 'correlation')
                ASMraster[i, j] = greycoprops(glcm, 'ASM')
        self.emit(SIGNAL(
            'textureDone(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)'),
                  contrastraster, dissimilarityraster, homogeneityraster, energyraster, correlationraster, ASMraster)
        self.exit(0)


class queryDatabase(QThread):

    def __init__(self, sql, conn, header_row, table, tab, img='pre'):
        QThread.__init__(self)
        self.sql = sql
        self.cursor = conn.cursor()
        self.conn = conn
        self.header_row = header_row
        self.table = table
        self.tab = tab
        self.img = img

    def __del__(self):
        self.wait()

    def run(self):
        queryResult = []
        try:
            self.cursor.execute(self.sql)
            if self.table:
                queryResult = self.cursor.fetchall()
            else:
                queryResult = self.cursor.fetchone()
            self.emit(SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                      queryResult, self.header_row, self.table, self.tab, self.img, True)
        except psycopg2.ProgrammingError:
            self.conn.rollback()
            self.emit(SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                      queryResult, self.header_row, self.table, self.tab, self.img, False)


class windowVisualization(QtGui.QMainWindow, windowVisualizationUI):

    def __init__(self, user, password, db, host, port, project, isNew, myParent, parent=None, lang='English'):
        super(windowVisualization, self).__init__(parent)
        self.setupUi(self)
        self.label_4.setPixmap(QtGui.QPixmap("images/icon.png"))
        self.iirsLogo.setPixmap(QtGui.QPixmap("images/iirs.png"))
        self.label_12.setPixmap(QtGui.QPixmap("images/ISRO.gif"))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle(project + ' - Project Visualization - Dharohar')
        self.btnRefresh.setIcon(QtGui.QIcon('images/ref.png'))
        self.setFixedSize(self.size())
        self.lblProjectNoti.setVisible(False)
        self.setSignals()
        self.username = user
        self.myParent = myParent
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.project = project
        self.lang = str(lang)
        self.txtProject.setText(self.project)
        self.txtUser.setText(self.username)
        self.tabImageProcessing.setCurrentIndex(0)
        self.conn = psycopg2.connect(database=self.db, user=self.username, host=self.host, password=self.password,
                                         port=self.port)
        self.cursor = self.conn.cursor()
        if not isNew:
            sql = "SELECT usename FROM pg_user, pg_group WHERE usesysid=ANY(grolist) AND groname='" + self.db + \
                  "_project_admins'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            superusers = []
            for row in rows:
                superusers.append(row[0])
            if self.username not in superusers:
                self.cursor.execute("SELECT privilege_type FROM information_schema.role_table_grants "
                                    "WHERE table_name='" + self.project + "_image' AND grantee='" + self.username + "'")
                rows = self.cursor.fetchall()
                privileges = [row[0] for row in rows]
                if 'INSERT' not in privileges:
                    self.btnPointCloud.setEnabled(False)
                    self.btnPointCloud.setFlat(True)
                    self.lblProjectNoti.setText("You don't have write permissions for this project.")
                    self.lblProjectNoti.setVisible(True)
                if 'SELECT' not in privileges:
                    self.frameVisualization.setEnabled(False)
                    self.lblProjectNoti.setText("You don't have read permissions for this project.")
                    self.lblProjectNoti.setVisible(True)
        else:
            self.lblProjectNoti.setText("There's nothing in the project to select or view from the database.")
            self.lblProjectNoti.setVisible(True)
            self.btnLoadImgDB.setEnabled(False)
            self.btnChgLoadPreDB.setEnabled(False)
            self.btnChgLoadPostDB.setEnabled(False)
            self.btnLoadImgList.setEnabled(False)
            # self.btnLoadImgList.setStyleSheet("background-color: white; color:rgb(70,0,0);")
            self.btnTextLoadDB.setEnabled(False)
            self.btnVisualize.setEnabled(False)

            self.btnLoadImgDB.setFlat(True)
            self.btnChgLoadPreDB.setFlat(True)
            self.btnChgLoadPostDB.setFlat(True)
            self.btnLoadImgList.setFlat(True)
            self.btnTextLoadDB.setFlat(True)
            self.btnVisualize.setFlat(True)

        self.tables = []
        self.imageWindows = []
        self.analysisImage = None
        self.chgPreImg = None
        self.chgPostImg = None
        self.textureImg = None
        self.pointAvailability = None
        self.imageWindow = None
        self.imageFromDB = None
        self.child = None
        self.childs = []

    def refresh(self):
        self.conn.close()
        self.conn = psycopg2.connect(database=self.db, user=self.username, host=self.host, password=self.password,
                                     port=self.port)
        self.cursor = self.conn.cursor()
        sql = "SELECT usename FROM pg_user, pg_group WHERE usesysid=ANY(grolist) AND groname='" + self.db + \
              "_project_admins'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        superusers = []
        for row in rows:
            superusers.append(row[0])
        if self.username in superusers:
            sql = "SELECT DISTINCT tablename FROM pg_tables WHERE tablename='" + self.project + \
                  "image'"
        else:
            sql = "SELECT DISTINCT table_name FROM information_schema.table_privileges WHERE grantee='" + \
                  self.username + "' AND table_name='" + self.project + "_image'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            self.lblProjectNoti.setText('There is nothing in the project to view from the database. Try saving first.')
        else:
            self.lblProjectNoti.setVisible(False)
            self.btnLoadImgDB.setEnabled(True)
            self.btnChgLoadPreDB.setEnabled(True)
            self.btnChgLoadPostDB.setEnabled(True)
            self.btnLoadImgList.setEnabled(True)
            self.btnTextLoadDB.setEnabled(True)
            self.btnVisualize.setEnabled(True)

            self.btnLoadImgDB.setFlat(False)
            self.btnChgLoadPreDB.setFlat(False)
            self.btnChgLoadPostDB.setFlat(False)
            self.btnLoadImgList.setFlat(False)
            self.btnTextLoadDB.setFlat(False)
            self.btnVisualize.setFlat(False)

    def help(self, event):
        webbrowser.open_new_tab(os.getcwd() + '/document/Complete User_manual.pdf')

    def credit(self):
        self.creditsWindow = credits()
        self.creditsWindow.exec_()

    def contact(self):
        self.contactWindow = contactUs()
        self.contactWindow.exec_()

    def setSignals(self):
        self.btnPointCloud.clicked.connect(self.pointCloud)
        self.rBtn3D.toggled.connect(self.pointAttrTypeChanged)
        self.rBtnRDT.toggled.connect(self.pointAttrTypeChanged)
        self.btnLoadImgList.clicked.connect(self.loadImgList)
        self.btnLoadImgDB.clicked.connect(self.anaLoadImgDB)
        self.btnLoadImgFile.clicked.connect(self.anaLoadImgFile)
        self.btnAnalysisProcess.clicked.connect(self.analysisProcess)
        self.btnAnalysisView.clicked.connect(self.analysisView)
        self.btnChgLoadPreDB.clicked.connect(self.chgLoadPreDB)
        self.btnChgLoadPostDB.clicked.connect(self.chgLoadPostDB)
        self.btnChgPreView.clicked.connect(self.chgPreView)
        self.btnChgPostView.clicked.connect(self.chgPostView)
        self.btnChgLoadPostFile.clicked.connect(self.chgLoadPostFile)
        self.btnChgLoadPreFile.clicked.connect(self.chgLoadPreFile)
        self.btnDetect.clicked.connect(self.detectChange)
        self.btnTextLoadDB.clicked.connect(self.textLoadDB)
        self.btnTextLoadFile.clicked.connect(self.textLoadFile)
        self.btnTextView.clicked.connect(self.textView)
        self.btnAnalyze.clicked.connect(self.textureAnalysis)
        self.btnVisualize.clicked.connect(self.pointVisualize)
        self.actionHelp.triggered.connect(self.help)
        self.actionCredits.triggered.connect(self.credit)
        self.actionContact_US.triggered.connect(self.contact)
        self.btnViewBandImg.clicked.connect(self.textViewBand)
        self.btnViewBandPix.clicked.connect(self.textViewPixels)
        self.btnStatistics.clicked.connect(self.textStatistics)
        self.btnRefresh.clicked.connect(self.refresh)
        self.label_5.mousePressEvent = self.help
        self.iirsLogo.mousePressEvent = self.gotoIIRS

    def gotoIIRS(self, event):
        webbrowser.open_new_tab("https://www.iirs.gov.in/")

    def pointCloud(self):
        parameters = self.project + ' '
        parameters += self.username + ' '
        parameters += self.password + ' '
        print self.host
        if self.host == '':
            parameters += 'localhost '
        else:
            parameters += self.host + ' '
        parameters += self.db + ' '
        if self.port == '':
            parameters += '5432 '
        else:
            parameters += self.port + ' '
        parameters += self.lang
        self.child = subprocess.Popen('release/untitled.exe ' + parameters)
        self.childs.append(self.child)

    def closeEvent(self, event):
        for table in self.tables:
            table.close()
        for imageWindow in self.imageWindows:
            imageWindow.close()
        for child in self.childs:
            child.terminate()
        sql = "SELECT usename FROM pg_user, pg_group WHERE usesysid=ANY(grolist) AND groname='" + self.db + \
              "_project_admins'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        superusers = []
        for row in rows:
            superusers.append(row[0])
        if self.username in superusers:
            sql = "SELECT DISTINCT tablename FROM pg_tables WHERE tablename SIMILAR TO '%_(image|xyz|rdt)'"
        else:
            sql = "SELECT DISTINCT table_name FROM information_schema.table_privileges WHERE grantee='" + self.username \
                  + "' AND table_name SIMILAR TO '%_(image|xyz|rdt)'"
        self.myParent.conn.close()
        self.myParent.conn = psycopg2.connect(database=self.db, user=self.username, host=self.host, password=self.password,
                                     port=self.port)
        self.myParent.cursor = self.conn.cursor()
        self.myParent.cursor.execute(sql)
        rows = self.myParent.cursor.fetchall()
        self.myParent.projects = []
        self.myParent.cbProject.clear()
        self.myParent.cbProject.addItem(QString('New Project...'))
        for row in rows:
            tablename = row[0]
            project = tablename.split('_')[0]
            self.myParent.projects.append(project)
        self.myParent.cbProject.addItems(QStringList(list(set(self.myParent.projects))))
        self.myParent.show()

    def visualizeResult(self, queryResult, header_row, table, tab, img='pre', success=False):
        if not success:
            self.queryThread.terminate()
            self.lblImgAnalysisNoti.setVisible(False)
            self.lblChgNoti.setVisible(False)
            self.lblTextNoti.setVisible(False)
            self.lblPointNoti.setVisible(False)
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Database operations are not possible with new projects.\nTry again after saving data.')
            message.setWindowTitle('Database Access Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            self.lblImgAnalysisNoti.setText('')
            self.lblChgNoti.setText('')
            self.lblTextNoti.setText('')
            self.lblPointNoti.setText('')
            self.lblImgAnalysisNoti.setVisible(True)
            self.lblChgNoti.setVisible(True)
            self.lblTextNoti.setVisible(True)
            self.lblPointNoti.setVisible(True)
            return

        if table:
            if not self.btnLoadImgList.isEnabled():
                dataModel = MyTableModel(queryResult, header_row, self)
                self.tvImgList.setModel(dataModel)
            elif tab == 3:
                if len(queryResult) == 0:
                    self.pointAvailability = False
                    return
                self.pointAvailability = True
                dataModel = MyTableModel(queryResult, header_row, self)
                self.tableWindow = tableVisualization(dataModel, img, queryResult, header_row)
                self.tableWindow.show()
                self.tables.append(self.tableWindow)
                self.txtPointRID.setText('')
        else:
            if tab == 0:
                self.analysisImage = Image.open(io.BytesIO(queryResult[0]))
            elif tab == 1:
                if img == 'pre':
                    self.chgPreImg = Image.open(io.BytesIO(queryResult[0]))
                else:
                    self.chgPostImg = Image.open(io.BytesIO(queryResult[0]))
            elif tab == 2:
                self.textureImg = Image.open(io.BytesIO(queryResult[0]))

    def pointVisualize(self):
        if not self.rBtn3D.isChecked() and not self.rBtnRDT.isChecked():
            self.lblPointNoti.setText('Please make a selection first.')
            return
        if self.rBtn3D.isChecked():
            if self.cbX.isChecked() or self.cbY.isChecked() or self.cbZ.isChecked():
                self.btnVisualize.setEnabled(False)
                self.btnVisualize.setFlat(True)
                self.lblPointNoti.setText('Processing...   Please wait...')
                columns = 'RID'
                header_row = ['RID']
                if self.cbX.isChecked():
                    columns += ', X'
                    header_row.append('X')
                if self.cbY.isChecked():
                    columns += ', Y'
                    header_row.append('Y')
                if self.cbZ.isChecked():
                    columns += ', Z'
                    header_row.append('Z')
                sql = 'SELECT ' + columns + ' FROM ' + self.project + '_xyz'
            else:
                self.lblPointNoti.setText('Select at least one from 3D Points.')
                return
        elif self.rBtnRDT.isChecked():
            if self.cbRadius.isChecked() or self.cbDepth.isChecked() or self.cbTheta.isChecked():
                self.btnVisualize.setEnabled(False)
                self.btnVisualize.setFlat(True)
                self.lblPointNoti.setText('Processing...   Please wait...')
                columns = 'RID'
                header_row = ['RID']
                if self.cbRadius.isChecked():
                    columns += ', R'
                    header_row.append('Radius')
                if self.cbDepth.isChecked():
                    columns += ', Depth'
                    header_row.append('Depth')
                if self.cbTheta.isChecked():
                    columns += ', Theta'
                    header_row.append('Theta')
                sql = 'SELECT ' + columns + ' FROM ' + self.project + '_rdt'
            else:
                self.lblPointNoti.setText('Select at least one from Radius, Depth and Theta.')
                return
        rid = str(self.txtPointRID.text())
        if rid != '':
            if not rid.isdigit():
                self.lblPointNoti.setText('RID must be an integer.')
                self.btnVisualize.setEnabled(True)
                self.btnVisualize.setFlat(True)
                self.txtPointRID.setFocus()
                return
            else:
                sql += ' WHERE RID = ' + rid
        rev = columns[:: -1]
        second = rev[: rev.index(',') - 1]
        columns = rev[rev.index(',') + 1:]
        heading = columns[:: -1] + ' and ' + second[:: -1]
        self.queryThread = queryDatabase(sql, self.conn, header_row, True, 3, heading)
        self.connect(self.queryThread,
                     SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                     self.visualizeResult)
        self.connect(self.queryThread, SIGNAL("finished()"), self.pointDone)
        self.queryThread.start()

    def pointDone(self):
        self.btnVisualize.setEnabled(True)
        self.btnVisualize.setFlat(False)
        if self.pointAvailability:
            self.lblPointNoti.setText('Processing done.')
        else:
            self.lblPointNoti.setText('No records found. May be RID is not available.')

    def loadImgListDone(self):
        self.btnLoadImgList.setEnabled(True)
        self.btnLoadImgList.setFlat(False)
        self.lblImgAnalysisNoti.setText('Image list loaded from database.')

    def loadImgList(self):
        sql = 'SELECT RID, FILENAME FROM ' + self.project + '_image'
        header_row = ['Image ID', 'File Name']
        self.queryThread = queryDatabase(sql, self.conn, header_row, True, -1, '')
        self.connect(self.queryThread, SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'), self.visualizeResult)
        self.connect(self.queryThread, SIGNAL('finished()'), self.loadImgListDone)
        self.queryThread.start()
        self.lblImgAnalysisNoti.setText('Loading...   Please wait...')
        self.btnLoadImgList.setEnabled(False)
        self.btnLoadImgList.setFlat(True)

    def pointAttrTypeChanged(self):
        if self.rBtn3D.isChecked():
            self.gbSel3D.setEnabled(True)
            self.gbSelRDT.setEnabled(False)
        else:
            self.gbSel3D.setEnabled(False)
            self.gbSelRDT.setEnabled(True)

    def anaLoadImgDBDone(self):
        self.btnLoadImgDB.setEnabled(True)
        self.btnLoadImgDB.setFlat(False)
        self.lblImgAnalysisNoti.setText('Image loaded from database.')

    def anaLoadImgDB(self):
        rid = str(self.txtImgAnaID.text())
        if rid == '':
            self.lblImgAnalysisNoti.setText('Error: Image ID field cannot be blank.')
            return
        if not rid.isdigit():
            self.lblImgAnalysisNoti.setText('Error: Image ID must be numeric.')
            return
        else:
            sql = "SELECT RID FROM " + self.project + "_image WHERE RID = " + rid
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is None:
                self.lblImgAnalysisNoti.setText('Error: Invalid image ID.')
                return
            sql = "SELECT ST_AsGDALRaster(rast, 'GTiff', ARRAY['QUALITY=100']) from " + self.project + \
                  "_image where rid = " + rid
            header_row = []
            self.queryThread = queryDatabase(sql, self.conn, header_row, False, 0, '')
            self.connect(self.queryThread, SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                         self.visualizeResult)
            self.connect(self.queryThread, SIGNAL('finished()'), self.anaLoadImgDBDone)
            self.queryThread.start()
            self.lblImgAnalysisNoti.setText('Loading...   Please wait...')
            self.btnLoadImgDB.setEnabled(False)
            self.btnLoadImgDB.setFlat(True)
            self.txtImgAnaID.setText('')

    def textLoadDBDone(self):
        self.imageFromDB = True
        self.btnTextLoadDB.setEnabled(True)
        self.btnTextLoadDB.setFlat(False)
        self.lblTextNoti.setText('Image loaded from database.')

    def textLoadDB(self):
        rid = str(self.txtTextureID.text())
        if rid == '':
            self.lblTextNoti.setText('Error: Image ID field cannot be blank.')
            return
        if not rid.isdigit():
            self.lblTextNoti.setText('Error: Image ID must be numeric.')
            return
        else:
            sql = "SELECT RID FROM " + self.project + "_image WHERE RID = " + rid
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is None:
                self.lblTextNoti.setText('Error: Invalid image ID.')
                return
            sql = "SELECT ST_AsGDALRaster(rast, 'GTiff', ARRAY['QUALITY=100']) from " + self.project + \
                  "_image where rid = " + rid
            header_row = []
            self.queryThread = queryDatabase(sql, self.conn, header_row, False, 2, '')
            self.connect(self.queryThread, SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                         self.visualizeResult)
            self.connect(self.queryThread, SIGNAL('finished()'), self.textLoadDBDone)
            self.queryThread.start()
            self.lblTextNoti.setText('Loading...   Please wait...')
            self.btnTextLoadDB.setEnabled(False)
            self.btnTextLoadDB.setFlat(True)
            self.txtTextureID.setText('')

    def chgLoadPreDBDone(self):
        self.btnChgLoadPreDB.setEnabled(True)
        self.btnChgLoadPreDB.setFlat(False)
        self.lblChgNoti.setText('Pre Image loaded from database.')

    def chgLoadPreDB(self):
        rid = str(self.txtChgDetRID.text())
        if rid == '':
            self.lblChgNoti.setText('Error: Image ID field cannot be blank.')
            return
        if not rid.isdigit():
            self.lblChgNoti.setText('Error: Image ID must be numeric.')
            return
        else:
            sql = "SELECT RID FROM " + self.project + "_image WHERE RID = " + rid
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is None:
                self.lblChgNoti.setText('Error: Invalid image ID.')
                return
            sql = "SELECT ST_AsGDALRaster(rast, 'GTiff', ARRAY['QUALITY=100']) from " + self.project + \
                  "_image where rid = " + rid
            header_row = []
            self.queryThread = queryDatabase(sql, self.conn, header_row, False, 1, 'pre')
            self.connect(self.queryThread, SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                         self.visualizeResult)
            self.connect(self.queryThread, SIGNAL('finished()'), self.chgLoadPreDBDone)
            self.queryThread.start()
            self.lblChgNoti.setText('Loading...   Please wait...')
            self.btnChgLoadPreDB.setEnabled(False)
            self.btnChgLoadPreDB.setFlat(True)
            self.txtChgDetRID.setText('')

    def chgLoadPostDBDone(self):
        self.btnChgLoadPostDB.setEnabled(True)
        self.btnChgLoadPostDB.setFlat(False)
        self.lblChgNoti.setText('Post Image loaded from database.')

    def chgLoadPostDB(self):
        rid = str(self.txtChgDetRID.text())
        if rid == '':
            self.lblChgNoti.setText('Error: Image ID field cannot be blank.')
            return
        if not rid.isdigit():
            self.lblChgNoti.setText('Error: Image ID must be numeric.')
            return
        else:
            sql = "SELECT RID FROM " + self.project + "_image WHERE RID = " + rid
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is None:
                self.lblChgNoti.setText('Error: Invalid image ID.')
                return
            sql = "SELECT ST_AsGDALRaster(rast, 'GTiff', ARRAY['QUALITY=100']) from " + self.project + \
                  "_image where rid = " + rid
            header_row = []
            self.queryThread = queryDatabase(sql, self.conn, header_row, False, 1, 'post')
            self.connect(self.queryThread, SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool, int, PyQt_PyObject, bool)'),
                         self.visualizeResult)
            self.connect(self.queryThread, SIGNAL('finished()'), self.chgLoadPostDBDone)
            self.queryThread.start()
            self.lblChgNoti.setText('Loading...   Please wait...')
            self.btnChgLoadPostDB.setEnabled(False)
            self.btnChgLoadPostDB.setFlat(True)
            self.txtChgDetRID.setText('')

    def anaLoadImgFile(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None,
                                                         QtGui.QFileDialog.DontUseNativeDialog))
        if not filename:
            self.lblImgAnalysisNoti.setText('Could not load image file.')
        else:
            self.analysisImage = Image.open(filename)
            self.lblImgAnalysisNoti.setText('Image loaded from file.')

    def textLoadFile(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None,
                                                         QtGui.QFileDialog.DontUseNativeDialog))
        if not filename:
            self.lblTextNoti.setText('Could not load image file.')
        else:
            self.textureImg = Image.open(filename)
            self.imageFromDB = False
            self.lblTextNoti.setText('Image loaded from file.')

    def chgLoadPreFile(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None,
                                                         QtGui.QFileDialog.DontUseNativeDialog))
        if not filename:
            self.lblChgNoti.setText('Could not load image file.')
        else:
            self.chgPreImg = Image.open(filename)
            self.lblChgNoti.setText('Pre Image loaded from file.')

    def chgLoadPostFile(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None,
                                                         QtGui.QFileDialog.DontUseNativeDialog))
        if not filename:
            self.lblChgNoti.setText('Could not load image file.')
        else:
            self.chgPostImg = Image.open(filename)
            self.lblChgNoti.setText('Post Image loaded from file.')

    def analysisView(self):
        if self.analysisImage is None:
            self.lblImgAnalysisNoti.setText('Please load an image before viewing.')
            return
        self.lblImgAnalysisNoti.setText('')

        titles = ['Image']
        images = [self.analysisImage]
        windowTitle = 'Image Analysis - Dharohar'
        self.imageWindow = figureViewDialog(titles, images, windowTitle)
        self.imageWindow.show()
        self.imageWindows.append(self.imageWindow)

    def textView(self):
        if self.textureImg is None:
            self.lblTextNoti.setText('Please load an image before viewing.')
            return
        self.lblTextNoti.setText('')

        titles = ['Image']
        images = [self.textureImg]
        windowTitle = 'Image (Texture Analysis) - Dharohar'

        self.imageWindow = figureViewDialog(titles, images, windowTitle)
        self.imageWindow.show()
        self.imageWindows.append(self.imageWindow)

    def chgPreView(self):
        if self.chgPreImg is None:
            self.lblChgNoti.setText('Please load an image before viewing.')
            return
        self.lblChgNoti.setText('')

        titles = ['Pre Image']
        images = [self.chgPreImg]
        windowTitle = 'Pre Image (Change Detection) - Dharohar'

        self.imageWindow = figureViewDialog(titles, images, windowTitle)
        self.imageWindow.show()
        self.imageWindows.append(self.imageWindow)

    def chgPostView(self):
        if self.chgPostImg is None:
            self.lblChgNoti.setText('Please load an image before viewing.')
            return
        self.lblChgNoti.setText('')

        titles = ['Post Image']
        images = [self.chgPostImg]
        windowTitle = 'Post Image (Change Detection) - Dharohar'

        self.imageWindow = figureViewDialog(titles, images, windowTitle)
        self.imageWindow.show()
        self.imageWindows.append(self.imageWindow)

    def detectChange(self):
        if self.chgPreImg is None:
            self.lblChgNoti.setText('Please load pre image before processing.')
            return
        if self.chgPostImg is None:
            self.lblChgNoti.setText('Please load post image before processing.')
            return
        self.lblChgNoti.setText('Processing...   Please wait...')
        self.btnDetect.setEnabled(False)
        self.btnDetect.setFlat(True)
        try:
            image1 = self.chgPreImg.convert('RGB')
            image2 = self.chgPostImg.convert('RGB')
            imageA = np.asarray(image1)
            imageB = np.asarray(image2)
            grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
            grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
            (score, diff) = compare_ssim(grayA, grayB, full=True)
            diff = (diff * 255).astype("uint8")
            # print("SSIM: {}".format(score))
            thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

            titles = ['Pre Image', 'Post Image', 'Change']
            images = [image1, image2, diff]
            windowTitle = 'Change Detection - Dharohar'

            self.imageWindow = figureViewDialog(titles, images, windowTitle)
            self.imageWindow.show()
            self.imageWindows.append(self.imageWindow)
            self.lblChgNoti.setText('Processing done.')
        except ValueError:
            self.lblChgNoti.setText('Image properties does not match.')
        except:
            self.lblChgNoti.setText('Image format error.')
        self.btnDetect.setEnabled(True)
        self.btnDetect.setFlat(False)

    def textStatistics(self):
        if self.textureImg is None:
            self.lblTextNoti.setText('Please load an image before processing.')
            return
        self.lblTextNoti.setText('Processing...   Please wait...')

        org = self.textureImg
        rgb_im = org.convert('RGB')
        nx, ny = rgb_im.size
        im2 = rgb_im.resize((int(nx), int(ny)), Image.BICUBIC)
        r, g, b = im2.split()
        if self.rBtnRed.isChecked():
            pix_vals = np.asarray(r)
            heading = 'R-Band Statistics'
            band = 'RED'

        elif self.rBtnGreen.isChecked():
            pix_vals = np.asarray(g)
            heading = 'G-Band Statistics'
            band = 'GREEN'

        elif self.rBtnBlue.isChecked():
            pix_vals = np.asarray(b)
            heading = 'B-Band Statistics'
            band = 'BLUE'

        else:
            self.lblTextNoti.setText('Please select a colour.')
            return

        count = nx * ny
        sum = pix_vals.sum()
        mean = pix_vals.mean()
        std = pix_vals.std()
        mini = pix_vals.min()
        maxi = pix_vals.max()
        modified = [[band, count, sum, mean, std, mini, maxi]]
        header_row = ['BAND', 'COUNT', 'SUM', 'MEAN', 'STD. DEVIATION', 'MINIMUM', 'MAXIMUM']
        dataModel = MyTableModel(modified, header_row, self)
        self.tableWindow = tableVisualization(dataModel, heading, modified, header_row)
        self.tableWindow.show()
        self.tables.append(self.tableWindow)

        self.lblTextNoti.setText('Processing done.')

    def textViewPixels(self):
        if self.textureImg is None:
            self.lblTextNoti.setText('Please load an image before processing.')
            return
        self.lblTextNoti.setText('Processing...   Please wait...')

        org = self.textureImg
        rgb_im = org.convert('RGB')
        nx, ny = rgb_im.size
        im2 = rgb_im.resize((int(nx), int(ny)), Image.BICUBIC)
        r, g, b = im2.split()
        if self.rBtnRed.isChecked():
            pix_vals = np.reshape(np.asarray(r), (nx * ny))
            heading = 'R-Band Pixels'

        elif self.rBtnGreen.isChecked():
            pix_vals = np.reshape(np.asarray(g), (nx * ny))
            heading = 'G-Band Pixels'

        elif self.rBtnBlue.isChecked():
            pix_vals = np.reshape(np.asarray(b), (nx * ny))
            heading = 'B-Band Pixels'

        else:
            self.lblTextNoti.setText('Please select a colour.')
            return

        modified = np.zeros((nx * ny, 3), dtype=int)
        col_val = np.arange(nx).reshape((nx))
        for row in range(ny):
            modified[nx * row: nx * (row + 1), 0] = row
            modified[nx * row: nx * (row + 1), 1] = col_val
        modified[:, 2] = pix_vals
        modified = list(modified)

        header_row = ['ROW_NUMBER', 'COL_NUMBER', 'PIXEL_VALUE']
        dataModel = MyTableModel(modified, header_row, self)
        self.tableWindow = tableVisualization(dataModel, heading, modified, header_row)
        self.tableWindow.show()
        self.tables.append(self.tableWindow)

        self.lblTextNoti.setText('Processing done.')

    def textViewBand(self):
        if self.textureImg is None:
            self.lblTextNoti.setText('Please load an image before processing.')
            return
        self.lblTextNoti.setText('Processing...   Please wait...')

        org = self.textureImg
        rgb_im = org.convert('RGB')
        nx, ny = rgb_im.size
        im2 = rgb_im.resize((int(nx), int(ny)), Image.BICUBIC)
        r, g, b = im2.split()
        if self.rBtnRed.isChecked():
            sarraster = np.asarray(r)
            titles = ['R-Band - Original']
            windowTitle = 'R-Band - Original Image (Gray Scale) - Dharohar'

        elif self.rBtnGreen.isChecked():
            sarraster = np.asarray(g)
            titles = ['G-Band - Original']
            windowTitle = 'G-Band - Original Image (Gray Scale) - Dharohar'

        elif self.rBtnBlue.isChecked():
            sarraster = np.asarray(b)
            titles = ['B-Band - Original']
            windowTitle = 'B-Band - Original Image (Gray Scale) - Dharohar'

        else:
            self.lblTextNoti.setText('Please select a colour.')
            return

        images = [sarraster]
        self.lblTextNoti.setText('Processing done.')
        self.imageWindow = figureViewDialog(titles, images, windowTitle)
        self.imageWindow.show()
        self.imageWindows.append(self.imageWindow)

    def textureDone(self, contrastraster, dissimilarityraster, homogeneityraster, energyraster, correlationraster, ASMraster):
        titles = ['Contrast', 'Dissimilarity', 'Homogeneity', 'Energy', 'Correlation', 'ASM']
        images = [contrastraster, dissimilarityraster, homogeneityraster, energyraster, correlationraster, ASMraster]
        windowTitle = 'GLCM Textures - Dharohar'

        self.imageWindow = figureViewDialog(titles, images, windowTitle)
        self.imageWindow.showMaximized()
        self.imageWindows.append(self.imageWindow)
        self.btnAnalyze.setEnabled(True)
        self.btnAnalyze.setFlat(False)
        self.lblTextNoti.setText('Processing done.')
        self.qThread.terminate()
        self.qThread.exit()
        self.qThread.exec_()
        self.qThread.stop()

    def textureAnalysis(self):
        if self.textureImg is None:
            self.lblTextNoti.setText('Please load an image before processing.')
            return
        self.lblTextNoti.setText('Processing...   Please wait...')
        self.btnAnalyze.setEnabled(False)
        self.btnAnalyze.setFlat(True)
        org = self.textureImg
        rgb_im = org.convert('RGB')
        nx, ny = rgb_im.size
        im2 = rgb_im.resize((int(nx), int(ny)), Image.BICUBIC)
        r, g, b = im2.split()

        if self.rBtnRed.isChecked():
            sarraster = np.asarray(r)

        elif self.rBtnGreen.isChecked():
            sarraster = np.asarray(g)

        elif self.rBtnBlue.isChecked():
            sarraster = np.asarray(b)

        else:
            self.lblTextNoti.setText('Please select a colour.')
            self.btnAnalyze.setEnabled(True)
            self.btnAnalyze.setFlat(False)
            return

        if self.txtDistance.text().isEmpty():
            self.lblTextNoti.setText('Please enter a distance.')
            self.btnAnalyze.setEnabled(True)
            self.btnAnalyze.setFlat(False)
            return
        else:
            d = str(self.txtDistance.text())

        a = str(self.cbAngle.currentText())
        if len(a) > 3:
            self.lblTextNoti.setText('Please select an angle .')
            self.btnAnalyze.setEnabled(True)
            self.btnAnalyze.setFlat(False)
            return
        else:
            a = str(self.cbAngle.currentText())
        self.qThread = texturethread(d, a, sarraster)
        self.connect(self.qThread, SIGNAL('textureDone(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)'),
                        self.textureDone)
        self.qThread.start()

    def analysisProcess(self):
        if self.analysisImage is None:
            self.lblImgAnalysisNoti.setText('Please load an image before processing.')
            return
        self.lblImgAnalysisNoti.setText('Processing...   Please wait...')
        self.btnAnalysisProcess.setEnabled(False)
        self.btnAnalysisProcess.setFlat(True)
        new_img = self.analysisImage.convert('RGB')
        img_array = np.asarray(new_img)
        r, g, b = new_img.split()

        if self.rBtnCorner.isChecked():
            try:
                img_copy = copy.copy(img_array)
                gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
                # remove noise
                # img_data = cv2.GaussianBlur(gray, (3, 3), 0)
                gray = np.float32(gray)
                dst = cv2.cornerHarris(gray, 2, 3, 0.04)

                # result is dilated for marking the corners, not important
                dst = cv2.dilate(dst, None)

                # Threshold for an optimal value, it may vary depending on the image
                img_copy[dst > 0.001 * dst.max()] = [0, 0, 255]

                titles = ['Original', 'After Corner Extraction']
                images = [img_array, img_copy]
                windowTitle = 'Corner Extraction - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnRGB2IHS.isChecked():
            try:
                img_ihs = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

                titles = ['Original - RGB', 'IHS']
                images = [img_array, img_ihs]
                windowTitle = 'RGB to IHS - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnIHS2RGB.isChecked():
            try:
                img_rgb = cv2.cvtColor(img_array, cv2.COLOR_HSV2RGB)

                titles = ['Original - IHS', 'RGB']
                images = [img_array, img_rgb]
                windowTitle = 'IHS to RGB - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnLaplacian.isChecked():
            try:
                lap1 = laplace(r)
                lap2 = laplace(g)
                lap3 = laplace(b)

                titles = ['Original', 'R-band', 'G-Band', 'B-Band']
                images = [new_img, lap1, lap2, lap3]
                windowTitle = 'Laplacian Edge Detection - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnSobel.isChecked():
            try:
                sobel1 = sobel(r)
                sobel2 = sobel(g)
                sobel3 = sobel(b)

                titles = ['Original', 'R-Band Sobel', 'G-Band Sobel', 'B-Band Sobel']
                images = [new_img, sobel1, sobel2, sobel3]
                windowTitle = 'Sobel Edge Detection - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnPrewitt.isChecked():
            try:
                pre1 = prewitt(r)
                pre2 = prewitt(g)
                pre3 = prewitt(b)

                titles = ['Original', 'R-Band Prewitt', 'G-band Prewitt', 'B-Band Prewitt']
                images = [new_img, pre1, pre2, pre3]
                windowTitle = 'Prewitt Edge Detection - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnScharr.isChecked():
            try:
                sch1 = scharr(r)
                sch2 = scharr(g)
                sch3 = scharr(b)

                titles = ['Original', 'R-Band Scharr', 'G-Band Scharr', 'B-Band Scharr']
                images = [new_img, sch1, sch2, sch3]
                windowTitle = 'Scharr Edge Detection - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        elif self.rBtnCanny.isChecked():
            try:
                r = np.asarray(r, dtype='float64')
                g = np.asarray(g, dtype='float64')
                b = np.asarray(b, dtype='float64')

                im = ndi.gaussian_filter(r, 4)
                im += 0.2 * np.random.random(im.shape)

                im1 = ndi.gaussian_filter(g, 4)
                im1 += 0.2 * np.random.random(im1.shape)

                im2 = ndi.gaussian_filter(b, 4)
                im2 += 0.2 * np.random.random(im2.shape)

                cn1 = feature.canny(im, sigma=2)
                cn2 = feature.canny(im1, sigma=2)
                cn3 = feature.canny(im2, sigma=2)

                titles = ['Original', 'R-Band Canny', 'G-Band Canny', 'B-Band Canny']
                images = [new_img, cn1, cn2, cn3]
                windowTitle = 'Canny Edge Detection - Dharohar'
                self.imageWindow = figureViewDialog(titles, images, windowTitle)
                self.imageWindow.show()
                self.imageWindows.append(self.imageWindow)

                self.lblImgAnalysisNoti.setText('Processing done.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)
            except:
                self.lblImgAnalysisNoti.setText('Image not suitable for processing.')
                self.btnAnalysisProcess.setEnabled(True)
                self.btnAnalysisProcess.setFlat(False)

        else:
            self.lblImgAnalysisNoti.setText('Please select an image analysis technique.')
            self.btnAnalysisProcess.setEnabled(True)
            self.btnAnalysisProcess.setFlat(False)
