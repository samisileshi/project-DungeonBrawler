# Ibrahim Mian
# Wed, Nov 4, 2026
# 1.0

import os
import time

clearTerminal : function = lambda : os.system("cls" if os.name == "nt" else "clear")

class Timer :
    def __init__(self, duration: float = 5.0) -> None :
        self.start = time.time() / 60.0
        self.duration = duration

    def isFinished(self) -> bool :
        if time.time() / 60.0 - self.start > self.duration :
            return True
        return False

    def isFinishedStr(self) -> str :
        return "Timer is" + (" " if self.isFinished() else " not ") + "finished."

if __name__ == "__main__" :
    clearTerminal()
    print("TIMERS DEMO:\n")

    dungeonTimer: Timer = Timer (1.0 / 6.0)
    print("Dungeon Timer: 10 s")
    time.sleep(5)
    print(dungeonTimer.isFinishedStr())
    time.sleep(5)
    print(dungeonTimer.isFinishedStr(), end = "", flush = True)
    time.sleep(1)

    clearTerminal()
    roundTimer: Timer = Timer (1.0 / 6.0)
    print("Round Timer: 10 s")
    time.sleep(5)
    print(roundTimer.isFinishedStr())
    time.sleep(5)
    print(roundTimer.isFinishedStr(), end = "", flush = True)
    time.sleep(1)

    clearTerminal()
    combatTimer: Timer = Timer (1.0 / 6.0)
    print("Combat Timer: 10 s")
    time.sleep(5)
    print(combatTimer.isFinishedStr())
    time.sleep(5)
    print(combatTimer.isFinishedStr(), end = "", flush = True)