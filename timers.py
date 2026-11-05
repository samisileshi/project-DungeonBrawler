# Ibrahim Mian
# Wed, Nov 4, 2026
# 1.0

# Todo: round timer, combat timer, overall timer

import time

dungeonStartTime: float
dungeonDuration: float

roundStartTime: float
roundDuration: float

combatStartTime: float
combatDuration: float

def dungeonStart (duration: float = 5.0) -> None :
    global dungeonStartTime
    global dungeonDuration
    dungeonStartTime = time.time() / 60.0
    dungeonDuration = duration

def isDungeonFinished() -> bool :
    if time.time() / 60.0 - dungeonStartTime > dungeonDuration :
        return True
    return False

def roundStart (duration: float = 5.0) -> None :
    global roundStartTime
    global roundDuration
    roundStartTime = time.time() / 60.0
    roundDuration = duration

def isRoundFinished() -> bool :
    if time.time() / 60.0 - roundStartTime > roundDuration :
        return True
    return False

def combatStart (duration: float = 5.0) -> None :
    global combatStartTime
    global combatDuration
    combatStartTime = time.time() / 60.0
    combatDuration = duration

def isCombatFinished() -> bool :
    if time.time() / 60.0 - combatStartTime > combatDuration :
        return True
    return False

if __name__ == "__main__" :
    print("TIMERS DEMO:\n")

    dungeonStart(1.0 / 6.0)
    time.sleep(5)
    print(str(isDungeonFinished()))
    time.sleep(5)
    print(str(isDungeonFinished()) + "\n")

    roundStart(1.0 / 6.0)
    time.sleep(5)
    print(str(isRoundFinished()))
    time.sleep(5)
    print(str(isRoundFinished()) + "\n")

    combatStart(1.0 / 6.0)
    time.sleep(5)
    print(str(isCombatFinished()))
    time.sleep(5)
    print(str(isCombatFinished()), end = "")