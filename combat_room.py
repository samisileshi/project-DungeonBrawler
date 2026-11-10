"""Sami's room combat rules: stages, boss fate, turns, rewards and timers."""
from __future__ import annotations
from dataclasses import dataclass, field
import random
import time
from typing import Callable

# FIXME: both combat_encounters and combat_parry already import combat_entities
#   -Ibrahim
from combat_entities import CombatPlayer, Enemy, Boss
from combat_encounters import EncounterFactory
from combat_parry import ParrySystem

ROOM_SECONDS = {"rookie":75, "adventurer":60, "dungeon master":45}

def expand_combat_stages(stages):
    """Recursively flatten a door's nested combat waves in their original order.

    Example: ["normal", ["elite", "boss"]] becomes three combat stages.
    This is useful when a team door groups several enemies into one wave.
    """
    if not stages:
        return []
    first, *remaining = stages
    if isinstance(first, (list, tuple)):
        return expand_combat_stages(first) + expand_combat_stages(remaining)
    return [first] + expand_combat_stages(remaining)


@dataclass
class CombatDoor:
    name: str
    stages: list[str]
    score_reward: int = 300
    room_seconds: float | None = None
    completed: bool = False
    completed_by: str | None = None
    failed_by: list[str] = field(default_factory=list)
    reward_given: bool = False

    @classmethod
    def from_data(cls, data: dict):
        """Accept team-door-style attributes or combat room description dictionaries."""
        stages = data.get("stages", data.get("enemies", []))
        if isinstance(stages, str):
            stages = [stages]
        stages = expand_combat_stages(stages)
        door_type = str(data.get("door_type", data.get("type", "normal"))).lower()
        if not stages and ("boss" in door_type or "combat" in door_type):
            stages = ["boss" if "boss" in door_type else "normal"]
        return cls(name=data.get("name", "Unknown Door"), stages=stages,
                   score_reward=int(data.get("score_reward",300)),
                   room_seconds=data.get("room_seconds",data.get("timer")),
                   completed=bool(data.get("completed",False)),
                   reward_given=bool(data.get("reward_given", False)),
                   completed_by=data.get("completed_by"),
                   failed_by=list(data.get("failed_by") or []))

    @classmethod
    def from_team_door(cls, door):
        return cls.from_data({"name": door.name, "door_type": door.door_type,
                 "score_reward": door.score_reward, "completed": door.completed,
                 "reward_given": getattr(door, "reward_given", False),
                 "completed_by": getattr(door, "completed_by", None),
                 "failed_by": getattr(door, "failed_by", None),
                 "stages": getattr(door, "stages", [])})

    @property
    def combat_active(self):
        return bool(self.stages) and not self.completed


@dataclass
class RoomResult:
    success: bool
    reason: str
    door: str
    coins: dict[str,int]
    renown: dict[str,int]
    contributions: dict[str,int]
    fate: str | None = None


class RoomCombat:
    """Event driven: start -> action -> pending attack -> parry -> next turn.

    A terminal runner handles prompts; the combat rules stay independent of input.
    Callbacks let the team integrate without changes to its modules.
    """
    def __init__(self, door: CombatDoor, entrant: CombatPlayer, opponent: CombatPlayer,
                 difficulty="adventurer", round_number=1, rng=None, clock=time.monotonic,
                 on_result: Callable[[RoomResult],None] | None=None, fate_override=None):
        if difficulty not in ROOM_SECONDS: raise ValueError("Unknown difficulty")
        self.door, self.entrant, self.opponent = door, entrant, opponent
        self.players = [entrant, opponent]
        if entrant is opponent or entrant.name == opponent.name: raise ValueError("Players need distinct names")
        self.rng = rng or random.Random()
        self.clock = clock
        self.difficulty = difficulty
        self.round_number = round_number
        self.parry = ParrySystem(self.rng)
        self.on_result = on_result
        self.started = self.clock()
        self.deadline = self.started + (door.room_seconds if door.room_seconds is not None else ROOM_SECONDS[difficulty])
        self.stage_index = -1
        self.enemy: Enemy | None = None
        self.participants: list[CombatPlayer] = []
        self.fate: str | None = None
        self.fate_override = fate_override
        self.pending: dict | None = None
        self.result: RoomResult | None = None
        self.messages: list[str] = []
        self.contributions = {p.name:0 for p in self.players}
        self.coins = {p.name:0 for p in self.players}
        self.renown = {p.name:0 for p in self.players}
        self.turn = 0
        self.stage_contributions = {p.name:0 for p in self.players}
        if self.door.completed:
            self.finish(False, "door already completed")
        elif not self.door.stages:
            self.finish(False, "no combat in this door")
        else:
            self._advance_stage()

    def say(self, msg): self.messages.append(str(msg))
    def remaining(self): return max(0.,self.deadline-self.clock())
    def check_timeout(self):
        if self.result: return True
        if self.clock() >= self.deadline:
            self.finish(False,"room timeout")
            return True
        if self.pending and self.clock() >= self.pending['deadline']:
            self.parry_attack(None)
        return bool(self.result)

    def _advance_stage(self):
        """Start the next enemy or finish the room after the last stage."""
        self.stage_index += 1
        if self.stage_index >= len(self.door.stages):
            self.finish(True,"all combat stages cleared")
            return
        descriptor = self.door.stages[self.stage_index]
        if isinstance(descriptor,dict):
            kind = descriptor.get('type','normal')
        else: kind = str(descriptor)
        if kind not in ('normal','elite','boss'):
            self.finish(False, f"unsupported combat stage: {kind}")
            return
        self.enemy = EncounterFactory(self.rng).create(self.round_number,self.difficulty,kind)
        self.fate = None
        if kind == 'boss':
            # Boss Fate: 60% entrant, 15% opponent, 25% cooperative.
            self.fate = self.fate_override or self.rng.choices(['entrant','opponent','both'], weights=[60,15,25])[0]
            if self.fate not in ('entrant','opponent','both'): raise ValueError('Bad fate')
            self.participants = {'entrant':[self.entrant], 'opponent':[self.opponent], 'both':self.players}[self.fate]
            if self.fate=='both':
                self.enemy.max_health = int(self.enemy.max_health*1.6)
                self.enemy.health = self.enemy.max_health
            self.say(f"BOSS FATE: {self.fate.upper()} ({', '.join(p.name for p in self.participants)})")
        else: self.participants=[self.entrant]
        self.turn = 0
        self.stage_contributions = {p.name:0 for p in self.players}
        self.say(f"Stage {self.stage_index+1}/{len(self.door.stages)}: {self.enemy.name} ({kind})")

    @property
    def current_player(self):
        living = [p for p in self.participants if p.alive]
        return living[self.turn % len(living)] if living else None

    def defeat_reason(self):
        """Describe only the fighters assigned to this encounter."""
        if len(self.participants) == 1:
            return f'{self.participants[0].name} defeated'
        return 'all cooperative fighters defeated'

    def action(self, action: str):
        """Resolve one player action and prepare the enemy response."""
        if self.check_timeout() or self.pending: return False
        p=self.current_player
        if p is None: return self.finish(False,self.defeat_reason())
        if action not in ('attack','special','potion','inspect'): return False
        if action=='inspect':
            self.say(f'{self.enemy.name}: {self.enemy.health}/{self.enemy.max_health} HP; ATK {self.enemy.attack}; DEF {self.enemy.defense}')
            return True
        if action=='special' and p.focus<15:
            self.say('Insufficient focus'); return False
        if action=='potion' and (p.potions<=0 or p.health>=p.max_health):
            self.say('No usable healing potion'); return False
        for msg in p.tick_statuses(): self.say(msg)
        if not p.alive:
            return self._after_player_out()
        if action=='potion':
            self.say(f'{p.name} heals {p.drink_potion()} HP')
        else:
            if action=='special':
                p.focus-=15; base=self.rng.randint(max(1,p.special-4),p.special+4)
            else:
                p.focus=min(p.max_focus,p.focus+5)
                base=self.rng.randint(max(1,p.attack-2),p.attack+2)
            enemy_parry=self.parry.resolve(self.enemy,difficulty=self.difficulty)
            damage=max(0,self.parry.mitigate(base,enemy_parry)-self.enemy.defense)
            actual=min(self.enemy.health,damage)
            self.enemy.take_damage(actual)
            self.contributions[p.name]+=actual
            self.stage_contributions[p.name]+=actual
            self.say(f'{p.name} uses {action}: {actual} damage ({enemy_parry} enemy parry)')
            if action=='special' and actual and self.rng.randrange(100)<25:
                self.enemy.apply_status('burn',2)
        if not self.enemy.alive:
            self._enemy_defeated(); return True
        for msg in self.enemy.tick_statuses(): self.say(msg)
        if not self.enemy.alive:
            self._enemy_defeated(); return True
        target=self.rng.choice([person for person in self.participants if person.alive])
        power,cue=self.enemy.attack_cue(self.rng)
        now=self.clock()
        # Reaction target is 0.55s after telegraph, normalized by difficulty.
        factor={'rookie':1.3,'adventurer':1.,'dungeon master':.7}[self.difficulty]
        normal=.23*factor
        perfect=.075*factor
        self.pending={'target':target,'power':power,'cue':cue,'telegraph':now,
                      'impact':now+.55,'deadline':now+.55+normal,
                      'normal':normal,'perfect':perfect}
        self.say(f'{self.enemy.name} prepares {cue} against {target.name}!')
        return True

    def parry_attack(self, pressed_at:float | None, randomized: bool = False):
        """Resolve a defensive parry; terminal play uses RNG."""
        if self.result or self.pending is None: return None
        if self.clock()>=self.deadline:
            self.finish(False,'room timeout'); return None
        attack=self.pending
        self.pending=None
        if randomized:
            # Terminal play uses probability based on parry stats and difficulty.
            outcome=self.parry.resolve(attack['target'],difficulty=self.difficulty)
        else:
            difference=abs(pressed_at-attack['impact']) if pressed_at is not None else float('inf')
            if difference<=attack['perfect']: outcome='perfect'
            elif difference<=attack['normal']: outcome='normal'
            else: outcome='missed'
        raw=self.parry.mitigate(attack['power'],outcome)
        damage=max(0,raw-attack['target'].defense)
        attack['target'].take_damage(damage)
        self.say(f'{attack["target"].name} {outcome} parry: {damage} damage taken')
        if outcome=='perfect':
            player=attack['target']
            counter=min(5,self.enemy.health)
            self.enemy.take_damage(counter)
            self.contributions[player.name]+=counter
            self.stage_contributions[player.name]+=counter
            player.focus=min(player.max_focus,player.focus+5)
            self.say(f'Perfect counterattack! {counter} damage, +5 Focus')
        if not self.enemy.alive:
            self._enemy_defeated()
        elif not any(p.alive for p in self.participants):
            self.finish(False,self.defeat_reason())
        else:
            if not attack['target'].alive and len(self.participants) > 1:
                survivors = ', '.join(p.name for p in self.participants if p.alive)
                self.say(f'{attack["target"].name} is down. {survivors} continues the boss fight!')
            self.turn+=1
        return outcome

    def _after_player_out(self):
        if not any(p.alive for p in self.participants): self.finish(False,self.defeat_reason())
        else: self.turn+=1
        return True

    def _enemy_defeated(self):
        """Grant enemy rewards once, then advance to the next stage."""
        e=self.enemy
        if not e.reward_claimed:
            pool = e.reward
            coins = self.rng.randint(12,22) + (40 if isinstance(e,Boss) else 15 if e.enemy_type=='elite' else 0)
            if len(self.participants)==1:
                splits={self.participants[0].name:pool}; coin_splits={self.participants[0].name:coins}
            else:
                # Equal coins; renown by damage contribution for THIS enemy.
                contrib={p.name:self.stage_contributions[p.name] for p in self.participants}
                total=sum(contrib.values())
                first=self.participants[0].name; second=self.participants[1].name
                first_score=round(pool*contrib[first]/total) if total else pool//2
                splits={first:first_score,second:pool-first_score}
                coin_splits={first:coins//2,second:coins-coins//2}
            for p in self.participants:
                p.score+=splits[p.name];p.coins+=coin_splits[p.name]
                self.renown[p.name]+=splits[p.name];self.coins[p.name]+=coin_splits[p.name]
                if self.stage_contributions[p.name]>0:
                    p.enemies_defeated+=1
                    if isinstance(e,Boss): p.bosses_defeated+=1
            e.reward_claimed=True
            self.say(f'Enemy cleared. Renown {splits}, coins {coin_splits}')
        self.pending=None
        self._advance_stage()

    def finish(self, success, reason):
        if self.result: return self.result
        self.pending=None
        if success and not self.door.completed and not self.door.reward_given:
            # Door score is granted once to entrant, distinct from enemy rewards.
            self.entrant.score+=self.door.score_reward
            self.renown[self.entrant.name]+=self.door.score_reward
            self.door.reward_given=True
            self.door.completed=True
            self.door.completed_by=self.entrant.name
        if not success and self.entrant.name not in self.door.failed_by:
            self.door.failed_by.append(self.entrant.name)
        self.result=RoomResult(success,reason,self.door.name,self.coins.copy(),self.renown.copy(),self.contributions.copy(),self.fate)
        self.say(f'ROOM {"COMPLETE" if success else "FAILED"}: {reason}')
        if self.on_result: self.on_result(self.result)
        return self.result

    def sync_to_team(self, team_stats:dict[str,dict], team_door=None):
        """Copy results into team-owned objects without changing their source files."""
        for p in self.players:
            if p.name in team_stats: p.update_team_stats(team_stats[p.name])
        if team_door is not None:
            team_door.completed = self.door.completed
            team_door.completed_by = self.door.completed_by
            team_door.reward_given = self.door.reward_given
            # Some team doors use None before the first failure.
            team_door.failed_by = list(self.door.failed_by)
        return self.result
