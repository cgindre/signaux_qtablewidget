# -*- coding: utf-8 -*-

import sys
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import *#QTableWidget, QTableWidgetItem, QComboBox, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor

from gestion_temps import Instant, ListeInstant
import conversions

#class tab_temps(QtWidgets.QWidget):
class tab_temps(QDialog):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.table = QtWidgets.QTableWidget(3, 2)
        #self.setCentralWidget(self.label)

    # def __init__(self, parent = None):
    #     QtWidgets.QWidget.__init__(self, parent)
    #
    #     self.table = QtWidgets.QTableWidget(3, 2)
    #     self.table.columnLabels = ["Temps", "Unité"]
    #     header = self.table.setHorizontalHeaderLabels(self.table.columnLabels)
    #
    #     self.table.show()

    def mouseMoveEvent(self, e):
        #self.label.setText("mouseMoveEvent")
        print("mouseMoveEvent")

    def mousePressEvent(self, e):
        #self.label.setText("mousePressEvent")
        print("mousePressEvent")

    def mouseReleaseEvent(self, e):
        #self.label.setText("mouseReleaseEvent")
        print("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        #self.label.setText("mouseDoubleClickEvent")
        print("mouseDoubleClickEvent")



if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    tb1 = tab_temps()
    tb1.show()
    app.exec()
