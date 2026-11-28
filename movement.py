#Written by Wilson Huang
from collections import deque

move_log_size = 5 

def log_move(move_log, message): # Create a function for keep track of moves,
    move_log.append(message) # Adds the move to the queue

    if len(move_log) > move_log_size: # Check if the amount of moves currently stored is less than the limit
        move_log.popleft() # If the it exceeds the limit pop the first move.

def print_move_log(move_log): # Function to print the move logs
    print("\nRecent moves:")

    if not move_log:
        print("No moves have been made yet.")
        return

    for entry in move_log:
        print("-", entry)


def movement(player_name, player_pos, board, move_log = None):

    # Display movement inputs.
    print("[W] Up")
    print("[A] Left")
    print("[S] Down")
    print("[D] Right")
    print("[L] Recent Moves")
    print("[Q] Quit")

    print("\nPlease choose a direction to move.")
    # Ask for the movement input from player.
    choice = input("> ").lower()
    
    while choice not in ["w","a","s","d","l","q"]:
        print("\nInvalid input. Please enter W, A, S, D, L or Q.")
        choice = input("> ").lower()

    if choice == 'l':
        print_move_log(move_log)
        return player_pos

    if choice == "q" :
        print("\nEnding your Turn.")

        return None

    new_x = player_pos[0]
    new_y = player_pos[1]

    if choice == "w" : # Character moves 1 tile upwards.
        new_y = new_y - 1 # -1 Because since its in the terminal the bottom is the highest number you need to go -1 line down to go up.
    elif choice == "a" :
        new_x = new_x - 1 # Charcter moves 1 tile to the left.
    elif choice == "s" :
        new_y = new_y + 1 # Character moves 1 tile downwards.
    elif choice == "d" :
        new_x = new_x + 1 # Character moves 1 tile to the right.

    # If the player is not within these bounds of the 4x3 grid, tell them they hit a wall and return the position of the player.
    if new_x < 0 or new_x > 3 or new_y < 0 or new_y > 2 :
        print("\nMovement blocked, you hit the dungeon wall.", end = "", flush = True)

        return player_pos

    # Update the player position after an input was decided and return where the player has moved to.
    player_pos[0] = new_x
    player_pos[1] = new_y
    print("\n" + player_name, "moved to cell (" + str(new_x) + ", " + str(new_y) + ")!", end = "", flush = True)
    log_move(move_log, player_name + " moved to cell (" + str(new_x) + ", " + str(new_y) + ")")
    return player_pos