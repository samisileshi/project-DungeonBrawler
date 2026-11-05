# Ibrahim Mian
# Mon, Sep 28, 2026
# 1.0

import random

legend: dict = {"door"           : 'D',
                "maybeDoor"      : '~',

                "wallHorizontal" : '-',
                "wallVertical"   : '|',
                "wallJunction"   : '+',

                "basicEnemy"     : 'e',
                "eliteEnemy"     : 'E',
                "boss"           : 'B',

                "empty"          : ' ',
                "maybeEntity"    : '#',

                "player1"        : '1',
                "player2"        : '2',

                "chest"          : 'C',
                "lootedChest"    : 'c',
                "pvpChest"       : 'V',
                "shop"           : '$',
                "shrine"         : '*',
                "trap"           : '!',
                "mystery"        : '?',
                "arena"          : 'A',
                "safeZone"       : 'S',

                "nullCell"       : '0'}

diffMods: dict = {"rookie"         : {"minDoors"      : 4,
                                      "extraDoorRoll" : 0.25,

                                      "shopRoll"      : 0.18,
                                      "pvpChestRoll"  : 0.33,
                                      "shrineRoll"    : 0.45,
                                      "trapRoll"      : 0.50,
                                      "mysteryRoll"   : 0.62,
                                      "safeRoll"      : 0.65,
                                      "pvpRoll"       : 0.75},

                  "adventurer"     : {"minDoors"      : 5,
                                      "extraDoorRoll" : 0.30,

                                      "shopRoll"      : 0.12,
                                      "pvpChestRoll"  : 0.24,
                                      "shrineRoll"    : 0.33,
                                      "trapRoll"      : 0.45,
                                      "mysteryRoll"   : 0.60,
                                      "safeRoll"      : 0.615,
                                      "pvpRoll"       : 0.70},

                  "dungeon master" : {"minDoors"      : 6,
                                      "extraDoorRoll" : 0.35,

                                      "shopRoll"      : 0.08,
                                      "pvpChestRoll"  : 0.18,
                                      "shrineRoll"    : 0.24,
                                      "trapRoll"      : 0.42,
                                      "mysteryRoll"   : 0.58,
                                      "safeRoll"      : 0.585,
                                      "pvpRoll"       : 0.65}}

dungeonMap: list[str] = ["+-------------------------------+",
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

maybeDoors: list[list[int]] = [[2, 8], [2, 16], [2, 24],
                               [4, 4], [4, 12], [4, 20], [4, 28],
                               [6, 8], [6, 16], [6, 24],
                               [8, 4], [8, 12], [8, 20], [8, 28],
                               [10, 8], [10, 16], [10, 24]]
maybeEntities: list[list[int]] = [[2, 4], [2, 12], [2, 20], [2, 28],
                                  [6, 4], [6, 28],
                                  [10, 4], [10, 12], [10, 20], [10, 28]]
maybeDoorsByRoom: list[list[list[int]]] = [[[2, 8], [4, 4]],
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

def getCell(coords: list[int] = [0, 0]) -> char :
    return dungeonMap[coords[0]][coords[1]]

def setCell(coords: list[int] = [0, 0], newCell: char = legend.get("nullCell")) -> None :
    dungeonMap[coords[0]] = dungeonMap[coords[0]][:coords[1]] + newCell + dungeonMap[coords[0]][coords[1] + 1:]

def generateMap(diff: str = "adventurer") -> None :
    diff = diff.lower()
    if diff not in diffMods :
        diff = "adventurer"
    allRoomsConnected: bool = False
    extraDoorRoll: float = diffMods.get(diff).get("extraDoorRoll")
    shopRoll: float = diffMods.get(diff).get("shopRoll")
    pvpChestRoll: float = diffMods.get(diff).get("pvpChestRoll")
    shrineRoll: float = diffMods.get(diff).get("shrineRoll")
    trapRoll: float = diffMods.get(diff).get("trapRoll")
    mysteryRoll: float = diffMods.get(diff).get("mysteryRoll")
    safeRoll: float = diffMods.get(diff).get("safeRoll")
    pvpRoll: float = diffMods.get(diff).get("pvpRoll")

    # this checks if each room has at least one door
    while not allRoomsConnected :
        doorsLeft: int = diffMods.get(diff).get("minDoors")
        for door in maybeDoors :
            setCell(door, legend.get("maybeDoor"))

        # generating the minimum number of doors
        while doorsLeft > 0 :
            door: list[int] = random.choice(maybeDoors)
            if getCell(door) is legend.get("maybeDoor") :
                setCell(door, legend.get("door"))
                doorsLeft -= 1

        # rolling for extra doors
        for door in maybeDoors :
            if getCell(door) is legend.get("maybeDoor") :
                if (1.00 - random.random()) >= extraDoorRoll :
                    setCell(door, legend.get("door"))
                elif door[0] % 4 == 0 :
                    setCell(door, legend.get("wallHorizontal"))
                else :
                    setCell(door, legend.get("wallVertical"))

        roomQueue: list[int] = [0]
        alreadyVisited: list[int] = []
        while len(roomQueue) > 0 :
            room: list[int] = maybeEntities[roomQueue[0]]
            if getCell([room[0] - 2, room[1]]) is legend.get("door") and roomQueue[0] - 4 not in alreadyVisited :
                roomQueue.append(roomQueue[0] - 4)
            if getCell([room[0], room[1] + 4]) is legend.get("door") and roomQueue[0] + 1 not in alreadyVisited :
                roomQueue.append(roomQueue[0] + 1)
            if getCell([room[0] + 2, room[1]]) is legend.get("door") and roomQueue[0] + 4 not in alreadyVisited :
                roomQueue.append(roomQueue[0] + 4)
            if getCell([room[0], room[1] - 4]) is legend.get("door") and roomQueue[0] - 1 not in alreadyVisited :
                roomQueue.append(roomQueue[0] - 1)

            alreadyVisited.append(roomQueue.pop(0))
        allRoomsConnected = (len(alreadyVisited) == 12) 

    # rolling for entity spawns
    for entity in maybeEntities :
        entityRoll: float = (1.00 - random.random())
        if entityRoll >= pvpRoll :
            setCell(entity, legend.get("arena"))
        elif entityRoll >= safeRoll :
            setCell(entity, legend.get("safeZone"))
        elif entityRoll >= mysteryRoll :
            setCell(entity, legend.get("mystery"))
        elif entityRoll >= trapRoll :
            setCell(entity, legend.get("trap"))
        elif entityRoll >= shrineRoll :
            setCell(entity, legend.get("shrine"))
        elif entityRoll >= pvpChestRoll :
            setCell(entity, legend.get("pvpChest"))
        elif entityRoll >= shopRoll :
            setCell(entity, legend.get("shop"))
        else :
            setCell(entity, legend.get("empty"))

def displayMap() -> None :
    print("\n".join(dungeonMap), end = "")

def printRoomDemo() -> None :
    print("Enemy in room: \"" + random.choice(["A foe", "A fearsome foe", "An ominous figure"]) + " charges from the gloom!\"")
    print("Chest in room: \"There is a chest in the room. Probably not a mimic.\"")
    print("Looted chest in room: \"Wasn't a mimic.\"")
    print("Door in room (after encounter/loot): \"A door leads " + random.choice(["north", "east", "south", "west"]) + ".\"")
    print("Other player in room: \"Oh... it's *that one*.\"", end = "")

if __name__ == "__main__" :
    print("MAP GEN DEMO:\n")
    diff: str = None

    while diff not in diffMods :
        print("Enter a difficulty: \"Rookie\", \"Adventurer\", or \"Dungeon Master\".")
        diff = input("> ").strip().lower()
        print()

        if diff not in diffMods :
            print("Error. ", end = "")

    generateMap(diff)
    displayMap()