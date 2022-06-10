# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Slot
import sys

data = {'col1': ['1', '2', '3', '4'],
        'col2': ['1', '2', '1', '3'],
        'col3': ['1', '1', '2', '1']}


class TableView(QTableWidget):
    # def __init__(self, data, *args):
    #     QTableWidget.__init__(self, *args)
    # Alternatively :
    def __init__(self, data):
        QTableWidget.__init__(self)
        self.data = data
        self.setData()
    #     self.resizeColumnsToContents()
    #     self.resizeRowsToContents()
    #
    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

if __name__ == "__main__":
    # main(sys.argv)
    app = QApplication()
    # table = TableView(data, 4, 3)
    table = TableView(data)
    table.show()
    sys.exit(app.exec())