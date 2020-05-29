import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import psycopg2

uiFile = 'forms/changePassword.ui'
changePasswordUI, QtBaseClass = uic.loadUiType(uiFile)

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


class changePassword(QtGui.QDialog, changePasswordUI):

    def __init__(self, db, user, password, host, port, parent=None):
        super(changePassword, self).__init__(parent)
        self.setupUi(self)
        self.txtOld.setEchoMode(QtGui.QLineEdit.Password)
        self.txtConfirm.setEchoMode(QtGui.QLineEdit.Password)
        self.txtNew.setEchoMode(QtGui.QLineEdit.Password)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnOK.clicked.connect(self.change)
        self.txtOld.returnPressed.connect(self.change)
        self.txtConfirm.returnPressed.connect(self.change)
        self.txtNew.returnPressed.connect(self.change)
        self.lblUser.setText('Username: ' + user)
        self.username = user
        self.password = password
        self.conn = psycopg2.connect(database=db, user=user, host=host, password=password, port=port)
        self.cursor = self.conn.cursor()
        self.retValue = None

    def closeEvent(self, event):
        if self.retValue:
            self.done(0)
        else:
            self.done(1)

    def cancel(self):
        self.retValue = False
        self.close()

    def change(self):
        old = str(self.txtOld.text())
        new = str(self.txtNew.text())
        confirm = str(self.txtConfirm.text())
        if not (old != '' and new != '' and confirm != ''):
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('All fields are mandatory.')
            message.setWindowTitle('Input Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            return
        if old != self.password:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Old password does not match.')
            message.setWindowTitle('Input Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            return
        if new != confirm:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('New and Confirm passwords do not match.')
            message.setWindowTitle('Input Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            return
        try:
            sql = "ALTER USER " + self.username + " WITH PASSWORD '" + new + "'"
            self.cursor.execute(sql)
            self.conn.commit()
            sql = "UPDATE password_change_status SET security_status=TRUE WHERE username='" + self.username + "'"
            self.cursor.execute(sql)
            self.conn.commit()
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Password changed. You will be logged out immediately.')
            message.setWindowTitle('Change Password')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            self.txtOld.setText('')
            self.txtNew.setText('')
            self.txtConfirm.setText('')
            self.conn.close()
            self.txtOld.setFocus()
            self.retValue = True
            self.close()
        except psycopg2.DatabaseError:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Critical)
            message.setText('Could not change password.\nPlease contact administrator.')
            message.setWindowTitle('Change Password')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            self.txtOld.setFocus()
