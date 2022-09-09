import sys
from PySide6.QtWidgets import QTreeView, QApplication, QMainWindow
from PySide6.QtCore import QDir, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel, Qt, QPainter, QRegion

tree_style = """
QTreeView {
    alternate-background-color: yellow;
}
"""

class StandardItem(QStandardItem):
    def __init__(self, txt=""):
        super().__init__()

        # Si on rend l'item éditable
        self.setEditable(False)

        self.setText(txt)
        self.mon_signal = Signal(bool)

class RegneLinne(QTreeView):
    def __init__(self):
        super(RegneLinne, self).__init__()
        self.setStyleSheet(tree_style)
        self.header().setStretchLastSection(True)

        self.setRootIsDecorated(True)

        treemodel = QStandardItemModel()
        treemodel.setColumnCount(1)
        treemodel.setHeaderData(0, Qt.Horizontal, "Règnes de Linné")
        rootNode = treemodel.invisibleRootItem()

        animaux = StandardItem("Animaux")

        chat = StandardItem("Chats")
        animaux.appendRow(chat)

        chien = StandardItem("Chien")
        animaux.appendRow(chien)

        vache = StandardItem("Vache")
        animaux.appendRow(vache)

        rootNode.appendRow(animaux)

        vegetaux = StandardItem("Vegetaux")

        petunia = StandardItem("Petunia")
        vegetaux.appendRow(petunia)

        dahlia = StandardItem("Dahlia")
        vegetaux.appendRow(dahlia)

        rootNode.appendRow(vegetaux)

        mineraux = StandardItem("Minéraux")
#        mineraux.mon_signal.

        quartz = StandardItem("Quartz")
        mineraux.appendRow(quartz)

        rootNode.appendRow(mineraux)

        self.setModel(treemodel)
        self.expandAll()
        self.resizeColumnToContents(0)


class AppDemo(QMainWindow) :
    def __init__(self):
        super().__init__()

        self.treeview = RegneLinne()
        self.treeview.clicked.connect(self.on_clicked)

        self.setCentralWidget(self.treeview)

    def on_clicked(self, signal):
        print("IN on clicked")
#         print("item = ", item)
        print("signal = ", signal)
#        tot = self.treeview.model().fil
        print(self.treeview.currentIndex())
#        self.treeview.currentChanged()
#        print("un test : ", self.treeview.indexFromItem(tree.currentItem().parent()))
        print("test1 : ", self.treeview.selectedIndexes()[0].parent().data())
        print("test2 : ", self.treeview.selectedIndexes()[0].data())


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec())

# lien tuto : https://www.youtube.com/watch?v=080bipFDWDk