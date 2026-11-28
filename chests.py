# Written by Youssouf Tive Madi

import random

# The chest class using pieces from the old make_chest method
class Chest :
    def __init__(self) :
        self.chest_loot = ["Health Potion", "Iron Sword"]
        self.loot = random.choice(self.chest_loot)

        # FIXME: the buffs list could be initialized outside the class, if self.buff just needs one buff
        #   -Ibrahim
        self.buffs = ["+10 damage buff", "+10 health buff", "+10 shield buff"]
        self.buff = random.choice(self.buffs)

        # FIXME: while self.opened_by is None, it can be used as a boolean, replacing self.opened
        #   -Ibrahim
        self.opened = False
        self.opened_by = None

    def access_chest (self, player) :
        if self.opened :
            return self.opened_by + " already opened the chest."

        self.opened = True
        self.opened_by = player.name
        player.inventory.append(self.loot)
        player.buffs.append(self.buff)

        return "Chest claimed by " + self.opened_by + "."

    def to_dict(self) :
        return {"loot"      : self.loot,
                "buff"      : self.buff,
                "opened"    : self.opened,
                "opened_by" : self.opened_by}

    @classmethod
    def from_dict (cls, data) :
        chest = cls()
        chest.loot = data["loot"]
        chest.buff = data["buff"]
        chest.opened = data["opened"]
        chest.opened_by = data["opened_by"]

        return chest