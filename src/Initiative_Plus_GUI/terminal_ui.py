from rich.console import Console
from rich.table import Table 
from rich.text import Text
from rich.style import Style
from rich import box

import sys
import os

#allows access to above directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from Systems.tracker import InititativeTracker

class Terminal_UI:
    def __init__(self):
        self.console = Console()

    def display_table(self, tracker):

        print()

        self.table = Table(title="DND Initiative Tracker", box=box.DOUBLE_EDGE, show_lines=True)
        self.tracker = tracker
        
        self.table.add_column("Name", justify="left", no_wrap=True)
        self.table.add_column("Initiative", style="yellow", justify="center")
        self.table.add_column("HP", style="deep_pink3", justify="left")
        self.table.add_column("AC", style="grey66", justify="center")

        self.table.caption = "Actions: \n1. Add Creature\n2. Remove Creature\n3. Apply Damage/Healing\n4. Manage Conditions\n5. Next Turn\n6. Save Initiative\n7. Load Initiative\n8. Undo\n9. Redo \n10. Quit"
        


        for i, creature in enumerate(self.tracker.creatures):
            name = Text(creature.name)
            if i == self.tracker.turn_index:
                name.stylize("bold honeydew2")

            self.table.add_row(name, str(creature.initiative), str(creature.hp), str(creature.ac))

        self.console.print(self.table)


        



    

