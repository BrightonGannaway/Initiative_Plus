from Systems.tracker import InititativeTracker
from Initiative_Plus_GUI.terminal_ui import Terminal_UI
from creature import Creature

def main():
    tracker = InititativeTracker()
    tui = Terminal_UI()
    presets = ["wt"]

    tracker.save_state()

    while True:

        tui.display_table(tracker=tracker)
        choice = input()

        try:
            if choice in presets or int(choice) <= 7:
                tracker.save_state()
        except ValueError:
            print("Unexpected value inputed. Please try again")

        match choice:
            case "1":
                tracker.add_creature() #Complete
            case "2": 
                tracker.remove_creature() #complete -> could be changed tyo edit creature
            case "3":
                tracker.apply_damage() #Needs work and needs escape for invalid inputs
            case "4":
                tracker.manage_conditions() #Complete
            case "5":
                tracker.next_turn() #Complete
            case "6": 
                tracker.save_to_file() #complete
            case "7":
                tracker.load_from_file() #complete
            case "8":
                tracker.undo() #complete
            case "9":
                tracker.redo() #complete
            case "10":
                break
#----------- Hidden Comamnds -----------#
            case "11":
                tracker.display_history() #must turn off console.clear
            case "12":
                print(tracker.search_creature()) 
            case"wt":
                tracker.load_from_file(filename="Windstallen_Tyrrany_Preset.json") #perhaps have custom presets in full gui version
                tracker.manage_initiatives()
            case _:
                print("\nInvalid choice, please try again") 

if __name__ == "__main__":
    main()
        
#TODO: make a quick quite command for the terminal version 