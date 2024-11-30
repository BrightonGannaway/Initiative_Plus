#Creature class creates a creature along with 
class Creature:
    def __init__(self, name, initiative, hp, ac, res = None, vul=None ):
        self.name = name
        self.initiative = initiative
        self.hp = hp
        self.ac = ac
        self.res = res or []
        self.vul = vul or []
        self.conditions = []

    def damage(self, dmg, dmg_type=None):

        if dmg_type in self.res:
            dmg = dmg // 2
        elif dmg_type in self.vul:
            dmg *= 2

        self.hp -= dmg
        return dmg
    
    def heal(self, heal_amt):
        self.hp += heal_amt
        return heal_amt
    
    def add_condition(self, condition_type):
        if condition_type not in self.conditions:
            self.conditions.append(condition_type)
            return condition_type
        else:
            print(f"{self.name} already is {condition_type}")
    
    def remove_condition(self, condition_type):
        if condition_type in self.conditions:
            self.conditions.remove(condition_type)
        else:
            print(f"{self.name} is not already {condition_type}")

