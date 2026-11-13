def selection_and_commits (player_name, player_pos, board) :
    # Get the wanted tile of the player.
    # FIXME: instead of naming the coord parameter player_pos and assigning it to target_pos, just name it target_pos to begin with
    #   -Ibrahim
    target_pos = (player_pos[0], player_pos[1])

    # If the player is is interacting with a cell that does not exist, return.
    if target_pos not in board :
        print("There is nothing in this cell.", end = "", flush = True)
        return

    # Get the information of the targeted cell.
    tile_data = board[target_pos]

    # Provide the menu.
    print(player_name, "Target Selection.")
    print("[1] Open the Door.")
    print("[2] Interact with Item.")

    # Gather the players input.
    choice = input("> ")

    if choice == "1" :
        if tile_data.get("door") is None : # If there is no door, return.
            print("\nThere is no door to open.", end = "", flush = True)
            
            # FIXME: don't return, just error-check
            #   -Ibrahim
            return

        # Gather the information about the door.
        door_name = "Door (" + tile_data["door"] + ")"

        # Confirm that this is the action the player wants.
        print("\nConfirm that this is the action you wish to proceed with. Y/N")
        confirm = input("> ").lower()

        if confirm == "y" :
            print("\nYou have opened the door.", end = "", flush = True)
        else:
            print("\nAction Cancelled.", end = "", flush = True)

    elif choice == "2" :
        if tile_data.get("item") == None : # If there is no item, return.
            print("\nThere is no item on this tile.", end = "", flush = True)
            
            # FIXME: don't return, just error-check
            #   -Ibrahim
            return
        
        # Gather the item information.
        item_name = tile_data["item"]

        # Confirm that this is the action the player wants.
        print("\nConfirm that this is the action you wish to proceed with. Y/N")
        confirm = input("> ").lower()

        if confirm == "y" :
            # If the item at the tile does not match the item name, it means that the other player has taken the item.
            if tile_data.get("item") != item_name :
                print("\nAnother player has taken this item.", end = "", flush = True)

                # FIXME: don't return, just error-check
                #   -Ibrahim
                return

            print("\nYou have succesfully picked the item:", item_name, end = "", flush = True)

            # Removes the item from the board to prevent duplicate items.
            tile_data["item"] = None 
        else :
            print("\nAction Cancelled.", end = "", flush = True)
    else :
        print("\nInvalid Selection.", end = "", flush = True)

if __name__ == "__main__" :
    demo_board = {(0, 0) : {"door" : None,
                            "item" : "Gold Coin"},

                  (0, 1) : {"door" : "Wooden Door",
                            "item" : None},

                  (1, 1) : {"door" : None,
                            "item" : None}}

    print("--- DEMO 1: Interacting with an Item ---")
    selection_and_commits("Player 1", (0, 0), demo_board)

    print("\n\nBoard state at (0, 0) after pick up:", demo_board[(0, 0)])

    print("\n--- DEMO 2: Interacting with an Empty Tile ---")
    selection_and_commits("Player 1", (1, 1), demo_board)