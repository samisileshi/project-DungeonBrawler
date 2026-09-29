#Written by Wilson Huang

def print_board(player_pos, width=4, height=3):
    for y in range(height):
        row = ""
        for x in range(width):
            if [x, y] == player_pos:
                row += "[ P ]"  
            else:
                row += "[ . ]"  
        print(row)



def movement(player_name, player_pos, board):

    # Display movement inputs.
    print("[W] Up")
    print("[A] Left")
    print("[S] Down")
    print("[D] Right")

    # Ask for the movement input from player.
    choice = input("Please choose a direction to move").lower()

    new_x = player_pos[0]
    new_y = player_pos[1]

    if choice == 'w': # Character moves 1 tile upwards.
        new_y = new_y - 1 # -1 Because since its in the terminal the bottom is the highest number you need to go -1 line down to go up.

    elif choice == 'a':
        new_x = new_x - 1 # Charcter moves 1 tile to the left.

    elif choice == 's':
        new_y = new_y + 1 # Character moves 1 tile downwards.

    elif choice == 'd': 
        new_x = new_x + 1 # Character moves 1 tile to the right.

    else: # If an input is not WASD, tell the player to put a valid input and returns the position of the player.
        print("Movement Cancelled. Please enter a valid input.")
        return player_pos

    # If the player is not within these bounds of the 4x3 grid, tell them they hit a wall and return the position of the player.
    if new_x < 0 or new_x > 3 or new_y < 0 or new_y > 2:
        print("Movement blocked, you hit the dungeon wall.")
        return player_pos

    # Update the player position after an input was decided and return where the player has moved to.
    player_pos[0] = new_x
    player_pos[1] = new_y
    print(player_name + "moved to cell,(" + str(new_x) + " , " + str(new_y) + "!")
    return player_pos

def main():
    player_name = "Hero"
    player_pos = [0, 0] 
    board = None         
    while True:
        print_board(player_pos)
        updated_pos = movement(player_name, player_pos, board)

            


if __name__ == "__main__":
    main()