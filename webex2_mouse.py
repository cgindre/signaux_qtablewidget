from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys

class Main(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout  = QHBoxLayout(self)
        table = QTableWidget(3, 2)
        table.setMouseTracking(True)
        layout.addWidget(table)
        self.show()

    def mousePressEvent(self, QMouseEvent):
        #print mouse position
        print(QMouseEvent.pos())

a = QApplication([])
m = Main()
#m.show()
sys.exit(a.exec_())
