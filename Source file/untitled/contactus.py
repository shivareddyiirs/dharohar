import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

uiFile = 'forms/contactus.ui'
contactUsUI, QtBaseClass = uic.loadUiType(uiFile)

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


class contactUs(QtGui.QDialog, contactUsUI):

    def __init__(self, parent=None):
        super(contactUs, self).__init__(parent)
        self.setupUi(self)
        self.loginFrameLabel1_6.setPixmap(QtGui.QPixmap("images/ISRO.gif"))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
