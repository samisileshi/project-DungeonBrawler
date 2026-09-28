def inspect_tile(player_name, player_pos, board):

    x = player_pos[0] #Get the player position and set it to x.
    y = player_pos[1] #Get the player position and set it to y.

    #Tell the player the tile is being inspected.
    print("\n" + player_name + " Inspecting Menu ")
    print("[1] Inspect current cell(" + str(x) + ", " + str(y) + ")")
    print("[2] Inspect adjacent cell (Up/Down/Left/Right)")

    choice = input()

    target_x = x
    target_y = y
    if choice == '2':
        print("Which direction would you like to inspect")
        print("[W] Up, [A] Left, [S] Down, [D] Right")
        direction_choice = input().lower()

        if direction_choice == 'w':
            target_y = target_y - 1
        elif direction_choice == 'a':
            target_x = target_x - 1

        elif direction_choice == 's':
            target_y = target_y + 1

        elif direction_choice == 'd':
            target_x = target_x + 1

        else:
            print("Invalid Tile, Inspection Cancelled")
            return
    elif choice != '1':
        print("Invalid input, Inspection Cancelled")
        return

    if(target_x < 0 or target_x > 3 or target_y < 0 or target_y > 2):
        print("You feel a cold hard surface, but it is just the dungeon wall")
        return

    #If the tile the player is within the board, get the tile_data at that coordinate.
    if(target_x,target_y) in board:
        tile_data = board[(target_x,target_y)]

        #Print the location and description of the tile.
        print("Location: " + str(tile_data.get('Name',' Room')))
        print("Descirption: " + str(tile_data.get('Description','Nothing abnormal')))

        if tile_data.get('door') !=None:
            print("Door:" + str(tile_data['door']))

        #If the tile_data is a trap, tell the player they have found a trap and the type of trap.
        if tile_data.get('trap') !=None:
            print("WARNING: You have found a trap: " + str(tile_data['trap']) + "!")
        else:
            print("Traps were not found")

        #If the tile_data is an item, tell the player the item they found
        if tile_data.get('item') !=None:
            print("ITEM FOUND: You have found a " + str(tile_data['item']) + "!")
        else: 
            print("No items found")
    #If its an ordinary room, skip everything.
    else: 
        print("This tile is an empty room")