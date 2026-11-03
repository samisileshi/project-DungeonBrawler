"""Sami F10: parry resolution, independent of display implementation."""
from __future__ import annotations
import random
from combat_entities import Combatant

class ParrySystem:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def resolve(self, defender: Combatant, attempt: bool = True, difficulty="adventurer", pvp=False):
        if not attempt:
            return "missed"
        factor = {"rookie": 1.15, "adventurer": 1., "dungeon master": .75}[difficulty]
        if pvp:
            factor *= .70
        chance = min(100, round(defender.parry_chance * factor))
        if self.rng.randint(1, 100) > chance:
            return "missed"
        return "perfect" if self.rng.randint(1, 100) <= defender.perfect_parry_chance else "normal"

    def mitigate(self, raw_damage: int, result: str) -> int:
        if result == "perfect":
            return 0
        if result == "normal":
            return int(raw_damage * self.rng.uniform(.35, .65))
        return raw_damage
