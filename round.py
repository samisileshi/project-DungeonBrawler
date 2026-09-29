#Written by Youssouf Tive Madi

#when given 2 dictionarries player 1 and 2 i return a dictionary of the names and
#point, then return the round number and if the game is over yet
def game_state(player_one, player_two):
    return {
        "player1": player_one["name"],
        "player2": player_two["name"],
        "score": {
            player_one["name"]: 0,
            player_two["name"]: 0,
        },
        "round": 1,
        "game_over": False,
    }

#Updates the current round
def update_round(game):
    game["round"] += 1
    return game


#test 
player_one = {
    "name": "Joe"
}

player_two = {
    "name": "Yapp"
}

game = game_state(player_one, player_two)
print(game)

#moves to the next round
update_round(game)


print("After update:")
print(game)

