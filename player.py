#This will be where the player class will be 
class Player:
     def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.score = 0
        self.sigils = 0
        self.doors_completed = 0
        self.inventory = []
        self.buffs = []
