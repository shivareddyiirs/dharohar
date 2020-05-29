import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
from PyQt4.QtCore import QThread, SIGNAL
import pandas as pd
import copy

uiFile = "forms/tableViewWindow.ui"
tableVisualizationUI, QtBaseClass = uic.loadUiType(uiFile)

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


class exportCSV(QThread):

    def __init__(self, filename, table):
        QThread.__init__(self)
        self.filename = filename
        self.table = table

    def __del__(self):
        self.wait()

    def run(self):
        self.emit(SIGNAL('exportIt(PyQt_PyObject, PyQt_PyObject)'), self.filename, self.table)


class tableVisualization(QtGui.QMainWindow, tableVisualizationUI):

    def __init__(self, dataModel, title, data, header_row, parent=None):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        super(tableVisualization, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.tvList.setModel(dataModel)
        self.setWindowTitle(title + ' - Dharohar')
        self.loginFrameLabel1_7.setPixmap(QtGui.QPixmap("images/icon.png"))
        self.loginFrameLabel1_6.setPixmap(QtGui.QPixmap("images/iirs.png"))
        self.table = pd.DataFrame(data, columns=header_row)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.btnExport.clicked.connect(self.export)
        self.success = None

    def exportIt(self, filename, table):
        try:
            table.to_csv(filename, index=False)
            self.success = True
        except IOError:
            self.success = False

    def exportDone(self):
        if self.success:
            self.lblNoti.setText('Successfully exported as a CSV.')
        else:
            self.lblNoti.setText('Cannot overwrite, file is in use.')
        self.btnExport.setEnabled(True)
        self.btnExport.setFlat(False)

    def export(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Comma delimited(*.csv)'
                                                         , None))
        if not filename:
            self.lblNoti.setText("To export,\nprovide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Exporting...   Please wait...')
            self.btnExport.setEnabled(False)
            self.btnExport.setFlat(True)
            self.exportThread = exportCSV(filename, self.table)
            self.connect(self.exportThread, SIGNAL('exportIt(PyQt_PyObject, PyQt_PyObject)'), self.exportIt)
            self.connect(self.exportThread, SIGNAL("finished()"), self.exportDone)
            self.exportThread.start()
