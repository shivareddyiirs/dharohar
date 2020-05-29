import os
# wrk_drr=os.path.dirname(os.path.realpath('__file__'))
# os.chdir(wrk_drr)
os.chdir(os.path.dirname(os.path.dirname(__file__)))
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import QStringList, QString, QTranslator
import PyQt4.uic as uic
import psycopg2, sys
from windowVisualization import windowVisualization
from changePassword import changePassword
from contactus import contactUs
from credits import credits
import webbrowser

uiFile = "forms\main.ui"
mainWindowUI, QtBaseClass = uic.loadUiType(uiFile)

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


class mainWindow(QtGui.QMainWindow, mainWindowUI):

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.qt_translator = QTranslator()
        items = ("English", "Tamil", "Hindi", "Bengali")
        self.item = 'English'
        self.item, self.okPressed = QtGui.QInputDialog.getItem(self, "Select Language:", "Available languages:", items,
                                                               0, False)
        self.item = str(self.item)
        self.translation(self.item)
        app.installEventFilter(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("images/icon.png"))
        self.label_4.setPixmap(QtGui.QPixmap("images/icon.png"))
        self.iirsLogo.setPixmap(QtGui.QPixmap("images/iirs.png"))
        self.label_12.setPixmap(QtGui.QPixmap("images/ISRO.gif"))
        self.setFixedSize(self.size())
        self.lblProceedNoti.setVisible(False)
        self.frameManageProject.setVisible(False)
        self.widget.hide()
        self.btnAuthenticate.clicked.connect(self.authenticate)
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.cbProject.currentIndexChanged.connect(self.toggleNewProject)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.lblLogout.mousePressEvent = self.logout
        self.txtUsername.returnPressed.connect(self.authenticate)
        self.txtPassword.returnPressed.connect(self.authenticate)
        self.txtDbLocation.returnPressed.connect(self.authenticate)
        self.txtDbName.returnPressed.connect(self.authenticate)
        self.txtPort.returnPressed.connect(self.authenticate)
        self.txtAddPassword.returnPressed.connect(self.addUser)
        self.txtAddUsername.returnPressed.connect(self.addUser)
        self.txtGroups.returnPressed.connect(self.addUser)
        self.txtManageGroups.returnPressed.connect(self.updateUser)
        self.txtManagePassword.returnPressed.connect(self.updateUser)
        self.txtNewPro.returnPressed.connect(self.proceed)
        self.dtValidity.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        self.dtValidity.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dtManageValidity.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        self.chkValidity.stateChanged.connect(self.addValidityStateChange)
        self.chkGroup.stateChanged.connect(self.addGroupStateChange)
        self.cbGroups.currentIndexChanged.connect(self.addGroupValueChange)
        self.chkManageValidity.stateChanged.connect(self.manageValidityStateChange)
        self.chkManageGroup.stateChanged.connect(self.manageGroupStateChange)
        self.cbManageGroups.currentIndexChanged.connect(self.manageGroupValueChange)
        self.btnAdd.clicked.connect(self.addUser)
        self.cbUsers.currentIndexChanged.connect(self.loadUserPrivileges)
        self.chkChangePassword.stateChanged.connect(self.managePasswordChange)
        self.btnDelete.clicked.connect(self.deleteUser)
        self.btnUpdate.clicked.connect(self.updateUser)
        self.btnProceed.clicked.connect(self.proceed)
        self.lblManage.mousePressEvent = self.manageProject
        self.btnBack.clicked.connect(self.back)
        self.btnDelProject.clicked.connect(self.deleteProject)
        self.btnGrant.clicked.connect(self.grantPrivilege)
        self.btnRevoke.clicked.connect(self.revokePrivilege)
        self.lblForgot.mousePressEvent = self.forgot
        self.lblChangePassword.mousePressEvent = self.changePass
        self.lblContact.mousePressEvent = self.contact
        self.lblCredits.mousePressEvent = self.credit
        self.lblHelp.mousePressEvent = self.help
        self.label_5.mousePressEvent = self.help
        self.iirsLogo.mousePressEvent = self.gotoIIRS

    def gotoIIRS(self, event):
        webbrowser.open_new_tab("https://www.iirs.gov.in/")

    def translation(self, item):
        if item.lower() != "english":
            self.qt_translator.load("language script/" + item + "py.qm")
            app.installTranslator(self.qt_translator)

    def help(self, event):
        webbrowser.open_new_tab(os.getcwd() + '/document/Complete User_manual.pdf')

    def credit(self, event):
        self.creditsWindow = credits()
        self.creditsWindow.exec_()

    def contact(self, event):
        self.contactWindow = contactUs()
        self.contactWindow.exec_()

    def changePass(self, event):
        self.chgPassword = changePassword(self.db, self.username, self.password, self.host, self.port)
        if self.chgPassword.exec_() == 0:
            self.logoutFn()

    def forgot(self, event):
        message = QtGui.QMessageBox()
        message.setIcon(QtGui.QMessageBox.Information)
        message.setText("Please contact the administrator regarding this.\nThe administrator will give you a default "
                        "password which you can use to log in.\n\nNote: After resetting the password to default, please "
                        "change it to keep your account safe.")
        message.setWindowTitle('Reset Password Instructions')
        message.setStandardButtons(QtGui.QMessageBox.Ok)
        message.exec_()

    def revokePrivilege(self):
        username = str(self.cbManageProject.currentText())
        if username == 'Usernames':
            self.lblManageProjectNoti.setText('Please select a user from the list to grant privileges.')
        else:
            if not self.chkManageInsert.isChecked() and not self.chkManageSelect.isChecked():
                self.lblManageProjectNoti.setText('Select at least one privilege to grant to the user.')
            else:
                project = str(self.cbProject.currentText())
                tables = project + '_image, ' + project + '_rdt, ' + project + '_xyz'
                sql = "REVOKE"
                if self.chkManageInsert.isChecked():
                    sql += " INSERT,"
                if self.chkManageSelect.isChecked():
                    sql += " SELECT,"
                sql = sql.rstrip(',') + " ON TABLE " + tables + " FROM " + username
                self.cursor.execute(sql)
                self.conn.commit()
                self.lblManageProjectNoti.setText('Privileges revoked from user ' + username + '.')
                self.chkManageInsert.setChecked(False)
                self.chkManageSelect.setChecked(False)

    def grantPrivilege(self):
        username = str(self.cbManageProjectUsers.currentText())
        if username == 'Usernames':
            self.lblManageProjectNoti.setText('Please select a user from the list to grant privileges.')
        else:
            if not self.chkManageInsert.isChecked() and not self.chkManageSelect.isChecked():
                self.lblManageProjectNoti.setText('Select at least one privilege to grant to the user.')
            else:
                project = str(self.cbProject.currentText())
                tables = project + '_image, ' + project + '_rdt, ' + project + '_xyz'
                sql = "GRANT"
                if self.chkManageInsert.isChecked():
                    sql += " INSERT,"
                if self.chkManageSelect.isChecked():
                    sql += " SELECT,"
                sql = sql.rstrip(',') + " ON TABLE " + tables + " TO " + username
                self.cursor.execute(sql)
                self.conn.commit()
                self.lblManageProjectNoti.setText('Privileges granted to user ' + username + '.')
                self.chkManageInsert.setChecked(False)
                self.chkManageSelect.setChecked(False)

    def deleteProject(self):
        project = str(self.cbProject.currentText())
        self.conn.close()
        self.conn = psycopg2.connect(database=self.db, user=self.username, host=self.host, password=self.password,
                                         port=self.port)
        self.cursor = self.conn.cursor()
        try:
            sql = "DROP TABLE IF EXISTS " + project + "_rdt CASCADE"
            self.cursor.execute(sql)
            self.conn.commit()
            print sql
            sql = "DROP TABLE IF EXISTS " + project + "_xyz CASCADE"
            self.cursor.execute(sql)
            self.conn.commit()
            print sql
            sql = "DROP TABLE IF EXISTS " + project + "_image CASCADE"
            self.cursor.execute(sql)
            self.conn.commit()
            print sql
            self.lblProceedNoti.setVisible(True)
            self.lblProceedNoti.setText("Project '" + project + "' deleted.")
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
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            self.projects = []
            self.cbProject.clear()
            self.cbProject.addItem(QString('New Project...'))
            for row in rows:
                tablename = row[0]
                project = tablename.split('_')[0]
                self.projects.append(project)
            self.cbProject.addItems(QStringList(list(set(self.projects))))
            self.back()
        except psycopg2.OperationalError:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Critical)
            message.setText("Database server closed unexpectedly.")
            message.setWindowTitle('Database Server Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            return

    def back(self):
        self.frameManageProject.setVisible(False)
        self.tabWidget.setVisible(True)

    def manageProject(self, event):
        project = str(self.cbProject.currentText())
        if project == 'New Project...':
            self.lblProceedNoti.setText('Select an existing project to manage.')
            self.lblProceedNoti.setVisible(True)
        else:
            sql = "SELECT usename FROM pg_user, pg_group WHERE usesysid=ANY(grolist) AND groname='" + self.db + \
                  "_project_admins'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            superusers = []
            for row in rows:
                superusers.append(row[0])
            if self.username in superusers:
                self.btnDelProject.setEnabled(True)
                self.btnDelProject.setFlat(False)
                sql = "SELECT DISTINCT tablename FROM pg_tables WHERE tablename SIMILAR TO '%_(image|xyz|rdt)'"
            else:
                self.btnDelProject.setEnabled(False)
                self.btnDelProject.setFlat(True)
                sql = "SELECT tablename FROM pg_tables WHERE tableowner='" + self.username + "'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            projects = []
            for row in rows:
                tablename = row[0]
                owner_project = tablename.split('_')[0]
                projects.append(owner_project)
            if project not in projects:
                self.lblProceedNoti.setText("You don't have privileges to manage this project.")
                self.lblProceedNoti.setVisible(True)
            else:
                self.lblProceedNoti.setText('')
                self.lblProceedNoti.setVisible(False)
                self.frameManageProject.setVisible(True)
                self.tabWidget.setVisible(False)
                self.chkManageInsert.setChecked(False)
                self.chkManageSelect.setChecked(False)
                self.lblManageProjectNoti.setText('')
                self.lblManageProjectHead.setText("Manage Project '" + project + "'")
                self.cbManageProjectUsers.clear()
                self.cbManageProjectUsers.addItem('Usernames')
                sql = "SELECT usename FROM pg_user WHERE usename NOT IN ('" + self.username + "', 'postgres')"
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                users = [user[0] for user in rows]
                self.cbManageProjectUsers.addItems(QStringList(users))

    def toggleNewProject(self):
        if self.cbProject.currentIndex() == 0:
            self.frameNewPro.setEnabled(True)
            self.lblNew.setEnabled(True)
            self.txtNewPro.setEnabled(True)
        else:
            self.frameNewPro.setEnabled(False)

    def loadUserPrivileges(self):
        self.txtManageGroups.setText('')
        if str(self.cbUsers.currentText()) == '' or str(self.cbUsers.currentText()) == 'Usernames':
            self.chkChangePassword.setChecked(False)
            self.txtManagePassword.setText('')
            self.chkManageValidity.setChecked(False)
            self.chkManagePassEnc.setChecked(False)
            self.chkManageGroup.setChecked(False)
            self.chkManageDB.setChecked(False)
            self.chkManageUsers.setChecked(False)
            self.chkManageGroup.setChecked(False)
            self.cbManageGroups.setCurrentIndex(0)
        else:
            self.selectedUser = str(self.cbUsers.currentText())
            sql = "SELECT * FROM PG_SHADOW WHERE USENAME='" + self.selectedUser + "'"
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row[7] is None or row[7] == 'infinity':
                self.chkManageValidity.setChecked(False)
            else:
                self.chkManageValidity.setChecked(True)
                validityDate = row[7].split(' ')[0].split('-')
                self.dtManageValidity.setDate(
                    QtCore.QDate(int(validityDate[0]), int(validityDate[1]), int(validityDate[2])))
            if row[6] is not None and row[6][:3] == 'md5' and len(row[6]) == 35 and row[6].isalnum():
                self.chkManagePassEnc.setChecked(True)
            else:
                self.chkManagePassEnc.setChecked(False)
            if row[3]:
                self.chkManageDB.setChecked(True)
            else:
                self.chkManageDB.setChecked(False)
            if row[3]:
                self.chkManageUsers.setChecked(True)
            else:
                self.chkManageUsers.setChecked(False)
            sql = "SELECT groname FROM pg_group WHERE " \
                  "(SELECT usesysid FROM pg_shadow WHERE " \
                  "usename='" + row[0] + "')= ANY(grolist)"
            user_data = row
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            groups = [row[0] for row in rows]
            self.selectedUserGroups = groups
            if len(groups) != 0:
                self.chkManageGroup.setChecked(True)
                for group in groups:
                    self.txtManageGroups.setText(self.txtManageGroups.text() + group + ',')
            else:
                self.chkManageGroup.setChecked(False)

    def updateUser(self):
        status = None
        if str(self.cbUsers.currentText()) == '' or str(self.cbUsers.currentText()) == 'Usernames':
            return
        username = self.selectedUser
        sql = 'ALTER USER ' + username + ' '
        if self.chkChangePassword.isChecked():
            status = False
            if str(self.txtManagePassword.text()) == '':
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Critical)
                message.setText("Please enter valid password if you want to change password.")
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                return
            password = str(self.txtManagePassword.text())
            if self.chkManagePassEnc.isChecked():
                sql = sql + "WITH ENCRYPTED PASSWORD '" + password + "' "
            else:
                sql = sql + "WITH UNENCRYPTED PASSWORD '" + password + "' "
        if self.chkManageDB.isChecked():
            sql = sql + 'SUPERUSER '
        else:
            sql = sql + 'NOCREATEDB '
            if self.chkManageUsers.isChecked():
                sql = sql + 'CREATEUSER'
            else:
                sql = sql + 'NOCREATEUSER'
        if self.chkValidity.isChecked():
            date = str(self.dtValidity.date().toString('MMM dd yyyy'))
            sql += " VALID UNTIL '" + date + "'"
        else:
            sql += " VALID UNTIL 'infinity'"
        if self.chkManageGroup.isChecked():
            if self.txtManageGroups.text() == '':
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Critical)
                message.setText("Please enter valid group names otherwise uncheck 'In Group'.")
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                return
            removedGroups = []
            groups = str(self.txtManageGroups.text()).split(',')
            for group in self.selectedUserGroups:
                if group not in groups:
                    removedGroups.append(group)
            group_sql = 'SELECT GRONAME FROM PG_GROUP'
            self.cursor.execute(group_sql)
            rows = self.cursor.fetchall()
            validGroups = [row[0] for row in rows]
            for group in groups:
                if group != '' and group not in validGroups:
                    message = QtGui.QMessageBox()
                    message.setIcon(QtGui.QMessageBox.Critical)
                    message.setText("Please enter valid group names otherwise uncheck 'In Group'.")
                    message.setWindowTitle('Input Error')
                    message.setStandardButtons(QtGui.QMessageBox.Ok)
                    message.exec_()
                    return
        else:
            removedGroups = self.selectedUserGroups
            groups = []
        try:
            if self.chkManageUsers.isChecked():
                self.cursor.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE password_change_status TO ' +
                                    username + ' WITH GRANT OPTION')
            else:
                self.cursor.execute('REVOKE GRANT OPTION FOR SELECT, INSERT, UPDATE, DELETE ON TABLE '
                                    'password_change_status FROM ' + username)
                self.cursor.execute('GRANT SELECT, UPDATE ON TABLE password_change_status TO ' + username)
            self.cursor.execute(sql)
            self.conn.commit()
            for group in removedGroups:
                self.cursor.execute('ALTER GROUP ' + group + ' DROP USER ' + self.selectedUser)
                self.conn.commit()
            for group in groups:
                if group != '':
                    self.cursor.execute('ALTER GROUP ' + group + ' ADD USER ' + self.selectedUser)
                    self.conn.commit()
            if self.chkManageDB.isChecked():
                self.cursor.execute('ALTER GROUP ' + self.db + '_project_admins ADD USER ' + self.selectedUser)
            else:
                self.cursor.execute('ALTER GROUP ' + self.db + '_project_admins DROP USER ' + self.selectedUser)
            self.conn.commit()
            sql = "select usename from pg_shadow where usename NOT IN ('" + self.username + "', 'postgres')"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            users = [user[0] for user in rows]
            self.cbUsers.clear()
            self.cbUsers.addItem(QString("Usernames"))
            self.cbUsers.addItems(QStringList(users))
            self.cbUsers.setCurrentIndex(0)
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('User altered successfully.')
            message.setWindowTitle('User alteration')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            if not status:
                sql = "UPDATE password_change_status SET security_status=FALSE WHERE username='" + self.selectedUser + "'"
                self.cursor.execute(sql)
                self.conn.commit()
            self.txtManagePassword.setText('')
            self.chkManageValidity.setChecked(False)
            self.chkManagePassEnc.setChecked(False)
            self.chkManageGroup.setChecked(False)
            self.chkManageDB.setChecked(False)
            self.chkManageUsers.setChecked(False)
            self.dtManageValidity.setDate(QtCore.QDate.currentDate())
            self.txtManageGroups.setText('')
            self.cbManageGroups.setCurrentIndex(0)
            self.dtManageValidity.setEnabled(False)
            self.cbManageGroups.setEnabled(False)
            self.txtManageGroups.setEnabled(False)
            self.conn.commit()
        except psycopg2.DatabaseError:
            self.conn.rollback()
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Critical)
            message.setText('Cannot alter user.\nPlease check inputs.')
            message.setWindowTitle('User alteration Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()

    def deleteUser(self):
        user = str(self.cbUsers.currentText())
        if user != 'Usernames':
            self.cursor.execute('ALTER GROUP ' + self.db + '_project_admins DROP USER ' + user)
            sql = 'DROP OWNED BY ' + user
            self.cursor.execute(sql)
            sql = 'DROP USER ' + user
            self.cursor.execute(sql)
            sql = "DELETE FROM password_change_status WHERE username='" + user + "'"
            self.cursor.execute(sql)
            self.conn.commit()
            sql = "select usename from pg_shadow where usename NOT IN ('" + self.username + "', 'postgres')"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            users = [user[0] for user in rows]
            self.cbUsers.clear()
            self.cbUsers.addItem(QString("Usernames"))
            self.cbUsers.addItems(QStringList(users))
            self.cbUsers.setCurrentIndex(0)
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('User deleted successfully.')
            message.setWindowTitle('User Deletion')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()

    def manageValidityStateChange(self):
        if self.chkManageValidity.isChecked():
            self.dtManageValidity.setEnabled(True)
        else:
            self.dtManageValidity.setEnabled(False)

    def manageGroupStateChange(self):
        if self.chkManageGroup.isChecked():
            self.cbManageGroups.setEnabled(True)
            self.txtManageGroups.setEnabled(True)
        else:
            self.cbManageGroups.setEnabled(False)
            self.txtManageGroups.setEnabled(False)

    def manageGroupValueChange(self):
        if self.cbManageGroups.currentText() != 'Available Groups':
            groups = self.txtManageGroups.text().split(',')
            group = str(self.cbManageGroups.currentText())
            if group not in groups:
                self.txtManageGroups.setText(self.txtManageGroups.text() + group + ',')

    def managePasswordChange(self):
        if self.chkChangePassword.isChecked():
            self.txtManagePassword.setEnabled(True)
            self.chkManagePassEnc.setEnabled(True)
        else:
            self.txtManagePassword.setEnabled(False)
            self.chkManagePassEnc.setEnabled(False)

    def addUser(self):
        username = str(self.txtAddUsername.text())
        password = str(self.txtAddPassword.text())
        if username != '' and password != '':
            if not username.islower():
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Information)
                message.setText('User names cannot have upper case letters.')
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                self.txtAddUsername.setFocus()
                return
            sql = 'select usename from pg_user'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            rolenames = [row[0] for row in rows]
            sql = 'select groname from pg_group'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            rolenames = rolenames + [row[0] for row in rows]
            if username in rolenames:
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Information)
                message.setText('Username already exist.\nTry with other usernames.')
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                self.txtAddUsername.setFocus()
            else:
                if not username.isalnum():
                    message = QtGui.QMessageBox()
                    message.setIcon(QtGui.QMessageBox.Information)
                    message.setText('Only alphanumeric characters are allowed for usernames.')
                    message.setWindowTitle('Input Error')
                    message.setStandardButtons(QtGui.QMessageBox.Ok)
                    message.exec_()
                    self.txtAddUsername.setFocus()
                else:
                    sql = 'CREATE USER ' + username + ' '
                    if self.chkPassEnc.isChecked():
                        sql = sql + "WITH ENCRYPTED PASSWORD '" + password + "' "
                    else:
                        sql = sql + "WITH UNENCRYPTED PASSWORD '" + password + "' "
                    if self.chkMgmtDB.isChecked():
                        sql = sql + 'SUPERUSER '
                    else:
                        sql = sql + 'NOCREATEDB '
                        if self.chkMgmtUsers.isChecked():
                            sql = sql + 'CREATEUSER'
                        else:
                            sql = sql + 'NOCREATEUSER'
                    if self.chkGroup.isChecked():
                        if self.txtGroups.text() == '':
                            message = QtGui.QMessageBox()
                            message.setIcon(QtGui.QMessageBox.Critical)
                            message.setText("Please enter valid group names otherwise uncheck 'In Group'.")
                            message.setWindowTitle('Input Error')
                            message.setStandardButtons(QtGui.QMessageBox.Ok)
                            message.exec_()
                            return
                        sql += ' IN GROUP '
                        groups = str(self.txtGroups.text()).split(',')
                        group_sql = 'SELECT GRONAME FROM PG_GROUP'
                        self.cursor.execute(group_sql)
                        rows = self.cursor.fetchall()
                        validGroups = [row[0] for row in rows]
                        for group in groups:
                            if group != '' and group not in validGroups:
                                message = QtGui.QMessageBox()
                                message.setIcon(QtGui.QMessageBox.Critical)
                                message.setText("Please enter valid group names otherwise uncheck 'In Group'.")
                                message.setWindowTitle('Input Error')
                                message.setStandardButtons(QtGui.QMessageBox.Ok)
                                message.exec_()
                                return
                            else:
                                sql += group + ', '
                        sql = sql.rstrip(', ')
                    if self.chkValidity.isChecked():
                        date = str(self.dtValidity.date().toString('MMM dd yyyy'))
                        sql += " VALID UNTIL '" + date + "'"
                    try:
                        self.cursor.execute(sql)
                        self.conn.commit()
                        sql = "select usename from pg_shadow where usename NOT IN ('" + self.username + "', 'postgres')"
                        self.cursor.execute(sql)
                        rows = self.cursor.fetchall()
                        users = [user[0] for user in rows]
                        self.cbUsers.clear()
                        self.cbUsers.addItem(QString("Usernames"))
                        self.cbUsers.addItems(QStringList(users))
                        self.cbUsers.setCurrentIndex(0)
                        message = QtGui.QMessageBox()
                        message.setIcon(QtGui.QMessageBox.Information)
                        message.setText('User created successfully.')
                        message.setWindowTitle('User Creation')
                        message.setStandardButtons(QtGui.QMessageBox.Ok)
                        message.exec_()
                        sql = "INSERT INTO password_change_status VALUES('" + username + "', FALSE)"
                        self.cursor.execute(sql)
                        if self.chkMgmtUsers.isChecked():
                            self.cursor.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE password_change_status '
                                                'TO ' + username + ' WITH GRANT OPTION')
                        else:
                            self.cursor.execute('GRANT SELECT, UPDATE ON TABLE password_change_status TO ' + username)
                        if self.chkMgmtDB.isChecked():
                            self.cursor.execute('ALTER GROUP ' + self.db + '_project_admins ADD USER ' + username)
                        self.conn.commit()
                        self.txtAddUsername.setText('')
                        self.txtAddPassword.setText('')
                        self.chkValidity.setChecked(False)
                        self.chkPassEnc.setChecked(False)
                        self.chkGroup.setChecked(False)
                        self.chkMgmtDB.setChecked(False)
                        self.chkMgmtUsers.setChecked(False)
                        self.dtValidity.setDate(QtCore.QDate.currentDate())
                        self.txtGroups.setText('')
                        self.cbGroups.setCurrentIndex(0)
                        self.dtValidity.setEnabled(False)
                        self.cbGroups.setEnabled(False)
                        self.txtGroups.setEnabled(False)
                    except psycopg2.DatabaseError:
                        self.conn.rollback()
                        message = QtGui.QMessageBox()
                        message.setIcon(QtGui.QMessageBox.Critical)
                        message.setText('Cannot create user.\nPlease check inputs.')
                        message.setWindowTitle('User Creation Error')
                        message.setStandardButtons(QtGui.QMessageBox.Ok)
                        message.exec_()
        else:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Critical)
            message.setText('Username and password cannot be empty.')
            message.setWindowTitle('Input Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            self.txtAddUsername.setFocus()

    def addValidityStateChange(self):
        if self.chkValidity.isChecked():
            self.dtValidity.setEnabled(True)
        else:
            self.dtValidity.setEnabled(False)

    def addGroupStateChange(self):
        if self.chkGroup.isChecked():
            self.cbGroups.setEnabled(True)
            self.txtGroups.setEnabled(True)
        else:
            self.cbGroups.setEnabled(False)
            self.txtGroups.setEnabled(False)

    def addGroupValueChange(self):
        if self.cbGroups.currentText() != 'Available Groups':
            groups = self.txtGroups.text().split(',')
            group = str(self.cbGroups.currentText())
            if group not in groups:
                self.txtGroups.setText(self.txtGroups.text() + group + ',')

    def afterLogIn(self):
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
            sql = "SELECT DISTINCT table_name FROM information_schema.table_privileges WHERE grantee='" + self.username\
              + "' AND table_name SIMILAR TO '%_(image|xyz|rdt)'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.projects = []
        self.cbUsers.clear()
        self.cbUsers.addItem(QString('Usernames'))
        self.cbProject.clear()
        self.cbProject.addItem(QString('New Project...'))
        for row in rows:
            tablename = row[0]
            project = tablename.split('_')[0]
            self.projects.append(project)
        self.cbProject.addItems(QStringList(list(set(self.projects))))
        sql = "select usename from pg_shadow where usename NOT IN ('" + self.username + "', 'postgres')"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            users = [user[0] for user in rows]
            self.cbUsers.addItems(QStringList(users))
            self.cbGroups.clear()
            self.cbGroups.addItem('Available Groups')
            sql = 'SELECT GRONAME FROM PG_GROUP'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            groups = [row[0] for row in rows]
            self.cbGroups.addItems(QStringList(groups))
            self.cbManageGroups.clear()
            self.cbManageGroups.addItem('Available Groups')
            self.cbManageGroups.addItems(QStringList(groups))
            self.txtAddUsername.setFocus()
        except psycopg2.DatabaseError:
            self.conn.rollback()
            self.tabCreate.setEnabled(False)
            self.tabManage.setEnabled(False)
            self.tabWidget.setCurrentIndex(2)
            self.cbProject.setFocus()
        self.lblProceedNoti.setVisible(False)
        sql = "SELECT security_status FROM password_change_status WHERE username='" + self.username + "'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row is not None and not row[0]:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('This is to notify you that your password has been changed by the administrator.\nPlease'
                            ' change your password to keep your account safe.')
            message.setWindowTitle('Security Issue.')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()

    def authenticate(self):
        self.username = str(self.txtUsername.text())
        self.password = str(self.txtPassword.text())
        self.db = str(self.txtDbName.text())
        self.host = str(self.txtDbLocation.text())
        self.port = str(self.txtPort.text())
        if self.username == '' or self.password == '' or self.db == '':
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('All fields are mandatory.\nPlease enter credentials properly.')
            message.setWindowTitle('Input Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
            self.txtDbLocation.setFocus()
            return
        try:
            self.conn = psycopg2.connect(database=self.db, user=self.username, host=self.host, password=self.password,
                                         port=self.port)
            self.cursor = self.conn.cursor()
            self.widget.show()
            self.frameAuthentication.hide()
            self.txtUsername.setText('')
            self.txtPassword.setText('')
            self.txtDbLocation.setText('')
            self.txtDbName.setText('')
            self.afterLogIn()
        except psycopg2.DatabaseError:
            message = QtGui.QMessageBox()
            message.setIcon(QtGui.QMessageBox.Information)
            message.setText('Cannot connect to database.\nPlease enter proper credentials.')
            message.setWindowTitle('Connection Error')
            message.setStandardButtons(QtGui.QMessageBox.Ok)
            message.exec_()
        self.txtDbLocation.setFocus()

    def logout(self, event):
        self.logoutFn()

    def logoutFn(self):
        self.frameAuthentication.show()
        self.conn.close()
        self.tabCreate.setEnabled(True)
        self.tabManage.setEnabled(True)
        self.tabWidget.setCurrentIndex(0)
        self.dtManageValidity.setEnabled(False)
        self.cbManageGroups.setEnabled(False)
        self.txtManageGroups.setEnabled(False)
        self.txtManagePassword.setEnabled(False)
        self.widget.hide()

    def proceed(self):
        self.lblProceedNoti.setVisible(False)
        self.lblProceedNoti.setText('')
        if self.cbProject.currentIndex() == 0:
            if self.txtNewPro.text() == '':
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Critical)
                message.setText('Project name cannot be empty.')
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                self.txtNewPro.setFocus()
                return
            if not str(self.txtNewPro.text()).isalnum():
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Information)
                message.setText('Only alphanumeric characters are allowed for usernames.')
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                self.txtNewPro.setFocus()
                return
            project = str(self.txtNewPro.text())
            self.txtNewPro.setText('')
            isNew = True
            self.cursor.execute("SELECT DISTINCT tablename FROM pg_tables WHERE tablename SIMILAR TO '%_(image|xyz|rdt)'")
            rows = self.cursor.fetchall()
            existing_projects = []
            for row in rows:
                existing_projects.append(row[0].split('_')[0])
            if project in existing_projects:
                message = QtGui.QMessageBox()
                message.setIcon(QtGui.QMessageBox.Information)
                message.setText('This project name is already in use. Try another.')
                message.setWindowTitle('Input Error')
                message.setStandardButtons(QtGui.QMessageBox.Ok)
                message.exec_()
                self.txtNewPro.setFocus()
                return
        else:
            project = str(self.cbProject.currentText())
            isNew = False
        self.visualizationWindow = windowVisualization(self.username, self.password, self.db, self.host,
                                                                      self.port, project, isNew, self, lang=self.item)
        self.hide()
        self.visualizationWindow.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/Nirmala.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/NIRMALAB.TTF')
    QtGui.QFontDatabase.addApplicationFont('fonts/BASKVILL.ttf')
    app_icon = QtGui.QIcon()
    app_icon.addFile('images/icon.png')
    app.setWindowIcon(app_icon)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())
