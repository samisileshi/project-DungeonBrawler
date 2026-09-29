def selection_and_commits(player_name, player_pos,board):
    # Get the wanted tile of the player.
    target_pos = (player_pos[0],player_pos[1])

    # If the player is is interacting with a cell that does not exist, return.
    if target_pos not in board:
        print("\nThere is nothing in this cell.")
        return

    # Get the information of the targeted cell.
    tile_data = board[target_pos]

    # Provide the menu.
    print("\n" + player_name + " Target Selection.")
    print("[1] Open the Door.")
    print("[2] Interact with Item.")

    # Gather the players input.
    choice = input()

    if choice == '1':
        if tile_data.get('door') is None: # If there is no door, return.
            print("There is no door to open.")
            return

        # Gather the information about the door.
        door_name = "Door (" + str(tile_data['door'] + ")") 

        # Confirm that his is the action the player wants.
        confirm = input("Confirm that this is the action you wish to proceed with. Y/N ").lower()

        if confirm == 'y':
            print("You have opened the door.")
        else:
            print("Action Cancelled.")

    elif choice == '2':
        if tile_data.get('item') == None: # If there is no item, return.
            print("There is no item on this tile.")
            return
        # Gather the item information.
        item_name = str(tile_data['item'])

        # Confirm that his is the action the player wants.
        confirm = input("Confirm that this is the action you wish to proceed with. Y/N ").lower()

        if confirm == 'y':
            # If the item at the tile does not match the item name, it means that the other player has taken the item.
            if tile_data.get('item') != item_name: 
                print("Another player has taken this item.")
                return
            print("You have succesfully picked the item: " + item_name)
            # Removes the item from the board to prevent duplicate items.
            tile_data['item'] = None 
        else:
            print("Action Cancelled.")

    else: 
        print("\nInvalid Selection.")

if __name__ == "__main__":
    demo_board = {
        (0, 0): {'door': None, 'item': 'Gold Coin'},
        (0, 1): {'door': 'Wooden Door', 'item': None},
        (1, 1): {'door': None, 'item': None}
    }

    print("--- DEMO 1: Interacting with an Item ---")
    selection_and_commits("Player 1", (0, 0), demo_board)

    print("\nBoard state at (0, 0) after pick up:", demo_board[(0, 0)])

    print("\n--- DEMO 2: Interacting with an Empty Tile ---")
    selection_and_commits("Player 1", (1, 1), demo_board)