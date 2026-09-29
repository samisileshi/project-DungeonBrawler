#Written by Youssouf Tive Madi

#F5: Door completion and failure

import random 

# the different door types.
door_types = {  
    "combat": "combat",  
    "chest": "chest",  
    #this will be left for future milestones when the minigames are made.
    "minigame": "minigame", 
}

def new_door(name, door_type, score_reward=200):
    #creates a simple door dictionary.
    return {
        "name": name,  
        "type": door_type,  
        "score_reward": score_reward,  
        "completed": False, 
        "completed_by": None, 
        "failed_by": [],  
        "reward_given": False, 
    }

def resolve_door(player, door: str[list], success: bool):
    #checks if another player already completed this door.
    if door["completed"]:
        return "Door already completed - no duplicate reward."

    #checks if the current player successfully completed the door.
    if success:
        door["completed"] = True  # Door is now completed/disappears.
        door["completed_by"] = player["name"] 

        #checks that the reward has not already been given.
        if door["reward_given"] is False:
            player["score"] += door["score_reward"]  #givee the player score.
            door["reward_given"] = True  

        #count as completed door.
        player["doors_completed"] += 1 

        # Tell the rest of the program that the door succeeded.
        return "Door completed"

    #record the player's failed attempt.
    if player["name"] not in door["failed_by"]:
        door["failed_by"].append(player["name"])  

    #the door stays available after failure.
    return "Door failed"


def check_door_completion(door_type, player, enemy=None, chest=None, minigame_won=False):
    #Checks if the door is a combat door.
    if door_type == door_types["combat"]:
        #Player must be alive and the enemy must be defeated.
        if player["hp"] > 0 and enemy["hp"] <= 0:
            return True 

        #Player is dead or enemy is still alive.
        return False  

    #check if the door is a chest door.
    if door_type == door_types["chest"]:
        #Player must be alive and the chest must still be unopened.
        if player["hp"] > 0 and chest["opened"] is False:
            return True 
        
        
        return False  

    #checks if the door is a minigame door.
    if door_type == door_types["minigame"]:
        if minigame_won:
            return True 

        
        return False 

    return False 


def can_attempt_door(player, door):
    #checks if the door was already completed.
    if door["completed"]:
        return False 

  
    return True 

#Test case
player = {
    "name": "Player 1",
    "hp": 100
}

enemy = {
    "name": "Enemy",
    "hp": 0
}

print(check_door_completion("combat", player, enemy))
