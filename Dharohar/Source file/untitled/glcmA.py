from PyQt4 import QtGui,QtCore
import matplotlib.pyplot as plt
import numpy as np
import PyQt4.uic as uic
from skimage.feature import greycomatrix, greycoprops
from PIL import Image
import time
from PyQt4.QtCore import QThread, SIGNAL
import psycopg2, sys, os, operator, io
QtDesignerFile = 'C:/Python27/mdtext.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(QtDesignerFile)

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

class queryDatabase(QThread):

    def __init__(self, sql, cursor, header_row, table):
        QThread.__init__(self)
        self.sql = sql
        self.cursor = cursor
        self.header_row = header_row
        self.table = table
    def __del__(self):
        self.wait()
    def run(self):
        self.cursor.execute(self.sql)
        if self.table:
            queryResult = self.cursor.fetchall()
        else:
            queryResult = self.cursor.fetchone()
        self.emit(SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool)'), queryResult, self.header_row, self.table)
class Window(QtGui.QMainWindow ,Ui_MainWindow):
    fileName="x"
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.outputTable.hide()
        self.loadBtn.clicked.connect(self.databaseload)
        self.open.clicked.connect(self.Load)
        self.vBtn.clicked.connect(self.vvBtn)
        self.imageList.clicked.connect(self.showlist)
        self.cBtn.clicked.connect(self.connectDatabase)
        self.labelConnected.hide()
        self.labelWait.hide()
        self.dataF.hide()
    def connectDatabase(self):
        username = self.uname.text()
        password = self.pswrd.text()
        try:
            self.conn = psycopg2.connect(database='Dhar_db', user=username, host='localhost', password=password)
            self.cursor = self.conn.cursor()
            self.loginFrame.setEnabled(False)
            self.labelConnected.show()
            self.dataF.show()
        except psycopg2.DatabaseError:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Cannot connect to database.\nPlease check connection details')
            message.setWindowTitle('Connection Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
        self.uname.setText('')
        self.pswrd.setText('')
    def Load(self):
        global fileName
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", "/","Image Files (*.png *.jpeg *.jpg *.tiff *.bmp *.tif)")
        fileName=str(fileName)
        if fileName:
            img=QtGui.QPixmap(fileName,"1")
            if img.isNull():
                QtGui.QMessageBox.information(self,"Message","Cannot load %s."%fileName)
                return
    def databaseload(self):
        try:
            global fileName
            rid=self.ridT.text()
            rid=str(rid)
            sql = "SELECT ST_AsJPEG(rast,100) As rastjpg FROM raster_image WHERE rid=" + rid + ""
            self.cursor.execute(sql)
            result=self.cursor.fetchone()
            fileName=io.BytesIO(result[0])
        except:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Please enter vaild RID')
            message.setWindowTitle('RID Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
    def visualizeResult(self, queryResult, header_row, table):
        if table:
            dataModel = MyTableModel(queryResult, header_row, self)
            self.outputTable.setModel(dataModel)
            self.outputTable.show()
    def showlist(self):
        header_row = ['RID', 'FileName']
        sql = 'SELECT rid, filename FROM raster_image'
        self.queryThread = queryDatabase(sql, self.cursor, header_row, True)
        self.connect(self.queryThread, SIGNAL('visualizeResult(PyQt_PyObject, PyQt_PyObject, bool)'),self.visualizeResult)
        self.queryThread.start()
    def vvBtn(self) :
        try:
            st = time.time()
            count=0
            d=1
            a=0
            org=Image.open(fileName)
            rgb_im=org.convert('RGB')
            nx,ny=rgb_im.size
            if nx>= 480 :
                nx1=480
            else:
                nx1=nx
            if ny>=500:
                ny1=500
            else:
                ny1=ny
            im2 = rgb_im.resize((int(nx1), int(ny1)), Image.BICUBIC)
            r,g,b=im2.split()
            if self.rBtn.isChecked():
                count=1
            elif self.gBtn.isChecked():
                count=2
            elif self.bBtn.isChecked():
                count=3
            if count==1 :
                sarraster=np.asarray(r)
                self.labelWait.show()
                plt.title('RBand - Original Image (Gray Scale)')
                plt.imshow(sarraster, cmap='gray')
                plt.show()
            elif count==2 :
                sarraster=np.asarray(g)
                self.labelWait.show()
                plt.title('GBand - Original Image (Gray Scale)')
                plt.imshow(sarraster, cmap='gray')
                plt.show()
            elif count==3 :
                sarraster=np.asarray(b)
                self.labelWait.show()
                plt.title('BBand - Original Image (Gray Scale)')
                plt.imshow(sarraster, cmap='gray')
                plt.show()
            #Create rasters to receive texture and define filenames
            contrastraster = np.copy(sarraster)
            contrastraster[:] = 0
            #print contrastraster
            dissimilarityraster = np.copy(sarraster)
            dissimilarityraster[:] = 0
            homogeneityraster = np.copy(sarraster)
            homogeneityraster[:] = 0
            energyraster = np.copy(sarraster)
            energyraster[:] = 0
            correlationraster = np.copy(sarraster)
            correlationraster[:] = 0
            ASMraster = np.copy(sarraster)
            ASMraster[:] = 0
            # Create figure to receive results
            fig = plt.figure()
            fig.suptitle('GLCM Textures')
            for i in range(sarraster.shape[0] ):      #returns the no of rows
                for j in range(sarraster.shape[1] ):     #returns the no of columns
                # windows needs to fit completely in image
                    if i<3 or j<3:
                        continue
                    if i > (contrastraster.shape[0] - 4) or j > (contrastraster.shape[1] - 4):
                        continue
                    # Define size of moving window
                    glcm_window = sarraster[i-3: i+4, j-3 : j+4]
                    # Calculate GLCM and textures
                    glcm = greycomatrix(glcm_window, [int(n) for n in str(d)], [int(n1) for n1 in str(a)],  symmetric = True, normed = True )
                    # Calculate texture and write into raster where moving window is centered
                    contrastraster[i,j]      = greycoprops(glcm, 'contrast')
                    dissimilarityraster[i,j] = greycoprops(glcm, 'dissimilarity')
                    homogeneityraster[i,j]   = greycoprops(glcm, 'homogeneity')
                    energyraster[i,j]        = greycoprops(glcm, 'energy')
                    correlationraster[i,j]   = greycoprops(glcm, 'correlation')
                    ASMraster[i,j]           = greycoprops(glcm, 'ASM')
                    glcm = None
                    glcm_window = None
            texturelist = {1: 'contrast', 2: 'dissimilarity', 3: ' homogeneity', 4: 'energy', 5: 'correlation', 6: 'ASM'}
            for key in texturelist:
                ax = plt.subplot(2,3,key)
                plt.axis('off')
                ax.set_title(texturelist[key])
                plt.imshow(eval(texturelist[key] + "raster"), cmap = 'gray')
            st1 = (time.time() - st)
            print("--- %s seconds ---" % st1)
            self.labelWait.hide()
            plt.show()
        except:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Please Select Any one Band and Image')
            message.setWindowTitle('Selection Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
