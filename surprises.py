# author: Obaidullah Ahmad
import random
import json
import argparse
surprises = ["mine", "medkit", "fog", "chain mine"]

# Average HP each event takes away (medkit heals, so it is negative).
# chain mine: 5 + 5*0.5 + 5*0.25 = 8.75, rounded to 9.
EVENT_DAMAGE = {"mine": 10, "chain mine": 9, "fog": 0, "medkit": -10}

# Total damage allowed in one planned batch of events, per difficulty.
DIFFICULTY_BUDGET = {"easy": 15, "normal": 35, "hard": 60}


# ===== Data structure (M3): Queue of upcoming surprise events =====
# A linked-list queue: enqueue adds at the back, dequeue removes from the
# front, both O(1). Events come out in the same order they were planned
# (first in, first out), so every player sees the planned sequence.
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class EventQueue:
    def __init__(self):
        self.front = None
        self.back = None
        self.size = 0

    def enqueue(self, value):
        node = Node(value)
        if self.back is None:      # empty queue: node is both ends
            self.front = node
        else:
            self.back.next = node
        self.back = node
        self.size += 1

    def dequeue(self):
        if self.front is None:
            raise IndexError("dequeue from empty EventQueue")
        node = self.front
        self.front = node.next
        if self.front is None:     # queue became empty
            self.back = None
        self.size -= 1
        return node.value

    def peek(self):
        if self.front is None:
            return None
        return self.front.value

    def is_empty(self):
        return self.size == 0

    def to_list(self):
        items = []
        node = self.front
        while node is not None:
            items.append(node.value)
            node = node.next
        return items


# ===== OOP: SurpriseDeck class (state = events + history) =====
class SurpriseDeck:
    def __init__(self):
        self.events = surprises
        self.history = []
        self.upcoming = EventQueue()   # planned events, drawn in order

    def pick(self):
        # Draw the next planned event; fall back to random if nothing planned.
        if not self.upcoming.is_empty():
            return self.upcoming.dequeue()
        return random.choice(self.events)

    # ===== Algorithm strategy (M3): greedy difficulty balancer =====
    # Plans `count` events so their total damage gets as close as possible
    # to the difficulty's damage budget without going over it.
    # Greedy choice: for each slot, take the MOST damaging event that still
    # fits the remaining budget (each event type at most count // 2 times,
    # so the batch stays varied). Then shuffle so the order is a surprise.
    # Big-O: sorting the k event types is O(k log k); each of the n slots
    # scans at most k types, so O(n * k). k = 4 here, so it is O(n).
    def balance_events(self, difficulty="normal", count=6):
        budget = DIFFICULTY_BUDGET[difficulty]
        limit = max(1, count // 2)
        # most damaging first (this ordering is what makes it greedy)
        ranked = sorted(EVENT_DAMAGE, key=EVENT_DAMAGE.get, reverse=True)
        used = {event: 0 for event in ranked}
        plan = []
        for _ in range(count):
            for event in ranked:
                if EVENT_DAMAGE[event] <= budget and used[event] < limit:
                    plan.append(event)
                    used[event] += 1
                    budget -= EVENT_DAMAGE[event]
                    break
        random.shuffle(plan)
        for event in plan:
            self.upcoming.enqueue(event)
        return plan

    # ===== File I/O: save/load history to a JSON file =====
    def to_dict(self):
        return {"history": self.history}

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self.history = data["history"]

    # ===== Recursion: chain mine calls itself until depth hits 0 =====
    def chain_mine(self, player, depth):
        if depth == 0:  # base case: stop
            return
        player["hp"] = player["hp"] - 5
        print("Chain mine! HP -5")
        if random.random() < 0.5:
            self.chain_mine(player, depth - 1)  # recursive call

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


# Demo (main.py can call run())
def run():
    # ===== Command-line args: --save-file picks the save file =====
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
    # ===== Interface (TUI): text menu loop =====
    while player["hp"] > 0:
        print("1) Step 2) History 3) Save 4) Quit")
        choice = input("Choose: ").strip()
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
        else:
            print("Invalid choice, please type 1, 2, 3 or 4.")

    if player["hp"] <= 0:
        print("You died!")
    deck.save(args.save_file)


if __name__ == "__main__":
    run()
