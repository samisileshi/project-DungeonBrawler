# Written by Youssouf Tive Madi

# When given 2 dictionaries, player 1 and 2, I return a dictionary of the names and
#   points, then return the round number and whether the game is over yet

# FIXME: round.py is redundant, just use game_state.py
#   -Ibrahim
def game_state (player_one, player_two) :
    return {"player1"  : player_one["name"],
            "player2"  : player_two["name"],
            "score"    : {player_one["name"] : 0,
                          player_two["name"] : 0},
            "round"    : 1,
            "game_over": False}

# Updates the current round
def update_round (game) :
    game["round"] += 1

    return game

# Test
player_one = {"name" : "Joe"}

player_two = {"name" : "Yapp"}

game = game_state(player_one, player_two)
print(game)

# Moves to the next round
update_round(game)
print("\nAfter update:")
print(game, end = "", flush = True)