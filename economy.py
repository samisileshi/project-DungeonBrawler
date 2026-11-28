# Written by Wilson Huang
import argparse
from inventory import INVENTORY_CAPACITY, load_items, count_item
from playerstats import Player

RARITY_VALUE = {"Common" : 1, "Rare" : 2, "Epic" : 3 } # Assign rarity values

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

def value_per_coin(item): # Create a function to see the value of each you are spending
    return RARITY_VALUE.get(item["rarity"],1) / item["price"] # Rarity value / price

def suggest_purchase(player, items):
    sorted_items = sorted(items,key = value_per_coin, reverse = True) # Sort the items in terms of value per coin
    slots_left = INVENTORY_CAPACITY - len(player.inventory) # Variable to store remaining slots
    coins_left = player.coins # Variable to store remaining coins
    chosen = []

    for item in sorted_items: # Runs for each item in the shop
        if item["price"] <= coins_left and slots_left > 0: # If the player can afford the item and can use it
            chosen.append(item["name"]) # Append the item to a list
            coins_left -= item["price"] # Checks how many coins are left for the algorithm to use
            slots_left -= 1 # Checks how many slots are left for the algorithm
    return chosen

def shop_menu (player, items) :
    while True : # Keep running until the player chooses to exit the shop
        print("==== SHOP ====")
        print("\nCoins:", player.coins)
        print("--------------")

        for i in range(len(items)) : # Display every item in the shop
            print("[" + str(i + 1) + "]", items[i]["name"], "Rarity:", items[i]["rarity"], items[i]["type"], "\b, Price is:", items[i]["price"], "coins")
        print("[" + str(len(items) + 1) + "] Leave")
        print("[" + str(len(items) + 2) + "] Suggest best purchase")
        choice = int(input("> ")) # Gather the players choice

        if choice == (len(items) + 1) :
            break

        if choice == (len(items) + 2) :
            suggestion = suggest_purchase(player,items)
            if suggestion :
                print("\nBest deals for your coins:", ", ".join(suggestion) + "\n")
            else :
                print("\nYou cannot afford anything right now.\n")

        elif choice >= 1 and choice <= len(items):
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