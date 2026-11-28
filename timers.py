# Ibrahim Mian
# Wed, Nov 4, 2026
# 1.0

import os
import time

clear_terminal : function = lambda : os.system("cls" if os.name == "nt" else "clear")

class Timer :
    def __init__ (self, duration: float = 5.0) -> None :
        self.start = time.time() / 60.0
        self.duration = duration

    def is_finished(self) -> bool :
        if time.time() / 60.0 - self.start > self.duration :
            return True
        return False

    def is_finished_str(self) -> str :
        return "Timer is" + (" " if self.is_finished() else " not ") + "finished."

if __name__ == "__main__" :
    clear_terminal()
    print("TIMERS DEMO:\n")

    dungeon_timer : Timer = Timer(1.0 / 6.0)
    print("Dungeon Timer: 10 s")
    time.sleep(5)
    print(dungeon_timer.is_finished_str())
    time.sleep(5)
    print(dungeon_timer.is_finished_str(), end = "", flush = True)
    time.sleep(1)

    clear_terminal()
    round_timer : Timer = Timer(1.0 / 6.0)
    print("Round Timer: 10 s")
    time.sleep(5)
    print(round_timer.is_finished_str())
    time.sleep(5)
    print(round_timer.is_finished_str(), end = "", flush = True)
    time.sleep(1)

    clear_terminal()
    combat_timer : Timer = Timer(1.0 / 6.0)
    print("Combat Timer: 10 s")
    time.sleep(5)
    print(combat_timer.is_finished_str())
    time.sleep(5)
    print(combat_timer.is_finished_str(), end = "", flush = True)