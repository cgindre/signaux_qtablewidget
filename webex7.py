from PyQt5.QtWidgets import QApplication, QMenu


class ClassMenu(QMenu):
    def __init__(self):
        super(ClassMenu, self).__init__()
        class_A = self.addMenu("ClassA")
        class_A1 = class_A.addAction("ClassA1")
        class_A2 = class_A.addMenu("ClassA2")
        class_A3 = class_A2.addAction("ClassA3")
        class_B = self.addAction("ClassB")

        class_A1.triggered.connect(self.onActionClicked)
        class_A3.triggered.connect(self.onActionClicked)
        class_B.triggered.connect(self.onActionClicked)

        print(class_A.menuAction())

    def onActionClicked(self):
        print(self.sender().text())

    def onMenuClicked(self, menu):
        print(menu.title())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        action = self.actionAt(event.pos())
        if not action:
            return
        menu = action.menu()
        if menu:
            self.onMenuClicked(menu)


def main():
    app = QApplication([])
    menu = ClassMenu()
    menu.move(100, 100)
    menu.exec_()


if __name__ == "__main__":
    main()