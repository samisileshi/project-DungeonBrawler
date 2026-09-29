# Written by Wilson Huang

INVENTORY_CAPACITY = 5
def display_equipment_and_inventory(inventory: list, equipment: dict):
    print("\nEquipped Gear")
    for slot, item in equipment.items(): # Goes through each equipment slot
        if item: # Checks if the item is there 
            name = item["name"] # Get the item name
        else: # If the item is not there, return empty
            name = "Empty"
        print(slot + ": " + name)

    print("\n Inventory (" + str(len(inventory)) + "/" + str(INVENTORY_CAPACITY) + ")")
    if not inventory: # If it is not in the inventory, return empty
        print("Empty")
    else:
        index = 1
        for item in inventory:
            print(str(index) + ". " + item["name"] + " (" + item["rarity"] + " " + item["type"] + ")")
            index += 1


if __name__ == "__main__":
    hero_equipment = {
        "Weapon": {"name": "Iron Sword", "type": "weapon", "rarity": "Common"},
        "Armor": None,
    }

    hero_inventory = [
        {"name": "Steel Plate", "type": "armor", "rarity": "Rare"},
        {"name": "Health Potion", "type": "consumable", "rarity": "Common"},
    ]

    display_equipment_and_inventory(hero_inventory, hero_equipment)