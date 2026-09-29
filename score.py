#Written by Youssouf Tive Madi

import random

doors_needed = 5

def give_score(player, amount):
    #add the score earned by the player.
    player["score"] += amount

    #gives 1 sigil for every 200 score.
    player["sigils"] = player["score"] /200


def roll_escape_door(player):
    #checks if the player has completed enough doors.
    if player["doors_completed"] < doors_needed:
        return "Requires 5 completed doors"

    #gives every players 10% chance to find an escape door.
    if random.randint(1, 100) <= 10:
        return "Escape door found!"

    #the escape door was not found.
    return "No escape door found."

#test
player = {
    "score": 0,
    "sigils": 0,
    "doors_completed": 0
}

give_score(player, 200)
print("Score:", player["score"])
print("Sigils:", player["sigils"])