from eg2_qtreeview import RegneLinne
from PySide6.QtWidgets import QApplication, QWidget, QTreeView

import sys

from dialog_qtreeview import Ui_Dialog

class a_window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.regnes_tv = RegneLinne()
        self.ui.horizontalLayout.addWidget(self.regnes_tv)

        # self.regnes_tv = QTreeView()
        # self.ui.horizontalLayout.addWidget(self.regnes_tv)


# app = QApplication(sys.argv)
# un_regne = RegneLinne()
# un_regne.show()
# sys.exit(app.exec())

app = QApplication(sys.argv)
ma_window = a_window()
ma_window.show()
sys.exit(app.exec())