# Written by Wilson Huang
import argparse
from inventory import INVENTORY_CAPACITY, load_items, count_item
from playerstats import Player

def buy_item(player,item):
    if player.coins < item['price']:
        print("Not Enough Coins")
        return
    if len(player.inventory) >= INVENTORY_CAPACITY:
        print("Your inventory is full")
        return
    player.coins -= item['price']
    player.inventory.append(item)
    owned = count_item(player.inventory, item['name'])
    print("Purchased " + item['name'] + ". Coins Left: " + str(player.coins) + " You now own " + str(owned) + " of " + item['name'])


def shop_menu(player,items):
    while True:
        print("\n==== SHOP ====")
        print("\nCoins: " + str(player.coins))
        print("--------------")
        number = 1
        for item in items:
            print("[" + str(number) + "] " + item['name'] + "Rarity: " + item['rarity'] + " " + item['type'] + " ,Price is: " + str(item['price']) + " coins")
            number += 1
        print("[0] Leave")
        choice = input()
        if choice == '0':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            buy_item(player,items[int(choice) - 1])
        else: 
            print("Invalid Choice")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", default="items.json", help="path to the items json file")
    args = parser.parse_args()
    print("Loading items from: " + args.items)

    hero = Player()
    hero.coins = 100
    shop_menu(hero, load_items(args.items))