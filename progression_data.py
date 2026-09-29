# Written by Wilson Huang
def track_progression_data(data: dict, event: str, value=None):

    # Checks if the dict is empty, if it is then generate the values
    if len(data) == 0:
        data = {
            "doors_completed": 0,
            "enemies_defeated": 0,
            "bosses_defeated": 0,
            "minigames_won": 0,
            "revivals": 1
        }

    if event == "increment":
        if value in data and value != "revivals": # Checks if the value exists in the dict and is not revivals
            data[value] += 1

    elif event == "check_revival": # Checks if the player can be revived
        if value == 0: # Checks if the players health has become 0 
            if data.get("revivals", 0) > 0: # Checks if the player is allowed to revive
                data["revivals"] -= 1 # Uses the revival
                return {"revived": True, "data": data}
            else:
                return {"revived": False, "data": data} # Game over

    return data


game = track_progression_data({}, "")
print(game)
track_progression_data(game, "increment", "enemies_defeated")
print("Enemies Defeated:", game["enemies_defeated"])

player_hp = 0
result = track_progression_data(game, "check_revival", value=player_hp)

print("Revived?", result["revived"])
print("Revivals Remaining:", result["data"]["revivals"])
