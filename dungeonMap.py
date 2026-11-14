# Ibrahim Mian
# Mon, Sep 28, 2026
# 1.0

import argparse
import os
import random

clear_terminal : function = lambda : os.system("cls" if os.name == "nt" else "clear")

legend : dict[str, char] = {"door"            : "D",
                            "maybe door"      : "~",

                            "horizontal wall" : "-",
                            "vertical wall"   : "|",
                            "wall junction"   : "+",

                            "basic enemy"     : "e",
                            "elite enemy"     : "E",
                            "boss"            : "B",

                            "empty"           : " ",
                            "maybe entity"    : "#",

                            "player 1"        : "1",
                            "player 2"        : "2",

                            "chest"           : "C",
                            "looted chest"    : "c",
                            "pvp chest"       : "V",
                            "shop"            : "$",
                            "shrine"          : "*",
                            "trap"            : "!",
                            "mystery"         : "?",
                            "arena"           : "A",
                            "safe zone"       : "S",

                            "null cell"       : "0"}

diff_mods : dict[dict[string, float]] = {"rookie"         : {"min doors"      : 4,
                                                             "extra door roll" : 0.75,

                                                             "shop roll"       : 0.25,
                                                             "pvp chest roll"  : 0.43,
                                                             "shrine roll"     : 0.58,
                                                             "trap roll"       : 0.70,
                                                             "mystery roll"    : 0.75,
                                                             "safe roll"       : 0.87,
                                                             "pvp roll"        : 0.90},

                                         "adventurer"     : {"min doors"       : 5,
                                                             "extra door roll" : 0.70,

                                                             "shop roll"       : 0.30,
                                                             "pvp chest roll"  : 0.42,
                                                             "shrine roll"     : 0.54,
                                                             "trap roll"       : 0.63,
                                                             "mystery roll"    : 0.75,
                                                             "safe roll"       : 0.90,
                                                             "pvp roll"        : 0.915},

                                         "dungeon master" : {"min doors"       : 6,
                                                             "extra door roll" : 0.65,

                                                             "shop roll"       : 0.35,
                                                             "pvp chest roll"  : 0.43,
                                                             "shrine roll"     : 0.53,
                                                             "trap roll"       : 0.59,
                                                             "mystery roll"    : 0.77,
                                                             "safe roll"       : 0.93,
                                                             "pvp roll"        : 0.935}}

dungeon_map : list[str] = ["+-------------------------------+",
                           "|       |       |       |       |",
                           "|   #   ~   #   ~   #   ~   #   |",
                           "|       |       |       |       |",
                           "|---~---+---~---+---~---+---~---|",
                           "|       |       |       |       |",
                           "|   #   ~   1   ~   2   ~   #   |",
                           "|       |       |       |       |",
                           "|---~---+---~---+---~---+---~---|",
                           "|       |       |       |       |",
                           "|   #   ~   #   ~   #   ~   #   |",
                           "|       |       |       |       |",
                           "+-------------------------------+"]

maybe_doors : list[list[int]] = [[2, 8], [2, 16], [2, 24],
                                [4, 4], [4, 12], [4, 20], [4, 28],
                                [6, 8], [6, 16], [6, 24],
                                [8, 4], [8, 12], [8, 20], [8, 28],
                                [10, 8], [10, 16], [10, 24]]
maybe_entities : list[list[int]] = [[2, 4], [2, 12], [2, 20], [2, 28],
                                   [6, 4], [6, 28],
                                   [10, 4], [10, 12], [10, 20], [10, 28]]
maybe_doors_by_room : list[list[list[int]]] = [[[2, 8], [4, 4]],
                                            [[2, 8], [2, 16], [4, 12]],
                                            [[2, 16], [2, 24], [4, 20]],
                                            [[2, 24], [4, 28]],
                                            [[4, 4], [6, 8], [8, 4]],
                                            [[4, 12], [6, 8], [6, 16], [8, 12]],
                                            [[4, 20], [6, 16], [6, 24], [8, 20]],
                                            [[4, 28], [6, 24], [8, 28]],
                                            [[8, 4], [10, 8]],
                                            [[8, 12], [10, 8], [10, 16]],
                                            [[8, 20], [10, 16], [10, 24]],
                                            [[8, 28], [10, 24]]]

def get_cell(coords : list[int] = [0, 0]) -> char :
    if len(coords) != 2 :
        coords = [0, 0]
    return dungeon_map[coords[0]][coords[1]]

def set_cell(coords : list[int] = [0, 0], new_cell : char = legend.get("null cell")) -> None :
    if len(coords) != 2 :
        coords = [0, 0]
    dungeon_map[coords[0]] = dungeon_map[coords[0]][0:coords[1]] + new_cell + dungeon_map[coords[0]][coords[1] + 1:len(dungeon_map[coords[0]])]

def generate_map() -> None :
    all_rooms_connected : bool = False
    extra_door_roll : float = diff_mods.get(diff).get("extra door roll")
    shop_roll : float = diff_mods.get(diff).get("shop roll")
    pvp_chest_roll : float = diff_mods.get(diff).get("pvp chest roll")
    shrine_roll : float = diff_mods.get(diff).get("shrine roll")
    trap_roll : float = diff_mods.get(diff).get("trap roll")
    mystery_roll : float = diff_mods.get(diff).get("mystery roll")
    safe_roll : float = diff_mods.get(diff).get("safe roll")
    pvp_roll : float = diff_mods.get(diff).get("pvp roll")

    # this checks if each room has at least one door
    while not all_rooms_connected :
        doors_left : int = diff_mods.get(diff).get("min doors")
        for door in maybe_doors :
            set_cell(door, legend.get("maybe door"))

        # generating the minimum number of doors
        while doors_left > 0 :
            door : list[int] = random.choice(maybe_doors)
            if get_cell(door) is legend.get("maybe door") :
                set_cell(door, legend.get("door"))
                doors_left -= 1

        # rolling for extra doors
        for door in maybe_doors :
            if get_cell(door) is legend.get("maybe door") :
                if (1.00 - random.random()) >= extra_door_roll :
                    set_cell(door, legend.get("door"))
                elif door[0] % 4 == 0 :
                    set_cell(door, legend.get("horizontal wall"))
                else :
                    set_cell(door, legend.get("vertical wall"))

        room_queue : list[int] = [0]
        already_visited : list[int] = []
        while len(room_queue) > 0 :
            room : list[int] = maybe_entities[room_queue[0]]
            if get_cell([room[0] - 2, room[1]]) is legend.get("door") and room_queue[0] - 4 not in already_visited :
                room_queue.append(room_queue[0] - 4)
            if get_cell([room[0], room[1] + 4]) is legend.get("door") and room_queue[0] + 1 not in already_visited :
                room_queue.append(room_queue[0] + 1)
            if get_cell([room[0] + 2, room[1]]) is legend.get("door") and room_queue[0] + 4 not in already_visited :
                room_queue.append(room_queue[0] + 4)
            if get_cell([room[0], room[1] - 4]) is legend.get("door") and room_queue[0] - 1 not in already_visited :
                room_queue.append(room_queue[0] - 1)

            already_visited.append(room_queue.pop(0))
        all_rooms_connected = (len(already_visited) == 12)

        # rolling for entity spawns
    for entity in maybe_entities :
        entity_roll : float = (1.00 - random.random())
        if entity_roll >= pvp_roll :
            set_cell(entity, legend.get("arena"))
        elif entity_roll >= safe_roll :
            set_cell(entity, legend.get("safe zone"))
        elif entity_roll >= mystery_roll :
            set_cell(entity, legend.get("mystery"))
        elif entity_roll >= trap_roll :
            set_cell(entity, legend.get("trap"))
        elif entity_roll >= shrine_roll :
            set_cell(entity, legend.get("shrine"))
        elif entity_roll >= pvp_chest_roll :
            set_cell(entity, legend.get("pvp chest"))
        elif entity_roll >= shop_roll :
            set_cell(entity, legend.get("shop"))
        else :
            set_cell(entity, legend.get("empty"))

def display_map() -> None :
    print("\n".join(dungeon_map), end = "", flush = True)

def print_roomDemo() -> None :
    print("Enemy in room: \"" + random.choice(["A foe", "A fearsome foe", "An ominous figure"]) + " charges from the gloom!\"")
    print("Chest in room: \"There is a chest in the room. Probably not a mimic.\"")
    print("Looted chest in room: \"Wasn't a mimic.\"")
    print("Door in room (after encounter/loot): \"A door leads " + random.choice(["north", "east", "south", "west"]) + ".\"")
    print("Other player in room: \"Oh... it's *that one*.\"", end = "", flush = True)

if __name__ == "__main__" :
    clear_terminal()
    print("MAP GEN DEMO:\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--diff", dest = "diff", type = str, default = None, help = "The difficulty decides which set of modifiers are applied to generation.")
    args = parser.parse_args()
    diff : str = args.diff

    while diff not in diff_mods :
        print("Enter a difficulty: \"Rookie\", \"Adventurer\", or \"Dungeon Master\".")
        diff = input("> ").strip().lower()
        clear_terminal()

        if diff not in diff_mods :
            print("Error. ", end = "", flush = True)

    clear_terminal()
    generate_map()
    display_map()