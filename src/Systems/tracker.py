#Author: Brighton Gannaway

import sys
import os

#allows access to above directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from Systems.undo_redo_manager import Undo_Redo_Manager
from creature import Creature
from constants import Constants
import json

class InititativeTracker:
    def __init__(self):
        self.creatures = []
        self.round = 1
        self.turn_index = 0
        self.history = Undo_Redo_Manager()

    """
    Sorts the creatures list by their initiative values in descending order.

    Uses the `sort()` method with a lambda function to determine the sorting key.
    The lambda function extracts the `initiative` attribute from each creature.
    """

    def sort_initiative(self):
        
        UnNoneInt = lambda c : c if c is not None else 0
        unNoneStr = lambda c : c if c is not None else "~~~~~~~~~~~~~~~~~~~~~~~~" #want to keep null vlaues below all

        self.creatures.sort(key=lambda c : UnNoneInt(c.initiative), reverse=True)
        
        
        for i in range(len(self.creatures) - 1):

            group_len = 1
            while i < len(self.creatures) - 1 and (UnNoneInt(self.creatures[i].initiative) == UnNoneInt(self.creatures[i + 1].initiative)):
                group_len = group_len + 1
                i = i + 1
            
            if group_len > 1:
                creature_group = self.creatures[i - group_len + 1: i + 1]
                creature_group.sort(key=lambda c : unNoneStr(c.name))
                self.creatures[i - group_len + 1: i + 1] = creature_group
                group_len = 1

    def add_creature(self, name=None, initiative=None, hp=None, ac=None):
        self.creatures.append(Creature(name, initiative, hp, ac))
        
    #initiative must be defualt 0 in order rot sort creatures 
    #TODO: have orde rbe able to be overwridden
    def manage_creature(self, index_r, name=None, initiative=0, hp=None, ac=None):
        #removes copy of creature if it exists, note this doesnt currently work.
        #perhaps add an identifier or make dynamic placement an attribute of that creature 
        #Or have None creatures that have only thte placement value filled <- do this
        self.creatures[index_r] = Creature(name, initiative, hp, ac)
        self.sort_initiative()
        
        for creature in self.creatures:
            creature.print_creature()

    #to manage individual changes to creatures 
    def manage_creature(self, index_r, value_Type, value):

        print("\nCreature length = ", len(self.creatures), "\n\n")
        creature = self.creatures[index_r]

        match value_Type:
            case Constants.Table_Constants.kColumn_Name_Title:
                creature.set_name(value)
            case Constants.Table_Constants.kColumn_Initiative_Title:
                creature.set_initiative(value)
            case Constants.Table_Constants.kColumn_HP_Title:
                creature.set_hp(value)
            case Constants.Table_Constants.kColumn_AC_Title:
                creature.set_ac(value)

    def clear_creatures_contents(self):
        length_saved = len(self.creatures)
        self.creatures.clear()
        for c in range(length_saved):
            self.add_creature()


    def remove_creature(self, index):
        self.creatures.pop(index)
    
    def search_creature(self, index):
        if index.isinstance(int):
            return self.creatures[index]
        elif index.isinstance(str):
            return self.creatures(index)
        else:
            return False

    def apply_damage(self, index, dmg):
        self.creatures[index].damage(dmg)


    
    def manage_conditions(self):
        
        target = self.search_creature()
        
        if not target:
            return
        
        condition_action = input("Add or Remove conditions: ")
        condition = input("Condition: ")

        if condition not in target.CONDITIONS:
            print(f"{condition} is an invalid condition")
            return

        if condition_action.lower() == "add":
            target.add_condition(condition.lower())
        elif condition_action.lower() == "remove":
            target.remove_condition(condition.lower())
        else:
            print("Invalid action please try again")

    def next_turn(self):
        #prevents crash if moving turn on empty table
        if len(self.creatures) == 0: 
            return
        self.turn_index = (self.turn_index + 1) % len(self.creatures)
        if self.turn_index == 0:
            self.round += 1


#--------------------Accessors-----------------------#

    def get_creatures(self):
        self.sort_initiative()
        return self.creatures
    
    def get_round(self): 
        return self.round
    
    def get_turn(self):
        return self.turn_index
    
#-----------------Mutators-------------------------#

#------------------FILE FORMATTING --------------------------------------------#

    def to_dict(self):
        dict = {Constants.Data_Constants.kDictionary_Creatures_List_Title:[creature.__dict__ for creature in self.creatures],
                    "Current Round" : self.round,
                    "Current Turn" : self.turn_index,
                    }

        
        return dict
    
    def from_dict(self, dict):
        self.creatures = [Creature(**creature_data) for creature_data in dict["Creatures"]]
        self.round = dict["Current Round"]
        self.turn_index = dict["Current Turn"]

#----------------- JSON HANDELING -----------------------------------------------#
        
    #Saves current state of intiative tracker to file (JSON)
    def save_to_file(self, filename="initiative_data.json"):
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file, indent=4)
            print(f"Initiative Data saved to {filename}\nCurrent Round: {self.round}\nNumber of Creatures: {len(self.creatures)}\n\n")

    #Loads data from JSON and populates tracker
    def load_from_file(self, filename="initiative_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.from_dict(data)
            print(f"Initiative Data loaded from {filename}\nCurrent Round: {self.round}\nNumber of Creatures: {len(self.creatures)}\n\n")
        except FileNotFoundError:
            print(f"Error {filename} not found")
        except json.JSONDecodeError:
            print(f"Error {filename} has invalid JSON")

#----------------- HISTORY HANDELING ------------------------------------------#

    def save_state(self):
        self.history.save_state(self.to_dict())

    def undo(self):
        new_dict = self.history.undo(self.to_dict())
        self.from_dict(new_dict)
        print(f"Tracker Updated: {self.creatures}, {self.round}, {self.turn_index}")

    def redo(self):
        self.from_dict(self.history.redo(self.to_dict()))

    """def display_history(self):
        print(f"History: {self.history.undo_Stack}")
    """

    def get_history_items(self):
        return self.history.get_history_length()
    
    def display_history(self):
        return self.history.get_history()

#--------------------------------------------------------------------------#


        
