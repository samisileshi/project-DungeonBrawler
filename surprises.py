# author: Obaidullah Ahmad
import random
surprises = ["mine", "medkit", "fog"]


def apply_surprises(player, pick):
    if pick == "mine":
        player["hp"] = player["hp"] - 10
        print("Mine. HP -10")
    elif pick == "medkit":
        if player["hp"] != player["max_hp"]:
            player["hp"] += 10
            if player["hp"] > player["max_hp"]:
                player["hp"] = player["max_hp"]
            print("Medkit. HP +10")
        else:
            print("Medkit. HP Maxed")
    elif pick == "fog":
        print("Fog. nothing happens")
    return player


# Demo
if __name__ == "__main__":

    player = {"hp": 80, "max_hp": 100, "attack": 15}

    pick = random.choice(surprises)
    apply_surprises(player, pick)
    print(player)
