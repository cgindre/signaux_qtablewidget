# -*- coding: utf-8 -*-

import os
import sys
from PySide6.QtWidgets import QFileDialog, QApplication

# chemin = os.getcwd()
# print("type(chemin) = ", type(chemin))
# os.chdir("/home/cyprien/Documents/Essai_PySide")

app = QApplication()

# window = QFileDialog()
# print("window.directory() = ", window.directory())
# window.getOpenFileName(dir=r"/home/cyprien/Documents/Essai_PySide")
# #window.setDirectory(chemin)
# #window.show()
#
# fileName = window.getOpenFileName(str("Open File"), "/home/cyprien/Videos/", str("Images (*.png *.xpm *.jpg)"))
# window.show()

file_dialog = QFileDialog()
file_dialog.setNameFilters("Text files (*.txt);;Images (*.png *.jpg)")
file_dialog.selectNameFilter("Images (*.png *.jpg)")
file_dialog.getOpenFileName()
file_dialog.show()

sys.exit(app.exec())
