# ==== QT6 ====
import os.path


from PySide6.QtCore import Qt, QPoint, Signal, Slot, QObject
from PySide6.QtGui import QPainter, QStandardItem, QStandardItemModel, QPixmap, Qt, QMouseEvent
from PySide6.QtWidgets import QWidget, QAbstractItemView, QSlider, QTableWidgetItem, QTreeWidgetItem, QMenu, \
    QFileDialog, QGraphicsItem, QTreeWidget, QTreeView
from PySide6.QtCharts import *
from PySide6.QtPrintSupport import QPrintDialog, QPrintPreviewDialog, QPrinter


# ==== Forms ====
import utils
from form.ui_res_widget import Ui_Form as Ui_ResultatWindow
from ihm.edition_resultat import EditionResultat
from calcul.conversions import scientific_notation, convertit_temps, convertit_matiere
from calcul.donnees_nucleaires import DonneesNucleaires
from calcul.gestion_temps import InstantSimple


from projectErastem import ErastemProject, ErastemProjectData, ErastemProjectParams, ErastemDataStructure, \
    ErastemDataMilieu, ErastemDataTransfert, ErastemDataElementCollection


class MyChartView(QChartView):
    def __init__(self, parent=None):
        super(MyChartView, self).__init__(parent)
        self.resultats_win = parent
        self.menu = QMenu(self)
        menu_unit = self.menu.addMenu("Choisir l'unité")

        menu_unit.addAction("Secondes", self.action_seconde)
        menu_unit.addAction("Minutes", self.action_minute)
        menu_unit.addAction("Heures", self.action_heure)
        menu_unit.addAction("Jours", self.action_jour)
        menu_unit.addAction("Ans", self.action_annee)

        self.menu.addAction("Enregistrer le graphique", self.action_save_graph)
        self.menu.addAction("Imprimer le graphique", self.action_print_graph)

    def action_seconde(self):
        """
        Fonction qui transforme l'unité de temps en secondes
        """
        res_win = self.resultats_win  # type: ResultatWindow
        res_win.draw_graph(res_win.idx_graph, res_win.bool_integral, 's')

    def action_minute(self):
        """
        Fonction qui transforme l'unité de temps en minutes
        """
        res_win = self.resultats_win  # type: ResultatWindow
        res_win.draw_graph(res_win.idx_graph, res_win.bool_integral, 'mn')

    def action_heure(self):
        """
        Fonction qui transforme l'unité de temps en heures
        """
        res_win = self.resultats_win  # type: ResultatWindow
        res_win.draw_graph(res_win.idx_graph, res_win.bool_integral, 'h')

    def action_jour(self):
        """
        Fonction qui transforme l'unité de temps en jours
        """
        res_win = self.resultats_win  # type: ResultatWindow
        res_win.draw_graph(res_win.idx_graph, res_win.bool_integral, 'j')

    def action_annee(self):
        """
        Fonction qui transforme l'unité de temps en années
        """
        res_win = self.resultats_win  # type: ResultatWindow
        res_win.draw_graph(res_win.idx_graph, res_win.bool_integral, 'an')

    def action_save_graph(self):
        """
        Fonction qui permet d'enregistrer le graphique
        """
        fd = QFileDialog(self)
        fd.setFileMode(QFileDialog.ExistingFiles)
        fd.setNameFilter("Images (*.png *.jpg *.xpm)")
        fd.setViewMode(QFileDialog.Detail)
        fd.setAcceptMode(QFileDialog.AcceptSave)
        filename = ""
        if fd.exec():
            filename = fd.selectedFiles()

        res_win = self.resultats_win  # type: ResultatWindow
        pixmap_graph = res_win.chart_view.grab()
        pixmap_graph.save(filename[0], "PNG")

    def action_print_graph(self):
        """
        Fonction qui permet d'imprimer le graphique
        """
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handle_paint_request)
        dialog.exec_()

    def handle_paint_request(self, printer):
        res_win = self.resultats_win  # type: ResultatWindow
        painter = QPainter(printer)
        painter.setViewport(res_win.chart_view.rect())
        painter.setWindow(res_win.chart_view.rect())
        res_win.chart_view.render(painter)
        painter.end()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.RightButton:
            mouse_pos = QPoint(event.screenPos().x(), event.screenPos().y())
            self.menu.exec(mouse_pos)

    def mouseReleaseEvent(self, event):
        pass

class ResultatItem(QStandardItem):
    def __init__(self, txt = ""):
        super().__init__()

        self.setEditable(False)
        self.setText(txt)
class ResultatTreeView(QTreeView, QObject) :
    mon_signal = Signal(str)
    def __init__(self, parent, name_and_id_elems, res_in_post_fic):
        QTreeView.__init__(self)



        # Clé dictionnaire -> nom de l'élément
        # Valeur dictionnaire -> liste de str, où chaque str est le nom d'un résultat
        # Par exemple -> {estomac : [R0, R1], thyroide : []}
        dict_elements_and_res_list = {}

        # Remplissage des clés et valeurs initialisées à liste vide
        for element in name_and_id_elems:
            dict_elements_and_res_list[element["Nom"]] = []

        # Remplissage des différents résultats pour chacun des éléments
        for resultat in res_in_post_fic:
            element_name = resultat["Element"]
            if element_name in dict_elements_and_res_list:
                dict_elements_and_res_list[element_name].append(resultat["Nom"])

        # Initialisation du QTreeView
        treemodel = QStandardItemModel()
        treemodel.setColumnCount(1)
        treemodel.setHeaderData(0, Qt.Horizontal, "Résultats")
        rootNode = treemodel.invisibleRootItem()

        # Utilisation de dict_elements_and_res_list dans QTreeView
        for element, res_list in dict_elements_and_res_list.items():
            parent_item = ResultatItem(element)
            for res in res_list:
                item = ResultatItem(res)
                parent_item.appendRow(item)

            rootNode.appendRow(parent_item)

        self.setModel(treemodel)
        self.expandAll()

        # self.clicked.connect(self.on_clicked)


    def mousePressEvent(self, event:QMouseEvent) -> None:
        """Permet de gérer la gestion du clic droit -> edition des résultats"""
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            print("CLIC DROIT")
            self.mon_signal.emit("CLIQUE DROIT")

    def on_clicked(self):
        """
        Gère l'affchage des différents onglets, suivant clic sur milieu ou résultat :
        - Tableau de sinstants de calcul
        - Synthèse graphique
        - Visualisation du schéma
        - Visualisation du scénario
        """

        # S'il s'agit d'un élément "enfant" i.e. d'un résultat sur un élément
        if self.selectedIndexes()[0].parent().data() is not None:
            print("enfant")
            self.is_child = True
        else:
            print("parent")
            self.is_child = False


        self.name_element_selected = self.selectedIndexes()[0].data()
#        ResultatWindow.set_tabwidget(self, self.is_child, self.name_element_selected)



            # if self.ui.tw_resultats.selectedItems()[0].parent() is not None:
            #     # -> OK "tableau des instants de calcul"
            #     self.ui.tabWidget.setTabEnabled(0, True)
            #     # -> OK "synthèse graphique"
            #     self.ui.tabWidget.setTabEnabled(1, True)
            #
            #     # Fixe à tableau instants calcul
            #     self.ui.tabWidget.setCurrentIndex(0)
            #
            #     # Initialisation du slider
            #     self.init_slider()
            #
            #     self.ui.l_results.setText(self.ui.tw_resultats.selectedItems()[0].parent().text(0))
            #     self.ui.l_name_results.setText(self.ui.tw_resultats.selectedItems()[0].text(0))
            #     for res in self.res_in_post_fic:
            #         if res["Element"] == self.ui.tw_resultats.selectedItems()[0].parent().text(0):
            #             self.ui.l_grandeur_base.setText(res["GrandeurDeBase"])
            #             self.ui.l_coeff_multi.setText(res["Coefficient"])
            #             self.ui.l_name_fic_multi.setText(res["Fichier"])
            #
            #     # TEST CGE
            #     # Récupération de l'index corespondant à l'item encours d'affichage
            #     tree = self.ui.tw_resultats
            #     tree_item_idx = tree.indexFromItem(tree.currentItem().parent())
            #
            #     # TODO :code utilisé plusieurs fois (fonction), eleme_name et elem_id en attributs peut-être + judicieux...
            #     elem_name = tree.itemFromIndex(tree_item_idx).text(0)
            #     elem_id = self.find_id_by_name(elem_name)
            #     print("Dans mon test : elem_name = ", elem_name)
            #     print("Dans mon test : elem_id = ", elem_id)
            #
            #     for val in self.res_in_res_fic:
            #         for i, val in enumerate(val[1]):
            #             if val["ID"].strip("ID_") == elem_id:
            #                 index_dict = i
            #
            #     # Demande un temps de calcul entraînant un lag
            #     # self.set_infos_for_graph(index_dict)
            #
            # # Sinon il s'agit d'un élément "parent"
            # else:
            #     self.ui.tabWidget.setTabEnabled(0, False)  # -> NOK "tableau des instants de calcul"
            #     self.ui.tabWidget.setTabEnabled(1, False)  # -> NOK "Synthèse graphique"
            #
            #     # Fixe à Visualisation du schéma
            #     self.ui.tabWidget.setCurrentIndex(2)


class ResultatWindow(QWidget):
    def __init__(self, parent=None, erastem_projet=None):
        super().__init__(parent)
        self.ui = Ui_ResultatWindow()
        self.ui.setupUi(self)

        self.wincreationcas = parent

        # Initialization
        self.chart_view = MyChartView(self)
        print("type(self.ui.gridLayout_3) = ", type(self.ui.gridLayout_3))
        self.ui.gridLayout_3.addWidget(self.chart_view, 2, 0, 1, 3)

        for item in self.wincreationcas.canvas.scene().items():
            item.setFlags(QGraphicsItem.ItemIsFocusable)

        print("type(self.ui.tabWidget) = ", type(self.ui.tabWidget))
        print("self.ui.tabWidget.currentIndex() = ", self.ui.tabWidget.currentIndex)
#        self.ui.tabWidget.currentChanged().connect(self.on_tabwidget_currentchanged)
        self.ui.tabWidget.currentChanged.connect(self.on_tabwidget_currentchanged)

        self.ui.tabWidget.addTab(self.wincreationcas.canvas, "Visualisation du schéma")
        self.ui.tabWidget.addTab(self.wincreationcas.scenario, "Visualisation du scénario")
        self.ui.tabWidget.setTabEnabled(0, False)
        self.ui.tabWidget.setTabEnabled(1, False)
        # self.ui.tw_resultats.setColumnCount(0)
        # self.ui.tw_resultats.setHeaderLabels(["Résultats"])

        self.dlg_edit_res = None

        # Connections
        self._connect_actions()

        # Remplacement de ""
        self.wincreationcas.mainwindow.central_widget.addWidget(self)
        self.wincreationcas.mainwindow.central_widget.setCurrentWidget(self)

        # Les differents attribus issus de la fonction self.collect_results_from_res(...)
        self.name_and_id_elems = []
        self.res_in_res_fic = []
        self.param_res_in_res_fic = {"erRel": None, "residu": None, "duree": None}

        # Attribut issu de la fonction self.collect_results_from_post(...)
        self.res_in_post_fic = []

        # Lecture du fichier résultat, .res
        self.collect_results_from_res(erastem_projet)

        # Lecture du fichier post-traitement, .post
        self.collect_results_from_post(erastem_projet)


        # self.display_res()
        # self.infos_for_graph = [None] * len(self.res_in_res_fic)

          # self.set_infos_for_graph() # S'assurer qu'il s'agit bien d'un résultat auparavant
          # self.infos_for_graph = self.infos_for_graph2


        self.resultat_treeview = ResultatTreeView(self, self.name_and_id_elems, self.res_in_post_fic)
        self.ui.layout_resultats.addWidget(self.resultat_treeview)
        self.resultat_treeview.clicked.connect(self.set_tabwidget)
        self.resultat_treeview.mon_signal.connect(self.ouvrir_edition_resultat)
        #self.resultat_treeview.mousePressEvent()

    @Slot(str)
    def ouvrir_edition_resultat(self):
        print("edition resultat")

        # Si l'index sélectionne correspond à un élément (non à un résultat) -> Ouverture édition résultat
        if self.resultat_treeview.selectedIndexes()[0].parent().data() is None:
            self.dlg_edit_res = EditionResultat()
            self.dlg_edit_res.show()
        # Sinon correspond à un résultat -> QMenu pour "Editer" ou "Spprimer"
        else :
            menu = QMenu()
            menu.addAction('Editer', self.action_clicked)
            menu.addAction('Supprimer', self.action_clicked)

#            menu.exec(event.globalPosition().toPoint())
            menu.exec_()

    def action_clicked(self):
        action = self.sender()
        print("type(action) = ", type(action))
        print('Action: ', action.text())

    def set_tabwidget(self, is_child):
        is_child = self.resultat_treeview.selectedIndexes()[0].parent().data() is not None

        # Si c'est un résultat, e.g. : R0
        if is_child:
            # -> OK "tableau des instants de calcul"
            self.ui.tabWidget.setTabEnabled(0, True)
            # -> OK "synthèse graphique"
            self.ui.tabWidget.setTabEnabled(1, True)

            # Fixe à tableau instants calcul
            self.ui.tabWidget.setCurrentIndex(0)

            # Initialisation du slider
            self.init_slider()
        # Sinon c'est un élement e.g. : Estomac
        else:
            # -> NOK "tableau des instants de calcul"
            self.ui.tabWidget.setTabEnabled(0, False)
            # -> NOK "Synthèse graphique"
            self.ui.tabWidget.setTabEnabled(1, False)

            # Fixe à Visualisation du schéma
            self.ui.tabWidget.setCurrentIndex(2)


    def _connect_actions(self):
        self.ui.pb_modif_cas.clicked.connect(self.on_pb_modif_cas)
        self.ui.chb_multigraphe.stateChanged.connect(self.chb_multigraphe_changed)
        self.ui.lw_sommes.itemPressed.connect(self.on_lw_sommes_item_pressed)
        self.ui.rb_grandeur.toggled.connect(self.on_rb_grandeur)
        self.ui.rb_integrale.toggled.connect(self.on_rb_integrale)
        self.bool_integral = False
        self.ui.slider_instants.valueChanged.connect(self.on_slider_value_changed)

    def on_tabwidget_currentchanged(self, index):
        print("IN on_tabwidget_currentchanged")
        print("index = ", index)

    def on_res_item_dbclicked(self):
        print("IN on res_item_dbcliked")
        if self.dlg_edit_res is None:
            self.dlg_edit_res = EditionResultat()

        if self.ui.tw_resultats.selectedItems()[0].parent() is None:
            self.dlg_edit_res.show()

    def on_res_item_clicked(self):
        print("IN on_res_item_clicked")
        print("self.ui.tw_resultats.selectedItems()[0] = ", self.ui.tw_resultats.selectedItems()[0].text(0))
        # print("self.ui.tw_resultats.selectedItems()[0].parent() = ", self.ui.tw_resultats.selectedItems()[0].parent().text(0))

        # S'il s'agit d'un élément "enfant" i.e. d'un résultat sur un élément
        if self.ui.tw_resultats.selectedItems()[0].parent() is not None:
            # -> OK "tableau des instants de calcul"
            self.ui.tabWidget.setTabEnabled(0, True)
            # -> OK "synthèse graphique"
            self.ui.tabWidget.setTabEnabled(1, True)

            # Fixe à tableau instants calcul
            self.ui.tabWidget.setCurrentIndex(0)

            # Initialisation du slider
            self.init_slider()

            self.ui.l_results.setText(self.ui.tw_resultats.selectedItems()[0].parent().text(0))
            self.ui.l_name_results.setText(self.ui.tw_resultats.selectedItems()[0].text(0))
            for res in self.res_in_post_fic:
                if res["Element"] == self.ui.tw_resultats.selectedItems()[0].parent().text(0):
                    self.ui.l_grandeur_base.setText(res["GrandeurDeBase"])
                    self.ui.l_coeff_multi.setText(res["Coefficient"])
                    self.ui.l_name_fic_multi.setText(res["Fichier"])


            # tree = self.ui.tw_resultats
            # tree_item_idx = tree.indexFromItem(tree.currentItem().parent())

            # TODO :code utilisé plusieurs fois (fonction), eleme_name et elem_id en attributs peut-être + judicieux...
            elem_name = tree.itemFromIndex(tree_item_idx).text(0)
            elem_id = self.find_id_by_name(elem_name)
            print("Dans mon test : elem_name = ", elem_name)
            print("Dans mon test : elem_id = ", elem_id)

            for val in self.res_in_res_fic:
                for i, val in enumerate(val[1]):
                    if val["ID"].strip("ID_") == elem_id:
                        index_dict = i

            # Demande un temps de calcul entraînant un lag
            # self.set_infos_for_graph(index_dict)

        # Sinon il s'agit d'un élément "parent"
        else:
            self.ui.tabWidget.setTabEnabled(0, False) # -> NOK "tableau des instants de calcul"
            self.ui.tabWidget.setTabEnabled(1, False) # -> NOK "Synthèse graphique"

            # Fixe à Visualisation du schéma
            self.ui.tabWidget.setCurrentIndex(2)

    def on_pb_modif_cas(self):
        # Remove windows and widgets needed to display results
        self.wincreationcas.affiche_cas()
        for item in self.wincreationcas.canvas.scene_era.items():
            item.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)


    def chb_multigraphe_changed(self):
        """
        Code executé lorsque le checkbox "Multigraphe" change d'état
        """
        multi = self.ui.chb_multigraphe
        listwidget = self.ui.lw_sommes
        if multi.isChecked():
            listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
            for i in range(0, listwidget.count()):
                listwidget.item(i).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                listwidget.item(i).setSelected(False)
            self.chart_view.chart().removeAllSeries()
            self.stock_graph_series = []
            for i in range(listwidget.count()):
                self.stock_graph_series.append(None)
        else:
            listwidget.setSelectionMode(QAbstractItemView.SingleSelection)
            for i in range(0, listwidget.count()):
                listwidget.item(i).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                listwidget.item(i).setSelected(False)
            self.chart_view.chart().removeAllSeries()

    def on_lw_sommes_item_pressed(self):
        """
        Code executé lorsqu'un item de la QListWidget "lw_sommes" est appuyé
        """
        print("IN on_lw_sommes_pressed")
        lw = self.ui.lw_sommes
        curr_item = lw.currentItem()
        self.idx_graph = lw.indexFromItem(curr_item).row()
        print("type(self.idx_graph) = ", type(self.idx_graph))
        print("self.idx_graph = ", self.idx_graph)

        if lw.selectionMode() == QAbstractItemView.SelectionMode.SingleSelection and curr_item.isSelected():
            self.draw_graph(self.idx_graph, self.bool_integral)

        if lw.selectionMode() == QAbstractItemView.SelectionMode.MultiSelection and curr_item.isSelected():
            self.draw_multi_graph(self.idx_graph, self.bool_integral)
        elif lw.selectionMode() == QAbstractItemView.SelectionMode.MultiSelection and not curr_item.isSelected():
            #self.ui.chart_view.chart().removeAllSeries()
            self.chart_view.chart().removeSeries(self.stock_graph_series[self.idx_graph])

    def on_rb_grandeur(self):
        """
        Code executé lorsque le radio button "rb_grandeur" change d'état
        """
        if self.ui.rb_grandeur.isChecked():
            self.bool_integral = 0
        self.draw_graph(self.idx_graph, self.bool_integral)

    def on_rb_integrale(self):
        """
        Code executé lorsque le radio button "rb_integrale" change d'état
        """
        if self.ui.rb_integrale.isChecked():
            self.bool_integral = 1
        self.draw_graph(self.idx_graph, self.bool_integral)


    def collect_results_from_post(self, erastem_projet: ErastemProject):
        """
        Récupère les informations concernant la partie "Résultat" à partir d'un fichier .post
        """
        self.res_in_post_fic = []
        print("AVANT : self.res_in_post_fic = ", self.res_in_post_fic)

        data_result = erastem_projet.getData().getResults()
        self.res_in_post_fic = data_result.getPostResult()


    def collect_results_from_res(self, erastem_projet: ErastemProject):
        """
        Récupère les informations concernant la partie "Résultats" en utilisant la classe ErastemProject
        """
        print("IN collect_results_from_res")

        data = erastem_projet.getData()
        data_result = data.getResults()
        data_structure = data.getStructure()

        liste_instants = data_result.getTis()

        liste_elements = ErastemDataElementCollection()
        liste_milieux = data_structure.getMilieux()
        liste_transferts = data_structure.getTransferts()

        for milieu in liste_milieux:
            liste_elements.add(milieu)
        for transfert in liste_transferts:
            liste_elements.add(transfert)

        for instant in liste_instants:
            list_instant_and_list_dicts_element = []
            list_instant_and_list_dicts_element.append("T=" + str(instant)[:-5])

            # La liste des dictionnaires correspondant chacun à un milieu
            list_dicts_element = []

            # Pour chacun de ces milieux, on construit le dictionnaire associé :
            for element in liste_elements :
                dict_element = {}

                # Le nom du milieu
                dict_element["Nom"] = element.getName()
                # L'ID du milieu
                dict_element["ID"] = element.getId()

                # On cherche à connaître la liste des isotopes constituant le milieu à un instant donné
                etat_element = element.getResults()
                matter_collection_in_element_at_instant = etat_element[instant.value]
                # Le nombre de lignes = le nombre d'isotopes différents
                dict_element["Nb_rows"] = str(matter_collection_in_element_at_instant.count())

                liste_isotopes = []

                for matter in matter_collection_in_element_at_instant :
                    str_isotope = "3 " + str(matter.getName()) + " " + str(matter.getNumberAtoms()) + " " + str(matter.getNumberAtomsIntegr())
                    liste_isotopes.append(str_isotope)

                # Apres création de laliste on l'ajoute au dictionnaire
                dict_element["Elements"] = liste_isotopes

                # Ajout du dictionnaire ainsi créé à la liste des dictionnaires
                list_dicts_element.append(dict_element)

            list_instant_and_list_dicts_element.append(list_dicts_element)

            self.res_in_res_fic.append(list_instant_and_list_dicts_element)

        for data_element in liste_elements :
            dict_name_id = {}
            dict_name_id["Nom"] = data_element.getName()
            dict_name_id["ID"] = utils.keep_only_number_id(data_element.getId())
            self.name_and_id_elems.append(dict_name_id)

        self.param_res_in_res_fic = data_result.getParamRes()


    def display_res(self):
        """
        Affiche les éléments du schéma et leur résultats associés s'il en existe, récupérés dans les fichiers .post et .res
        """
        items = []

        for value in self.name_and_id_elems:
            item = QTreeWidgetItem(self.ui.tw_resultats)
            item.setText(0, value["Nom"])
            items.append(item)

        for value in self.res_in_post_fic:
            text = value["Element"]
            for item in items:
                if item.text(0) == text:
                    child = QTreeWidgetItem(item)
                    child.setText(0, value["Nom"])

    def init_slider(self):
        """
        Initialise le slider pour qu'il varie en fonction des instants de calcul
        """
        self.ui.slider_instants.blockSignals(True)

        min_val = 0
        max_val = len(self.res_in_res_fic) - 1
        step = 1

        self.ui.slider_instants.setMinimum(min_val)
        self.ui.slider_instants.setMaximum(max_val)
        self.ui.slider_instants.setTickInterval(0)
        self.ui.slider_instants.setSingleStep(step)
        self.ui.slider_instants.setPageStep(step)
        self.ui.slider_instants.setTickPosition(QSlider.TicksAbove)

        for i in range(min_val, max_val):
            self.ui.slider_instants.setValue(i)
        self.ui.slider_instants.setValue(min_val)

        self.ui.slider_instants.blockSignals(False)

    def on_slider_value_changed(self):
        """
        Code lu lorsque la valeur du slider change
        """
        print("IN on_slider_value_changed")
        table = self.ui.tableWidget

        # Efface les données correspondantes à l'instant précédent
        table.clearContents()
        # Remet un nombre de lignes par défaut
        table.setRowCount(1)

        value = self.ui.slider_instants.value()

        # Affichage texte en-dessous slider
        self.update_label_instants(value)

        # Récupération de l'index corespondant à l'item encours d'affichage
        elem_name = self.resultat_treeview.selectedIndexes()[0].data()
        elem_id = self.find_id_by_name(elem_name)

        index_dict = 0 # TODO -> A priori ici ne sert à rien d'initialiser ...
        for val in self.res_in_res_fic:
            for i, val in enumerate(val[1]):
                if val["ID"].strip("ID_") == elem_id:
                    index_dict = i


        grandeur_sum = 0
        integrale_sum = 0

        matieres = self.res_in_res_fic[value][1][index_dict]["Elements"]
        data_matieres = DonneesNucleaires()

        # print("matieres = ", matieres)
        for row, mat in enumerate(matieres):

            # print("mat = ", mat)
            mat = mat.split()
            isotope_name = mat[1]
            # print("isotope_name = ", isotope_name)


            #print("data_matieres.is_stable(isotope_name)", data_matieres.is_stable(isotope_name))
            if isotope_name != "Autre" and not data_matieres.is_stable(isotope_name):
                #print("data_matieres.is_stable(isotope_name)", data_matieres.is_stable(isotope_name))
                table.insertRow(0)

                table.setItem(0, 0, QTableWidgetItem(isotope_name))
                # Nombre Bq à un instant donné
                nb_bq = scientific_notation(convertit_matiere(mat[2], "At", "Bq", isotope=isotope_name))
                # Intégrale sur le temps -> Bq * s
                nb_bq_x_s = scientific_notation(convertit_matiere(mat[3], "At", "Bq", isotope=isotope_name))
                # print("nb_bq = ", nb_bq)
                # print("nb_bq_x_s = ", nb_bq_x_s)

                table.setItem(0, 1, QTableWidgetItem(nb_bq))
                table.setItem(0, 2, QTableWidgetItem(nb_bq_x_s))

                # Somme les valeurs pour chaque isotope sur la grandeur et l'intégrale de la grandeur
                grandeur_sum += float(nb_bq)
                integrale_sum += float(nb_bq_x_s)


            sum_index = table.rowCount() - 1
            # print("sum_index = ", sum_index)
            table.setItem(sum_index, 0, QTableWidgetItem("Somme"))
            table.setItem(sum_index, 1, QTableWidgetItem(scientific_notation(grandeur_sum)))
            table.setItem(sum_index, 2, QTableWidgetItem(scientific_notation(integrale_sum)))

#            table.resizeColumnsToContents()


        #print("value = ", value)

        #self.infos_for_graph[value] = {"Instant": self.res_in_res_fic[value][0], "SommeGrandeur": grandeur_sum,
        #                           "SommeIntegrale": integrale_sum}

        #print("Appel de la fonction set_infos_for_graph")
        #self.set_infos_for_graph()
        #print("self.infos_for_graph = ", self.infos_for_graph)

    def set_infos_for_graph(self, index_dict):
        """
        index_dict -> indice de la position du dictionnaire dans la liste res_in_res_fic
        set l'attribut infos_for_graph (liste de dictionaires), essentiel pour plotter les graphiques
        e.g.: dictionnaire type = {'Instant': 'T=3.0000e+02s', 'SommeGrandeur': 0, 'SommeIntegrale': 0}
        """
        print("IN set_infos_for_graph")
        self.infos_for_graph2 = []

        # Parcours de l'attribut self.res_in_res_fic
        for value in range(len(self.res_in_res_fic)):
            print("value = ", value)

            grandeur_sum, integrale_sum = self.get_grandeur_and_integrale_sum(value, index_dict)
            dict_grandeur_and_integrale_sum = {"Instant": self.res_in_res_fic[value][0], "SommeGrandeur": 10,
                                       "SommeIntegrale": 10}
            # dict_grandeur_and_integrale_sum = {"Instant": self.res_in_res_fic[value][0], "SommeGrandeur": grandeur_sum,
            #                            "SommeIntegrale": integrale_sum}

            self.infos_for_graph2.append(dict_grandeur_and_integrale_sum)

        print("self.infos_for_graph2 = ", self.infos_for_graph2)


    def get_grandeur_and_integrale_sum(self, value, index_dict):
        """
        value -> localise l'indice de la liste et par extension l'instant
        index_dict -> localise l'element (milieu ou transfert) sur lequel on somme
        Permet de calculer, pour un instant donné et un compartiment donné,
        les sommes nb_bq et nb_bs_x_s (grandeur et intégral)
        """
        grandeur_sum = 0
        integrale_sum = 0

        matieres = self.res_in_res_fic[value][1][index_dict]["Elements"]
        data_matieres = DonneesNucleaires()

        # print("matieres = ", matieres)
        for row, mat in enumerate(matieres):
            # print("mat = ", mat)
            mat = mat.split()
            isotope_name = mat[1]
            # print("isotope_name = ", isotope_name)

            # print("data_matieres.is_stable(isotope_name)", data_matieres.is_stable(isotope_name))
            if isotope_name != "Autre" and not data_matieres.is_stable(isotope_name):
                # print("data_matieres.is_stable(isotope_name)", data_matieres.is_stable(isotope_name))
                nb_bq = scientific_notation(convertit_matiere(mat[2], "At", "Bq", isotope=isotope_name))
                nb_bq_x_s = scientific_notation(
                convertit_matiere(mat[3], "At", "Bq", isotope=isotope_name))  # Intégrale sur le temps -> Bq * s
                # print("nb_bq = ", nb_bq)
                # print("nb_bq_x_s = ", nb_bq_x_s)

                # Somme les valeurs pour chaque isotope sur la grandeur et l'intégrale de la grandeur
                grandeur_sum += float(nb_bq)
                integrale_sum += float(nb_bq_x_s)

        return grandeur_sum, integrale_sum


    def find_id_by_name(self, name):
        """
        Fonction de récupérer l'id depuis le nom d'un élément
        """
        for value in self.name_and_id_elems:
            if value["Nom"] == name:
                return value["ID"].strip("ID_")

    def update_label_instants(self, value):
        """
        Mise à jour du texte affiché par le label sous le slider en fonction du changement de valeur du slider
        """
        self.ui.l_instants_calcul.setText(self.res_in_res_fic[value][0])

    def draw_graph(self, graph_choice, grand_or_int, time_unit='s'):
        """
        Trace les graphiques correspondant à la synthèse du calcul effectué
        """
        chart = QChart()
        chart.setAnimationOptions(QChart.AllAnimations)
        self.chart_view.setChart(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)

        data = []
        time = []

        if grand_or_int == False:
            print("grand_or_int vaut True")
            print("grand_or_int=0, self.infos_for_graph = ", self.infos_for_graph)
            for i, info in enumerate(self.infos_for_graph):
                print("i = ", i)
                print("info = ", info)
                text_axe_y = "Grandeur[Bq]"
                data.append(info["SommeGrandeur"])
                temps = info["Instant"].strip("T=")
                temps_val = temps[0:len(temps)-1:1]
                temps_unit = temps[-1]
                convert_temps = convertit_temps(temps_val, temps_unit, time_unit)
                time.append(convert_temps)
        elif grand_or_int == True:
            print("grand_or_int vaut False")
            print("grand_or_int=1, self.infos_for_graph = ", self.infos_for_graph)
            for i, info in enumerate(self.infos_for_graph):
                text_axe_y = "Intégrale[Bq*s-1]"
                data.append(info["SommeIntegrale"])
                temps = info["Instant"].strip("T=")
                temps_val = temps[0:len(temps)-1:1]
                temps_unit = temps[-1]
                convert_temps = convertit_temps(temps_val, temps_unit, time_unit)
                time.append(convert_temps)

        match graph_choice:
            case 0:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_series("Somme des RNs", time, data, chart, text_axe_x, text_axe_y)
                return 1
            case 1:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_series("Somme Halogènes", time, data, chart, text_axe_x, text_axe_y)
                return 2
            case 2:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_series("Somme Gaz rares", time, data, chart, text_axe_x, text_axe_y)
                return 3
            case 3:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_series("Somme RNs Sélectionnés", time, data, chart, text_axe_x, text_axe_y)
                return 4
            case _:
                return 0

    def draw_multi_graph(self, graph_choice, grand_or_int, time_unit='s'):
        """
        Trace les graphiques correspondant à la synthèse du calcul effectué en mode multigraphe
        """
        chart = self.chart_view.chart()
        chart.setAnimationOptions(QChart.AllAnimations)
        self.chart_view.setChart(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)

        data = []
        time = []

        if grand_or_int == 0:
            for i, info in enumerate(self.infos_for_graph):
                text_axe_y = "Grandeur[Bq]"
                data.append(info["SommeGrandeur"])
                temps = info["Instant"].strip("T=")
                temps_val = temps[0:len(temps)-1:1]
                temps_unit = temps[-1]
                convert_temps = convertit_temps(temps_val, temps_unit, time_unit)
                time.append(convert_temps)
        elif grand_or_int == 1:
            for i, info in enumerate(self.infos_for_graph):
                text_axe_y = "Intégrale[Bq*s-1]"
                data.append(info["SommeIntegrale"])
                temps = info["Instant"].strip("T=")
                temps_val = temps[0:len(temps)-1:1]
                temps_unit = temps[-1]
                convert_temps = convertit_temps(temps_val, temps_unit, time_unit)
                time.append(convert_temps)

        match graph_choice:
            case 0:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_multi_series("Somme des RNs", time, data, chart, text_axe_x, text_axe_y, graph_choice)
                return 1
            case 1:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_multi_series("Somme Halogènes", time, data, chart, text_axe_x, text_axe_y, graph_choice)
                return 2
            case 2:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_multi_series("Somme Gaz rares", time, data, chart, text_axe_x, text_axe_y, graph_choice)
                return 3
            case 3:
                text_axe_x = "Temps["+time_unit+"]"
                self.add_multi_series("Somme RNs Sélectionnés", time, data, chart, text_axe_x, text_axe_y, graph_choice)
                return 4
            case _:
                return 0

    def add_series(self, name, x_data, y_data, chart, x_axis_name, y_axis_name):
        """
        Permet de créer et d'ajouter le tracer du graph
        """
        # Create QLineSeries
        series = QLineSeries()
        series.setName(name)

        # Filling QLineSeries
        for i in range(max(len(x_data), len(y_data))):
            series.append(x_data[i], y_data[i])

        chart.addSeries(series)

        # Setting X-axis
        axis_x = QValueAxis()
        axis_x.setTickCount(10)
        axis_x.setLabelFormat("%.2f")
        axis_x.setTitleText(x_axis_name)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        # Setting Y-axis
        axis_y = QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat("%.2f")
        axis_y.setTitleText(y_axis_name)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

    def add_multi_series(self, name, x_data, y_data, chart, x_axis_name, y_axis_name, idx_series):
        """
        Permet de créer et d'ajouter le tracer du graph
        """
        # Create QLineSeries
        series = QLineSeries()
        series.setName(name)

        # Filling QLineSeries
        for i in range(max(len(x_data), len(y_data))):
            series.append(x_data[i], y_data[i])

        if idx_series + 1 > len(self.stock_graph_series):
            self.stock_graph_series.append(series)
        else:
            self.stock_graph_series[idx_series] = series

        chart.addSeries(series)

        if chart.axes(Qt.Horizontal | Qt.Vertical) == []:
            # Setting X-axis
            axis_x = QValueAxis()
            axis_x.setTickCount(10)
            axis_x.setLabelFormat("%.2f")
            axis_x.setTitleText(x_axis_name)
            chart.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x)

            # Setting Y-axis
            axis_y = QValueAxis()
            axis_y.setTickCount(10)
            axis_y.setLabelFormat("%.2f")
            axis_y.setTitleText(y_axis_name)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y)

    def removeAllAxis(self, chart):
        """
        Fonction permettant d'enlever tous les axes du Chart en argument
        """
        axes = chart.axes(Qt.Vertical | Qt.Horizontal)
        for axe in axes:
            chart.removeAxis(axe)

    def update_number_of_digits(self, n_digits):
        pass
