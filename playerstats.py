# Written by Wilson Huang
def player_stats(data: dict, action:str , value=None) :

    if len(data) == 0: # If the data dictionary is empty, generate the player stats, if not done like this everytime the function is called, the player stats get reset
        data = { 
            "username":"Hero",
            "hp":100,
            "max_hp":100,
            "attack":15,
            "defense":5,
            "focus":50,
            "coins":0,
            "renown":0,
            "escape_sigil":0,
            "inventory":[],
            "equipment":{"weapon":None,"armor":None},
            "buffs":[],
            "debuffs":[],
            "doors_completed":0,
            "enemies_defeated":0,
            "bosses_defeated":0,
            "minigames_won":0,
            "revivals":1
        }

    # If 
    if action == "modify_hp":
        # Update the hp, min() caps health at max_hp, max() prevents dropping below 0.
        data['hp'] = max(0, min(data['max_hp'], data['hp'] + value)) 

    elif action == "modify_focus":
        # Update the focus, and prevent it from dropping below 0 
        data['focus'] = max(0, data['focus'] + value)

    elif action == "equip_item":
        # Checks if the slot is open 
        slot,item_name = value
        if slot in data['equipment']:
            data['equipment'][slot] = item_name
    elif action == 'increment_stat':
        if value in data and value != 'revivals':
            data[value] += 1

    elif action == 'check_revival':
        if data ['hp'] == 0 and data['revivals'] > 0:
            data['revivals'] -= 1
            data['hp'] = data['max_hp']
            data['revived_last_check'] = True
        else:
            data['revived_last_check'] = False
    return data



player = player_stats({}, "init")
print(f"Start HP: {player['hp']}")  # 100


player_stats(player, "modify_hp", -30)
print(f"After Damage HP: {player['hp']}")  # 70


player_stats(player, "equip_item", ("weapon", "Iron Sword"))
print(f"Weapon: {player['equipment']['weapon']}")  # Iron Sword


player_stats(player, "increment_stat", "enemies_defeated")
print(f"Enemies Defeated: {player['enemies_defeated']}")  # 1
        