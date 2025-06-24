
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
        kDictionary_Creatures_List_conditions_Title = "conditions"
        kDictionary_Creatures_List_vulnerabilities_Title = "vul"
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
        kRound_Display.setFamily("Georgia")
        kRound_Display.setPixelSize(23)

        kCell_Display = QFont()
        kCell_Display.setFamily("Georgia")
        kCell_Display.setPixelSize(14)

    class Properties:
        KDamage_Types = (
        
        "----",
        "Acid", "Bludgeoning", "Cold", "Fire", "Force", 
        "Lightning", "Necrotic", "Piercing", "Poison", 
        "Psychic", "Radiant", "Slashing", "Thunder"

        )

        kConditions = (
             
        "Blinded", "Charmed", "Deafened", 
        "Frightened", "Grappled", "Incapacitated",
        "Invisible","Paralyzed", "Petrified",
        "Poisoned", "Prone", "Restrained", 
        "Unconscious"

        )

        kDefenseOptions = (
            "vulnerable", "resistant", "immune"
        )

        kVulnerability = "vulnerable"
        kResistance = "resistant"
        kImmunity = "immune"
    
    class Delegate_Options:
        kConditions_Command_Call = "conditionsCALL"
        kDefense_Command_Call = "defenseCALL"

    class Display_Constants:
        kCondition_HTML_Color_Format_Single_Digit_Dict = {
            "Blinded" : "<font color='beige'>B</font> ",
            "Charmed" : "<font color='pink'>C</font> ",
            "Deafened" : "<font color='darkgray'>D</font> ",
            "Frightened" : "<font color='maroon'>F</font> ",
            "Grappled" : "<font color='saddlebrown'>G</font> ",
            "Incapacitated" : "<font color='darkslategrey'>I</font> ",
            "Invisible" : "<font color='white'>I</font> ",
            "Paralyzed" : "<font color='yellow'>P</font> ",
            "Petrified" : "<font color='rosybrown'>P</font> ",
            "Poisoned" : "<font color='darkgreen'>P</font> ",
            "Prone" : "<font color='palevioletred'>P</font> ",
            "Restrained" : "<font color='palegoldenrod'>R</font> ",
            "Unconscious" : "<font color='purple'>U</font> "
        }

        kCondition_Tooltips = {
            "Blinded" : " - A blinded creature can't see and automatically fails any ability checks that require sight" 
                        "\n - Attack rolls against the creature have advantage, and the creature's attack rolls have disadvantage",
            "Charmed" : " - A charmed creature can't attack the charmer or target the charmer with harmful abilities or magical effects"
                        "\n - The charmer has advantage on any ability checks to interact socially with the creature",
            "Deafened" : " - A deafened creature can't hear and automatically fails any ability check that requires hearing",
            "Frightened" : " - A frightened creature has disadvantage on ability checks and attack rolls while its source of "
                        "\nfear is within line of sight"
                        "\n - the creature can't willingly move closer to its source of fear",
            "Grappled" : " - A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed"
                        "\n - The condition ends if the grappler is incapacitated (see the condition)"
                        "\n - The condition also ends if an effect removes the grappled creature from the reach of the grappler"
                        "\n or grappler effect, such as when the creature is hurled by the thunderwave spell",
            "Incapacitated" : " - An incapacitated creature can't take actions or reactions",
            "Invisible" : " - An invisible creature is impossible to see without the aid of magic or a special sense. For the"
                        "\n purposes of hiding, the creature is heavily obscured. The creature's location can be detected by an"
                        "\n noise it makes or any tracks it leaves."
                        "\n - Attack rolls against the creature have disadvantage, and the creature's attack rolls have advantage",
            "Paralyzed" : " - A paralyzed creature is incapacitated (see the condition) and can't move or speak"
                        "\n - The creature automatically fails Strength and Dexterity saving throws"
                        "\n - Attack rolls against the creature have advantage"
                        "\n - Any attack that his the creature is a critical hit if the attacker is within 5 feet of that creature",
            "Petrified" : " - A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into"
                        "\n a solid inanimate substance (usually stone). Its weight increases by a factor of ten, and it ceases aging"
                        "\n - The creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings."
                        "\n - Attack rolls against the creature have advantage"
                        "\n - the creature automatically fails Strength and Dexterity saving throws"
                        "\n - The creature has resistance to all damage"
                        "\n - The creature is immune to poison and disease. although a poison or disease already in the system is"
                        "\n suspended, not neutralized",
            "Poisoned" : " - A poisoned creature has disadvantage on attack rolls and ability checks",
            "Prone" : " - A prone creature's only movement option is to crawl, unless it stands up. and thereby ends the condition"
                        "\n - The creature has disadvantage on attack rolls"
                        "\n - An attack roll against the creature has advantage if the attacker is within 5 feet of the creature."
                        "\n Otherwise, the attack roll has disadvantage",
            "Restrained" : " - A restrained creature's speed becomes 0, and it can't benefit from any both to its speed"
                        "\n Attack rolls against the creature advantage, the creature's attack rolls have disadvantage"
                        "\n The creature has disadvantage on Dexterity saving throws",
            "Stunned" : " - A stunned creature is incapacitated (see the condition), can't move, and can speak only falteringly"
                        "\n - The creature automatically fails Strength and Dexterity saving throws"
                        "\n - Attack rolls against the creature have advantage",
            "Unconscious" : " - An unconscious creature is incapacitated (see the condition), can't move or speak, and is unaware"
                        "\n of its surroundings"
                        "\n - the creature drops whatever it's holding and falls prone (see the condition)"
                        "\n - The creature automatically fails Strength and Dexterity saving throws"
                        "\n - Attack rolls against the creature have advantage"
                        "\n - Any attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature"
        }

    class Image_Constants:
        undo_image_path = "assets/undo.png"   
        redo_image_path = "assets/redo.png"
        shield_image_path = "assets/shield.png"
