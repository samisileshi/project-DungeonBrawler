def inspect_tile (player_name, player_pos, board) :
    x = player_pos[0] # Get the player position and set it to x.
    y = player_pos[1] # Get the player position and set it to y.

    # Provide a menu.
    print(player_name, "Inspecting Menu")
    print("[1] Inspect current cell (" + str(x) + ", " + str(y) + ")")
    print("[2] Inspect adjacent cell (Up/Down/Left/Right)")

    # Gather player input.
    choice = input("> ")

    # Set the wanted cell.
    target_x = x
    target_y = y

    if choice == "2" :
        print("\nWhich direction would you like to inspect?")
        print("[W] Up, [A] Left, [S] Down, [D] Right")
        direction_choice = input("> ").lower()

        # FIXME: use a match case statement instead of a bunch of if statements
        #   -Ibrahim
        if direction_choice == "w" :
            target_y = target_y - 1 # Character moves 1 tile upwards.
        elif direction_choice == "a" :
            target_x = target_x - 1 # Character moves 1 tile left.
        elif direction_choice == "s" :
            target_y = target_y + 1 # Character moves 1 tile downwards.
        elif direction_choice == "d" :
            target_x = target_x + 1 # Character moves 1 tile right.
        else :
            print("\nInvalid Tile, Inspection Cancelled.", end = "", flush = True)

            # FIXME: don't cancel, just error-check
            #   -Ibrahim
            return
    # If the input was invalid, cancel the inspection.
    elif choice != "1" :
        print("\nInvalid input, Inspection Cancelled.", end = "", flush = True)

        # FIXME: don't cancel, just error-check
        #   -Ibrahim
        return

    # Check if the target is within the 4x3 board, if not, it is a dungeon wall.
    if (target_x < 0 or target_x > 3 or target_y < 0 or target_y > 2) :
        print("\nYou feel a cold hard surface, but it is just the dungeon wall.", end = "", flush = True)
        return

    # If the tile the player is within the board, get the tile_data at that coordinate.
    if (target_x,target_y) in board :
        tile_data = board[(target_x, target_y)]

        # Print the location and description of the tile.
        print("\nLocation:", tile_data.get("Name", "Room"))
        print("Description:", tile_data.get("Description", "Nothing abnormal"))

        if tile_data.get('door') != None :
            print("Door:", tile_data["door"])

        # If the tile_data is a trap, tell the player they have found a trap and the type of trap.
        if tile_data.get("trap") != None :
            print("WARNING: You have found a trap:", tile_data['trap'] + "!")
        else :
            print("Traps were not found.")

        # If the tile_data is an item, tell the player the item they found.
        if tile_data.get('item') != None :
            print("ITEM FOUND: You have found a", tile_data['item'] + "!")
        else :
            print("No items found.")
    # If it's an ordinary room, skip everything.
    else :
        print("\nThis tile is an empty room.")

if __name__ == "__main__" :
    board = {(0, 0) : {"Name"        : "Entrance",
                       "Description" : "A chilly doorway."},

             (1, 0) : {"Name"        : "Hallway",
                       "Description" : "Dark corridor.",
                       "trap"        : "Spikes"},

             (0, 1) : {"Name"        : "Armory",
                       "Description" : "Weapon racks.",
                       "item"        : "Sword"}}

    inspect_tile("Hero", (0, 0), board)