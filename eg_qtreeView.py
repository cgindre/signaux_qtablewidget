from PySide6.QtWidgets import QTreeView, QFileSystemModel, QApplication
from PySide6.QtCore import QDir


if __name__ == "__main__" :
    app = QApplication()

    model = QFileSystemModel()
    model.setRootPath(QDir.currentPath())

    tree = QTreeView()
    tree.setModel(model)
    tree.show()

    app.exec()