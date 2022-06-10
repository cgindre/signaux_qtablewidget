# -*- coding: utf-8 -*-

import sys
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor

from gestion_temps import Instant, ListeInstant
import conversions

class ComboboxUnit(QComboBox):
    def __init__(self):
        (QComboBox).__init__(self)
        self.liste_unite = ["s", "mn", "h", "j", "an"]
        self.addItems(self.liste_unite)


class tab_temps(QtWidgets.QWidget):

    def on_cb_convert(self, index):
        def on_cb_convert():
            unite = self.table.cellWidget(index, 1).currentText()
            value = self.list_temps.data[index].valeur()
            new_value = conversions.convertit_temps(value, "s", unite)
            new_value = QTableWidgetItem(conversions.scientific_notation(str(new_value)))
            #new_value.setForeground(QBrush(QColor("#81F8E3")))
            new_value.setForeground(QBrush(Qt.blue))
            self.table.setItem(index, 0, new_value)
        return on_cb_convert

    def on_item_changed(self):
        print("IN on_item_changed")

    def on_item_entered(self):
        print("IN on_item_entered")

    def on_current_item_changed(self):
        print("IN on_current_item_changed")

    def on_cell_entered(self):
        print("IN on_cell_entered")

    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.table = QtWidgets.QTableWidget(3, 2)
        self.table.columnLabels = ["Temps", "Unité"]
        header = self.table.setHorizontalHeaderLabels(self.table.columnLabels)

        self.list_temps = ListeInstant()
        # une_liste_valeurs = [10, 20, 30, 40, 50, 60, 70, 120]
        # for valeur in une_liste_valeurs:
        #     self.list_temps.ajoute_instant(str(valeur) + "s" + " manu")


        # print("self.list_temps = \n", self.list_temps)
        #
        # nb_rows = len(self.list_temps)
        # self.table.setRowCount(nb_rows)
        #
        # liste_unite = ["s", "mn", "h", "j", "an"]
        # for i in range(nb_rows):
        #     value = QTableWidgetItem(conversions.scientific_notation(str(self.list_temps.data[i].valeur())))
        #     unit = str(self.list_temps.data[i].unite())
        #
        #     self.table.setItem(i, 0, value)
        #
        #     self.table.cb_unit = ComboboxUnit()
        #     mon_index = liste_unite.index(unit)
        #     self.table.cb_unit.setCurrentIndex(mon_index)
        #     self.table.cb_unit.currentTextChanged.connect(self.on_cb_convert(i))
        #     self.table.setCellWidget(i, 1, self.table.cb_unit)
        #
        # # Affiche une ligne supplementaire par defaut
        # last_row_nb = self.table.rowCount()
        # self.table.insertRow(last_row_nb)
        # self.table.setCellWidget(last_row_nb, 1, ComboboxUnit())

        # Formatage largeur de colonnes
        self.table.setColumnWidth(1, 50)
        self.table.resizeColumnToContents(0)
        #self.table.show()

        # Detection changement d'item
        self.table.setMouseTracking(True)
        self.table.itemChanged.connect(self.on_item_changed)
        self.table.itemEntered.connect(self.on_item_entered)
        self.table.currentItemChanged.connect(self.on_current_item_changed)
        self.table.cellEntered.connect(self.on_cell_entered)

        # Detection d'un changement d'unité
        # print(type(self.table.cellWidget(0,1)), type(self.table.cellWidget(0,1)))
        # self.table.cellWidget(0,1).currentTextChanged.connect(self.on_cb_changed)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    tb1 = tab_temps()
    app.exec()

