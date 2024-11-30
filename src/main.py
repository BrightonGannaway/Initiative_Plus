from tracker import InititativeTracker
from creature import Creature

def main():
    tracker = InititativeTracker()
    while True:
        print("\nD&D Initiative Tracker")
        print("1. Add a Creature")
        print("2. View Initiative Order")
        print("3. Apply Damage/Healing")
        print("4. Manage Conditions")
        print("5. End Turn")
        print("6. Exit")

        choice = input("Choose an Option: ")

        match choice:
            case "1":
                tracker.add_creature()
            case "2": 
                tracker.display_order()
            case "3":
                tracker.apply_damage()
            case "4":
                tracker.manage_conditions()
            case "5":
                tracker.next_turn()
            case "6": 
                break
            case _: 
               print("\nInvalid choice, please try again") 

if __name__ == "__main__":
    main()
        