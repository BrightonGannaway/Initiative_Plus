from rich.console import Console
from rich.table import Table 
from rich.text import Text
from rich.color import Color
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

        self.CONDITION_TEXT_FORMAT = { #stored in creature class as to create a unique colored string for each creature uniquely
        
                        "blinded": Text.styled("Blinded", style="yellow"),  # Impairment often represented with yellow
                        "charmed": Text.styled("Charmed", style="magenta"),  # Represents enchantment or magic
                        "deafened": Text.styled("Deafened", style="blue"),  # Blue can signify sensory loss
                        "frightened": Text.styled("Frightened", style="red"),  # Fear often linked with red
                        "grappled": Text.styled("Grappled", style="green"),  # Physical condition linked with nature/strength
                        "incapacitated": Text.styled("Incapacitated", style="grey37"),  # Neutral grey for inaction
                        "invisible": Text.styled("Invisible", style="dim"),  # Dim to signify hidden or unseen
                        "paralyzed": Text.styled("Paralyzed", style="cyan"),  # Cyan for shock or immobility
                        "petrified": Text.styled("Petrified", style="white"),  # Stone-like condition linked to white
                        "poisoned": Text.styled("Poisoned", style="dark_green"),  # Green for toxins or poison
                        "prone": Text.styled("Prone", style="grey50"),  # Neutral grey for a grounded state
                        "restrained": Text.styled("Restrained", style="orange1"),  # Orange for physical restriction
                        "unconscious": Text.styled("Unconscious", style="dark_red"),  # Dark red for a state of helplessness

                        }
    
    def format_condition_text(self, creature):
        self.condition_text = Text()

        if not creature.conditions:
            self.condition_text = Text("None")
            return self.condition_text
            
        creature.conditions.sort()

        for condition in creature.conditions:
            self.condition_text += (self.CONDITION_TEXT_FORMAT[condition])[:1]
        
        return self.condition_text

        #all condition styles
    def display_table(self, tracker):

        self.console.clear()
        print()

        self.TITLE_TEXT = "DND Initiative Tracker, Round: " + str(tracker.round)
        self.table = Table(title=self.TITLE_TEXT, box=box.DOUBLE_EDGE, show_lines=True)
        self.tracker = tracker
        
        self.table.add_column("Name", justify="left", no_wrap=True)
        self.table.add_column("Initiative", style="yellow", justify="center")
        self.table.add_column("HP", style="deep_pink3", justify="left")
        self.table.add_column("AC", style="grey66", justify="center")
        self.table.add_column("Conditions", justify="right")

        self.table.caption = "Actions: \n1. Add Creature\n2. Remove Creature\n3. Apply Damage/Healing\n4. Manage Conditions\n5. Next Turn\n6. Save Initiative\n7. Load Initiative\n8. Undo\n9. Redo \n10. Quit"
        


        for i, creature in enumerate(self.tracker.creatures):


            #best be to use accessors to get values from creature for security
            name = Text(creature.name)
            ini = Text(str(creature.initiative))
            hp = Text(str(creature.hp))
            ac = Text(str(creature.ac))
            ct = self.format_condition_text(creature)


            if i == self.tracker.turn_index:
                name.stylize("bold honeydew2")
            if creature.hp <= 0:

                name.stylize("red")
                ini.stylize("red")
                hp.stylize("red")
                ac.stylize("red")
                self.table.add_row(name, ini, hp, ac, ct)
            else: self.table.add_row(name, ini, hp, ac, ct)

        self.console.print(self.table)


        



    

