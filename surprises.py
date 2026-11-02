# author: Obaidullah Ahmad
import random
surprises = ["mine", "medkit", "fog"]


class SurpriseDeck:
    def __init__(self):
        self.events = surprises
        self.history = []

    def pick(self):
        return random.choice(self.events)

    def apply_surprises(self, player, pick):
        self.history.append(pick)
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
    deck = SurpriseDeck()

    while player["hp"] > 0:
        input("Press Enter to step on the next square...")

        pick = deck.pick()
        deck.apply_surprises(player, pick)
        print(player)
    print("You died!")
