#controller acts as a middleman between GUI and cls.tracker processing data

from Systems.tracker import InititativeTracker
from Systems.data_Processor import Data_Processor

from constants import Constants

class Controller:

    tracker = InititativeTracker()
    processor = Data_Processor()
    

    #GUI -> cls.tracker methods

    #make sure to have condition updates processed seperately
    @classmethod
    def update_Creature_Item(cls, column_header, item):
        cls.save_state()
        value = cls.processor.get_Expected_Type(header=column_header, item=item)
        cls.tracker.manage_creature(item.row(), column_header, value)
        return cls.get_tracker_dict()
    
    @classmethod
    def clear_creatures(cls):
        cls.save_state()
        cls.tracker.clear_creatures_contents()
        return cls.get_tracker_dict()
    
    @classmethod
    def remove_Creature(cls, row):
        cls.save_state()
        cls.tracker.remove_creature(row)
        return cls.get_tracker_dict()
    
    @classmethod   
    def damage_Creature(cls, index, dmg_type, dmg):

        cls.save_state()
        cls.tracker.apply_damage(index, dmg_type, dmg)
        return cls.get_tracker_dict()

    @classmethod
    def heal_Creature(cls, index, hp):
        cls.save_state()
        cls.tracker.heal(index, hp)
        return cls.get_tracker_dict()

    @classmethod
    def next_turn(cls):
        cls.save_state()
        cls.tracker.next_turn()
        return cls.get_tracker_dict() 
    
    @classmethod
    def sort_initiative(cls):
        cls.save_state()
        cls.tracker.sort_initiative()
        return cls.get_tracker_dict()
    
    @classmethod    
    def save_state(cls):
        cls.tracker.save_state()

    @classmethod
    def undo(cls):
        cls.tracker.undo()
        return cls.get_tracker_dict()
    
    @classmethod
    def redo(cls):
        cls.tracker.redo()
        return cls.get_tracker_dict()  

    @classmethod    #to be only called upon the creation of a new row - method acts weird when loading data
    def create_Blank_Creature(cls):
        cls.save_state()
        cls.tracker.add_creature()

    @classmethod    #delegate calls - allows a backdoor for GUI delegates to manipulate cls.tracker data
    def delegate_options_call(cls, call, index, value):
        cls.save_state()
        match call:
            case Constants.Delegate_Options.kConditions_Command_Call:
                cls.tracker.manage_creature(index, Constants.Table_Constants.kColumn_Conditions_Title, value)
                return cls.get_tracker_dict()
            case Constants.Delegate_Options.kDefense_Command_Call:
                cls.tracker.manage_creature(index, Constants.Delegate_Options.kDefense_Command_Call, value)
                return cls.get_tracker_dict()
            
    @classmethod
    def save_to_file(cls, file_path):
        cls.tracker.save_to_file(file_path)

    @classmethod    
    def load_from_file(cls, file_path="initiative_data.json"):
        cls.save_state()
        cls.tracker.load_from_file(file_path)
        return cls.get_tracker_dict()
    
    @classmethod
    def get_tracker_dict(cls):
        return cls.tracker.to_dict()
    
    @classmethod
    def get_tracker_creature_list_length(cls):
        return len(cls.tracker.creatures)
    
    

