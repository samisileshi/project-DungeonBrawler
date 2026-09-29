"""

F9  Core Combat System
F10 Parry System
F11 Enemies and Elite Enemies
F12 Boss System

"""

import random



# F11/F12: enemy definitions

NORMAL_ENEMIES = [
    {"name": "Goblin", "health": 45, "attack": 9, "parry_chance": 15, "special_chance": 10, "reward": 25},
    {"name": "Skeleton", "health": 55, "attack": 11, "parry_chance": 20, "special_chance": 12, "reward": 25},
    {"name": "Dungeon Rat", "health": 35, "attack": 8, "parry_chance": 8, "special_chance": 8, "reward": 25},
]

ELITE_ENEMIES = [
    {"name": "Elite Knight", "health": 85, "attack": 16, "parry_chance": 30, "special_chance": 20, "reward": 60},
    {"name": "Elite Orc", "health": 95, "attack": 18, "parry_chance": 20, "special_chance": 25, "reward": 60},
]

BOSSES = [
    {"name": "Dungeon Warden", "health": 160, "attack": 23, "parry_chance": 25, "special_chance": 35, "reward": 100},
    {"name": "Ash Dragon", "health": 190, "attack": 26, "parry_chance": 18, "special_chance": 40, "reward": 100},
]

DIFFICULTY_MULTIPLIERS = {
    "rookie": 0.85,
    "adventurer": 1.00,
    "dungeon master": 1.20,
}


def create_player(name):
    """Create simple player combat data for the terminal prototype. Later into class"""
    return {
        "name": name,
        "health": 100,
        "max_health": 100,
        "attack": 15,
        "defense": 3,
        "speed": 10,
        "special": 28,
        "parry_chance": 35,
        "perfect_parry_chance": 25,
        "potions": 2,
        "coins": 0,
        "score": 0,
    }


def create_enemy(round_number=1, difficulty="adventurer", enemy_type="normal"):
    """Create a normal, elite, or boss enemy scaled by round and difficulty."""
    difficulty = difficulty.lower()
    multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty, 1.00)
    round_multiplier = 1 + max(0, round_number - 1) * 0.08

    if enemy_type == "elite":
        template = random.choice(ELITE_ENEMIES)
    elif enemy_type == "boss":
        template = random.choice(BOSSES)
    else:
        template = random.choice(NORMAL_ENEMIES)
        enemy_type = "normal"

    enemy = template.copy()
    enemy["type"] = enemy_type
    enemy["max_health"] = max(1, int(enemy["health"] * multiplier * round_multiplier))
    enemy["health"] = enemy["max_health"]
    enemy["attack"] = max(1, int(enemy["attack"] * multiplier * round_multiplier))
    return enemy



# F10: parry system

def try_parry(parry_chance, perfect_parry_chance=20):
    """Return perfect or partial  or failed from percentage chances."""
    parry_roll = random.randint(1, 100)

    if parry_roll > parry_chance:
        return "failed"

    perfect_roll = random.randint(1, 100)
    if perfect_roll <= perfect_parry_chance:
        return "perfect"

    return "partial"


def damage_after_parry(raw_damage, parry_result):
    """Apply the result of a parry to incoming damage."""
    if parry_result == "perfect":
        return 0

    if parry_result == "partial":
        # A non-perfect parry blocks a random 35%-65% of damage.
        damage_multiplier = random.uniform(0.35, 0.65)
        return max(0, int(raw_damage * damage_multiplier))

    return raw_damage


def enemy_parry(enemy, incoming_damage):
    """Allow an enemy to parry a player's attack."""
    parry_result = try_parry(enemy["parry_chance"], 15)
    final_damage = damage_after_parry(incoming_damage, parry_result)
    return parry_result, final_damage


# -----------------------------
# F9: core combat actions
# -----------------------------
def calculate_player_damage(player, action):
    """Calculate damage for a normal or special player attack."""
    if action == "special":
        # Special attacks vary slightly so every hit is not identical.
        return random.randint(player["special"] - 4, player["special"] + 4)

    return random.randint(player["attack"] - 2, player["attack"] + 2)


def player_attack(player, enemy, action="attack"):
    """Resolve one player attack, including the enemy's parry chance."""
    raw_damage = calculate_player_damage(player, action)
    parry_result, final_damage = enemy_parry(enemy, raw_damage)
    enemy["health"] = max(0, enemy["health"] - final_damage)

    if parry_result == "perfect":
        print(enemy["name"] + " PERFECT PARRIED the attack. No damage taken!")
    elif parry_result == "partial":
        print(enemy["name"] + " parried part of the attack.")

    print(player["name"] + " dealt " + str(final_damage) + " damage to " + enemy["name"] + ".")
    return final_damage


def enemy_attack(player, enemy):
    """Resolve one enemy attack and the player's parry attempt."""
    raw_damage = random.randint(max(1, enemy["attack"] - 2), enemy["attack"] + 2)

    if random.randint(1, 100) <= enemy["special_chance"]:
        raw_damage = int(raw_damage * 1.5)
        print(enemy["name"] + " used a SPECIAL ATTACK!")

    parry_result = try_parry(player["parry_chance"], player["perfect_parry_chance"])
    final_damage = damage_after_parry(raw_damage, parry_result)

    # Defense reduces damage that gets through the parry.
    final_damage = max(0, final_damage - player["defense"])
    player["health"] = max(0, player["health"] - final_damage)

    if parry_result == "perfect":
        print("PERFECT PARRY! " + player["name"] + " took no damage.")
    elif parry_result == "partial":
        print(player["name"] + " partially parried the attack.")
    else:
        print(player["name"] + " failed to parry.")

    print(enemy["name"] + " dealt " + str(final_damage) + " damage to " + player["name"] + ".")
    return final_damage


def use_potion(player):
    """Use one health potion if available."""
    if player["potions"] <= 0:
        print("You do not have any health potions.")
        return False

    if player["health"] >= player["max_health"]:
        print("Your health is already full.")
        return False

    heal_amount = min(30, player["max_health"] - player["health"])
    player["health"] += heal_amount
    player["potions"] -= 1
    print("You restored " + str(heal_amount) + " health.")
    return True


def show_combat_status(player, enemy):
    """Display current combat health and inventory information."""
    print("\n----------------------------------------")
    print(player["name"] + ": " + str(player["health"]) + "/" + str(player["max_health"]) + " HP")
    print(enemy["name"] + " [" + enemy["type"].upper() + "]: " + str(enemy["health"]) + "/" + str(enemy["max_health"]) + " HP")
    print("Potions: " + str(player["potions"]) + " | Coins: " + str(player["coins"]) + " | Score: " + str(player["score"]))
    print("----------------------------------------")


def give_combat_reward(player, enemy):
    """Give score/coins for defeating an enemy from Sami's combat slice."""
    player["score"] += enemy["reward"]
    coins_found = random.randint(5, 12)
    if enemy["type"] == "elite":
        coins_found += 8
    elif enemy["type"] == "boss":
        coins_found += 20

    player["coins"] += coins_found
    print("Victory! +" + str(enemy["reward"]) + " score and +" + str(coins_found) + " coins.")


def combat(player, enemy):
    """Run a complete turn-based fight between one player and one enemy."""
    print("\nA " + enemy["type"] + " enemy appeared: " + enemy["name"] + "!")

    while player["health"] > 0 and enemy["health"] > 0:
        show_combat_status(player, enemy)
        print("[1] Base Attack")
        print("[2] Special Attack")
        print("[3] Health Potion")
        print("[4] Inspect Enemy")

        choice = input("Choose an action: ").strip()

        if choice == "1":
            player_attack(player, enemy, "attack")
        elif choice == "2":
            player_attack(player, enemy, "special")
        elif choice == "3":
            used = use_potion(player)
            if not used:
                # Invalid potion use should not waste the combat turn.
                continue
        elif choice == "4":
            print("\n" + enemy["name"] + " stats:")
            print("Attack: " + str(enemy["attack"]))
            print("Parry Chance: " + str(enemy["parry_chance"]) + "%")
            print("Special Chance: " + str(enemy["special_chance"]) + "%")
            continue
        else:
            print("Invalid action. Choose 1, 2, 3, or 4.")
            continue

        if enemy["health"] <= 0:
            give_combat_reward(player, enemy)
            return True

        enemy_attack(player, enemy)

    print(player["name"] + " was defeated by " + enemy["name"] + ".")
    return False



# F11/F12: encounter selection

def roll_combat_encounter(round_number=1, difficulty="adventurer", force_type=None):
    """Choose a combat encounter after a door triggers combat.

    ``force_type`` is useful when another feature explicitly creates a normal,
    elite, or boss door. Otherwise the encounter is randomly selected.
    """
    if force_type in ("normal", "elite", "boss"):
        return create_enemy(round_number, difficulty, force_type)

    roll = random.randint(1, 100)

    # Bosses remain rare in random door encounters. The team can force one for
    # a final-boss event by calling force_type="boss".
    if roll <= 5:
        enemy_type = "boss"
    elif roll <= 25:
        enemy_type = "elite"
    else:
        enemy_type = "normal"

    return create_enemy(round_number, difficulty, enemy_type)


def start_combat_from_door(player, round_number=1, difficulty="adventurer", encounter_chance=70):
    """Door hook: roll whether entering a door starts combat system."""
    roll = random.randint(1, 100)
    if roll > encounter_chance:
        print("No enemy was found behind this door.")
        return None

    enemy = roll_combat_encounter(round_number, difficulty)
    return combat(player, enemy)


def combat_demo():
    print("=== Dungeon Brawler: Combat Prototype ===")
    name = input("Player name: ").strip()
    if name == "":
        name = "Player 1"

    print("\nDifficulty")
    print("[1] Rookie")
    print("[2] Adventurer")
    print("[3] Dungeon Master")
    difficulty_choice = input("Choose difficulty: ").strip()

    if difficulty_choice == "1":
        difficulty = "rookie"
    elif difficulty_choice == "3":
        difficulty = "dungeon master"
    else:
        difficulty = "adventurer"

    print("\nEncounter")
    print("[1] Normal Enemy")
    print("[2] Elite Enemy")
    print("[3] Boss")
    encounter_choice = input("Choose encounter: ").strip()

    if encounter_choice == "2":
        enemy_type = "elite"
    elif encounter_choice == "3":
        enemy_type = "boss"
    else:
        enemy_type = "normal"

    player = create_player(name)
    enemy = create_enemy(1, difficulty, enemy_type)
    combat(player, enemy)


if __name__ == "__main__":
    combat_demo()
