#Author: Brighton Gannaway

import sys
import os

#allows access to above directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from Systems.undo_redo_manager import Undo_Redo_Manager
from creature import Creature
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
        self.creatures.sort(key=lambda c: c.initiative, reverse=True)
    
    def add_creature(self):
        #TODO add roll or input to intitiative
        #TODO add resistance and vulnerabilties input 
        name = input("Name: ")

        #Below Tests for acceptable values
        if name == "":
            print("Your creature must have a name. Try again")
            return
          
        try:
            initiative = int(input("Initiative: "))
            hp = int(input("HP: "))
            ac = int(input("AC: "))
        except ValueError:
            print("Please input an acceptable value. Try Again")
            return 
   

        self.creatures.append(Creature(name, initiative, hp, ac))
        self.sort_initiative()


    def remove_creature(self):
        print("Available Creatures: ", *(Creature.name for Creature in self.creatures), sep=", ")
        target = self.search_creature()
        if target: self.creatures.remove(target)
    

    #Returns a tuple: T(0) is the creature object and T(1) is a boolean reffering to if that creature exists
    #Assists in stability as it allows the searching to be DRY but also prevents bugs from cases that a creature wasn't found
    def search_creature(self):
        target_name = input("Target Creature: ")

        #option if targeted creature is an index
        #The returned is a tuple since
        if target_name.isnumeric() and int(target_name) < len(self.creatures):
            return self.creatures[int(target_name)]
        elif target_name.isnumeric():
            print(f"Target at index: {target_name} is out of bounds")

        #Use an iterator to check if the targeted creature exists
        target = next((c for c in self.creatures if c.name == target_name), None)
        if not target: 
            print(f"{target_name}Creature Not Found")
            return None
        else:
            return target

#--------------Display Order is unused--------------#
    def display_order(self):
        print(self.creatures)
        print(f"\nInitiative Order (Round {self.round})\n~~~~~~~~~~~~~~~~~~~~~~~~~")
        #for loop below points to current round holder by indexing the creatures list
        for i, Creature in enumerate(self.creatures):
            if i == self.turn_index:
                turn_marker = " <- Current Turn" 
            else: 
                turn_marker = ""
            print(f"{Creature.name}: {Creature.hp} HP (AC: {Creature.ac}){turn_marker}\n")

#--------------------------------------------------#

    def apply_damage(self):

        target = self.search_creature()

        if not target:
            return    
        
        style = input("Damage or Heal: ")
        #damage condition looks for amount and type and goes into creature class to damage said creature
        if style.lower() == "damage" or style.lower() == "d":
            damage = int(input("Damage Amount: "))
            damage_type = input("Damage Type(if any): ")
            real_damage = target.damage(damage, damage_type)
            print(f"{target.name} took {real_damage} damage. Remaining HP: {target.hp}")

        elif style.lower() == "heal" or style.lower() == "h":
            healing_amount = int(input("Healing Amount: "))
            healing = target.heal(healing_amount)
            print(f"{target.name} received {healing} healing. Remaining HP: {target.hp}")

        else:
            print("Invalid input: please try again")
            return
    
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

    def manage_initiatives(self):
        for creature in self.creatures:
            initiative = input(f"Initiative of {creature.name}: ").strip()
            while not initiative.isnumeric():
                initiative = input(f"Initaitive must be a number, Initiative of {creature.name}: ")
            creature.initiative = int(initiative)    
        self.sort_initiative()

    def next_turn(self):
        #prevents crash if moving turn on empty table
        if len(self.creatures) == 0: 
            return
        self.turn_index = (self.turn_index + 1) % len(self.creatures)
        if self.turn_index == 0:
            self.round += 1

#------------------FILE FORMATTING --------------------------------------------#

    def to_dict(self):
        dict = {"Creatures":[creature.__dict__ for creature in self.creatures],
                    "Current Round" : self.round,
                    "Current Turn" : self.turn_index,
                    }

        
        return dict
    
    def from_dict(self, dict):
        self.creatures = [Creature(**creature_data) for creature_data in dict["Creatures"]]
        self.sort_initiative()
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
        print(new_dict)
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




        
