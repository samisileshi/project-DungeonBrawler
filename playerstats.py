# Written by Wilson Huang
class Player:
    def __init__(self,username='Player'):
        self.username = username
        self.hp = 100
        self.maxhp = 100
        self.attack = 15
        self.defense = 5
        self.focus = 50
        self.coins = 0
        self.renown = 0 
        self.escape_sigils = 0
        self.inventory = []
        self.equipment = {'weapon':None,'armor':None}
        self.buffs = []
        self.debuffs = []
        self.doors_completed = 0
        self.bosses_defeated = 0
        self.minigames_won = 0
        self.revivals = 1

    def modify_hp(self,amount):
        self.hp = max(0,min(self.maxhp, self.hp + amount)) #Caps the hp at max_hp and prevents it from dropping below 0
            
    def modify_focus(self,amount):
        self.focus = max(0,self.focus + amount) #Update focus and prevent it from dropping below 0

    def equip_item(self,slot,item): 
        if slot in self.equipment: #Only equip if the slot is open
            self.equipment[slot] = item

    def check_revival(self):
        if self.hp == 0 and self.revival > 0: # Checks if the player has died and has a revival
            self.revivals -= 1 # Use one revival
            self.hp = self.maxhp # Restore hp
            return True
        return False

    def display_stats(self):
        print("\n==== " + self.username + "'s Stats ====")
        print("HP: " + str(self.hp) + "/" + str(self.maxhp))
        print("Attack: " + str(self.attack))
        print("Defense: " + str(self.defense))
        print("Focus: " + str(self.focus))
        print("Coins: " + str(self.coins))
        print("Renown: " + str(self.renown))
        print("Escape Sigils: " + str(self.escape_sigils))
        print("Inventory: " + str(len(self.inventory)) + " items")

        print("Equipment:")
        for slot, item in self.equipment.items(): 
            if item: 
                print("  " + slot + ": " + str(item))
            else:
                print("  " + slot + ": Empty")

        print("Buffs: " + str(self.buffs))
        print("Debuffs: " + str(self.debuffs))
        print("Doors Completed: " + str(self.doors_completed))
        print("Bosses Defeated: " + str(self.bosses_defeated))
        print("Minigames Won: " + str(self.minigames_won))
        print("Revivals: " + str(self.revivals))
        
if __name__ == "__main__":
    hero = Player("Player 1")
    hero.display_stats()