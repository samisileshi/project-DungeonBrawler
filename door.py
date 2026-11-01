#Written by Youssouf Tive Madi

#F5: Door completion and failure

import random 
#Thsi is my door class
class door:
    #This Door constructor replaces the new_door method
    def __init__(self, name, door_type, score_reward = 200):
        self.name = name
        self.door_type = door_type
        self.score_reward = score_reward
        self.completed = False
        self.completed_by = None
        self.failed_by = None
        #So rewards arent given more then once
        self.reward_given = False

#This method is the old resolve_door method but changed to fit the door class

def resolve(self, player, success: bool):
    #checks if another player already completed this door.
    if self.completed:
        return "Door already completed."

    #checks if the current player successfully completed the door.
    if success:
        self.completed = True 
        self.completed_by = player["name"] 

        #checks that the reward has not already been given.
        if self.reward_given is False:
            player["score"] += self.score_reward  #givee the player score.
            self.reward_given = True  

        #count as completed door.
        player["doors_completed"] += 1 

        # Tell the rest of the program that the door succeeded.
        return "Door completed"

    #record the player's failed attempt.
    if player["name"] not in self.failed_by:
        self.failed_by.append(player["name"])  

    #the door stays available after failure.
    return "Door failed"


def can_attempt_door(self):
    #checks if the door was already completed.
    if self.completed:
        return False 
    
    return True 

