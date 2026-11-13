# Written by Youssouf Tive Madi

import random

doors_needed = 5

def give_score (player, amount) :
    # Add the score earned by the player.
    player["score"] += amount

    # Gives 1 sigil for every 200 score.
    # FIXME: use two slashes for int division
    #   -Ibrahim
    player["sigils"] = player["score"] / 200


# FIXME: this method should probably be in escape_sys.py
#   -Ibrahim
def roll_escape_door (player) :
    # Checks if the player has completed enough doors.
    if player["doors_completed"] < doors_needed :
        return "Requires 5 completed doors."

    # Gives every players 10% chance to find an escape door.
    if random.randint(1, 100) <= 10 :
        return "Escape door found!"

    # The escape door was not found.
    return "No escape door found."

# Test
# FIXME: wrap your demo code in an if statement that checks if __name__ == "__main__"
#   -Ibrahim
player = {"score"           : 0,
          "sigils"          : 0,
          "doors_completed" : 0}

give_score(player, 200)
print("Score:", player["score"])
print("Sigils:", player["sigils"], end = "", flush = True)