from PySide6 import * #QtCore

from PySide6 import QtGui
from PySide6.QtGui import * #QApplication, QMainWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QTextBrowser, QMenuBar, QStatusBar
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 132)
        self.centralwidget = QWidget(MainWindow)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.textBrowser_1 = QTextBrowser(self.centralwidget)
        self.horizontalLayout.addWidget(self.textBrowser_1)
        self.textBrowser_2 = QTextBrowser(self.centralwidget)
        self.horizontalLayout.addWidget(self.textBrowser_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MyMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()  # This is from a python export from QtDesigner
        self.ui.setupUi(self)
        self.setMouseTracking(True)
        self.ui.textBrowser_1.setMouseTracking(True)
        self.ui.textBrowser_2.setMouseTracking(True)
        self.ui.menubar.setMouseTracking(True)
        self.ui.statusbar.setMouseTracking(True)

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QWidget):
                child.setMouseTracking(flag)
                recursive_set(child)
        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.ui.textBrowser_1.append(str(pos.x()))
        self.ui.textBrowser_2.append(str(pos.y()))
        QMainWindow.mouseMoveEvent(self, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainscreen = MyMainScreen()
    mainscreen.show()
    app.exec_()