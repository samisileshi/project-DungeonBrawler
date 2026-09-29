# Written by Wilson Huang
def handle_economy(player, action_type, item_index=0):
    # Create a mini shop with prices
    shop = [
        {"name": "Healing Potion", "price": 20},
        {"name": "Iron Sword", "price": 50},
        {"name": "Revival Charm", "price": 100}
    ]

    if action_type == "buy": # If the player wants to buy.
        item = shop[item_index]
        player["coins"] -= item["price"] # Subtract the coins from the players inventory.
        player["inventory"].append(item["name"]) # Add the item to the players inventory.
        print("Bought " + item["name"] + "! Coins left: " + str(player["coins"])) # Display the shopping message.

    elif action_type == "sell": # If the player wants to sell.
        item_name = player["inventory"][item_index] 
        del player["inventory"][item_index] # Remove the item from the inventory

        sell_price = 15 # Set a random price for now
        player["coins"] += sell_price # Add the coins to the players inventory after selling
        print("Sold " + item_name + " for " + str(sell_price) + " coins! Total coins: " + str(player["coins"]))


if __name__ == "__main__":
    player_data = {"coins": 100, "inventory": []}
    handle_economy(player_data, "buy", 0)  
    handle_economy(player_data, "buy", 1)   
    handle_economy(player_data, "sell", 0)  