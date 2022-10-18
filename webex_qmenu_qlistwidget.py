#!/usr/bin/python
# -*- coding: utf-8 -*-

# Modules
# ------------------------------------------------------------------------------
import sys
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QWidget, QApplication, QListWidget, QMenu, QAbstractItemView, QGridLayout

# Variables
# ------------------------------------------------------------------------------
listItems = ["A","B","C","D","E","F","G"]

# widget
# ------------------------------------------------------------------------------
class Example(QWidget):

    def __init__(self,):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        # formatting
        self.setGeometry(300, 300, 250, 300)
        self.setWindowTitle("Input List")

        # widgets
        self.itemList = QListWidget()
        self.itemList.addItems(listItems)
        self.itemList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # context menu
        self.edit_menu = QMenu()
        removeItem = self.edit_menu.addAction('Remove Item')
        removeItem.triggered.connect(self.RemoveItem)

        self.editItem = self.edit_menu.addAction('Edit Item')
        self.editItem.triggered.connect(self.EditItem)

        self.itemList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.itemList.customContextMenuRequested.connect(self.on_context_menu)
        self.itemList.itemDoubleClicked.connect(self.EditItem)

        # layout
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.itemList, 0, 0)
        self.show()

    # def on_context_menu(self, pos):
    #     self.edit_menu.exec_(self.mapToGlobal(pos))

    def on_context_menu(self, pos):
        if len(self.itemList.selectedItems()) == 1:
            self.editItem.setEnabled(False)
        else:
            self.editItem.setEnabled(True)
        self.edit_menu.exec_(self.mapToGlobal(pos))

    def EditItem(self):
        print("Edit Item")

    def RemoveItem(self):
        print("Remove Item")

# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())