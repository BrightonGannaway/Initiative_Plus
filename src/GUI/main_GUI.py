import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTableWidget, QTableWidgetItem, QTableView, QPushButton, 
                            QLabel, QMenuBar, QMenu, QFileDialog, QMessageBox, QAbstractItemView,
                            QStyle, QHeaderView)
from PyQt6.QtGui import QColor, QPixmap, QIcon, QMouseEvent, QFont, QAction, QKeySequence
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtBoundSignal, QModelIndex, QSize, pyqtSlot, QEvent
from PyQt6.QtSvgWidgets import QSvgWidget


from controller import Controller
from constants import Constants
from GUI.Delegates.Damage_Delegate import Damage_Delegate
from GUI.Delegates.Options_Delegate import Options_Delegate
from GUI.Delegates.Cell_Aware_Delegate import Cell_Aware_Delegate
from GUI.Clickable_Image import Clickable_Image
from GUI.Popups.Error_Popup import Error_Popup



class QTablewidgetCustom(QTableWidget):

    emitted_value = pyqtSignal(int, int) #start index, dropped index

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.set_dragDrop(True)
        return super().mousePressEvent(e)
    
    def mouseReleaseEvent(self, e):

        if e.button() == Qt.MouseButton.RightButton:
            self.clearSelection()
            self.set_dragDrop(False)
        return super().mouseReleaseEvent(e)
    
    def dropEvent(self, event):
        event_pos = event.position().toPoint()
        drag_drop_start_index = self.selectedIndexes()[0]
        drag_drop_end_index = self.indexAt(event_pos)

        self.emitted_value.emit(drag_drop_start_index.row(), drag_drop_end_index.row())
        event.accept()


        self.set_dragDrop(False)
    
    def set_dragDrop(self, setting: bool):
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) if setting else self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) if setting else self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragEnabled(setting)
        self.setAcceptDrops(setting)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove) if setting else self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.setDragEnabled(setting)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(setting)
        # for row in range(self.rowCount()):
        #     for col in range(self.columnCount()):
        #         self.item(row, col).setFlags(self.item(row, col).flags() & ~Qt.ItemFlag.ItemIsEditable) if setting else self.item(row, col).setFlags(Qt.ItemFlag.ItemIsEditable)


        if setting is False:
            self.reset()

class Initiative_Tracker_GUI(QMainWindow):
    def __init__(self):


        #-----------------------------------#
        #----- Window and PyQt6 Setup ------#
        #-----------------------------------#


        self.app = QApplication(sys.argv)
        self.controller = Controller()

        self.current_turn = 0
        self.current_round = 1
        self.max_rows = 0

        super().__init__()

        #main window
        self.setWindowTitle("D&D Initiative Tracker ")
        self.width = Constants.Table_Constants.kWidth
        self.height = Constants.Table_Constants.kHeight
        self.setGeometry(100, 100, self.width, self.height)
        # self.setMaximumHeight(self.height)
        # self.setMaximumWidth(self.width)

        #menu bar options
        self.menu = QMenuBar()
        self.file = QMenu("File")
        self.save_action = QAction("Save")
        self.save_action.triggered.connect(self.save)
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.saveAs_action = QAction("Save As...")
        self.saveAs_action.triggered.connect(self.save_as)
        self.saveAs_action.setShortcut(QKeySequence("Shift+Ctrl+S"))
        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.open)
        self.open_action.setShortcut(QKeySequence("Ctrl+O"))
        self.file.addAction(self.save_action)
        self.file.addAction(self.saveAs_action)
        self.file.addAction(self.open_action)
        self.menu.addMenu(self.file)


        #PyQt requires central widget to base off all other widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        #table
        self.table = QTablewidgetCustom()
        self.table.setColumnCount(5)
        self.table.setAlternatingRowColors(True)
        # self.table.setDragEnabled(True)
        # self.table.acceptDrops()
        self.table.setHorizontalHeaderLabels([
                                                Constants.Table_Constants.kColumn_Name_Title, 
                                                Constants.Table_Constants.kColumn_Initiative_Title, 
                                                Constants.Table_Constants.kColumn_HP_Title, 
                                                Constants.Table_Constants.kColumn_AC_Title, 
                                                Constants.Table_Constants.kColumn_Conditions_Title
                                            ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.emitted_value.connect(self.drag_drop_receiver)
        
        
        #delegates
        self.master_Delegate_Conditions = Cell_Aware_Delegate(self.table)
        self.condition_delegates = {}
        self.table.setItemDelegateForColumn(Constants.Table_Constants.kColumn_Conditions_Index, self.master_Delegate_Conditions)
        self.master_Delegate_AC = Cell_Aware_Delegate(self.table)
        self.AC_delegates = {}
        self.table.setItemDelegateForColumn(Constants.Table_Constants.kColumn_AC_Index, self.master_Delegate_AC)
        self.damage_delegate = Damage_Delegate(self.table)
        self.damage_delegate.emitted_value_damage.connect(self.damage_creature_row)
        self.damage_delegate.emitted_value_heal.connect(self.heal_creature_row)
        self.table.setItemDelegateForColumn(Constants.Table_Constants.kColumn_HP_Index, self.damage_delegate)
        
        self.table.itemChanged.connect(self.table_updated)
        self.main_layout.addWidget(self.table, stretch=3)

        #table matrix
        self.creature_Matrix = []

        self.tableView = QTableView()

        #Button Layout
        self.vertical_button_layout = QVBoxLayout()
        self.horizontal_button_layout = QHBoxLayout()

        #Dynamic Buttons
        self.add_row_button = QPushButton(Constants.Button_Constants.kButton_Add_Creature_Title)
        self.add_row_button.clicked.connect(self.add_creature_row)

        self.next_turn_button = QPushButton(Constants.Button_Constants.kButton_Next_Turn_Title)
        self.next_turn_button.clicked.connect(self.next_turn)

        self.sort_initiative_button = QPushButton(Constants.Button_Constants.kButton_Sort_Initiative_Title)
        self.sort_initiative_button.clicked.connect(self.sort_initiative)
        self.sort_initiative_button.setStyleSheet("background-color: #cdcdc2; color: black")
        

        #clear table button
        self.clear_table_button = QPushButton(Constants.Button_Constants.kButton_Clear_Table_Title)
        self.clear_table_button.clicked.connect(self.clear_table)

        #Placeholder Buttons
        self.remove_row_button = QPushButton(Constants.Button_Constants.kButton_Remove_Creature_Title)
        self.remove_row_button.clicked.connect(self.remove_selected_row)

        #Button Order
        self.vertical_button_layout.addWidget(self.add_row_button)
        self.vertical_button_layout.addWidget(self.remove_row_button)
        self.vertical_button_layout.addWidget(self.clear_table_button)
        self.vertical_button_layout.addWidget(self.next_turn_button)
        self.vertical_button_layout.addWidget(self.sort_initiative_button)

        #Undo Redo Buttons
        self.pixmap_undo = QPixmap(self.resource_path(Constants.Image_Constants.undo_image_path)).scaled(self.width // 10, self.height // 10, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pixmap_redo = QPixmap(self.resource_path(Constants.Image_Constants.redo_image_path)).scaled(self.width // 10, self.height // 10, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.undo_button = Clickable_Image()
        self.redo_button = Clickable_Image()
        self.undo_button.setPixmap(self.pixmap_undo)
        self.redo_button.setPixmap(self.pixmap_redo)
        self.undo_button.connect(self.undo)
        self.redo_button.connect(self.redo)
        self.horizontal_button_layout.addWidget(self.undo_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.horizontal_button_layout.addWidget(self.redo_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.vertical_button_layout.addLayout(self.horizontal_button_layout)
        #add spacer to push buttons to top
        self.vertical_button_layout.addStretch()
        self.main_layout.addLayout(self.vertical_button_layout)

        #display turn and round
        self.round_display = QLabel()
        self.round_display.setFont(Constants.Fonts.kRound_Display)
        self.round_display.setText(f"Round: {self.current_round} | Turn: {self.current_turn + 1}")
        self.vertical_button_layout.addWidget(self.round_display, alignment=Qt.AlignmentFlag.AlignBottom)


        #other values
        self.value_locally_updated = False

        #Prevents computer inputs from triggering recursive loop
        self.is_Program_Cell_Change = False


        #load qss for styling
        self.dict_to_table(self.controller.get_tracker_dict())
        self.load_stylesheet()
        self.update_Row_Background(self.current_turn)
    

    #unused, for debugging purpose
    # def configureMatrix(self):

    #     self.creature_Matrix.clear()

    #     for row in range(self.table.rowCount()):
    #         creature_dict = {}
    #         for column in range(self.table.columnCount()):
    #             header = self.table.horizontalHeaderItem(column).text()
    #             item = self.table.item(row,column)
    #             if item:
    #                 creature_dict[header] = value

    #             else:
    #                 value = ""
    #                 creature_dict[self.table.horizontalHeaderItem(column).text()] = value

    #         self.creature_Matrix.append(copy.deepcopy(creature_dict))
    #         creature_dict.clear()
    

    #-----------------------------------#
    #----- Handle table updates  -------#
    #-----------------------------------#


    #tomorrow update the validate integer method to return 0 if input is not an integer 
    def table_updated(self, item):
        if not self.is_Program_Cell_Change:
            self.is_Program_Cell_Change = True

            header = self.table.horizontalHeaderItem(item.column()).text()
            dict = self.controller.update_Creature_Item(header, item)
            self.dict_to_table(dict)


            
    #-----------------------------------#
    #--------  table methods  ----------#

    #-----------------------------------#
    #data should be a list of creatures or a creature itself
    #index of creature stored as creature name. Only exclusive to creature spot
    #update tracker parameter used as caution if tracker already has data beyond table data. ex: when loading from a filled file
    def add_creature_row(self, creatures=None, update_tracker=True):

        #create conditions delegate
        op_delegate_conditions = Options_Delegate(self.table, icon=QPixmap(self.resource_path(Constants.Image_Constants.plus_image_path)).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation), options=Constants.Properties.kConditions, use_html_display=True, option_tooltips=Constants.Display_Constants.kCondition_Tooltips)
        op_delegate_conditions.emitted_value.connect(self.options_delegate_receiver)
        self.condition_delegates[(self.table.rowCount(), Constants.Table_Constants.kColumn_Conditions_Index)] = op_delegate_conditions
        self.master_Delegate_Conditions.register_delegate(self.table.rowCount(), Constants.Table_Constants.kColumn_Conditions_Index, op_delegate_conditions)

        #create AC delegate
        op_delegate_AC = Options_Delegate(self.table, icon=QPixmap(self.resource_path(Constants.Image_Constants.shield_image_path)).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation), options=Constants.Properties.KDamage_Types[1:], sub_options=Constants.Properties.kDefenseOptions)
        op_delegate_AC.emitted_value_with_sub_options.connect(self.options_delegate_receiver_for_sub_options)
        self.AC_delegates[(self.table.rowCount(), Constants.Table_Constants.kColumn_AC_Index)] = op_delegate_AC
        self.master_Delegate_AC.register_delegate(self.table.rowCount(), Constants.Table_Constants.kColumn_AC_Index, op_delegate_AC)

        self.table.insertRow(self.table.rowCount())
        if update_tracker:
            self.controller.create_Blank_Creature()
        #self.max_rows += 1

    #upon the selection of 1 or more rows, this method creates a list of index applied
    #returning nothing if no rows have been selected
    def remove_selected_row(self):
        current_rows = [index.row() for index in self.table.selectedIndexes()]
        if len(current_rows) == 0: return
        if current_rows != -1:
            self.dict_to_table(self.controller.remove_Creature(current_rows))

        self.update_Row_Background(self.current_turn)
    
    @pyqtSlot(int, str, int)
    def damage_creature_row(self, row_index, dmg_type, dmg):
        self.is_Program_Cell_Change = False
        self.dict_to_table(self.controller.damage_Creature(row_index, dmg_type, dmg))

    @pyqtSlot(int, int)
    def heal_creature_row(self, row_index, hp):
        self.is_Program_Cell_Change = False
        self.dict_to_table(self.controller.heal_Creature(row_index, hp))

    def clear_table(self):
        self.dict_to_table(self.controller.clear_creatures())

    def next_turn(self):
        self.dict_to_table(self.controller.next_turn())
        self.round_display.setText(f"Round: {self.current_round } | Turn: {self.current_turn + 1}")

    def sort_initiative(self):
        self.dict_to_table(self.controller.sort_initiative())

    def undo(self):
        self.dict_to_table(self.controller.undo(), False)
    
    def redo(self):
        self.dict_to_table(self.controller.redo(), False)


    #-----------------------------------#
    #----- Tracker data -> GUI  --------#
    #-----------------------------------#


    def dict_to_table(self, dict, update_tracker=True):

        #So that all updated cells aren't each individually passed to undo/redo stacks
        self.is_Program_Cell_Change = True

        #name of the list that holds all the creatures 
        C_list_name = Constants.Data_Constants.kDictionary_Creatures_List_Title

        #all these are the keys used in the json that are attached to the values corresponded
        C_name_key = Constants.Data_Constants.kDictionary_Creatures_List_name_Title
        C_initiative_key = Constants.Data_Constants.kDictionary_Creatures_List_initiative_Title
        C_hp_key = Constants.Data_Constants.kDictionary_Creatures_List_hp_Title
        C_ac_key = Constants.Data_Constants.kDictionary_Creatures_List_ac_Title
        C_conditions_key = Constants.Data_Constants.kDictionary_Creatures_List_conditions_Title
        C_vul_key = Constants.Data_Constants.kDictionary_Creatures_List_vulnerabilities_Title
        C_res_key = Constants.Data_Constants.kDictionary_Creatures_List_resistances_Title
        C_imu_key = Constants.Data_Constants.kDictionary_Creatures_List_immunities_Title

        row_count = self.table.rowCount()
        dict_row_count = len(dict[C_list_name])

        #add and delete rows only when tracker rows don't match
        if (dict_row_count > row_count):
            for r in range(dict_row_count - row_count):
                self.add_creature_row(update_tracker=update_tracker)
        elif (row_count > dict_row_count):
            for _ in range(row_count - dict_row_count):
                self.table.removeRow(self.table.rowCount() - 1)

        for row, creature in enumerate(dict[C_list_name]):
            # enumerate through each column and name of column
            for col, key in enumerate([C_name_key, C_initiative_key, C_hp_key, C_ac_key, C_conditions_key]): 
                item = self.table.item(row, col) 

                creature_attribute = creature[key]
                updated_value = ""


                if (isinstance(creature_attribute, list) and len(creature_attribute) == 0) or key == C_conditions_key:
                    updated_value = ""
                else:
                    updated_value = str(creature_attribute) if creature_attribute is not None else ""
                

                self.verify_item_and_display_text(item, row, col, updated_value)

            #handle option delegates
            con_delegate = self.condition_delegates.get((row, Constants.Table_Constants.kColumn_Conditions_Index))
            con_delegate.set_saved_options(creature[C_conditions_key])


            conditions_display_string = ""
            for c in creature[C_conditions_key]:
                if c in Constants.Properties.kConditions:
                    conditions_display_string = conditions_display_string + Constants.Display_Constants.kCondition_HTML_Color_Format_Single_Digit_Dict[c]
            
            #apply all defensive properties(vul, res, imu) first get ac delegate
            #dictionary is passed so that each damage type is hashed to the creatures vul, res, or imu
            ac_delegate = self.AC_delegates.get((row, Constants.Table_Constants.kColumn_AC_Index))
            defenses_dict = {}
            vul_list, res_list, imu_list = creature["vul"], creature["res"], creature["imu"]
            
            for vul in vul_list:
                defenses_dict[vul] = Constants.Properties.kVulnerability
            for res in res_list:
                defenses_dict[res] = Constants.Properties.kResistance
            for imu in imu_list:
                defenses_dict[imu] = Constants.Properties.kImmunity
            
            ac_delegate.set_saved_options(sub_options=defenses_dict)
            
            #make sure rows of conditions can hold data and aren't empty
            item = self.table.item(row, Constants.Table_Constants.kColumn_Conditions_Index)
            if item is None:
                self.table.setItem(row, Constants.Table_Constants.kColumn_Conditions_Index, QTableWidgetItem())

            #userRole inlays html without person actually seeing it - To be extracted later in options delegate itself
            item.setData(Qt.ItemDataRole.UserRole, conditions_display_string)




        
        self.current_round = dict["Current Round"]
        self.current_turn = dict["Current Turn"]

        self.update_Row_Background(self.current_turn)
        self.is_Program_Cell_Change = False 
        
        #let's so how exponentially slow this can get considering python's run time

 
    #-----------------------------------#
    #----------- GUI Methods -----------#
    #-----------------------------------#

    def load_stylesheet(self):
        qss_path = self.resource_path("src/GUI/styles.css")
        try:
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Error: {qss_path} not found.")

    def update_Row_Background(self, current_turn):
        
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)

                if item is None:
                    item = QTableWidgetItem("")
                    self.table.setItem(row, col, item)
                
                #highlights row of current turn else it goes back to default colors
                if row == current_turn:
                    item.setBackground(Constants.Color.Lichen)
                    item.setForeground(Constants.Color.Dark_Navy) 
                elif row % 2 == 0:
                    item.setBackground(Constants.Color.Dark_Navy)
                    item.setForeground(Constants.Color.Bluish_Gray)  
                else:
                    item.setBackground(Constants.Color.Pale_Dark_Navy)
                    item.setForeground(Constants.Color.Off_White)

        self.table.viewport().update()
        

    #-----------------------------------#
    #---------- Menu Methods -----------#
    #-----------------------------------#

    def save(self, file_path="initiative_data.json"):
        self.controller.save_to_file(file_path)
    
    def save_as(self, file_path="initiative_data.json"):
        file_path = QFileDialog.getSaveFileName(None, "Save As", "", "JSON Files (*.json);;All Files (*)")[0]
        try:
            self.save(file_path)
        except FileNotFoundError:
            return
        #displays file name without .json as window title
        self.setWindowTitle("D&D Initiative Tracker - " + file_path.rsplit("/", 1)[1].rsplit(".")[0]) 
    
    def open(self):
        try:
            file_path = QFileDialog.getOpenFileName(None, "Open File", "", "JSON Files (*.json);;All Files (*)")[0]
            self.dict_to_table(self.controller.load_from_file(file_path), False)
            #displays file name without .json as window title
            if file_path: self.setWindowTitle("D&D Initiative Tracker - " + file_path.rsplit("/", 1)[1].rsplit(".")[0])
            #make sure everything is displayed
            self.dict_to_table(self.controller.get_tracker_dict())
        except KeyError:
            err_msg = Error_Popup(message="Could not open selected file - please open a valid file")
            err_msg.show_popup()
            self.open()
    #-------------------------------------#
    #---------- Helper Methods -----------#
    #-------------------------------------#

    @pyqtSlot(int, list)
    def options_delegate_receiver(self, row_index, conditions):
        self.is_Program_Cell_Change = False
        self.dict_to_table(self.controller.delegate_options_call(Constants.Delegate_Options.kConditions_Command_Call, row_index, conditions))

    @pyqtSlot(int, dict)
    def options_delegate_receiver_for_sub_options(self, row_index, defenses_dict):
        self.is_Program_Cell_Change = False
        self.dict_to_table(self.controller.delegate_options_call(Constants.Delegate_Options.kDefense_Command_Call, row_index, defenses_dict))

    @pyqtSlot(int, int)
    def drag_drop_receiver(self, drag_drop_start_row, drag_drop_end_row):
        self.is_Program_Cell_Change = False
        self.dict_to_table(self.controller.drag_drop_handler(drag_drop_start_row, drag_drop_end_row))

    
    
    def pre_load_rows(self, preload_amt):
        for i in range(preload_amt):
            self.add_creature_row()
        
    def verify_item_and_display_text(self, item, row, col, string):
        if item is None:
            self.table.setItem(row, col, QTableWidgetItem())
        elif item.text() != string:
            item.setText(string)
    
    def get_current_tracker_state(self):
        self.dict_to_table(self.controller.get_tracker_dict())
            
             


    

        


    def run(self):
        self.menu.show()
        self.controller.save_state()
        self.show()
        self.pre_load_rows(3)
        self.dict_to_table(self.controller.get_tracker_dict())
        self.app.setWindowIcon(QIcon("assets/Initiative_Plus_Icon_Rounded.icn"))
        sys.exit(self.app.exec())()
    
    #--------- asset handling ----------#

    def get_asset_path(self, asset_name):
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script
        assets_dir = os.path.join(script_dir, 'assets') # Construct the path to the assets directory
        return os.path.join(assets_dir, asset_name) # Construct the full path to the asset

    #used to access .css styles 
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    