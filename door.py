#Written by Youssouf Tive Madi

#F5: Door completion and failure

import random 
#Thsi is my door class
class Door:
    #This Door constructor replaces the new_door method
    def __init__(self, name, door_type, score_reward = 200):
        self.name = name
        self.door_type = door_type
        self.score_reward = score_reward
        self.completed = False
        self.completed_by = None
        self.failed_by = []
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
            self.completed_by = player.name 

            #checks that the reward has not already been given.
            if self.reward_given is False:
                player.score += self.score_reward  
                self.reward_given = True  

            #count as completed door.
            player.doors_completed += 1 

            return "Door completed"

        #record the player's failed attempt.
        if player.name not in self.failed_by:
            self.failed_by.append(player.name)  

        #the door stays available after failure.
        return "Door failed"


    def can_attempt_door(self):
        #checks if the door was already completed.
        if self.completed:
            return False 
        
        return True 


    def count_comp_doors(doors: list["Door"]):
        # base case is when the list is empty
        if not doors:
            return 0

        if doors[0].completed:
            current = 1
        else:
            current = 0

        # recursive case
        return current + Door.count_comp_doors(doors[1:])


    def door_menu(player, doors:list[Door]):
        #shows the menu until the player exits.
        while True:
            print("\nDoor Menu----")
            #displays all doors.
            for i, door in enumerate(doors):
                if door.completed:
                    status = "Completed"
                else:
                    status = "Available"

                print(i+1, ":" , door.name, "-", status)
                
            print("press 0 to exit")

            #asks the player to select door.
            choice = input("Choose a door: ")

            #exits
            if choice == "0":
                break

            # checks its a numba
            if choice.isdigit():
                door_index = int(choice) - 1
                if 0 <= door_index and door_index <= len(doors):
                    selec_door = doors[door_index]
                    # Check whether the door can be attempted.
                    if selec_door.can_attempt_door(player):
                        print("selected:", selec_door.name)
                    else:
                        print("door is already completed")
                else:
                    print("invalid door number")
            else:
                print("not a number")

    def to_dict(self):
        #converts the door into a dictionary for JSON
        return {
            "name": self.name,
            "type": self.door_type,
            "score_reward": self.score_reward,
            "completed": self.completed,
            "completed_by": self.completed_by,
            "failed_by": self.failed_by,
            "reward_given": self.reward_given
        }

    @classmethod

    def from_dict(cls, data):
        #recreates a door from saved dictionary data.
        door = cls(data["name"], data["type"], data["score_reward"])
        
        #restores its previous state.
        door.completed = data["completed"]
        door.completed_by = data["completed_by"]
        door.failed_by = data["failed_by"]
        door.reward_given = data["reward_given"]
        return door

