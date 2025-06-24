#Creature class creates a creature along with 
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
        self.vul.clear()
        self.res.clear()
        self.imu.clear()
        for dmg_type, defense_type in defenses_dict.items():
            match defense_type:
                case Constants.Properties.kVulnerability:
                    self.vul.append(dmg_type)
                case Constants.Properties.kResistance:
                    self.res.append(dmg_type)
                case Constants.Properties.kImmunity:
                    self.imu.append(dmg_type)
    



