# Written by Youssouf Tive Madi

import random

# For this file I'll change it from escape to score because it should be the player class that handles the score
#   For the score I'll make it a class where that determines the score and if a player can escape
class EscapeSystem :
    def __init__ (self, escape_chance = 10, doors_needed = 5) :
        # The probability that the door if an escape door
        self.escape_chance = escape_chance

        # How many doors are needed to escape the dungeon.
        self.doors_needed = doors_needed

    # FIXME: this method is redundant and doesn't even need the EscapeSystem class, just import score.py
    #   -Ibrahim
    def give_score (self, player, amount) :
        player.score += amount

        # One sigil for every 200 score.
        player.sigils = player.score // 200

    def roll_escape_door (self, player) :
        if player.doors_completed < self.doors_needed :
            return "Requires 5 completed doors."

        # gives every players a 10% chance to find an escape door.
        if random.randint(1, 100) <= self.escape_chance :
            return "Escape door found!"

        return "No escape door found."