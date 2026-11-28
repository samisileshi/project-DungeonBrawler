# Entry point for the group project.

#   `python main.py` must run your project at every milestone, so keep this file working
#   from Milestone 1 onward. Replace the placeholder below with your own core loop.

# By Youssouf: Command line argument to set the difficulty by setting the chance to find an escape door at the start of the game
import argparse
import json
import os

from combat_launcher import *
from door import *
from escape_sys import *
from game_state import *
from player import *

clear_terminal : function = lambda : os.system("cls" if os.name == "nt" else "clear")

parser : ArgumentParser = argparse.ArgumentParser()
parser.add_argument("-e", "--escape-chance", type = int, default = 10, help = "Set the escape door chance.")
args : Namespace = parser.parse_args()

# FIXME: `main.py` isn't for demos, this is supposed to be the final product!
#   -Ibrahim
def run_sami_combat (argv = None, **kwargs) :
    # The team can call this when combat is enabled; returns the battle result.
    if not ENABLE_COMBAT_DEMO :
        return None

    try :
        return run_combat(argv, **kwargs)
    finally :
        # Reset the opt-in switch after combat, even when something fails.
        disable_combat_demo()

clear_terminal()

p1 : Player = Player("Youssouf", 100)
doors : list[Door] = [Door("Fire Door", "Combat", 200), Door("Ice Door", "Combat", 200), Door("Boss Door", "Combat", 200)]

# makes the escape sys using the new chance
escape_system : EscapeSystem = EscapeSystem(escape_chance = args.escape_chance)

ENABLE_COMBAT_DEMO : bool = True

Door.door_menu(p1, doors)

print(f"\nEscape chance: {args.escape_chance}%")

# return run_sami_combat() or
result = run_sami_combat()