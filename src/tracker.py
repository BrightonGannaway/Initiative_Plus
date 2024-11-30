from creature import Creature

class InititativeTracker:
    def __init__(self):
        self.creatures = []
        self.round = 1
        self.turn_index = 0

    def add_creature(self):
        #TODO add roll or input to intitiative
        #TODO add resistance and vulnerabilties input 
        name = input("Name: ")
        initiative = int(input("Initiative: "))
        hp = int(input("HP: "))
        ac = int(input("AC: "))

        self.creatures.append(Creature(name, initiative, hp, ac))
        self.sort_initiative()
    
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

    def display_order(self):
        print(f"\nInitiative Order (Round {self.round})")
        #for loop below points to current round holder by indexing the creatures list
        for i, Creature in enumerate(self.creatures):
            if i == self.turn_index:
                turn_marker = " <- Current Turn" 
            else: 
                turn_marker = ""
            print(f"{Creature.name}: {Creature.hp} HP (AC: {Creature.ac}){turn_marker})\n")

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
        self.turn_index = (self.turn_index + 1) % len(self.creatures)
        if self.turn_index == 0:
            self.round += 1

        
