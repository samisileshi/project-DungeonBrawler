# author: Obaidullah Ahmad
import random
import json
surprises = ["mine", "medkit", "fog"]


class SurpriseDeck:
    def __init__(self):
        self.events = surprises
        self.history = []

    def pick(self):
        return random.choice(self.events)

    def to_dict(self):
        return {"history": self.history}

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self.history = data["history"]

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
    try:
        deck.load("surprises_save.json")
    except FileNotFoundError:
        print("No save yet, starting fresh.")
    print("Surprises so far:", len(deck.history))
    while player["hp"] > 0:
        input("Press Enter to step on the next square...")

        pick = deck.pick()
        deck.apply_surprises(player, pick)
        print(player)
    print("You died!")
    deck.save("surprises_save.json")
