# author: Obaidullah Ahmad
import random
import json
import argparse
surprises = ["mine", "medkit", "fog", "chain mine"]


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

    def chain_mine(self, player, depth):
        if depth == 0:
            return
        player["hp"] = player["hp"] - 5
        print("Chain mine! HP -5")
        if random.random() < 0.5:
            self.chain_mine(player, depth - 1)

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
        elif pick == "chain mine":
            self.chain_mine(player, 3)
        return player


# Demo
def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-file", default="surprises_save.json")
    args = parser.parse_args()
    player = {"hp": 80, "max_hp": 100, "attack": 15}
    deck = SurpriseDeck()
    try:
        deck.load(args.save_file)
    except FileNotFoundError:
        print("No save yet, starting fresh.")
    print("Surprises so far:", len(deck.history))
    while player["hp"] > 0:
        # FIXME: error-check the input
        #   -Ibrahim
        print("1) Step 2) History 3) Save 4) Quit")
        choice = input("Choose: ")
        if choice == "1":
            pick = deck.pick()
            deck.apply_surprises(player, pick)
            print(player)
        elif choice == "2":
            print(deck.history)
        elif choice == "3":
            deck.save(args.save_file)
        elif choice == "4":
            break

    if player["hp"] <= 0:
        print("You died!")
    deck.save(args.save_file)


if __name__ == "__main__":
    run()
