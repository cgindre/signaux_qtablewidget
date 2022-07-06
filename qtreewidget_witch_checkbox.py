# -*- coding: utf-8 -*-

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
import donnees_nucleaires

list_symbole = donnees_nucleaires.list_fields_from_table("symbole", "Elements")
print("list_symbole = ", list_symbole)


def verifie_case():
    print("IN verifie_case")

    if cg.checkState(0) == Qt.Checked:
        print('item is checked')
    elif cg.checkState(0) == Qt.Unchecked:
        print('item is unchecked')

    print("Appel de list_items_checked()")
    list_items_checked()

def list_items_checked():
    """ Retourne une liste de tous les items qui ont été cochés """
    list_items_checked = []
    it = QTreeWidgetItemIterator(tw)
    print("type(it) = ", type(it))

    while it.value() :
        print("it.value().text(0) = ", it.value().text(0))
        print("it.value().text(1) = ", it.value().text(1))

        if it.value().checkState(0) == Qt.Checked:
            print(it.value().text(0) + " coché")
            # list_items_checked.append(it.value())
        it +=1

    print("FIN DU WHILE !!!")


app = QApplication()

tw = QTreeWidget()
tw.setHeaderLabels(['Name', 'Cost($)'])

cg = QTreeWidgetItem(tw, ['carrots', '2.99'])

#cg.setFlags(cg.flags() | Qt.ItemIsUserCheckable)
# cg.setFlags(cg.flags())
# cg.setCheckState(0, Qt.Unchecked)

ch = QTreeWidgetItem(tw, ['radishes', '1.99'])

cg1 = QTreeWidgetItem(cg, ['carrot', '0.33'])
cg1.setFlags(cg1.flags())
cg1.setCheckState(0, Qt.Unchecked)

cg2 = QTreeWidgetItem(cg, ['carrottes rondes', '2.33'])
cg2.setFlags(cg2.flags())
cg2.setCheckState(0, Qt.Unchecked)

ch1 = QTreeWidgetItem(ch, ['radish', '1.33'])
ch1.setFlags(ch1.flags())
ch1.setCheckState(0, Qt.Unchecked)

tw.itemChanged.connect(verifie_case)
tw.show()



app.exec()