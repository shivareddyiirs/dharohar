from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
import matplotlib.pyplot as plt

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


class NavigationToolbar(NavigationToolbar2QT):

    toolitems = [toolitem for toolitem in NavigationToolbar2QT.toolitems if toolitem[0] != 'Save']


class figureViewDialog(QtGui.QDialog):

    def __init__(self, titles, images, windowTitle, parent=None):
        super(figureViewDialog, self).__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvasHeight = self.canvas.height()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet('background-image:url(./images/b1.png); background-attachment: fixed; color: rgb(70, 0, 0);')
        self.images = images
        self.titles = titles
        self.setStyleSheet('background-image:url(./images/kb.png); background-attachment: fixed; color: rgb(70, 0, 0);')
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(9)
        font.setFamily('Nirmala UI')
        buttonsFrame = QtGui.QFrame()
        buttonsFrame.setStyleSheet('background-image:url(./images/b1.png); background-attachment: fixed; color: rgb(70, 0, 0);')
        buttonsFrame.setFixedHeight(50)
        buttonsLayout = QtGui.QHBoxLayout()
        numOfButtons = len(titles)
        self.buttons = []
        for i in range(numOfButtons):
            newButton = QtGui.QPushButton()
            newButton.setMinimumHeight(31)
            newButton.setFont(font)
            newButton.setStyleSheet('background-image:url(./images/kb.png); background-attachment: fixed; '
                                    'color: rgb(70, 0, 0);')
            newButton.setAutoDefault(False)
            buttonsLayout.addWidget(newButton)
            self.buttons.append(newButton)
        buttonsFrame.setLayout(buttonsLayout)
        self.lblNoti = QtGui.QLabel()
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(8)
        font.setFamily('Nirmala UI')
        self.lblNoti.setFont(font)
        self.setStyleSheet('QLabel {color: #8c4600;}')
        self.lblNoti.setText('')
        self.lblNoti.setFixedHeight(15)
        self.lblNoti.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        lblFrame = QtGui.QFrame()
        lblFrame.setStyleSheet(
            'background-image:url(./images/b1.png); background-attachment: fixed; color: rgb(70, 0, 0);')
        lblFrameLayout = QtGui.QHBoxLayout()
        lblFrame.setStyleSheet('QFrame {background-color: white;}')
        self.lblHead = QtGui.QLabel()
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setFamily('Baskerville Old Face')
        self.lblHead.setFont(font)
        self.lblHead.setStyleSheet('QLabel {color: #8c4600;}')
        self.lblHead.setText('DHAROHAR')
        self.lblHead.setFixedHeight(25)
        self.lblHead.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        lblFrameLayout.addWidget(self.lblHead)
        lblFrame.setLayout(lblFrameLayout)
        topFrame = QtGui.QFrame()
        topFrame.setStyleSheet(
            'background-image:url(./images/b1.png); background-attachment: fixed; color: rgb(70, 0, 0);')
        topFrame.setMaximumHeight(55)
        toplayout = QtGui.QHBoxLayout()
        toplayout.addWidget(self.toolbar)
        toplayout.addWidget(lblFrame)
        topFrame.setLayout(toplayout)
        self.canvas.setMinimumHeight(500)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(topFrame)
        mainLayout.addWidget(self.canvas)
        mainLayout.addWidget(buttonsFrame)
        mainLayout.addWidget(self.lblNoti)
        self.setLayout(mainLayout)
        self.setWindowTitle(windowTitle)
        self.connections()
        self.plot()

    def connections(self):
        if len(self.titles) == 6:
            self.buttons[0].clicked.connect(self.saveFigure1)
            self.buttons[1].clicked.connect(self.saveFigure2)
            self.buttons[2].clicked.connect(self.saveFigure3)
            self.buttons[3].clicked.connect(self.saveFigure4)
            self.buttons[4].clicked.connect(self.saveFigure5)
            self.buttons[5].clicked.connect(self.saveFigure6)
        elif len(self.titles) == 5:
            self.buttons[0].clicked.connect(self.saveFigure1)
            self.buttons[1].clicked.connect(self.saveFigure2)
            self.buttons[2].clicked.connect(self.saveFigure3)
            self.buttons[3].clicked.connect(self.saveFigure4)
            self.buttons[4].clicked.connect(self.saveFigure5)
        elif len(self.titles) == 4:
            self.buttons[0].clicked.connect(self.saveFigure1)
            self.buttons[1].clicked.connect(self.saveFigure2)
            self.buttons[2].clicked.connect(self.saveFigure3)
            self.buttons[3].clicked.connect(self.saveFigure4)
        elif len(self.titles) == 3:
            self.buttons[0].clicked.connect(self.saveFigure1)
            self.buttons[1].clicked.connect(self.saveFigure2)
            self.buttons[2].clicked.connect(self.saveFigure3)
        elif len(self.titles) == 2:
            self.buttons[0].clicked.connect(self.saveFigure1)
            self.buttons[1].clicked.connect(self.saveFigure2)
        elif len(self.titles) == 1:
            self.buttons[0].clicked.connect(self.saveFigure1)

    def saveFigure1(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None))
        if not filename:
            self.lblNoti.setText("To save a figure, provide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Saving...   Please wait...')
            self.buttons[0].setEnabled(False)
            self.buttons[0].setFlat(True)
            plt.imsave(filename, self.images[0], cmap='gray')
            self.lblNoti.setText("Figure '" + self.titles[0] + "' Saved.")
            self.buttons[0].setEnabled(True)
            self.buttons[0].setFlat(False)

    def saveFigure2(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None))
        if not filename:
            self.lblNoti.setText("To save a figure, provide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Saving...   Please wait...')
            self.buttons[1].setEnabled(False)
            self.buttons[1].setFlat(True)
            plt.imsave(filename, self.images[1], cmap='gray')
            self.lblNoti.setText("Figure '" + self.titles[1] + "' Saved.")
            self.buttons[1].setEnabled(True)
            self.buttons[1].setFlat(False)

    def saveFigure3(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None))
        if not filename:
            self.lblNoti.setText("To save a figure, provide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Saving...   Please wait...')
            self.buttons[2].setEnabled(False)
            self.buttons[2].setFlat(True)
            plt.imsave(filename, self.images[2], cmap='gray')
            self.lblNoti.setText("Figure '" + self.titles[2] + "' Saved.")
            self.buttons[2].setEnabled(True)
            self.buttons[2].setFlat(False)

    def saveFigure4(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None))
        if not filename:
            self.lblNoti.setText("To save a figure, provide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Saving...   Please wait...')
            self.buttons[3].setEnabled(False)
            self.buttons[3].setFlat(True)
            plt.imsave(filename, self.images[3], cmap='gray')
            self.lblNoti.setText("Figure '" + self.titles[3] + "' Saved.")
            self.buttons[3].setEnabled(True)
            self.buttons[3].setFlat(False)

    def saveFigure5(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None))
        if not filename:
            self.lblNoti.setText("To save a figure, provide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Saving...   Please wait...')
            self.buttons[4].setEnabled(False)
            self.buttons[4].setFlat(True)
            plt.imsave(filename, self.images[4], cmap='gray')
            self.lblNoti.setText("Figure '" + self.titles[4] + "' Saved.")
            self.buttons[4].setEnabled(True)
            self.buttons[4].setFlat(False)

    def saveFigure6(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', 'Image Files(*.png *.jpeg *.jpg *.tiff '
                                                                                '*.bmp *.tif)', None))
        if not filename:
            self.lblNoti.setText("To save a figure, provide a file name and click 'Save'.")
        else:
            self.lblNoti.setText('Saving...   Please wait...')
            self.buttons[5].setEnabled(False)
            self.buttons[5].setFlat(True)
            plt.imsave(filename, self.images[5], cmap='gray')
            self.lblNoti.setText("Figure '" + self.titles[5] + "' Saved.")
            self.buttons[5].setEnabled(True)
            self.buttons[5].setFlat(False)

    def plot(self):
        R = 1
        C = len(self.titles)
        for i in range(1, C + 1):
            fig = self.figure.add_subplot(R, C, i)
            fig.clear()
            fig.imshow(self.images[i - 1], cmap='gray')
            fig.set_title(self.titles[i - 1])
            fig.axis('off')
            self.buttons[i - 1].setText("Save - '" + self.titles[i - 1] + "'")
        self.canvas.draw()
