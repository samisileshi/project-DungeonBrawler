"""Sami F9-F12: combat controller and backward-compatible integration API.

Concrete enemy templates live in combat_enemies.json.
Combat sessions can be saved to JSON using --combat-save PATH.
"""

# FIXME: you're not using annotations from __future__
#   -Ibrahim
from __future__ import annotations
from dataclasses import dataclass, field
import json
from os import write
from pathlib import Path
import random
import time
from typing import Callable

# FIXME: both combat_encounters and combat_parry already import combat_entities
#   -Ibrahim
from combat_entities import Combatant, CombatPlayer, Enemy, Boss
from combat_encounters import (EncounterFactory, recursive_boss_fate,
    DIFFICULTY_MULTIPLIERS, NORMAL_ENEMIES, ELITE_ENEMIES, BOSSES)
from combat_parry import ParrySystem

@dataclass
class CombatResult:
    # FIXME: create an __init__() function for CombatResult, just for structure at least
    #   -Ibrahim
    won: bool
    reason: str
    turns: int
    coins: int = 0
    score: int = 0
    contributions: dict[str, int] = field(default_factory=dict)

class CombatEngine:
    """One combat session; UI-free turn resolution, with optional CLI presenter."""
    SPECIAL_COST = 15

    def __init__(self, player: CombatPlayer, enemy: Enemy, difficulty="adventurer",
                 rng: random.Random | None = None, timeout_seconds: float = 180,
                 clock: Callable[[], float] = time.monotonic):
        if difficulty not in DIFFICULTY_MULTIPLIERS:
            raise ValueError("Invalid difficulty")
        self.player, self.enemy, self.difficulty = player, enemy, difficulty

        # FIXME: you don't need self.rng, just call random. + whatever method
        #   -Ibrahim
        self.rng = rng or random.Random()
        self.parry = ParrySystem(self.rng)
        self.timeout_seconds = timeout_seconds
        self.clock = clock
        self.started = clock()
        self.turns = 0
        self.log: list[str] = []
        self.contributions: dict[str, int] = {player.name: 0}
        self.result: CombatResult | None = None

    def _say(self, message):
        self.log.append(message)

    def _finish(self, won: bool, reason: str):
        # FIXME: the "is not None" part is redundant, just putting "if self.result" automatically checks whether it's None
        #   -Ibrahim
        if self.result is not None:
            return self.result
        coins = score = 0
        if won and not self.enemy.reward_claimed:
            score = self.enemy.reward
            coins = self.rng.randint(5, 12) + (20 if isinstance(self.enemy, Boss) else 8 if self.enemy.enemy_type == "elite" else 0)
            self.player.score += score
            self.player.coins += coins
            self.player.enemies_defeated += 1
            if isinstance(self.enemy, Boss):
                self.player.bosses_defeated += 1
            self.enemy.reward_claimed = True
        self.result = CombatResult(won, reason, self.turns, coins, score, self.contributions.copy())
        self._say(f"Combat ended: {reason}. Reward: {score} score, {coins} coins.")
        return self.result

    def step(self, action: str, parry_attempt=True) -> CombatResult | None:
        """Perform one turn. Invalid actions never consume a turn."""
        if self.result:
            return self.result
        if self.clock() - self.started >= self.timeout_seconds:
            return self._finish(False, "timeout")
        if not self.player.alive:
            return self._finish(False, "player defeated")
        if not self.enemy.alive:
            return self._finish(True, "enemy defeated")
        if action not in {"attack", "special", "potion", "inspect"}:
            raise ValueError("Use attack, special, potion, or inspect")
        if action == "inspect":
            self._say(f"{self.enemy.name}: HP={self.enemy.health}, attack={self.enemy.attack}, defense={self.enemy.defense}, effects={self.enemy.status_effects}")
            return None
        if action == "special" and self.player.focus < self.SPECIAL_COST:
            self._say("Not enough focus.")
            return None
        if action == "potion" and (self.player.potions <= 0 or self.player.health >= self.player.max_health):
            self._say("No usable potion or health already full.")
            return None
        self.turns += 1
        for message in self.player.tick_statuses():
            self._say(message)
        if not self.player.alive:
            return self._finish(False, "status damage")

        # FIXME: combine this with the existing action == "potion" statement and make the rest of the boolean expression a separate statement nested inside
        #   -Ibrahim
        if action == "potion":
            self._say(f"{self.player.name} heals {self.player.drink_potion()} HP.")
        else:
            if action == "special":
                self.player.focus -= self.SPECIAL_COST

                # FIXME: try this instead: raw = max(1, self.player.special + self.rng.randint(-4, 4))
                #   -Ibrahim
                raw = self.rng.randint(max(1, self.player.special - 4), self.player.special + 4)
            else:
                # FIXME: try this instead: raw = max(1, self.player.attack + self.rng.randint(-4, 4))
                #   -Ibrahim
                raw = self.rng.randint(max(1, self.player.attack - 2), self.player.attack + 2)
                self.player.focus = min(self.player.max_focus, self.player.focus + 5)
            parry = self.parry.resolve(self.enemy, difficulty=self.difficulty)
            actual = self.enemy.take_damage(max(0, self.parry.mitigate(raw, parry) - self.enemy.defense))
            self.contributions[self.player.name] += actual
            self._say(f"{self.player.name} uses {action}: {actual} damage. Enemy parry: {parry}.")

            # FIXME: shouldn't you check if randint >= 80?
            #   -Ibrahim
            if action == "special" and actual and self.rng.randint(1, 100) <= 20:
                self.enemy.apply_status("burn", 2)
                self._say(f"{self.enemy.name} is burning (2 turns).")
        if not self.enemy.alive:
            return self._finish(True, "enemy defeated")
        for message in self.enemy.tick_statuses():
            self._say(message)
        if not self.enemy.alive:
            return self._finish(True, "enemy defeated")
        raw, cue = self.enemy.attack_cue(self.rng)
        self._say(f"Attack cue: {self.enemy.name} prepares {cue}!")
        parry = self.parry.resolve(self.player, parry_attempt, self.difficulty)
        actual = self.player.take_damage(max(0, self.parry.mitigate(raw, parry) - self.player.defense))
        self._say(f"{self.enemy.name} deals {actual} damage. Player parry: {parry}.")
        if parry == "perfect":
            counter = self.enemy.take_damage(5)
            self.contributions[self.player.name] += counter
            self._say(f"Perfect parry counterattack: {counter} damage!")
        if not self.player.alive:
            return self._finish(False, "player defeated")
        if not self.enemy.alive:
            return self._finish(True, "enemy defeated")
        return None

    def serialize(self) -> dict:
        """Combat-only snapshot. Never saves the whole team's game state."""
        from dataclasses import asdict
        return {"version": 1, "difficulty": self.difficulty,
                "player": asdict(self.player), "enemy": asdict(self.enemy),
                "turns": self.turns, "contributions": self.contributions,
                "remaining_seconds": max(0., self.timeout_seconds - (self.clock() - self.started)),
                "result": asdict(self.result) if self.result else None}

    def save(self, path: str | Path):
        # FIXME: I don't think you need to import Path and create a directory, opening a file to write should automatically create the file
        #   -Ibrahim
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.serialize(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path, rng=None, clock=time.monotonic):
        # FIXME: again, you don't need to import Path, just use the built-in write stuff
        #   -Ibrahim
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            if data["version"] != 1:
                raise ValueError("Unsupported combat save version")
            player = CombatPlayer(**data["player"])
            enemy_data = data["enemy"]
            enemy = (Boss if enemy_data["enemy_type"] == "boss" else Enemy)(**enemy_data)
            engine = cls(player, enemy, data["difficulty"], rng=rng,
                         timeout_seconds=float(data["remaining_seconds"]), clock=clock)
            engine.turns = int(data["turns"])
            engine.contributions = dict(data["contributions"])
            if data["result"] is not None:
                engine.result = CombatResult(**data["result"])
            return engine
        except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot load combat save: {exc}") from exc

def run_door_combat(player_stats: dict, round_number=1, difficulty="adventurer",
                    enemy_type=None, action_provider=None, rng=None) -> CombatResult:
    """Integration hook for door owner; adapters avoid editing their code."""
    # FIXME: still don't need rng, just use random. whatever function
    #   -Ibrahim
    rng = rng or random.Random()
    player = CombatPlayer.from_team_stats(player_stats)
    enemy = EncounterFactory(rng).roll(round_number, difficulty, enemy_type)
    engine = CombatEngine(player, enemy, difficulty, rng)
    result = play_terminal(engine, action_provider)
    player.update_team_stats(player_stats)
    return result

def play_terminal(engine: CombatEngine, action_provider=None) -> CombatResult:
    """Text interface; action_provider is injectable for automated tests."""
    choose = action_provider or input
    print(f"\nEncounter: {engine.enemy.name} [{engine.enemy.enemy_type}]")
    seen = 0
    while engine.result is None:
        p, e = engine.player, engine.enemy
        print(f"\n{p.name}: {p.health}/{p.max_health} HP, {p.focus} Focus, {p.potions} potions")
        print(f"{e.name}: {e.health}/{e.max_health} HP | Turn {engine.turns + 1}")
        raw = choose("[1] Attack [2] Special (15 focus) [3] Potion [4] Inspect: ").strip()
        action = {"1": "attack", "2": "special", "3": "potion", "4": "inspect"}.get(raw)
        if action is None:
            print("Invalid selection.")
            continue
        engine.step(action)
        for message in engine.log[seen:]:
            print(message)
        seen = len(engine.log)
    return engine.result

def combat_demo(name="Player 1", difficulty="adventurer", enemy_type="normal",
                round_number=1, seed=None, load=None, save=None):
    rng = random.Random(seed)
    if load:
        engine = CombatEngine.load(load, rng=rng)
    else:
        engine = CombatEngine(CombatPlayer(name=name, max_health=100, attack=15, defense=3,
                                           parry_chance=35, perfect_parry_chance=25),
                              EncounterFactory(rng).create(round_number, difficulty, enemy_type),
                              difficulty, rng)
    try:
        return play_terminal(engine)
    finally:
        if save:
            engine.save(save)

if __name__ == "__main__":
    combat_demo()
