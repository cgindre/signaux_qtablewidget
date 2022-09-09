# -*- coding: utf-8 -*-

import os
import sys

from PySide6.QtCore import Qt
from PySide6 import QtGui
from PySide6.QtGui import QBrush, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QTabWidget, QCheckBox, QTableWidget, QTableWidgetItem, QComboBox, \
    QRadioButton, QTextEdit, QColumnView, QFileDialog, QMenu, QDialog, QTreeWidgetItem, QLineEdit, QDialogButtonBox, \
    QTreeWidgetItemIterator, QMainWindow, QApplication, QVBoxLayout


from gestion_temps import Instant, ListeInstant
import conversions as conversions
from test_TableTemps import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.btn = QPushButton("Charger")
        self.btn.pressed.connect(self.on_pb_charger)

        liste_t = ListeInstant()
        self.tab_temps = TableTemps(liste_t)

        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.tab_temps)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)


    def on_pb_charger(self):
        print("IN on_pb_charger")
        # self.ui.tab_temps.blockSignals(True)

        self.tab_temps.blockSignals(True)

        file_dg = QFileDialog(self)
        #file_dg.setDirectory(os.path.join(utils.AppDefaultPath.PATH_DI_EXAMPLE_IMPORT))
        file_dg.setDirectory("C:\\Users\\cygindre\\Documents\\MissionCEA\\Erastem3\\Erastem2_v2.7.5.win32_noprotect\\imports\\")
        file_dg.setWindowTitle("Charger des instants de calcul")
        file_dg.setWindowIcon(QIcon(QPixmap(':/images_canvas/ptiRadioactif')))
        file_dg.setViewMode(QFileDialog.Detail)
        file_dg.setFileMode(QFileDialog.AnyFile)
        file_dg.setNameFilter("Instants (*.csv)")
        file_dg.setAcceptMode(QFileDialog.AcceptOpen)
        res = file_dg.exec()
        if res == 0:
            return None
        files = file_dg.selectedFiles()
        infile = open(files[0], "r")
        lines = infile.readlines()
        infile.close()


        nb_rows = self.tab_temps.rowCount()

        # Parcourt les lignes issues du fichier .csv
        for i in range(0, len(lines)):
            tokens = lines[i].strip().split(";")
            instant_tmp = tokens[0] + tokens[1] + " manu"
            self.tab_temps.list_temps.ajoute_instant(instant_tmp)

        self.tab_temps.display_tab_temps()


        #
        # nb_rows = len(self.tab_temps.list_temps)
        # self.tab_temps.setRowCount(nb_rows)
        #
        # for i in range(0, nb_rows):
        #     # Colonne valeur "Temps" de tableau manuel
        #     value = QTableWidgetItem(conversions.scientific_notation(str(self.tab_temps.list_temps.data[i].valeur())))
        #     # Fixe la valeur du temps dans tableau manuel, couleur et ajuste largeur colonne
        #     self.tab_temps.setItem(i, 0, value)
        #     self.tab_temps.on_item_tab_temps_set_color(i)
        #     self.tab_temps.resizeColumnToContents(0)
        #
        #     # Colonne unité de tableau manuel
        #     unit = str(self.tab_temps.list_temps.data[i].unite())
        #     self.tab_temps.setItem(i, 1, QTableWidgetItem(unit))
        #
        # # Affiche une ligne supplementaire par defaut avec liste déroulante dans unité
        # self.tab_temps.on_item_tab_temps_add_row()
        #
        # self.tab_temps.blockSignals(False)
        # print("liste : \n", self.tab_temps.list_temps)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec()