import sys
import os
import copy

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTableWidget, QTableWidgetItem, QTableView, QPushButton, 
                            QLabel, QMenuBar, QMenu, QFileDialog)
from PyQt6.QtGui import QColor, QPixmap, QIcon, QMouseEvent, QFont, QAction, QKeySequence
from PyQt6.QtCore import Qt


from controller import Controller
from constants import Constants
from GUI.Delegates.Damage_Delegate import Damage_Delegate
from GUI.Delegates.Options_Delegate import Options_Delegate
from GUI.Delegates.Cell_Aware_Delegate import Cell_Aware_Delegate
from GUI.Clickable_Image import Clickable_Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 


class Initiative_Tracker_GUI(QMainWindow):
    def __init__(self):


        #-----------------------------------#
        #----- Window and PyQt6 Setup ------#
        #-----------------------------------#


        self.app = QApplication(sys.argv)
        self.controller = Controller()

        self.current_turn = 0
        self.current_round = 1

        super().__init__()

        #main window
        self.setWindowTitle("D&D Initiative Tracker ")
        self.width = Constants.Table_Constants.kWidth
        self.height = Constants.Table_Constants.kHeight
        self.setGeometry(100, 100, self.width, self.height)
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)

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
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalHeaderLabels([
                                                Constants.Table_Constants.kColumn_Name_Title, 
                                                Constants.Table_Constants.kColumn_Initiative_Title, 
                                                Constants.Table_Constants.kColumn_HP_Title, 
                                                Constants.Table_Constants.kColumn_AC_Title, 
                                                Constants.Table_Constants.kColumn_Conditions_Title
                                            ])
        
        self.master_Delegate_Conditions = Cell_Aware_Delegate(self.table)
        self.table.setItemDelegateForColumn(Constants.Table_Constants.kColumn_HP_Index, Damage_Delegate(self.table))
        self.table.setItemDelegateForColumn(Constants.Table_Constants.kColumn_Conditions_Index, self.master_Delegate_Conditions)
        
        self.table.itemChanged.connect(self.table_updated)
        self.main_layout.addWidget(self.table, stretch=3)

        #table matrix
        self.creature_Matrix = []

        self.tableView = QTableView()

        #Button Layout
        self.verticle_button_layout = QVBoxLayout()
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
        self.verticle_button_layout.addWidget(self.add_row_button)
        self.verticle_button_layout.addWidget(self.remove_row_button)
        self.verticle_button_layout.addWidget(self.clear_table_button)
        self.verticle_button_layout.addWidget(self.next_turn_button)
        self.verticle_button_layout.addWidget(self.sort_initiative_button)

        #Undo Redo Buttons
        self.undo_image_path = "assets/undo_button_IT.png"   
        self.redo_image_path = "assets/redo_button_IT.png"
        self.pixmap_undo = QPixmap(self.undo_image_path).scaled(self.width // 12, self.height // 12)
        self.pixmap_redo = QPixmap(self.redo_image_path).scaled(self.width // 12, self.height // 12)
        self.undo_button = Clickable_Image()
        self.redo_button = Clickable_Image()
        self.undo_button.setPixmap(self.pixmap_undo)
        self.redo_button.setPixmap(self.pixmap_redo)
        self.undo_button.connect(self.undo)
        self.redo_button.connect(self.redo)
        self.horizontal_button_layout.addWidget(self.undo_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.horizontal_button_layout.addWidget(self.redo_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.verticle_button_layout.addLayout(self.horizontal_button_layout)
        #add spacer to push buttons to top
        self.verticle_button_layout.addStretch()
        self.main_layout.addLayout(self.verticle_button_layout, stretch=1)

        #display turn and round
        self.round_display = QLabel()
        self.round_display.setFont(Constants.Fonts.kRound_Display)
        self.round_display.setText(f"Round: {self.current_round} | Turn: {self.current_turn + 1}")
        self.verticle_button_layout.addWidget(self.round_display, alignment=Qt.AlignmentFlag.AlignBottom)


        #other values
        self.value_locally_updated = False

        #Prevents computer inputs from triggering recursive loop
        self.is_Program_Cell_Change = False


        #finally, load qss for styling
        self.dict_to_table(self.controller.get_tracker_dict())
        self.load_stylesheet()
        self.update_Row_Backround(self.current_turn)
     



    def pre_load_rows(self, preload_amt):
        for i in range(preload_amt):
            self.add_creature_row()

    #unused, for debugging purpose
    def configureMatrix(self):

        self.creature_Matrix.clear()

        for row in range(self.table.rowCount()):
            creature_dict = {}
            for column in range(self.table.columnCount()):
                header = self.table.horizontalHeaderItem(column).text()
                item = self.table.item(row,column)
                if item:
                    creature_dict[header] = value

                else:
                    value = ""
                    creature_dict[self.table.horizontalHeaderItem(column).text()] = value

            self.creature_Matrix.append(copy.deepcopy(creature_dict))
            creature_dict.clear()
    

    #-----------------------------------#
    #----- Handle table updates  -------#
    #-----------------------------------#


    #tommorow update the validate integer method to return 0 if input is not an integer 
    def table_updated(self, item):
        if not self.is_Program_Cell_Change:
            print("\n\n==Current Matrix==\n\n", self.creature_Matrix, "\n\n\n")
            self.is_Program_Cell_Change = True

            header = self.table.horizontalHeaderItem(item.column()).text()
            dict = self.controller.update_Creature_Item(header, item)
            self.dict_to_table(dict)


            
    #table methods
    #data should be a list of creatures or a creature itself
    #index of creature stored as creature name. Only exclusive to creature spot
    def add_creature_row(self, creatures=None):
        self.master_Delegate_Conditions.register_delegate(self.table.rowCount(), Constants.Table_Constants.kColumn_Conditions_Index, Options_Delegate(self.table))
        self.table.insertRow(self.table.rowCount())
        self.controller.create_Blank_Creature()

    def remove_selected_row(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            self.dict_to_table(self.controller.remove_Creature(current_row))

        #make sure to reset backround colors
        self.update_Row_Backround(self.current_turn)

    def clear_table(self):
        self.dict_to_table(self.controller.clear_creatures())

    def next_turn(self):
        self.dict_to_table(self.controller.next_turn())
        self.round_display.setText(f"Round: {self.current_round } | Turn: {self.current_turn + 1}")

    def sort_initiative(self):
        self.dict_to_table(self.controller.sort_initiative())

    def undo(self):
        print("Undo Attempted")
        self.dict_to_table(self.controller.undo())
    
    def redo(self):
        print("redo Attmepted")
        self.dict_to_table(self.controller.redo())

    def dict_to_table(self, dict):

        #self.load_stylesheet()
        self.is_Program_Cell_Change = True

        C_list_name = Constants.Data_Constants.kDictionary_Creatures_List_Title

        C_name_key = Constants.Data_Constants.kDictionary_Creatures_List_name_Title
        C_initiative_key = Constants.Data_Constants.kDictionary_Creatures_List_initiative_Title
        C_hp_key = Constants.Data_Constants.kDictionary_Creatures_List_hp_Title
        C_ac_key = Constants.Data_Constants.kDictionary_Creatures_List_ac_Title
        C_condtions_key = Constants.Data_Constants.kDictionary_Creatures_List_condtions_Title

        row_count = self.table.rowCount()
        dict_row_count = len(dict[C_list_name])
        print("Expecting rows: ", dict_row_count)

        #add and delete rows only when necessary
        if (dict_row_count > row_count):
            for _ in range(dict_row_count - row_count):
                self.table.insertRow(self.table.rowCount())
        elif (row_count > dict_row_count):
            for _ in range(row_count - dict_row_count):
                self.table.removeRow(self.table.rowCount() - 1)

        for row, creature in enumerate(dict[C_list_name]):
            for col, key in enumerate([C_name_key, C_initiative_key, C_hp_key, C_ac_key, C_condtions_key]):
                item = self.table.item(row, col) 

                creature_attribute = creature[key]
                updated_value = ""


                #checks for empty list: TODO should be replaced by formatting to string in controller
                if isinstance(creature_attribute, list) and len(creature_attribute) == 0:
                    updated_value = ""
                else:
                    updated_value = str(creature_attribute) if creature_attribute is not None else ""

                

                #print(f"updating row: {row}, col: {col} with value {updated_value}\n")
                
                if item is None:
                    self.table.setItem(row, col, QTableWidgetItem(updated_value))
                elif item.text() != updated_value:
                    item.setText(updated_value)
        
        self.current_round = dict["Current Round"]
        self.current_turn = dict["Current Turn"]

        self.update_Row_Backround(self.current_turn)
        self.is_Program_Cell_Change = False

 
    #-----------------------------------#
    #----------- GUI Methods -----------#
    #-----------------------------------#

    def load_stylesheet(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qss_path = os.path.join(script_dir, "styles.css")
        try:
            with open(qss_path, "r") as file:
                print(f"qss filepath -> {qss_path}")
                self.setStyleSheet(file.read())
                print("Styling applied")
        except FileNotFoundError:
            print(f"Error: {qss_path} not found.")

    def update_Row_Backround(self, current_turn):
        
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
        self.save(file_path)
    
    def open(self):
        file_path = QFileDialog.getOpenFileName(None, "Open File", "", "JSON Files (*.json);;All Files (*)")[0]
        self.dict_to_table(self.controller.load_from_file(file_path))

    

        


    def run(self):
        self.menu.show()
        self.controller.save_state()
        self.show()
        self.pre_load_rows(3)
        sys.exit(self.app.exec())()
    
    #--------- asset handling ----------#

    def get_asset_path(self, asset_name):
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script
        assets_dir = os.path.join(script_dir, 'assets') # Construct the path to the assets directory
        return os.path.join(assets_dir, asset_name) # Construct the full path to the asset


    
#connect buttons to methods in tracker
#all buttons shoudl adress methods in tracker -> take data from tracker and put to table