# Sami's automatic combat entry point and optional command-line settings.

import argparse

# FIXME: you don't need Path, just use the built-in file I/O stuff
#   -Ibrahim
from pathlib import Path
from combat_room import ROOM_SECONDS

TOGGLE_ON = "ENABLE_COMBAT_DEMO = True"
TOGGLE_OFF = "ENABLE_COMBAT_DEMO = False"

def disable_combat_demo() :
    # Turn the opt-in source switch off when the battle returns.
    main_path = Path(__file__).with_name("main.py")
    source = main_path.read_text(encoding = "utf-8")
    lines = source.splitlines(keepends = True)
    for index, line in enumerate(lines) :
        if line.strip() == TOGGLE_ON :
            lines[index] = line.replace(TOGGLE_ON, TOGGLE_OFF, 1)
            main_path.write_text("".join(lines), encoding = "utf-8")

            return True

    return False

def parse_args (argv = None) :
    parser = argparse.ArgumentParser(description = "Sami's automatic terminal battle")
    parser.add_argument("--name", default = "Player 1")
    parser.add_argument("--difficulty", choices = ROOM_SECONDS, default = "adventurer")
    parser.add_argument("--round", dest = "round_number", type = int, default = 1)
    parser.add_argument("--seed", type = int)
    parser.add_argument("--combat-save")
    parser.add_argument("--combat-load")
    parser.add_argument("--result-seconds", type = float, default = 5, help = "Duration of Tkinter results (default 5)")
    parser.add_argument("--no-results-window", action = "store_true", help = "Skip Tkinter popup on headless computers")
    args = parser.parse_args(argv)

    if args.round_number < 1 :
        parser.error("--round must be at least 1")
    if args.result_seconds < 0 :
        parser.error("--result-seconds must be >= 0")

    return args


def run_combat (argv = None, *, door = None, entrant = None, opponent = None, output = print, on_result = None) :
    # Run one automatic encounter, show its result, and return RoomResult.
    from combat_terminal import run_terminal

    args = parse_args(argv)
    result = run_terminal(args, door = door, entrant = entrant, opponent = opponent, output = output, on_result = on_result)

    if not args.no_results_window :
        from combat_results import show_result

        show_result(result, seconds = args.result_seconds)

    return result