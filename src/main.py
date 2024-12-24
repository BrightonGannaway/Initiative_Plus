from Systems.tracker import InititativeTracker
from Initiative_Plus_GUI.terminal_ui import Terminal_UI
from creature import Creature

def main():
    tracker = InititativeTracker()
    tui = Terminal_UI()

    tracker.save_state()

    while True:

        tui.display_table(tracker=tracker)
        choice = input()

        try:
            if int(choice) <= 7:
                tracker.save_state()
        except ValueError:
            print("Unexpected value inputed. Please try again")

        match choice:
            case "1":
                tracker.add_creature() #
            case "2": 
                tracker.remove_creature()
            case "3":
                 tracker.apply_damage()
            case "4":
                tracker.manage_conditions() #
            case "5":
                tracker.next_turn() #
            case "6": 
                tracker.save_to_file() #
            case "7":
                tracker.load_from_file() #
            case "8":
                tracker.undo() 
            case "9":
                tracker.redo()
            case "10":
                break
            case "11":
                tracker.display_history()
            case _:
               print("\nInvalid choice, please try again") 

if __name__ == "__main__":
    main()
        