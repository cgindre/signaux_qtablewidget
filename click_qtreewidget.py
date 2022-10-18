# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QAction
from PySide6 import QtCore
import donnees_nucleaires

class SymbolesElements(QTreeWidget) :
    def __init__(self):
        super().__init__()
        list_symbole = donnees_nucleaires.list_fields_from_table("symbole", "Elements")
        print("list_symbole = ", list_symbole)

        self.list_tw = []
        for symbole in list_symbole:
            self.list_tw.append(QTreeWidgetItem(self, [symbole]))

        self.setHeaderLabels(['Élément'])

        self.itemPressed.connect(self.on_item_pressed)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("IN mouse_press_event")
        print("child clicked !")

        if (event.button() == QtCore.Qt.RightButton):
            print("right click !")
        elif (event.button() == QtCore.Qt.LeftButton):
            print("left click !")
            print("self.treePosition() = ", self.treePosition())

    def on_item_pressed(self) :
        print("IN on_item_pressed")
#
# def on_item_clicked() :
#     print("IN on_item_clicked")
#
# def on_item_double_clicked() :
#     print("IN on_item_double_clicked")

if __name__ == "__main__" :
    app = QApplication()

    eg = SymbolesElements()
    eg.show()

    app.exec()

# tw.itemPressed.connect(on_item_pressed)
# tw.itemClicked.connect(on_item_clicked)
# tw.itemDoubleClicked.connect(on_item_double_clicked)

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

# tw.show()
#
# app.exec()
