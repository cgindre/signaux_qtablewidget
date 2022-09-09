# -*- coding: utf-8 -*-

import os

# ==== QT6 ====
from PySide6.QtCore import Qt
from PySide6 import QtGui
from PySide6.QtGui import QBrush, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QTabWidget, QCheckBox, QTableWidget, QTableWidgetItem, QComboBox, \
    QRadioButton, QTextEdit, QColumnView, QFileDialog, QMenu, QDialog, QTreeWidgetItem, QLineEdit, QDialogButtonBox, \
    QTreeWidgetItemIterator

from gestion_temps import Instant, ListeInstant
import conversions as conversions

class TableTemps(QTableWidget):
    def __init__(self, liste_instants:ListeInstant, parent=None):
        super().__init__(parent)
        self.win_creation_cas = parent

        self.list_temps = liste_instants

        self.init_table()

    def init_table(self):
        """ Initialisation graphique du tableau des instants de calcul"""
        self.blockSignals(True)

        rows = 1
        cols = 2
        columnLabels = ["Temps", "Unité"]

        self.setRowCount(rows)
        self.setColumnCount(cols)
        self.setHorizontalHeaderLabels(columnLabels)
        self.resizeColumnsToContents()

        # Variable associé à la ligne cliqué avant de tableau_temps, gestion qcombobox_unit
        self.previous_row = -1

        # Par défaut affiche "s" (seconde) dans colonne Unité
        self.setItem(0, 1, QTableWidgetItem("s"))

        self.display_tab_temps()

        self.blockSignals(False)


    def on_item_tab_temps_set_color(self, index):
        """Fixe couleur texte QTableWidgetItem indexé : noir->"manu", bleu->"auto" """
        print("IN on_item_tab_temps_set_color")
        self.blockSignals(True)
        if self.list_temps.data[index].auto:
            self.item(index, 0).setForeground(QBrush(Qt.blue))
        else:
            self.item(index, 0).setForeground(QBrush(Qt.black))
        self.blockSignals(False)

    def on_item_tab_temps_add_row(self):
        """Fixe une ligne supplémentaire à la fin de tableau temps manuel avec liste déroulante dans unité"""
        print("IN on_item_tab_temps_add_row")
        self.blockSignals(True)
        nb_rows = self.rowCount()

        self.setRowCount(nb_rows + 1)

        unit_default = QTableWidgetItem("s")
        self.setItem(nb_rows, 1, unit_default)
        self.blockSignals(False)


    def display_tab_temps(self):
        print("IN display_tab_temps")

        self.blockSignals(True)

        nb_rows = len(self.list_temps)
        print("nb_rows = ", nb_rows)
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

        self.itemChanged.connect(self.on_item_tab_temps_modified)

        self.blockSignals(False)


    def on_cb_convert(self, index):
        def on_cb_convert():
            self.blockSignals(True)
            try:
                unite = self.cellWidget(index, 1).currentText()
                print("unite = ", unite)
                value = self.list_temps.data[index].value
                print("value = ", value)
                new_value = conversions.convertit_temps(value, "s", unite)
                print("new_value = ", new_value)

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
        self.blockSignals(True)
        print("IN on_cell_clicked")
        print("column = ", column)
        print("row = ", row)
        # S'il s'agit de la colonne des unités ... Ajout d'une combobox
        if column == 1:
            liste_unite = ["s", "mn", "h", "j", "an"]
            unit = self.item(row, column).text()
            print("unit = ", unit)
            self.cb_unit = ComboboxUnit()
            mon_index = liste_unite.index(unit)
            self.cb_unit.setCurrentIndex(mon_index)
            self.cb_unit.currentTextChanged.connect(self.on_cb_convert(row))

            self.setCellWidget(row, 1, self.cb_unit)

        print("self.previous_row = ", self.previous_row)
        print("row = ", row)
        # Si une combobobox existait déjà, on enlève son affichage
        if self.previous_row != row and self.previous_row != -1:
            self.removeCellWidget(self.previous_row, 1)
            print("self.list_temps", self.list_temps)
            print("len(self.list_temps) = ", len(self.list_temps))
            try:
                unit = QTableWidgetItem(self.list_temps.data[self.previous_row].unite())
            except IndexError:
                unit = QTableWidgetItem("s")
            self.setItem(self.previous_row, 1, unit)

        self.previous_row = row
        self.blockSignals(False)

    def on_item_tab_temps_modified(self):
        print("IN on_item_tab_temps_modified")

        self.blockSignals(True)
        print("valeur blockSignals : ", self.blockSignals())

        try:
            valeur_saisie = self.currentItem().text()

            # Si valeur_saisie est bien un nombre alors
            if conversions.verifie_valeur(valeur_saisie):
                # Affichage valeur saisie dans tableau manuel
                self.currentItem().setText(conversions.scientific_notation(valeur_saisie))
                self.resizeColumnToContents(0)

                # Changement de self.list_temps
                print("self.currentRow() = ", self.currentRow())
                print("self.currentColumn() = ", self.currentColumn())
                print("type(self.cellWidget(self.currentRow(), self.currentColumn()) = ", type(self.cellWidget(self.currentRow(), self.currentColumn() + 1)))
                print("type(self.cellWidget(self.currentRow(), self.currentColumn()) = ", type(self.cellWidget(self.currentRow(), self.currentColumn())))
                print("lecture_unite = ", self.item(self.currentRow(), self.currentColumn() + 1).text())
                #current_instant = Instant(tab.currentItem().text() + tab.cellWidget(tab.currentRow(), tab.currentColumn() + 1).currentText() + " manu")
                current_value = self.currentItem().text()
                print("self.currentRow() = ", self.currentRow())
                print("toules les unites : ")
                for i in range(self.rowCount()):
                    print("unite = ", self.item(i, self.currentColumn() + 1).text())
                print("self.currentRow() = ", self.currentRow(), "len(self.list_temps)", len(self.list_temps))

                try:
                    current_unit = self.cellWidget(self.currentRow(), 1).currentText()
                    print("current_unit (cellWidget) = ", current_unit)
                except:
                    current_unit = self.item(self.currentRow(), self.currentColumn() + 1).text()
                    print("current_unit (item) = ", current_unit)

                # current_unit = tab.item(tab.currentRow(), tab.currentColumn() + 1).text()
                print("current_value + current_unit + manu = ", current_value + current_unit + " manu")
                current_instant = Instant(current_value + current_unit + " manu")

                # Si une valeur de self.liste_temps doit être modifié
                if self.currentRow() < len(self.list_temps):
                    # self.tab_temps.list_temps.modifie_instant(tab.currentRow(), current_instant)
                    self.list_temps.modifie_instant(self.currentRow(), current_instant)
                    nb_current_row = self.currentRow()

                    # self.tab_temps.on_item_tab_temps_set_color(tab.currentRow())
                    self.on_item_tab_temps_set_color(self.currentRow())
                # Sinon une valeur de self.list_temps doit être ajouté
                else:
                    # Un instant a été ajouté, une ligne supplémentaire est donc insérée avec liste déroulante dans unité
                    # self.tab_temps.list_temps.ajoute_instant(current_instant)
                    self.list_temps.ajoute_instant(current_instant)
                    self.on_item_tab_temps_add_row()
            # Sinon ce n'est pas un nombre
            else:
                print("ce n'est pas un nombre")
                # Essaye de remettre l'élément de self.list_temps affiché précédemment
                try: self.currentItem().setText(
                    # conversions.scientific_notation(str(self.list_temps.data[tab.currentRow()].valeur())))
                    conversions.scientific_notation(str(self.list_temps.data[self.currentRow()].valeur())))
                # Sinon, on met du "blanc".
                except: self.currentItem().setText("")
        except:
            pass
        self.blockSignals(False)

        print("self.list_temps = ", self.list_temps)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()

    liste_t = ListeInstant()
    # liste_t.ajoute_auto("0s manu", "20s manu", 5, 0)
    liste_t.ajoute_auto("0s auto", "30mn auto", 5, 0)
    ma_table = TableTemps(liste_t)
    ma_table.show()


    app.exec()