# -*- coding: utf-8 -*-

import os
import sys
from PySide6.QtWidgets import QFileDialog, QApplication

app = QApplication()

dlg = QFileDialog()
dlg.setFileMode(QFileDialog.AnyFile)
#dlg.setNameFilter("Text fichiers (*.txt)")
#filenames = QStringList()

fname = QFileDialog.getOpenFileName('Open file', '/home/cyprien/Documents/Essai_PySide', "Image files (*.jpg *.gif)")
if dlg.exec():
   filenames = dlg.selectedFiles()

sys.exit(app.exec())