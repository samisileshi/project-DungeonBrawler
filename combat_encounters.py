"""Sami F11/F12: enemy selection, difficulty scaling, and boss fate."""
from __future__ import annotations
from pathlib import Path
import json
import random
from combat_entities import Enemy, Boss

DIFFICULTY_MULTIPLIERS = {"rookie": .85, "adventurer": 1., "dungeon master": 1.20}

def load_enemy_templates(path=None):
    """File I/O: enemy stats live in combat_enemies.json, not hard-coded classes."""
    path = Path(path) if path else Path(__file__).with_name("combat_enemies.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    for category in ("normal", "elite", "boss"):
        if not isinstance(data.get(category), list) or not data[category]:
            raise ValueError(f"Missing enemy category: {category}")
    return data

ENEMY_TEMPLATES = load_enemy_templates()
NORMAL_ENEMIES = ENEMY_TEMPLATES["normal"]
ELITE_ENEMIES = ENEMY_TEMPLATES["elite"]
BOSSES = ENEMY_TEMPLATES["boss"]

class EncounterFactory:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def create(self, round_number=1, difficulty="adventurer", enemy_type="normal") -> Enemy:
        if difficulty not in DIFFICULTY_MULTIPLIERS:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        if enemy_type not in {"normal", "elite", "boss"}:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
        pool = {"normal": NORMAL_ENEMIES, "elite": ELITE_ENEMIES, "boss": BOSSES}[enemy_type]
        template = self.rng.choice(pool)
        multiplier = DIFFICULTY_MULTIPLIERS[difficulty] * (1 + max(0, round_number - 1) * .08)
        cls = Boss if enemy_type == "boss" else Enemy
        return cls(name=template["name"], max_health=max(1, int(template["health"] * multiplier)),
                   attack=max(1, int(template["attack"] * multiplier)),
                   defense=max(0, int(template["defense"] * multiplier)),
                   parry_chance=template["parry_chance"],
                   special_chance=template["special_chance"], reward=template["reward"],
                   enemy_type=enemy_type)

    def roll(self, round_number=1, difficulty="adventurer", force_type=None) -> Enemy:
        if force_type is None:
            value = self.rng.randint(1, 100)
            # Hidden boss chance: 10%; the team's every-second-round boss door
            # should call force_type="boss" explicitly.
            force_type = "boss" if value <= 10 else "elite" if value <= 30 else "normal"
        return self.create(round_number, difficulty, force_type)

def recursive_boss_fate(players: list[str], rng: random.Random | None = None) -> list[str]:
    """Recursively choose boss entrants, supporting one or two players.

    Recursion walks the available entrants; each joins with 50% probability.
    Guarantees at least one entrant (the original door entrant). O(n) time/stack.
    The calling door/round owner decides who is eligible for this boss event.
    """
    if not players:
        raise ValueError("At least one entrant is required")
    rng = rng or random.Random()

    def pick(index: int) -> list[str]:
        if index >= len(players):
            return []
        selection = [players[index]] if rng.randint(0, 1) else []
        return selection + pick(index + 1)

    return pick(0) or [players[0]]
