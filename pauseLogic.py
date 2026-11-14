# Ibrahim Mian
# Mon, Sep 28, 2026
# 1.0

from inventory import display_equipment_and_inventory
import os
from playerstats import Player
import time
import tkinter

clear_terminal : function = lambda : os.system("cls" if os.name == "nt" else "clear")

def pause(pausing_player : Player = Player("Pausing player"), other_player : Player = Player("Other player")) -> None :
    print(pausing_player.username, "needs a break. What about you,", other_player.username + "? (Yes/No)")
    answer : str = input("> ").strip().lower()
    clear_terminal()

    while not (answer == "yes" or answer == "no") :
        print("Error. Enter either \"Yes\" or \"No\", case insensitive.")
        answer = input("> ").strip().lower()
        clear_terminal()

    if answer == "yes" :
        print(other_player.username, "agrees to take a break.", end = "", flush = True)
        time.sleep(1)

        pause_menu: Tk = tkinter.Tk()
        pause_menu.title("Dungeon Brawler Pause _menu")
        pause_menu.geometry("150x175")
        pause_message: Label = tkinter.Label(pause_menu, text = f"{pausing_player.username} has paused.")
        pause_message.pack(pady = 10)

        def resume() -> None :
            clear_terminal()
            pause_menu.destroy()
            print(pausing_player.username, "has resumed.", end = "", flush = True)

        def display_inventory() -> None :
            clear_terminal()
            display_equipment_and_inventory(inventory, equipment)
            print("\b", end = "", flush = True)

        def display_stats() -> None :
            clear_terminal()
            pausing_player.display_stats()
            print("\b", end = "", flush = True)

        def settings() -> None :
            clear_terminal()
            print("WIP", end = "", flush = True)

        def quit_game() -> None :
            clear_terminal()
            quit()

        resume_button : Button = tkinter.Button(pause_menu, text = "Resume", command = resume)
        resume_button.pack()
        inventory_button : Button = tkinter.Button(pause_menu, text = "Inventory", command = display_inventory)
        inventory_button.pack()
        stats_button : Button = tkinter.Button(pause_menu, text = "Stats", command = display_stats)
        stats_button.pack()
        options_button : Button = tkinter.Button(pause_menu, text = "Options", command = settings)
        options_button.pack()
        quit_button : Button = tkinter.Button(pause_menu, text = "Quit", command = quit_game)
        quit_button.pack()

        pause_menu.deiconify()
        pause_menu.resizable(True, True)
        pause_menu.lift()
        pause_menu.attributes("-topmost", True)
        pause_menu.attributes("-topmost", False)
        pause_menu.focus_force()
        pause_menu.mainloop()
    else :
        print(other_player.username, "doesn't want to take a break.", end = "", flush = True)

if __name__ == "__main__" :
    clear_terminal()
    print("PAUSE DEMO:\n")

    inventory : list[dict[str, str]] = [{"name"   : "Steel Plate",
                                         "type"   : "armor",
                                         "rarity" : "Rare"}]
    equipment : dict = {"Weapon" : {"name"   : "Iron Sword",
                                    "type"   : "weapon",
                                    "rarity" : "Common"},
                        "Armor"  : None}

    print("Pausing Player:")
    pausing_player : Player = Player(input("> ").strip())
    clear_terminal()

    print("Other Player:")
    other_player : Player = Player(input("> ").strip())
    clear_terminal()

    pause(pausing_player, other_player)