# Written by Youssouf Tive Madi

# Make the game_state class

class GameState :
    def __init__ (self, player_one, player_two) :
        # The list of players
        self.players = [player_one, player_two]
        # Starts at round 1
        self.round = 1
        self.game_over = False

    # This method goes to the next round
    def next_round(self) :
        self.round += 1

    # Checks if the game is over
    def is_game_over(self) :
        return self.game_over