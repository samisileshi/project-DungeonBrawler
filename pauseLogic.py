# Ibrahim Mian
# Mon, Sep 28, 2026
# 1.0

from inventory import display_equipment_and_inventory
import os
from playerstats import Player
import time
import tkinter

clearTerminal : function = lambda : os.system("cls" if os.name == "nt" else "clear")

def pause(pausingPlayer : Player = Player("pausingPlayer"), otherPlayer : Player = Player("otherPlayer")) -> None :
    print(pausingPlayer.username + " needs a break. What about you, " + otherPlayer.username + "? (Yes/No)")
    answer : str = input("> ").strip().lower()
    clearTerminal()

    while not (answer == "yes" or answer == "no") :
        print("Error. Enter either \"Yes\" or \"No\", case insensitive.")
        answer = input("> ").strip().lower()
        clearTerminal()

    if answer == "yes" :
        print(otherPlayer.username + " agrees to take a break.", end = "", flush = True)
        time.sleep(1)

        pauseMenu: Tk = tkinter.Tk()
        pauseMenu.title("Dungeon Brawler Pause Menu")
        pauseMenu.geometry("150x175")
        pauseMessage: Label = tkinter.Label(pauseMenu, text = pausingPlayer.username + " has paused.")
        pauseMessage.pack(pady = 10)

        def resume() -> None :
            clearTerminal()
            pauseMenu.destroy()
            print(pausingPlayer.username + " has resumed.", end = "", flush = True)

        def displayInventory() -> None :
            clearTerminal()
            display_equipment_and_inventory(inventory, equipment)
            print("\b", end = "", flush = True)

        def displayStats() -> None :
            clearTerminal()
            pausingPlayer.display_stats()
            print("\b", end = "", flush = True)

        def settings() -> None :
            clearTerminal()
            print("WIP", end = "", flush = True)

        def quitGame() -> None :
            clearTerminal()
            quit()

        resumeButton: Button = tkinter.Button(pauseMenu, text = "Resume", command = resume)
        resumeButton.pack()
        inventoryButton: Button = tkinter.Button(pauseMenu, text = "Inventory", command = displayInventory)
        inventoryButton.pack()
        statsButton: Button = tkinter.Button(pauseMenu, text = "Stats", command = displayStats)
        statsButton.pack()
        optionsButton: Button = tkinter.Button(pauseMenu, text = "Options", command = settings)
        optionsButton.pack()
        quitButton: Button = tkinter.Button(pauseMenu, text = "Quit", command = quitGame)
        quitButton.pack()

        pauseMenu.deiconify()
        pauseMenu.resizable(True, True)
        pauseMenu.lift()
        pauseMenu.attributes("-topmost", True)
        pauseMenu.attributes("-topmost", False)
        pauseMenu.focus_force()
        pauseMenu.mainloop()
    else :
        print(otherPlayer.username + " doesn't want to take a break.", end = "", flush = True)

if __name__ == "__main__" :
    clearTerminal()
    print("PAUSE DEMO:\n")

    inventory : list[dict] = [{"name"   : "Steel Plate",
                               "type"   : "armor",
                               "rarity" : "Rare"}]
    equipment : dict = {"Weapon" : {"name"   : "Iron Sword",
                                    "type"   : "weapon",
                                    "rarity" : "Common"},
                        "Armor"  : None}

    print("Pausing Player:")
    pausingPlayer : Player = Player(input("> ").strip())
    clearTerminal()

    print("Other Player:")
    otherPlayer : Player = Player(input("> ").strip())
    clearTerminal()

    pause(pausingPlayer, otherPlayer)