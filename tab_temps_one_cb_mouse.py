# -*- coding: utf-8 -*-

import sys
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6 import * #QtCore

from gestion_temps import Instant, ListeInstant
import conversions

class ComboboxUnit(QComboBox):
    def __init__(self):
        (QComboBox).__init__(self)
        self.liste_unite = ["s", "mn", "h", "j", "an"]
        self.addItems(self.liste_unite)


#class tab_temps(QtWidgets.QWidget):
class tab_temps(QTableWidget):
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent=parent)

        self.columnLabels = ["Temps", "Unité"]
        header = self.setHorizontalHeaderLabels(self.columnLabels)

        self.previous_row = -1

        self.list_temps = ListeInstant()
        une_liste_valeurs = [10, 20, 30, 40, 50, 60, 70, 120]
        for valeur in une_liste_valeurs:
            self.list_temps.ajoute_instant(str(valeur) + "s" + " auto")

        print("self.list_temps = \n", self.list_temps)

        nb_rows = len(self.list_temps)
        self.setRowCount(nb_rows)

        liste_unite = ["s", "mn", "h", "j", "an"]
        for i in range(nb_rows):
            value = QTableWidgetItem(conversions.scientific_notation(str(self.list_temps.data[i].valeur())))
            unit = QTableWidgetItem(str(self.list_temps.data[i].unite()))

            self.setItem(i, 0, value)
            self.on_item_tab_temps_set_color(i)
            self.setItem(i, 1, unit)

        # Affiche une ligne supplementaire par defaut
        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 1)
        unit_default = QTableWidgetItem("s")
        self.setItem(nb_rows, 1, unit_default)

        # Formatage largeur de colonnes
        self.setColumnWidth(1, 50)
        self.resizeColumnToContents(0)
        self.show()

        self.cellClicked.connect(self.on_cell_clicked)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
            print("CLIC DROIT")
            menu = QMenu()

            # act1 = menu.addAction('Action1')
            # act1.triggered.connect(self.test())

            menu.addAction('Action1', self.actionClicked)
            menu.addAction('Action2', self.actionClicked)
            menu.addAction('Action3', self.actionClicked)

            #menu.exec(event.globalPos())
            menu.exec(event.globalPosition().toPoint())

    def actionClicked(self):
        action = self.sender()
        print('Action: ', action.text())

    def test(self):
        print("click")

    def on_item_tab_temps_set_color(self, index):
        """Fixe couleur texte QTableWidgetItem indexé : noir->"manu", bleu->"auto" """
        if self.list_temps.data[index].auto:
            self.item(index, 0).setForeground(QBrush(Qt.blue))
        else:
            self.item(index, 0).setForeground(QBrush(Qt.black))

    def on_cb_convert(self, index):
        def on_cb_convert():
            self.blockSignals(True)
            try:
                unite = self.cellWidget(index, 1).currentText()
                value = self.list_temps.data[index].value
                new_value = conversions.convertit_temps(value, "s", unite)
                # Sauvegarde nouvelle unité temps d'expression d'instant
                self.list_temps.data[index].set_unit(unite)
                print("nouvelle liste : \n", self.list_temps)

                # Modification affichage dans tableau temps manuel
                new_value = QTableWidgetItem(conversions.scientific_notation(str(new_value)))
                self.setItem(index, 0, new_value)
                self.on_item_tab_temps_set_color(index)
            except:
                pass
            self.blockSignals(False)
        return on_cb_convert

    def on_cell_clicked(self, row, column):
        print("IN on_cell_clicked")
        print("column = ", column)
        print("row = ", row)
        # S'il s'agit de la colonne des unités ... Ajout d'une combobox
        if column == 1:
            liste_unite = ["s", "mn", "h", "j", "an"]
            print("type(self.item(row, column)) = ", type(self.item(row, column)))
            unit = self.item(row, column).text()
            print("unit = ", unit)
            self.cb_unit = ComboboxUnit()
            mon_index = liste_unite.index(unit)
            self.cb_unit.setCurrentIndex(mon_index)
            self.cb_unit.currentTextChanged.connect(self.on_cb_convert(row))
            self.setCellWidget(row, 1, self.cb_unit)

        if self.previous_row != row and self.previous_row != -1:
            self.removeCellWidget(self.previous_row, 1)
            unit = QTableWidgetItem(self.list_temps.data[self.previous_row].unite())
            self.setItem(self.previous_row, 1, unit)

        self.previous_row = row


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    tb1 = tab_temps(3, 2)
    tb1.show()
    app.exec()

