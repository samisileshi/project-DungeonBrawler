# Ibrahim Mian
# Wed, Nov 4, 2026
# 1.0

import time

class Timer :
    def __init__ (self, duration: float = 5.0) -> None :
        self.start = time.time() / 60.0
        self.duration = duration

    def isFinished (self) -> bool :
        if time.time() / 60.0 - self.start > self.duration :
            return True
        return False

if __name__ == "__main__" :
    print("TIMERS DEMO:\n")

    dungeonTimer: Timer = Timer (1.0 / 6.0)
    time.sleep(5)
    print(str(dungeonTimer.isFinished()))
    time.sleep(5)
    print(str(dungeonTimer.isFinished()) + "\n")

    roundTimer: Timer = Timer (1.0 / 6.0)
    time.sleep(5)
    print(str(roundTimer.isFinished()))
    time.sleep(5)
    print(str(roundTimer.isFinished()) + "\n")

    combatTimer: Timer = Timer (1.0 / 6.0)
    time.sleep(5)
    print(str(combatTimer.isFinished()))
    time.sleep(5)
    print(str(combatTimer.isFinished()), end = "")