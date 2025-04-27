
from Systems.tracker import InititativeTracker
from creature import Creature
from GUI.main_GUI import Initiative_Tracker_GUI

def main():
    tracker = InititativeTracker()
    tracker_GUI = Initiative_Tracker_GUI()
    tracker_GUI.run()


if __name__ == "__main__":
    main()
        
#TODO: Be able to save conditions (this means having creature conditions processed)
#TODO: