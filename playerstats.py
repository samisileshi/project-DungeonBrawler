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
            self.hp = max(0,min(self.max_hp, self.hp + amount)) #Caps the hp at max_hp and prevents it from dropping below 0
            
        def modify_focus(self,amount):
            self.focus = max(0,self.focus + amount) #Update focus and prevent it from dropping below 0

        def equip_item(self,slot,item): 
            if slot in self.equipment: #Only equip if the slot is open
                self.equipment[slot] = item

        def check_revival(self):
            if self.hp == 0 and self.revival > 0: # Checks if the player has died and has a revival
                self.revivals -= 1 # Use one revival
                self.hp = self.max_hp # Restore hp
                return True
            return False
        
if __name__ == "__main__":
    player = Player()
    print(f"Start HP: {player.hp}")  

    player.modify_hp(-30)
    print(f"After Damage HP: {player.hp}")  

    player.equip_item("weapon", "Iron Sword")
    print(f"Weapon: {player.equipment['weapon']}")  

    player.enemies_defeated += 1
    print(f"Enemies Defeated: {player.enemies_defeated}")  