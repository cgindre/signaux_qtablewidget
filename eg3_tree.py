import os, sys

# from PyQt5 import QtCore, QtGui, QtWidgets

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

import treelib


class BlockHierarchyNode(object):
    def __init__(self, icon_path=None, name="", description="", is_category=False):
        if icon_path is not None:
            self._icon = QtGui.QPixmap(icon_path)
            if self._icon.size() == QtCore.QSize():  # zero size (loading error)
                assert False

        else:
            self._icon = None

        self._is_category = bool(is_category)
        self._name = str(name)
        self._description = str(description)

    @property
    def icon(self):
        return self._icon

    @property
    def is_category(self):
        return self._is_category

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def __str__(self):
        if self.is_category:
            return "[%s]" % self.name
        else:
            return self.name


class AvailableBlocksModel(QtCore.QAbstractItemModel):
    def __init__(self, data_tree, parent=None):
        super(AvailableBlocksModel, self).__init__(parent)

        self._tree = data_tree
        assert isinstance(data_tree, treelib.Tree)

    def columnCount(self, parent_index):
        if parent_index.isValid():
            return 1
        else:
            return 1

    def rowCount(self, parent_index):
        if parent_index.isValid():
            return len(self._tree.children(parent_index.internalPointer().identifier))
        else:  # root node
            return 1

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            return str(index.internalPointer().data)
        elif role == QtCore.Qt.DecorationRole:
            icon = index.internalPointer().data.icon
            if icon is not None:
                return icon

        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if parent.isValid():
            parent_node = parent.internalPointer()
            children = self._tree.children(parent_node.identifier)
            return self.createIndex(row, column, children[row])
        else:
            return self.createIndex(row, column, self._tree.nodes[self._tree.root])

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        parent_item = self._tree.parent(child_item.identifier)

        if parent_item is None:
            return QtCore.QModelIndex()

        parent_row = 0
        siblings = self._tree.siblings(parent_item.identifier)
        for i, elm in enumerate(siblings):
            if elm == parent_item:
                parent_row = i

        return self.createIndex(parent_row, 0, parent_item)

    # def parent(self, index):
    #     if not index.isValid():
    #         return QtCore.QModelIndex()
    #
    #     child_item = index.internalPointer()
    #     parent_item = self._tree.parent(child_item.identifier)
    #
    #     if parent_item is None:
    #         return QtCore.QModelIndex()
    #
    #     if parent_item.is_root():
    #         parent_row = 0
    #     else:
    #         #siblings = self._tree.children(parent_item.bpointer)
    #         siblings = self._tree.children(parent_item.predecessor)
    #         for i, elm in enumerate(siblings):
    #             if elm == parent_item:
    #                 parent_row = i


class MegaTree(treelib.Tree):
    def add_block_node(self, data_block, identifier=None, parent_node=None):
        id = identifier if identifier is not None else data_block.name
        if parent_node is None:
            return self.create_node(str(data_block), id, data=data_block)
        else:
            return self.create_node(str(data_block), id, data=data_block, parent=parent_node.identifier)

    @staticmethod
    def create_demo_tree():
        tree = MegaTree()
        root_data = BlockHierarchyNode(name="All blocks", is_category=True)
        root_node = tree.add_block_node(root_data, "root")  # root node


        waveforms_data = BlockHierarchyNode(name="Waveforms", is_category=True)
        waveforms_node = tree.add_block_node(waveforms_data, parent_node=root_node)

        rect_waveform_data = BlockHierarchyNode(name="Rectangular waveform", is_category=False)
        rect_waveform_node = tree.add_block_node(rect_waveform_data, parent_node=waveforms_node)

        lfm_waveform_data = BlockHierarchyNode(name="LFM waveform", is_category=False)
        lfm_waveform_node = tree.add_block_node(lfm_waveform_data, parent_node=waveforms_node)

        phasecoded_waveform_data = BlockHierarchyNode(name="Phase coded waveform", is_category=False)
        phasecoded_waveform_node = tree.add_block_node(phasecoded_waveform_data, parent_node=waveforms_node)


        sensor_array_data = BlockHierarchyNode(name="Sensor arrays", is_category=True)
        sensor_array_node = tree.add_block_node(sensor_array_data, parent_node=root_node)

        ura_data = BlockHierarchyNode(name="URA", is_category=False)
        ura_node = tree.add_block_node(ura_data, parent_node=sensor_array_node)

        ula_data = BlockHierarchyNode(name="ULA", is_category=False)
        ula_node = tree.add_block_node(ula_data, parent_node=sensor_array_node)

        return tree


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    model = AvailableBlocksModel(MegaTree.create_demo_tree())

    view = QtWidgets.QTreeView()

    view.setModel(model)
    view.expandAll()
    view.show()

    sys.exit(app.exec_())