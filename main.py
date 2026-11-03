"""Entry point for the group project.

`python main.py` must run your project at every milestone, so keep this file working
from Milestone 1 onward. Replace the placeholder below with your own core loop.
"""

#By Youssouf: Command line agrument to set the difficulty by setting the chance to find an escape door at the start of the game
from escape_sys import EscapeSystem
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--escape-chance", type = int, default =10, help ="Set the escape door chance.")
args = parser.parse_args()

#makes the ecape sys using the new chance
escape_system = EscapeSystem(escape_chance = args.escape_chance)

ENABLE_COMBAT_DEMO = False


def run_sami_combat(argv=None, **kwargs):
    """The team can call this when combat is enabled; returns the battle result."""
    if not ENABLE_COMBAT_DEMO:
        return None
    from combat_launcher import disable_combat_demo, run_combat
    try:
        return run_combat(argv, **kwargs)
    finally:
        # Reset the opt-in switch after combat, even when something fails.
        disable_combat_demo()




def main():
    #return run_sami_combat() or
    result = run_sami_combat()



if __name__ == '__main__':
    main()
