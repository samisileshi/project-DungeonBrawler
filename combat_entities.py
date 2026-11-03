"""Sami F9-F12: combat actors and their persistent combat stats."""
from __future__ import annotations
from dataclasses import dataclass, field
import random

@dataclass
class Combatant:
    name: str
    max_health: int
    attack: int
    defense: int = 0
    parry_chance: int = 20
    perfect_parry_chance: int = 20
    health: int | None = None
    status_effects: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if self.health is None:
            self.health = self.max_health
        self.health = max(0, min(self.max_health, self.health))

    @property
    def alive(self):
        return self.health > 0

    def take_damage(self, amount: int) -> int:
        amount = max(0, int(amount))
        actual = min(self.health, amount)
        self.health -= actual
        return actual

    def heal(self, amount: int) -> int:
        healed = min(max(0, amount), self.max_health - self.health)
        self.health += healed
        return healed

    def apply_status(self, name: str, turns: int):
        if turns > 0:
            self.status_effects[name] = max(turns, self.status_effects.get(name, 0))

    def tick_statuses(self) -> list[str]:
        """Apply poison/burn and decrease durations; called at start of turn."""
        messages = []
        for status, duration in list(self.status_effects.items()):
            if status in {"poison", "burn"} and self.alive:
                damage = self.take_damage(4 if status == "poison" else 6)
                messages.append(f"{self.name} takes {damage} {status} damage.")
            if duration <= 1:
                del self.status_effects[status]
            else:
                self.status_effects[status] = duration - 1
        return messages

@dataclass
class CombatPlayer(Combatant):
    focus: int = 50
    max_focus: int = 50
    special: int = 28
    potions: int = 2
    coins: int = 0
    score: int = 0
    enemies_defeated: int = 0
    bosses_defeated: int = 0

    @classmethod
    def from_team_stats(cls, stats: dict) -> "CombatPlayer":
        """Adapt team player statistics without editing the team module."""
        return cls(name=stats.get("username", stats.get("name", "Hero")),
                   max_health=stats.get("max_hp", stats.get("max_health", 100)),
                   health=stats.get("hp", stats.get("health", 100)),
                   attack=stats.get("attack", 15), defense=stats.get("defense", 3),
                   focus=stats.get("focus", 50), coins=stats.get("coins", 0),
                   score=stats.get("renown", stats.get("score", 0)),
                   enemies_defeated=stats.get("enemies_defeated", 0),
                   bosses_defeated=stats.get("bosses_defeated", 0))

    def update_team_stats(self, stats: dict):
        """Copy combat-related statistics into the team player dictionary."""
        hp_key = "hp" if "hp" in stats else "health"
        stats[hp_key] = self.health
        for key, value in (("focus", self.focus), ("coins", self.coins),
                           ("enemies_defeated", self.enemies_defeated),
                           ("bosses_defeated", self.bosses_defeated)):
            if key in stats:
                stats[key] = value
        if "renown" in stats:
            stats["renown"] = self.score
        elif "score" in stats:
            stats["score"] = self.score

    def drink_potion(self) -> int:
        if self.potions <= 0 or self.health == self.max_health:
            return 0
        healed = self.heal(30)
        self.potions -= 1
        return healed

@dataclass
class Enemy(Combatant):
    enemy_type: str = "normal"
    special_chance: int = 10
    reward: int = 25
    skill_name: str = "Power strike"
    reward_claimed: bool = False

    def attack_cue(self, rng: random.Random) -> tuple[int, str]:
        is_special = rng.randint(1, 100) <= self.special_chance
        damage = rng.randint(max(1, self.attack - 2), self.attack + 2)
        return (int(damage * 1.5), self.skill_name) if is_special else (damage, "Basic strike")

@dataclass
class Boss(Enemy):
    enemy_type: str = "boss"
    skill_name: str = "Crushing boss strike"
