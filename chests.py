#Written by Youssouf Tive Madi

import random

#The chest class using pieces from the old make_chest metho
class Chest:
    def __init__(self):
        self.chest_loot = ["Health Potion", "Iron Sword"]
        self.loot = random.choice(self.chest_loot)
        self.buffs = ["+10 damage buff", "+10 health buff", "+10 shield buff"]
        self.buff = random.choice(self.buffs)
        self.opened = False
        self.opened_by = None

    def access_chest(self, player):
        if self.opened:
            return f"{self.opened_by} already opened the chest"

        self.opened = True
        self.opened_by = player.name
        player.inventory.append(self.loot)
        player.buffs.append(self.buff)
        return f"Chest claimed by {self.opened}"

    def to_dict(self):
        return {
            "loot": self.loot,
            "buff": self.buff,
            "opened": self.opened,
            "opened_by": self.opened_by
        }

    @classmethod

    def from_dict(cls, data):
        chest = cls()
        chest.loot = data["loot"]
        chest.buff = data["buff"]
        chest.opened = data["opened"]
        chest.opened_by = data["opened_by"]
        return chest

