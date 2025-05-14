#Creature class creates a creature along with 
from rich.text import Text
from rich.style import Style
from constants import Constants

class Creature:

    CONDITIONS = {"blinded", "charmed", "deafened", 
                    "frightened", "grappled", "incapacitated",
                      "invisible","paralyzed", "petrified",
                      "poisoned", "prone", "restrained", 
                      "unconscious"}
    
    DAMAGE_TYPES = {
        "acid", "bludgeoning", "cold", "fire", "force", 
        "lightning", "necrotic", "piercing", "poison", 
        "psychic", "radiant", "slashing", "thunder"
    }
    

    def __init__(self, name=None, initiative=None, hp=None, ac=None, res=None, vul=None, imu=None, conditions=None, condition_text=None):
        self.name = name
        self.initiative = initiative
        self.hp = hp
        self.ac = ac
        self.vul = vul or []
        self.res = res or []
        self.imu = imu or []
        self.conditions = conditions or []



    def damage(self, dmg_type, dmg):
        if self.hp is None:
            self.hp = 0

        if dmg_type not in Constants.Properties.KDamage_Types: dmg_type = None

        if dmg_type in self.res:
            dmg = dmg // 2
        
        elif dmg_type in self.vul:
            dmg = dmg * 2
        
        elif dmg_type in self.imu:
            dmg = 0

        self.hp -= dmg
    
    def heal(self, heal_amt):
        if self.hp is None:
            self.hp = 0
        self.hp += heal_amt
    
    def set_name(self, name):
        self.name = name
    
    def set_initiative(self, initiative):
        self.initiative = initiative
    
    def set_hp(self, hp):
        self.hp = hp
    
    def set_ac(self, ac):
        self.ac = ac
    
    def set_conditions(self, con):
        self.conditions = con

    def clear_defenses(self):
        self.vul.clear()
        self.res.clear()
        self.imu.clear()

    def set_defenses(self, defenses_dict):
        for dmg_type, defense_type in defenses_dict.items():
            match defense_type:
                case Constants.Properties.kVunerability:
                    self.vul.append(dmg_type)
                case Constants.Properties.kResistance:
                    self.res.append(dmg_type)
                case Constants.Properties.kImmunity:
                    self.imu.append(dmg_type)
    
    def add_condition(self, condition_type):
        if condition_type.lower() in self.CONDITIONS and condition_type.lower() not in self.conditions:
            self.conditions.append(condition_type.lower())
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

