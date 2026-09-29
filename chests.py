#Written by Youssouf Tive Madi

import random

chest_loot = ["Health Potion", "Iron Sword"]


def make_chest():
    #returns a chest dictionary.
    return {
        "loot": random.choice(chest_loot),  
        "buff": "+10 damage buff",
        "opened": False,  
        "opened_by": None,  
    }

def access_chest(player, chest):
    #checks if someone already accessed the chest
    if chest["opened"]:
        return "Chest already claimed."  # Prevent the second player from getting it

    #marks the chest as opened
    chest["opened"] = True  # First access claims the chest

    #which player accessed it first
    chest["opened_by"] = player["name"]

    #gives the player the randomly selected loot
    player["inventory"].append(chest["loot"])

    #gives the player the chest buff
    player["buffs"].append(chest["buff"])

    #returns what the player received
    return "Chest claimed: " + chest["loot"] + " + " + chest["buff"]


#test makes chest
chest = make_chest()

print("Chest loot:", chest["loot"])