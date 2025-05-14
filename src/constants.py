
from PyQt6.QtGui import QColor, QFont

class Constants:
    class Table_Constants:

        kColumn_Name_Title = "Name"
        kColumn_Name_Type = "string"

        kColumn_Initiative_Title = "Initiative"
        kColumn_Initiative_Type = "int"

        kColumn_HP_Title = "HP"
        kColumn_HP_Type = "int"
        kColumn_HP_Index = 2

        kColumn_AC_Title = "AC"
        kColumn_AC_Type = "int"
        kColumn_AC_Index = 3

        kColumn_Conditions_Title = "Conditions"
        kColumn_Conditions_Type = "string"
        kColumn_Conditions_Index = 4

        kColumns_Type_Dictionary = {

                                    kColumn_Name_Title : kColumn_Name_Type,
                                    kColumn_Initiative_Title : kColumn_Initiative_Type,
                                    kColumn_HP_Title : kColumn_HP_Type,
                                    kColumn_AC_Title : kColumn_AC_Type,
                                    kColumn_Conditions_Title : kColumn_Conditions_Type

                                    }
        
        kWidth = 757
        kHeight = 600
    
    class Data_Constants :

        kDictionary_Creatures_List_Title = "Creatures"
        kDictionary_Creatures_List_name_Title = "name"
        kDictionary_Creatures_List_initiative_Title = "initiative"
        kDictionary_Creatures_List_hp_Title = "hp"
        kDictionary_Creatures_List_ac_Title = "ac"
        kDictionary_Creatures_List_condtions_Title = "conditions"
        kDictionary_Creatures_List_vulnerabilties_Title = "vul"
        kDictionary_Creatures_List_resistances_Title = "res"
        kDictionary_Creatures_List_immunities_Title = "imu"



    class Button_Constants:
        kButton_Add_Creature_Title = "Add Creature"
        kButton_Remove_Creature_Title = "Remove Selected"
        kButton_Load_Data_Title= "Load Data"
        kButton_Clear_Table_Title= "Clear Table"
        kButton_Next_Turn_Title= "Next Turn"
        kButton_Sort_Initiative_Title= "Sort Initiative"

    class Color:
        Dark_Navy = QColor("#13151b")
        Pale_Dark_Navy = QColor("#1e2026")
        Navy = QColor("#26324c")
        Light_Navy = QColor("#38435b")
        Bluish_Gray = QColor("#8a9291")
        Off_White = QColor("#cdcdc2")
        Lichen = QColor("#6b8378")
    
    class Fonts:
        kRound_Display = QFont()
        kRound_Display.setFamily("Garamond")
        kRound_Display.setPixelSize(23)

        kCell_Display = QFont()
        kCell_Display.setFamily("Garamond")
        kCell_Display.setPixelSize(14)

    class Properties:
        KDamage_Types = (
        
        "----",
        "Acid", "Bludgeoning", "Cold", "Fire", "Force", 
        "Lightning", "Necrotic", "Piercing", "Poison", 
        "Psychic", "Radiant", "Slashing", "Thunder"

        )

        kConditions = (
             
        "blinded", "charmed", "deafened", 
        "frightened", "grappled", "incapacitated",
        "invisible","paralyzed", "petrified",
        "poisoned", "prone", "restrained", 
        "unconscious"

        )

        kDefenseOptions = (
            "vulnerable", "resistant", "immune"
        )

        kVunerability = "vulnerable"
        kResistance = "resistant"
        kImmunity = "immune"
    
    class Delegate_Options:
        kConditions_Command_Call = "conditionsCALL"
        kDefense_Command_Call = "defenseCALL"

    class Display_Constants:
        kCondition_HTML_Color_Format_Single_Digit_Dict = {
            "blinded" : "<font color='black'>B</font> ",
            "charmed" : "<font color='pink'>C</font> ",
            "deafened" : "<font color='gray'>D</font> ",
            "frightened" : "<font color='maroon'>F</font> ",
            "grappled" : "<font color='saddlebrown'>G</font> ",
            "incapacitated" : "<font color='darkslategrey'>I</font> ",
            "invisible" : "<font color='white'>I</font> ",
            "paralyzed" : "<font color='yellow'>P</font> ",
            "petrified" : "<font color='rosybrown'>P</font> ",
            "poisoned" : "<font color='seagreen'>P</font> ",
            "prone" : "<font color='palevioletred'>P</font> ",
            "restrained" : "<font color='palegoldenrod'>R</font> ",
            "unconscious" : "<font color='purple'>U</font> "
        }

    class Image_Constants:
        undo_image_path = "assets/undo_button_IT.png"   
        redo_image_path = "assets/redo_button_IT.png"
        shield_image_path = "assets/resistence_shield.png"
