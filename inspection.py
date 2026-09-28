def inspect_tile(player_name, player_pos, board):

    x = player_pos[0] #Get the player position and set it to x.
    y = player_pos[1] #Get the player position and set it to y.

    #Tell the player the tile is being inspected.
    print("\n" + player_name + " Inspecting tile,(" + str(x) + "," + str(y) + ")")

    #If the tile the player is within the board, get the tile_data at that coordinate.
    if(x,y) in board:
        tile_data = board[(x,y)]

        #Print the location and description of the tile.
        print("Location: " + str(tile_data.get('Name',' Room')))
        print("Descirption: " + str(tile_data.get('Description','Nothing abnormal')))

        #If the tile_data is a trap, tell the player they have found a trap and the type of trap.
        if tile_data.get('trap') !=None:
            print("WARNING: You have found a trap: " + str(tile_data['trap']) + "!")
        else:
            print("Traps were not found")

        #If the tile_data is an item, tell the player the item they found
        if tile_data.get('item') !=None:
            print("ITEM FOUND: You have found a " + str(tile_data['item'] + "!"))
        else: 
            print("No items found")
    #If its an ordinary room, skip everything.
    else: 
        print("This tile is an empty room")