#Creature class creates a creature along with 
from rich.text import Text
from rich.style import Style

class Creature:

    CONDITIONS = {"blinded", "charmed", "defeaned", 
                    "frightened", "grappled", "incapacitated",
                      "invisible","paralyzed", "petrified",
                      "poisoned", "prone", "restrained", 
                      "unconscious"}
    
    DAMAGE_TYPES = {
        "acid", "bludgeoning", "cold", "fire", "force", 
        "lightning", "necrotic", "piercing", "poison", 
        "psychic", "radiant", "slashing", "thunder"
    }
    

    def __init__(self, name=None, initiative=None, hp=None, ac=None, res=None, vul=None, conditions=None, condition_text=None):
        self.name = name
        self.initiative = initiative
        self.hp = hp
        self.ac = ac
        self.res = res or []
        self.vul = vul or []

        self.conditions = conditions or []


    def damage(self, dmg, dmg_type=None):
        if dmg_type not in self.DAMAGE_TYPES:
            dmg_type = None #makes invalid damage types none so only valids can be used

        if dmg_type in self.res:
            dmg = dmg // 2
        elif dmg_type in self.vul:
            dmg *= 2

        self.hp -= dmg
        return dmg
    
    def heal(self, heal_amt):
        self.hp += heal_amt
        return heal_amt
    
    def set_name(self, name):
        self.name = name
    
    def set_initiative(self, initiative):
        self.initiative = initiative
    
    def set_hp(self, hp):
        self.hp = hp
    
    def set_ac(self, ac):
        self.ac = ac
    
    def add_condition(self, condition_type):
        if condition_type.lower() in self.CONDITIONS and condition_type.lower() not in self.conditions:
            self.conditions.append(condition_type.lower())
            return condition_type
        else:
            print(f"{self.name} already is {condition_type}")
    
    def remove_condition(self, condition_type):
        if condition_type.lower() in self.conditions:
            self.conditions.remove(condition_type)
        else:
            print(f"{self.name} is not already {condition_type}")


    def print_creature(self):
        print(self.name)
        print("\t", self.initiative)
        print("\t", self.hp)
        print("\t", self.ac)

