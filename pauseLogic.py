# Ibrahim Mian
# Mon, Sep 28, 2026
# 1.0

import time
import tkinter
from playerstats import Player
from inventory import display_equipment_and_inventory

inventory: list[dict] = [{"name"   : "Steel Plate",
                          "type"   : "armor",
                          "rarity" : "Rare"}]
equipment: dict = {"Weapon" : {"name"   : "Iron Sword",
                               "type"   : "weapon",
                               "rarity" : "Common"},
                   "Armor"  : None}

def pause(pausingPlayer: Player = Player("pausingPlayer"), otherPlayer: Player = Player("otherPlayer")) -> None :
    print(pausingPlayer.username + " needs a break. What about you, " + otherPlayer.username + "? (Yes/No)")
    answer: str = input("> ").strip().lower()

    while not (answer == "yes" or answer == "no") :
        print("\nError. Enter either \"Yes\" or \"No\", case insensitive.")
        answer = input("> ").strip().lower()

    if answer == "yes" :
        print("\n" + otherPlayer.username + " agrees to take a break.", end = "")
        time.sleep(1)

        pauseMenu: Tk = tkinter.Tk()
        pauseMenu.title("Dungeon Brawler Pause Menu")
        pauseMenu.geometry("150x175")
        pauseMessage: Label = tkinter.Label(pauseMenu, text = pausingPlayer.username + " has paused.")
        pauseMessage.pack(pady = 10)

        resumeButton: Button = tkinter.Button(pauseMenu, text = "Resume", command = pauseMenu.destroy)
        resumeButton.pack()
        inventoryButton: Button = tkinter.Button(pauseMenu, text = "Inventory", command = lambda : (print(), display_equipment_and_inventory(inventory, equipment), print("\b", end = "")))
        inventoryButton.pack()
        statsButton: Button = tkinter.Button(pauseMenu, text = "Stats", command = lambda : (print(), pausingPlayer.display_stats(), print("\b", end = "")))
        statsButton.pack()
        optionsButton: Button = tkinter.Button(pauseMenu, text = "Options", command = lambda : print("\n\nWIP", end = ""))
        optionsButton.pack()
        quitButton: Button = tkinter.Button(pauseMenu, text = "Quit", command = quit)
        quitButton.pack()

        pauseMenu.deiconify()
        pauseMenu.lift()
        pauseMenu.attributes("-topmost", True)
        pauseMenu.attributes("-topmost", False)
        pauseMenu.focus_force()
        pauseMenu.mainloop()

        print("\n\n" + pausingPlayer.username + " has resumed.")
    else :
        print("\n" + otherPlayer.username + " doesn't want to take a break.")

    if __name__ == "__main__" :
        print("\b", end = "")

if __name__ == "__main__" :
    print("PAUSE DEMO:\n")

    print("Pausing Player:")
    pausingPlayer: Player = Player(input("> ").strip())
    print("Other Player:")
    otherPlayer: Player = Player(input("> ").strip())
    print()

    pause(pausingPlayer, otherPlayer)