# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Slot
import sys
import donnees_nucleaires

list_symbole = donnees_nucleaires.list_fields_from_table("symbole", "Elements")
print("list_symbole = ", list_symbole)

app = QApplication()

tw = QTreeWidget()
# tw.setHeaderLabels(['Name', 'Cost($)'])
# cg = QTreeWidgetItem(tw, ['carrots', '2.99'])
# ch = QTreeWidgetItem(tw, ['radishes', '1.99'])
# cg1 = QTreeWidgetItem(cg, ['carrot', '0.33'])
# cg2 = QTreeWidgetItem(cg, ['carrottes rondes', '2.33'])
# ch1 = QTreeWidgetItem(ch, ['radish', '1.33'])

tw.setColumnCount(2)
cities = QTreeWidgetItem(tw)
cities.setText(0, "Cities")
osloItem = QTreeWidgetItem(cities)
osloItem.setText(0, "Oslo")
osloItem.setText(1, "Yes")




print(QMouseEvent.pos())

tw.show()

app.exec()