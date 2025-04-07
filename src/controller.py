#controller acts as a middleman between GUI and Tracker processing data

from Systems.tracker import InititativeTracker
from Systems.data_Processor import Data_Processor

class Controller:

    def __init__(self):
        self.processor = Data_Processor()
        self.tracker = InititativeTracker()
        pass

    #GUI -> Tracker methods

    #make sure to have condition updates processed seperately
    def update_Creature_Item(self, column_header, item):
        self.save_state()
        value = self.processor.get_Expected_Type(header=column_header, item=item)
        self.tracker.manage_creature(item.row(), column_header, value)
        return self.get_tracker_dict()

    def clear_creatures(self):
        self.save_state()
        self.tracker.clear_creatures_contents()
        return self.get_tracker_dict()

    def remove_Creature(self, row):
        self.save_state()
        self.tracker.remove_creature(row)
        return self.get_tracker_dict()
    
    def damage_Creature(self, row, dmg):
        self.save_state()
        self.tracker.apply_damage(row, dmg)

    def next_turn(self):
        self.save_state()
        self.tracker.next_turn()
        return self.get_tracker_dict() 

    def sort_initiative(self):
        self.save_state()
        self.tracker.sort_initiative()
        return self.get_tracker_dict()
    
    def save_state(self):
        self.tracker.save_state()

    def undo(self):
        self.tracker.undo()
        return self.get_tracker_dict()

    def redo(self):
        self.tracker.redo()
        return self.get_tracker_dict()  

    #to be only called upon the creation of a new row
    def create_Blank_Creature(self):
        self.save_state()
        self.tracker.add_creature()

    def get_tracker_dict(self):
        return self.tracker.to_dict()

