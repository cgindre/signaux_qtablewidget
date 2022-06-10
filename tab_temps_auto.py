# -*- coding: utf-8 -*-

import sys
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt

from gestion_temps import Instant, ListeInstant
import conversions

class tab_temps_auto(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.table = QtWidgets.QTableWidget(3, 4)
        self.table.columnLabels = ["t1", "t2", "N", ""]
        self.table.rowLabels = ["lin", "log", "exp"]
        self.table.setVerticalHeaderLabels(self.table.rowLabels)
        header = self.table.setHorizontalHeaderLabels(self.table.columnLabels)

        #self.table.setColumnWidth(2, 5)

        #header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(2, QtWidgets.QHeaderView.resizeSection(2, 5))

        self.table.resizeColumnToContents(2)
        self.table.show()

        # Ensemble de valeurs test
        for i in range(3):
            #self.table.setItem(i, 0, QTableWidgetItem("0s"))

            item = QTableWidgetItem()
            #item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight)
            self.table.setItem(i, 0, item)

            self.table.setItem(i, 0, item)
            item.setText("0s")
            #self.table.setItem(i, 0, QTableWidgetItem("0s").setTextAlignment(Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight))
            self.table.setItem(i, 1, QTableWidgetItem("20s"))
            self.table.setItem(i, 2, QTableWidgetItem("4"))

        for i in range(0, 3):
            self.table.pb_ajouter = QPushButton()
            self.table.pb_ajouter.setText("Ajouter")
            self.table.pb_ajouter.clicked.connect(self.on_pb_ajouter(i))
            self.table.setCellWidget(i, 3, self.table.pb_ajouter)

    def on_pb_ajouter(self, mode):
        def on_pb_ajouter():
            number_of_digits = 4
            print("on_pb_ajouter")
            t1 = self.table.item(mode, 0).text()
            t2 = self.table.item(mode, 1).text()
            N = self.table.item(mode, 2).text()
            print("t1 = ", t1, " t2 = ", t2, " N = ", N)
            if conversions.verifie_ligne_decoupage_temps(t1, t2, N):
                list_inst = ListeInstant()
                list_inst.ajoute_auto(t1 + " auto", t2 + " auto", int(N), mode)
                print(list_inst)
            else:
                print("probleme")
        return on_pb_ajouter


class QButton(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.button = QtWidgets.QPushButton('Button', self)
        self.name='me'
        self.button.clicked.connect(self.calluser)
    def calluser(self):
        print(self.name)

def demo_QButton():
    app = QtWidgets.QApplication(sys.argv)
    # tb = QButton()
    # tb.show()
    tb1 = tab_temps_auto()
    #tb1.show()
    app.exec()

if __name__=='__main__':
    demo_QButton()