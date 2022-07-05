from PySide6 import * #QtCore

from PySide6 import QtGui
from PySide6.QtGui import * #QApplication, QMainWindow
from PySide6.QtWidgets import * #QMainWindow, QApplication, QWidget, QHBoxLayout, QTextBrowser, QMenuBar, QStatusBar, QTableWidget, QTableWidgetItem
import sys


class Main(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QGridLayout(self)
        layout.addWidget(Table(3, 2, parent=self), 0, 0, 1, 1)  # Ligne 0, colonne 0, 1 ligne, 1 colonne
        layout.addWidget(QTextEdit(parent=self), 0, 1, 1, 1)  # Ligne 0, colonne 1, 1 ligne, 1 colonne
        layout.addWidget(QTextEdit(parent=self), 1, 0, 1, 2)  # Ligne 1, colonne 0, 1 ligne, 2 colonnes
        self.show()


# __init__()
# class Main

class Table(QTableWidget):
    def __init__(self, rows, cols, *args, **kwargs):
        super().__init__(rows, cols, *args, **kwargs)

    def mousePressEvent(self, event):
        print(event.pos())
        print(event.button())

        menu = QMenu()
        menu.addAction('Action1')
        menu.addAction('Action2')
        menu.addAction('Action3')
        menu.exec_(event.globalPos())


# class Table

a = QApplication(sys.argv)
m = Main()
sys.exit(a.exec_())