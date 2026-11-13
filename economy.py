# Written by Wilson Huang
import argparse
from inventory import INVENTORY_CAPACITY, load_items, count_item
from playerstats import Player

def buy_item (player, item) :
    if player.coins < item["price"] : # Checks if the player is able to afford the item
        print("\nNot Enough Coins\n")

        return

    if len(player.inventory) >= INVENTORY_CAPACITY : # Checks if the player has enough inventory space
        print("\nYour inventory is full\n")

        return
    player.coins -= item["price"] # Subtract the player coins from the item price
    player.inventory.append(item) # Add the item to the inventory
    owned = count_item(player.inventory, item["name"]) # Count the amount of copies the player has and store it
    print("\nPurchased", item["name"] + ". Coins Left:", player.coins, "You now own", owned, "of", item["name"] + "\n")


def shop_menu (player, items) :
    while True : # Keep running until the player chooses to exit the shop
        print("==== SHOP ====")
        print("\nCoins:", player.coins)
        print("--------------")

        for i in range(len(items)) : # Display every item in the shop
            print("[" + str(i + 1) + "]", items[i]["name"], "Rarity:", items[i]["rarity"], items[i]["type"], "\b, Price is:", items[i]["price"], "coins")

        print("[" + str(len(items) + 1) + "] Leave")
        choice = int(input("> ")) # Gather the players choice

        if choice is (len(items) + 1) :
            break

        if choice >= 1 and choice <= len(items):
            buy_item(player,items[int(choice) - 1])
        else :
            print("\nInvalid Choice\n")

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", default = "items.json", help = "Path to the items JSON file")
    args = parser.parse_args()
    print("Loading items from:", args.items + "\n")

    hero = Player()
    hero.coins = 100
    shop_menu(hero, load_items(args.items))