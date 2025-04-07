
from PyQt6.QtGui import QColor

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
    
    class Data_Constants :

        kDictionary_Creatures_List_Title = "Creatures"
        kDictionary_Creatures_List_name_Title = "name"
        kDictionary_Creatures_List_initiative_Title = "initiative"
        kDictionary_Creatures_List_hp_Title = "hp"
        kDictionary_Creatures_List_ac_Title = "ac"
        kDictionary_Creatures_List_condtions_Title = "conditions"


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

    class Proporties:
        KDamage_Types = (

        "acid", "bludgeoning", "cold", "fire", "force", 
        "lightning", "necrotic", "piercing", "poison", 
        "psychic", "radiant", "slashing", "thunder"

        )

        kConditions = (
             
        "blinded", "charmed", "defeaned", 
        "frightened", "grappled", "incapacitated",
        "invisible","paralyzed", "petrified",
        "poisoned", "prone", "restrained", 
        "unconscious"

        )

