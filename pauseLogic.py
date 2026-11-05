# Ibrahim Mian
# Mon, Sep 28, 2026
# 1.0

import random
from playerstats import Player
from inventory import display_equipment_and_inventory as displayInventory

def pause(pausingPlayer: Player = Player("pausingPlayer"), otherPlayer: Player = Player("otherPlayer"), inventory: list[dict] = [], equipment: dict = {}) -> None :
    print(pausingPlayer.username + " needs a break. What about you, " + otherPlayer.username + "? (Yes/No)")
    answer: str = input("> ").strip().lower()

    while not (answer == "yes" or answer == "no") :
        print("\nError. Enter either \"Yes\" or \"No\", case insensitive.")
        answer = input("> ").strip().lower()

    if answer == "yes" :
        print("\n" + otherPlayer.username + " agrees to take a break.")
        paused: bool = True

        while paused :
            print("\n\t----------Pause Menu----------\t")
            choice: int = 0;

            while choice < 1 or choice > 5 :
                print("""Please select one of the options below by number:\n
                         \r\t\t 1. Resume
                         \r\t\t 2. Inventory
                         \r\t\t 3. Stats
                         \r\t\t 4. Options
                         \r\t\t 5. Quit\n""")
                choice = int(input("> ").strip())

                if choice < 1 or choice > 5 :
                    print("\nError. ", end = "")

            match choice :
                case 1 :
                    paused = False;
                case 2 :
                    displayInventory(inventory, equipment)
                case 3 :
                    pausingPlayer.display_stats()
                case 4 :
                    print("\nComing Soon!")
                case 5 :
                    quit()
                case _ :
                    print("\nHow did you find this? This shouldn't even be possible!")
    else :
        print("\n" + otherPlayer.username + " doesn't want to take a break.", end = "")

if __name__ == "__main__" :
    print("PAUSE DEMO:\n")

    print("Pausing Player:")
    pausingPlayer: Player = Player(input("> ").strip())
    print("Other Player:")
    otherPlayer: Player = Player(input("> ").strip())
    print()

    pause(pausingPlayer, otherPlayer, [{"name": "Steel Plate", "type": "armor", "rarity": "Rare"}], {"Weapon": {"name": "Iron Sword", "type": "weapon", "rarity": "Common"}, "Armor": None})