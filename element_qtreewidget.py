# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Slot
import sys
import donnees_nucleaires

def on_item_pressed() :
    print("IN on_item_pressed")

def on_item_clicked() :
    print("IN on_item_clicked")

def on_item_double_clicked() :
    print("IN on_item_double_clicked")

def mousePressEvent(self, event) :
    print("IN mouse_press_event")
    print("child clicked !")

    if (event.button() == QtCore.Qt.RightButton) :
        print("right click !")

list_symbole = donnees_nucleaires.list_fields_from_table("symbole", "Elements")
print("list_symbole = ", list_symbole)

app = QApplication()

tw = QTreeWidget()
tw.setHeaderLabels(['Élément'])

list_tw = []
for symbole in list_symbole:
    list_tw.append(QTreeWidgetItem(tw, [symbole]))


tw.itemPressed.connect(on_item_pressed)
tw.itemClicked.connect(on_item_clicked)
tw.itemDoubleClicked.connect(on_item_double_clicked)

# tw.setHeaderLabels(['Name', 'Cost($)'])
# cg = QTreeWidgetItem(tw, ['carrots', '2.99'])
# ch = QTreeWidgetItem(tw, ['radishes', '1.99'])
# cg1 = QTreeWidgetItem(cg, ['carrot', '0.33'])
# cg2 = QTreeWidgetItem(cg, ['carrottes rondes', '2.33'])
# ch1 = QTreeWidgetItem(ch, ['radish', '1.33'])

# Quelques optons de QTreeWidgetItem
# print("item = ", item)
# print("item.parent = ", item.parent())
# print("item.parent.text() = ", item.parent().text(0))
# print("type(item.parent) = ", type(item.parent()))

tw.show()

app.exec()

