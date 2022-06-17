# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Slot
import sys

app = QApplication()

tw = QTreeWidget()
tw.setHeaderLabels(['Name', 'Cost($)'])
cg = QTreeWidgetItem(tw, ['carrots', '2.99'])
ch = QTreeWidgetItem(tw, ['radishes', '1.99'])
cg1 = QTreeWidgetItem(cg, ['carrot', '0.33'])
cg2 = QTreeWidgetItem(cg, ['carrottes rondes', '2.33'])
ch1 = QTreeWidgetItem(ch, ['radish', '1.33'])

tw.show()

app.exec()