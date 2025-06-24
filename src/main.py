import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Systems.tracker import InitiativeTracker
from creature import Creature
from GUI.main_GUI import Initiative_Tracker_GUI

def main():
    tracker = InitiativeTracker()
    tracker_GUI = Initiative_Tracker_GUI()
    tracker_GUI.run()


if __name__ == "__main__":
    main()
        