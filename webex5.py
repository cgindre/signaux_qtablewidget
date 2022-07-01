from PySide6 import * #QtCore

from PySide6 import QtGui
from PySide6.QtGui import * #QApplication, QMainWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QTextBrowser, QMenuBar, QStatusBar, QTableWidget, QTableWidgetItem
import sys


class Test(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.clipboardLabel = QtWidgets.QLabel()
        layout.addWidget(self.clipboardLabel)
        self.tableWidget = QtWidgets.QTableWidget(10, 10)
        layout.addWidget(self.tableWidget)
        self.tableWidget.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                print("CLIC GAUCHE")
                #index = self.tableWidget.indexAt(event.pos())
                index = self.tableWidget.indexAt(event.position().toPoint())
                if index.data():
                    self.clipboardLabel.setText(index.data())
            elif event.button() == QtCore.Qt.RightButton:
                print("CLIC DROIT")
                #index = self.tableWidget.indexAt(event.pos())
                index = self.tableWidget.indexAt(event.position().toPoint())
                if index.isValid():
                    item = self.tableWidget.itemFromIndex(index)
                    if not item:
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(index.row(), index.column(), item)
                    item.setText(self.clipboardLabel.text())
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainscreen = Test()
    mainscreen.show()
    app.exec_()

# https://stackoverflow.com/questions/63992863/how-to-catch-left-and-right-mouse-click-event-on-qtablewidget-in-pyqt5