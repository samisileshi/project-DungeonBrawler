# Written by Wilson Huang

class Progression:
    def __init__(self):
        self.doors_completed = 0
        self.enemies_defeated = 0
        self.bosses_defeated = 0
        self.minigames_won = 0
        self.revivals = 1
        self.revived = False

    def complete_door(self):
        self.doors_completed += 1

    def defeat_enemy(self):
        self.enemies_defeated += 1

    def defeat_boss(self):
        self.bosses_defeated += 1

    def win_minigame(self):
        self.minigames_won += 1

    def check_revival(self, hp):
        self.revived = False
        if hp == 0 and self.revivals > 0:
            self.revivals -= 1 
            self.revived = True
        return self.revived

if __name__ == "__main__":
    progress = Progression()
    print("Enemies Defeated before:", progress.enemies_defeated) 

    progress.defeat_enemy()
    print("Enemies Defeated now:", progress.enemies_defeated) 

    print("Revived?", progress.check_revival(0))  
    print("Revivals Remaining:", progress.revivals)  

    print("Revived?", progress.check_revival(0))  