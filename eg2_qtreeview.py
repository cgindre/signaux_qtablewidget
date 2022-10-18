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

        self.treemodel = QStandardItemModel()
        self.treemodel.setColumnCount(1)

        treemodel2 = QStandardItemModel()
        treemodel2.setColumnCount(1)

        # treemodel.setRowCount(0)
        self.treemodel.setHeaderData(0, Qt.Horizontal, "Règnes de Linné")
        treemodel2.setHeaderData(1, Qt.Horizontal, "Modèle à 5 règnes")
        rootNode = self.treemodel.invisibleRootItem()
        rootNode2 = treemodel2.invisibleRootItem()

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

        champignons = StandardItem("Champignons")
        rootNode2.appendRow(champignons)

        self.setModel(self.treemodel)
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

        print("TEST ACTUALISATION TREEVIEW : ")
        print("test3 type : ", type(self.treeview.currentIndex()))
        print("test3 : ", self.treeview.currentIndex())
        print("test3 parent: ", self.treeview.currentIndex().parent())
        curr_index = self.treeview.currentIndex().parent()
        self.treeview.setCurrentIndex(curr_index)
        # self.treeview.treemodel.in

        # global_position = treeView.mapToGlobal(position)
        # index = treeView.indexAt(position)
        # model = treeView.model()
        # item = model.itemFromIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec())

# lien tuto : https://www.youtube.com/watch?v=080bipFDWDk