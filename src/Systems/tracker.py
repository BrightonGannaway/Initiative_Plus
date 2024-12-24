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
        target = input("Name: ")
        for creature in self.creatures:
            if target == creature.name:
                self.creatures.remove(creature)
                return
        print(f"{target} not found, please try again")
    
    def search_creature(self):
        target_name = input("Target Creature: ")
        #Use an iterator to check if the targeted creature exists
        target = next((c for c in self.creatures if c.name == target_name), None)
        if not target: 
            print("Creature Not Found")
            return
        else:
            return target

    def sort_initiative(self):
        self.creatures.sort(key=lambda c: c.initiative, reverse=True)

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
        if style.lower() == "damage":
            damage = int(input("Damage Amount: "))
            damage_type = input("Damage Type(if any): ")
            real_damage = target.damage(damage, damage_type)
            print(f"{target.name} took {real_damage} damage. Remaining HP: {target.hp}")

        elif style.lower() == "heal":
            healing_amount = int(input("Healing Amount: "))
            healing = target.heal(healing_amount)
            print(f"{target.name} received {healing} healing. Remaining HP: {target.hp}")

        else:
            print("Invalid input: please try again")
            return
    
    def manage_conditions(self):
        conditions = ["blinded", "charmed", "defeaned", 
                      "frightened", "grappled", "incapacitated",
                      "invisible","paralyzed", "petrified",
                      "poisoned", "prone", "restrained", 
                      "Unconscious"]
        
        target = self.search_creature()
        if not target:
            return
        
        condition_action = input("Add or Remove conditions: ")
        condition = input("Condition: ")

        if conditions not in conditions:
            print(f"{condition} is an invalid condition")
            return

        if condition_action.lower() == "add":
            target.add_condition(condition)
        elif condition_action.lower() == "remove":
            target.remove_condition(condition)
        else:
            print("Invalid action please try again")

    def next_turn(self):
        #prevents crash if moving turn on empty table
        if len(self.creatures) == 0: 
            return
        self.turn_index = (self.turn_index + 1) % len(self.creatures)
        if self.turn_index == 0:
            self.round += 1




#------------------JSON & HISTORY HANDELING--------------------------------------------#

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


    

#--------------------------------------------------------------------------#




        
