# Sami"s automatic text battle. The team can call this without input prompts.

import json
import random
from dataclasses import asdict

# FIXME: you don"t need Path, just use the built-in file I/O stuff
#   -Ibrahim
from pathlib import Path

from combat_doors import DEMO_DOORS
from combat_entities import CombatPlayer
from combat_room import CombatDoor, RoomCombat


def run_terminal(args, *, door = None, entrant = None, opponent = None, output = print, on_result = None) :
    # Run one complete RNG battle and return its RoomResult to the caller.

    #   When the team supplies a door or players, use those rather than demo data.
    #   No input() calls are made here: both actions and parries are simulated.
    # FIXME: just use random.<whatever method> instead of creating a Random object
    #   -Ibrahim
    rng = random.Random(args.seed)
    entrant = entrant or CombatPlayer(args.name, 100, 15, 3, parry_chance = 35)
    opponent = opponent or CombatPlayer("Player 2" if entrant.name != "Player 2" else "Player 1", 100, 15, 3, parry_chance = 35)

    if args.combat_load and entrant is not None :
        saved = json.loads(Path(args.combat_load).read_text(encoding = "utf-8"))

        if saved.get("format") != "roomcombat-players-v1" :
            raise ValueError("Invalid combat save file")

        entrant = CombatPlayer(**saved["entrant"])
        opponent = CombatPlayer(**saved["opponent"])

    if door is None :
        # Demo battle: randomly pick a combat door, not a library/shop room.
        data = rng.choice([item for item in DEMO_DOORS if item["stages"]])
        door = CombatDoor.from_data(data)
    elif isinstance(door, dict) :
        door = CombatDoor.from_data(door)
    elif not isinstance(door, CombatDoor) :
        door = CombatDoor.from_team_door(door)

    room = RoomCombat(door, entrant, opponent, difficulty = args.difficulty, round_number = args.round_number, rng = rng, on_result = on_result)
    output(f"=== Sami combat:", door.name, "===")
    shown = 0
    turns = 0

    while room.result is None :
        room.check_timeout()

        for message in room.messages[shown:] :
            output(message)

        shown = len(room.messages)

        if room.result :
            break

        if room.pending :
            # Terminal parries use chance-based outcomes rather than input timing.
            room.parry_attack(None, randomized = True)
            continue

        actor = room.current_player

        if actor is None :
            room.finish(False, room.defeat_reason())
            continue

        # Skills when affordable; otherwise use normal attacks. Heal when low.
        if actor.health <= actor.max_health // 3 and actor.potions :
            action = "potion"
        elif actor.focus >= 15 and rng.random() < .45 :
            action = "special"
        else :
            action = "attack"

        output(actor.name, f"({actor.health} HP) chooses", action + ".")
        room.action(action)
        turns += 1

        # Guard against a battle with zero damage lasting indefinitely.
        if turns >= 1000 and room.result is None :
            room.finish(False, "automatic turn safety limit")

    for message in room.messages[shown:] :
        output(message)

    result = room.result
    output("BATTLE RESULT:", "Victory" if result.success else "Defeat", "—", result.reason)
    output(f"Renown: {result.renown} | Coins: {result.coins}", end = "", flush = True)

    if args.combat_save :
        snapshot = {"format"   : "roomcombat-players-v1",
                    "entrant"  : asdict(entrant),
                    "opponent" : asdict(opponent)}
        Path(args.combat_save).write_text(json.dumps(snapshot, indent = 2), encoding = "utf-8")

    return result