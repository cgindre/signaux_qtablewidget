# -*- coding: utf-8 -*-

import sys
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor

from tab_temps import tab_temps
from tab_temps_auto import tab_temps_auto

from gestion_temps import Instant, ListeInstant
import conversions
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tb1 = tab_temps()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    tb1 = tab_temps()
    tb1.show()
    #tb2 = tab_temps_auto()

    #window  = MainWindow()
    #window.show()
    app.exec()