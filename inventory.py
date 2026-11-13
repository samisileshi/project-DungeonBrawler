# Written by Wilson Huang
import json
INVENTORY_CAPACITY = 5

def load_items (path) :
    with open(path) as f : # Open the JSON file, and converts the items into list of dictionaries
        return json.load(f)

def count_item (inventory, name) :
    if not inventory : # No items left to check
        return 0

    if inventory[0]["name"] == name : # If the very first item is the item we are looking for
        return 1 + count_item(inventory[1:], name) # Count 1 and then add the amount in the rest of the list

    return count_item(inventory[1:], name) #If the first item we checked isnt the one we are looking for, keep looking

def display_equipment_and_inventory (inventory : list, equipment : dict) :
    print("Equipped Gear")

    for slot, item in equipment.items() : # Goes through each equipment slot
        if item : # Checks if the item is there
            name = item["name"] # Get the item name
        else : # If the item is not there, return empty
            name = "Empty"

        print(slot + ": " + name)

    print("\nInventory (" + str(len(inventory)) + "/" + str(INVENTORY_CAPACITY) + ")")

    if not inventory : # If it is not in the inventory, return empty
        print("Empty")
    else :
        for i in range(len(inventory)) :
            print(str(i + 1) + ".", inventory[i]["name"], "(" + inventory[i]["rarity"], inventory[i]["type"] + ")")

if __name__ == "__main__" :
    hero_equipment = {"Weapon" : {"name"   : "Iron Sword",
                                  "type"   : "weapon",
                                  "rarity" : "Common"},
                      "Armor"  : None}
    hero_inventory = [{"name"   : "Steel Plate",
                       "type"   : "armor",
                       "rarity" : "Rare"}]

    display_equipment_and_inventory(hero_inventory, hero_equipment)
    print("\nHealth Potions owned:", count_item(hero_inventory, "Health Potion"))         

    items = load_items("items.json")
    print("Items loaded from items.json:", len(items), end = "", flush = True)