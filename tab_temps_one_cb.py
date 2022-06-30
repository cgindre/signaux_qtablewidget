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

    def on_current_cell_changed(self):
        print("IN on_current_cell_changed")

    def on_cell_changed(self):
        print("IN on_cell_changed")

    def on_cell_clicked(self, row, column):
        print("IN on_cell_clicked")

        # S'il s'agit de la colonne des unités ... Ajout d'une combobox
        if column == 1:
            liste_unite = ["s", "mn", "h", "j", "an"]
            print("type(self.table.item(row, column)) = ", type(self.table.item(row, column)))
            unit = self.table.item(row, column).text()
            print("unit = ", unit)
            self.table.cb_unit = ComboboxUnit()
            mon_index = liste_unite.index(unit)
            self.table.cb_unit.setCurrentIndex(mon_index)
            self.table.cb_unit.currentTextChanged.connect(self.on_cb_convert(row))
            self.table.setCellWidget(row, 1, self.table.cb_unit)

        if self.previous_row != row:
            print("cellule différente ! AVANT : ", self.previous_row, " MTN : ", row)
            #unit = self.table.cb_unit.currentText()
            #print("unit = ", unit)
            self.table.removeCellWidget(self.previous_row, 1)
            self.previous_row = row



    # def on_item_tab_temps_add_row(self):
    #     """Fixe une ligne supplémentaire à la fin de tableau temps manuel avec liste déroulante dans unité"""
    #     nb_rows = self.rowCount()
    #     self.setRowCount(nb_rows + 1)
    #     unit_default = QTableWidgetItem("s")
    #     self.setItem(nb_rows, 1, unit_default)

    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.table = QtWidgets.QTableWidget(3, 2)
        self.table.columnLabels = ["Temps", "Unité"]
        header = self.table.setHorizontalHeaderLabels(self.table.columnLabels)

        self.previous_row = -1

        self.list_temps = ListeInstant()
        une_liste_valeurs = [10, 20, 30, 40, 50, 60, 70, 120]
        for valeur in une_liste_valeurs:
            self.list_temps.ajoute_instant(str(valeur) + "s" + " manu")


        print("self.list_temps = \n", self.list_temps)

        nb_rows = len(self.list_temps)
        self.table.setRowCount(nb_rows)

        liste_unite = ["s", "mn", "h", "j", "an"]
        for i in range(nb_rows):
            value = QTableWidgetItem(conversions.scientific_notation(str(self.list_temps.data[i].valeur())))
            unit = QTableWidgetItem(str(self.list_temps.data[i].unite()))

            self.table.setItem(i, 0, value)
            self.table.setItem(i, 1, unit)

        # Affiche une ligne supplementaire par defaut
        nb_rows = self.table.rowCount()
        self.table.setRowCount(nb_rows + 1)
        unit_default = QTableWidgetItem("s")
        self.table.setItem(nb_rows, 1, unit_default)


        # Formatage largeur de colonnes
        self.table.setColumnWidth(1, 50)
        self.table.resizeColumnToContents(0)
        self.table.show()

        # Detection changement d'item
        # self.table.setMouseTracking(True)
        # self.table.itemChanged.connect(self.on_item_changed)
        # self.table.itemEntered.connect(self.on_item_entered)
        # self.table.currentItemChanged.connect(self.on_current_item_changed)
        # self.table.cellEntered.connect(self.on_cell_entered)

        self.table.cellClicked.connect(self.on_cell_clicked)
        # self.table.cellChanged.connect(self.on_cell_changed)
        # self.table.currentCellChanged.connect(self.on_current_cell_changed)

        # Detection d'un changement d'unité
        # print(type(self.table.cellWidget(0,1)), type(self.table.cellWidget(0,1)))
        # self.table.cellWidget(0,1).currentTextChanged.connect(self.on_cb_changed)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    tb1 = tab_temps()
    app.exec()

