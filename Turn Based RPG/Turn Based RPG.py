import random
import time

# Classes for characters and special skills
class Attributes:
    def __init__(self, name: str, health: float, attack: float, defence: float, action_points: float):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.action_points = action_points

class Witcher(Attributes):
    def __init__(self, name: str, health: float, attack: float, defence: float, action_points: float):
        super().__init__(name, health, attack, defence, action_points)

class Mage(Attributes):
    def __init__(self, name: str, health: float, attack: float, defence: float, action_points: float):
        super().__init__(name, health, attack, defence, action_points)

class ElderBlood(Attributes):
    def __init__(self, name: str, health: float, attack: float, defence: float, action_points: float):
        super().__init__(name, health, attack, defence, action_points)

class SpecialMoves:
    def __init__(self, name: str, damage_type: str):
        self.name = name
        self.damage_type = damage_type

class Signs(SpecialMoves):
    def __init__(self, name: str, damage_type: str, damage_stats: float):
        SpecialMoves.__init__(self, name, damage_type)
        self.damage_stats = damage_stats

class Magic(SpecialMoves):
    def __init__(self, name: str, damage_type: str, damage_stats: float):
        SpecialMoves.__init__(self, name, damage_type)
        self.damage_stats = damage_stats

class ElderMagic(SpecialMoves):
    def __init__(self, name: str, damage_type: str, damage_stats: float):
        SpecialMoves.__init__(self, name, damage_type)
        self.damage_stats = damage_stats

# Create Display and main menu:
def display():

    display_menu = [1, 2]
    print("\n\nHello Player! Welcome to The Witcher Arena!\n")
    time.sleep(1)
    print("What would you like to do: \n\t1 - Start Game\n\t2 - Quit\n")

    while True:
        display_select = int(input("Type the option you want: "))
        if display_select in display_menu:
            break
        else:
            print("Wrong input. Please select again: ")

    if display_select == 1:
        arena_display()

    elif display_select == 2:
        print("Ok, Good Bye!")
        exit()

def arena_display():
    time.sleep(1)
    print("\nThe Arena is a 1v1 challenge where you fight a computer opponent!")
    time.sleep(2)
    print("Prepare yourself!!\n")
    time.sleep(2)

# Prompts the user to create a character from the 3 different class types: Witcher, Mage and Elder Blood
def create_character():
    while True:
        choice = [1, 2, 3]
        # print("Welcome to Witcher Arena!\n")
        class_choice = int(input("Please choose your character:\n1-For Geralt\n2-For Yennefer\n3-For Ciri\nYour Choice:"))
        if class_choice in choice:
            break
        else:
            print("Invalid choice, try again:")

    if class_choice == 1:
        print("\n")
        print("You have chosen Geralt of Rivia!")
        player = Witcher("Geralt of Rivia", 100, 25, 9, 10)
        print(f"Your fighter stats are:\n"
                f"Name: {player.name}\n"
                f"Health : {player.health}\n"
                f"Attack: {player.attack}\n"
                f"Defence: {player.defence}\n"
                f"Action Points: {player.action_points}")
        return player

    elif class_choice == 2:
        print("\n")
        print("You have chosen Yennefer!")
        player = Mage("Yennefer", 100, 23, 5, 10)
        print(f"Your fighter stats are:\n"
                f"Name: {player.name}\n"
                f"Health : {player.health}\n"
                f"Attack: {player.attack}\n"
                f"Defence: {player.defence}\n"
                f"Action Points: {player.action_points}")
        return player

    elif class_choice == 3:
        print("\n")
        print("You have chosen Ciri!")
        player = ElderBlood("Ciri", 100, 28, 8, 10)
        print(f"Your fighter stats are:\n"
                f"Name: {player.name}\n"
                f"Health : {player.health}\n"
                f"Attack: {player.attack}\n"
                f"Defence: {player.defence}\n"
                f"Action Points: {player.action_points}")
        return player

# Create special skills for each fighter's:

def special_moves(player):

    if type(player) == Witcher:
        player_ss = Signs("Igni", "Fire Sign Attack", 40)
        time.sleep(2)
        print(f"Your fighter special skill is {player_ss.name}\n"
              f"Skill description: {player_ss.damage_type}\n"
              f"Skill damage: {player_ss.damage_stats}")
        return player_ss

    elif type(player) == Mage:
        player_ss = Magic("Fire", "Fire Bolt attack", 30)
        time.sleep(2)
        print(f"Your fighter special skill is {player_ss.name}\n"
              f"Skill description: {player_ss.damage_type}\n"
              f"Skill damage: {player_ss.damage_stats}")
        return player_ss

    elif type(player) == ElderBlood:
        player_ss = ElderMagic("Elder", "Elder slash attack", 30)
        time.sleep(2)
        print(f"Your fighter special skill is {player_ss.name}\n"
              f"Skill description: {player_ss.damage_type}\n"
              f"Skill damage: {player_ss.damage_stats}")
        return player_ss

# Simulating Enemy Stats:

def enemy_hp():
    health = []
    for i in range(1, 7):
        health.insert(i, (i * 30) + 20)
    return health

def enemy_armour():
    armour = []
    for block in range(5, 10):
        armour.insert(block, (block + 1) * 2)
    return armour

def enemy_attack():
    enemy_basic_attack = [20]
    return enemy_basic_attack

def enemy_action_points():
    enemy_ac = []
    for ac in range(5, 10):
        enemy_ac.insert(ac, (ac + 3))
    return enemy_ac

# Create enemies:
def create_rival():
    name = ["Letho", "Triss", "Eredin"]
    health = enemy_hp()
    attack = enemy_attack()
    armour = enemy_armour()
    eac = enemy_action_points()

    enemy_selected = []

    for num in range(0, 3):
        enemy_choice = random.randint(0, 2)
        if enemy_choice == 0:
            enemy = Witcher(name[0], health[0], attack[0], armour[0], eac[0])
            # health.pop(0)
            time.sleep(1)
            print("\n----------------Versus----------------------\n")
            time.sleep(1)
            print(f"Your enemy is :\n"
                    f"Name: {enemy.name}\n"
                    f"Health : {enemy.health}\n"
                    f"Attack: {enemy.attack}\n"
                    f"Defence: {enemy.defence}\n"
                    f"Action Points: {enemy.action_points}")
            enemy_selected.append(enemy)
            break

        elif enemy_choice == 1:
            enemy = Mage(name[1], health[0], attack[0], armour[0], eac[0])
            time.sleep(1)
            print("\n----------------Versus----------------------\n")
            time.sleep(1)
            print(f"Your enemy is:\n"
                   f"Name: {enemy.name}\n"
                   f"Health : {enemy.health}\n"
                   f"Attack: {enemy.attack}\n"
                   f"Defence: {enemy.defence}\n"
                   f"Action Points: {enemy.action_points}")
            enemy_selected.append(enemy)
            break

        else:
            enemy = ElderBlood(name[2], health[0], attack[0], armour[0], eac[0])
            time.sleep(1)
            print("\n----------------Versus----------------------\n")
            time.sleep(1)
            print(f"Your enemy is:\n"
                    f"Name: {enemy.name}\n"
                    f"Health : {enemy.health}\n"
                    f"Attack: {enemy.attack}\n"
                    f"Defence: {enemy.defence}\n"
                    f"Action Points: {enemy.action_points}")
            enemy_selected.append(enemy)
            break

    return enemy_selected

# Damage logics

def player_damage(player, enemy):
    damage_calc = float(player.attack)
    true_damage = enemy.defence - damage_calc
    if true_damage <= 0:
        enemy.health += true_damage
        time.sleep(2)
    return f"\nDamage inflicted in your enemy: {enemy.name}\n" \
            f"Your damage is: {true_damage}\n" \
            f"Enemy has: {enemy.health} HP left"

def player_special_damage(player, enemy):
    damage_calc = float(player.damage_stats)
    true_damage = enemy.defence - damage_calc
    if true_damage <= 0:
        enemy.health += true_damage
        time.sleep(2)
    return f"\n{player.damage_type} inflicted in your enemy: {enemy.name}\n" \
            f"Your damage is: {true_damage}\n" \
            f"Enemy has: {enemy.health}  HP left"

def enemy_damage(player, enemy):
    damage_calc = float(enemy.attack)
    true_enemy_damage = player.defence - damage_calc
    if true_enemy_damage <= 0:
        player.health += true_enemy_damage
        time.sleep(2)
        print("\n----Enemy Turn!---")
        time.sleep(2)
    return f"\nDamage inflicted in your fighter: {player.name}\n" \
           f"Enemy damage is: {true_enemy_damage}\n" \
           f"You have: {player.health} HP left"

def main():
    display()
    player = create_character()
    player_ss = special_moves(player)
    enemy1 = create_rival().pop(0)

    while (enemy1.health != 0) or (player.health != 0):

        if player.health <= 0:
            print("\n-----You lost!-----")
            break

        time.sleep(2)
        print("\n----Player's Turn!----")
        time.sleep(2)
        combat_choice = int(input("\nWhat do you want to do:\n1-For Normal Attack (Costs 1 Action Point)\n2-For Special Attack (Costs 2 Action Points)\nChoose:"))
        if combat_choice == 1:
            player_turn = player_damage(player, enemy1)
            player.action_points -= 1
            print(player_turn)
            print(f"Action points remain: {player.action_points}")
        elif combat_choice == 2:
            player_turn = player_special_damage(player_ss, enemy1)
            player.action_points -= 2
            print(player_turn)
            print(f"Player Action Points remain: {player.action_points}")

        if enemy1.health <= 0:
            print("\n-----Enemy defeated! You Won!-----")
            break

        enemy_turn = enemy_damage(player, enemy1)
        enemy1.action_points -= 1
        print(enemy_turn)
        print(f"Enemy Action Points remain: {enemy1.action_points}")

        if (player.action_points <= 0) and (enemy1.action_points <= 0):
            print("No more action points! The game ended with a draw!")
            break

    play_again()

def play_again():
    choose = input("\nDo you want to play again?\n(Y / N ):")
    if choose == "Y":
        main()
    elif choose == "N":
        print("\nOk, Good Bye!")
        exit()
    else:
        print("Wrong Input! Exit program in...")
        time.sleep(1)
        print(3)
        time.sleep(1)
        print(2)
        time.sleep(1)
        print(1)
        time.sleep(1)
        print("Good Bye!")

if __name__ == "__main__":
    main()
