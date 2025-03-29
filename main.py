import json as json
import random as random
from os import listdir
from os.path import isfile, join


def dl():
    """
    Wypisuje dluga linie na 60 znakow
    """
    for i in range(60):
        if i == 0:
            print("+", end="")
        elif i == 59:
            print("+")

        else:
            print("-", end="")


def dane(char):
    chartoprint = [
        "| (",
        char["currentSlot"],
        ") ",
        char["name"],
        " HP:",
        char["CurrentHp"],
        "/",
        char["MaxHp"],
        " Mana:",
        char["CurrentMana"],
        "/",
        char["MaxMana"],
        " ",
    ]
    if char["isStunned"]:
        chartoprint.append("S")
    if char["isOnFire"]:
        chartoprint.append("F")
    if char["isWeak"]:
        chartoprint.append("W")
    if char["CurrentHp"] == "0":
        chartoprint.append("D")
    chartoprint = "".join(chartoprint)

    if int(char["CurrentHp"]) <= 0 and char["isEnemy"] == True:
        chartoprint = "|"
    length = len(chartoprint)
    print(chartoprint, end="")
    for i in range(59 - length):
        print(" ", end="")
        if i == 58 - length:
            print("|", end="\n")


def load(characterfile, slot, typ):
    characterfile = "./" + typ + "/" + characterfile + ".json"
    with open(characterfile, "r", encoding="utf8") as read_it:
        localchar = json.load(read_it)
        slot = str(slot)
    localchar.update({"currentSlot": slot})
    return localchar


def printer(str):
    print("|", end="")
    dl = len(str) + 1

    print(str, end="")
    for i in range(59 - dl):
        print(" ", end="")
        if i == 58 - dl:
            print("|", end="\n")


def ab(id, slot):
    a1 = load(str(id), 1, "ability")
    a1str = (
        "("
        + str(slot)
        + ") "
        + "Nazwa: "
        + a1["name"]
        + ", Obrazenia: "
        + a1["dmg"]
        + ", Koszt: "
        + a1["mana"]
    )
    printer(a1str)


def actions(char):
    dl()
    printer("(0) Standardowy atak")
    ab(char["Slot1ID"], 1)
    ab(char["Slot2ID"], 2)
    ab(char["Slot3ID"], 3)
    dl()


def display_team():
    print("Team:")
    dl()
    dane(char1)
    dane(char2)
    dane(char3)
    dl()


def display_enemy():
    print("Enemy:")
    dl()
    dane(enemy1)
    dane(enemy2)
    dane(enemy3)
    dl()


def action(char1, act):
    # print(char1)
    if act in (1, 2, 3):
        search = "Slot" + str(act) + "ID"
        characterfile = "./ability/" + char1[search] + ".json"
        with open(characterfile, "r", encoding="utf8") as read_it:
            abilityinfo = json.load(read_it)
        dmg = int(abilityinfo["dmg"])
        mana = int(abilityinfo["mana"])
    else:
        dmg = int(char1["AD"])
        mana = 0
    currmana = int(char1["CurrentMana"])
    if char1["isStunned"] == False:
        if currmana + 1 > mana:
            display_enemy()
            print("Wybierz cel:")
            target = int(input())
            if int(char1["CurrentHp"]) <= 0:
                print("Postać jest martwa - utrata akcji")
            else:
                if target == 1:
                    enemyhp1 = int(enemy1["CurrentHp"])
                    enemy1["CurrentHp"] = str(enemyhp1 - dmg)
                    char1["CurrentMana"] = str(currmana - mana)
                if target == 2:
                    enemyhp2 = int(enemy2["CurrentHp"])
                    enemy2["CurrentHp"] = str(enemyhp2 - dmg)
                    char1["CurrentMana"] = str(currmana - mana)
                if target == 3:
                    enemyhp3 = int(enemy3["CurrentHp"])
                    enemy3["CurrentHp"] = str(enemyhp3 - dmg)
                    char1["CurrentMana"] = str(currmana - mana)

        else:
            print("Nie masz tyle many - stracona tura!")
    else:
        print("Postać jest zestunowana - akcja nie możliwa!")


def enemyaction(attacker, ability, char1, char2, char3):
    if ability in (1, 2, 3):
        search = "Slot" + str(ability) + "ID"
        characterfile = "./ability/" + attacker[search] + ".json"
        with open(characterfile, "r", encoding="utf8") as read_it:
            abilityinfo = json.load(read_it)
        dmg = int(abilityinfo["dmg"])
        mana = int(abilityinfo["mana"])
    else:
        dmg = int(attacker["AD"])
        mana = 0

    currmana = int(attacker["CurrentMana"])

    if not attacker["isStunned"]:
        if currmana >= mana:
            living_targets = [
                char for char in [char1, char2, char3] if int(char["CurrentHp"]) > 0
            ]
            if not living_targets:
                print("To się nie powinno pokazac, ale nic sie nie stalo")
                return

            target = random.choice(living_targets)
            target_index = [char1, char2, char3].index(target) + 1

            print(
                f"Przeciwnik {attacker['name']} atakuje bohatera {target_index} umiejetnoscia ze slotu {ability} za {dmg} obrazen."
            )
            target["CurrentHp"] = str(int(target["CurrentHp"]) - dmg)
            attacker["CurrentMana"] = str(currmana - mana)
        else:
            print(
                f"Przeciwnik {attacker['name']} nie posiada wystarczajaco duzo many zeby dokonac ataku nr {ability}."
            )
    else:
        print(
            f"Przeciwnik {attacker['name']} jest zestunowany i nie moze atakowac"
        )  # ale to jest piekne


def get_living_enemies(enemylist):
    return [enemy for enemy in enemylist if int(enemy["CurrentHp"]) > 0]


def listuj(folder):
    # otwiera folder i zwraca liste plikow w nim
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    return onlyfiles


def process_character(character):
    # Remove stun after 1 round
    if character["isStunned"]:
        character["isStunned"] = False

    # Reduce HP if on fire
    if character["isOnFire"]:
        character["CurrentHp"] = max(0, int(character["CurrentHp"]) - 5)
        character["CurrentHp"] = str(character["CurrentHp"])

    # Reduce AD if weak
    if character["isWeak"]:
        character["AD"] = max(0, int(character["AD"]) - 5)
        character["AD"] = str(character["AD"])


def roundtick(char1, char2, char3, enemy1, enemy2, enemy3):
    process_character(char1)
    process_character(char2)
    process_character(char3)
    process_character(enemy1)
    process_character(enemy2)
    process_character(enemy3)


# tutaj powinien byc main, ale nie chce mi sie go robic
# otworz folder characters i enemy i zobacz jakie sa tam pliki, wpisz nazwe pliku bez .json

# wypisz postacie

print("Postacie:", *listuj("characters"))

print("Podaj nazwe postaci 1: ")
char1name = str(input())
char1 = load(char1name, 1, "characters")

print("Podaj nazwe postaci 2: ")
char2name = input()
char2 = load(char2name, 2, "characters")

print("Podaj nazwe postaci 3: ")
char3name = input()
char3 = load(char3name, 3, "characters")

print("Przeciwnicy:", *listuj("enemy"))

print("Podaj nazwe przeciwnika 1: ")
enemy1name = input()
enemy1 = load(enemy1name, 1, "enemy")

print("Podaj nazwe przeciwnika 2: ")
enemy2name = input()
enemy2 = load(enemy2name, 2, "enemy")

print("Podaj nazwe przeciwnika 3: ")
enemy3name = input()
enemy3 = load(enemy3name, 3, "enemy")

while True:
    display_team()
    display_enemy()
    char = int(input("Wybierz postac: "))
    if char == 1:
        actions(char1)
    elif char == 2:
        actions(char2)
    elif char == 3:
        actions(char3)
    else:
        print("Nie ma takiej postaci")
        continue
    act = int(input("Wybierz akcje: "))
    if char == 1:
        action(char1, act)
    elif char == 1:
        action(char1, act)
    elif char == 2:
        action(char2, act)
    elif char == 3:
        action(char3, act)
    else:
        print("Nie ma takiej postaci")
        continue

    living_enemies = get_living_enemies([enemy1, enemy2, enemy3])
    if not living_enemies:
        print("Wygrales!")
        break

    attacker = random.choice(living_enemies)
    ability = random.randint(1, 3)
    enemyaction(attacker, ability, char1, char2, char3)
    if (
        int(char1["CurrentHp"]) <= 0
        and int(char2["CurrentHp"]) <= 0
        and int(char3["CurrentHp"]) <= 0
    ):
        print("Przegrales!")
        break
    display_team()
    display_enemy()
    char = int(input("Wybierz postac: "))
    if char == 1:
        actions(char1)
    elif char == 2:
        actions(char2)
    elif char == 3:
        actions(char3)
    else:
        print("Nie ma takiej postaci")
        continue
    act = int(input("Wybierz akcje: "))
    if char == 1:
        action(char1, act)
    elif char == 2:
        action(char2, act)
    elif char == 3:
        action(char3, act)
    else:
        print("Nie ma takiej postaci")
        continue

    living_enemies = get_living_enemies([enemy1, enemy2, enemy3])
    if not living_enemies:
        print("Wygrales!")
        break

    attacker = random.choice(living_enemies)
    ability = random.randint(1, 3)
    enemyaction(attacker, ability, char1, char2, char3)
    if (
        int(char1["CurrentHp"]) <= 0
        and int(char2["CurrentHp"]) <= 0
        and int(char3["CurrentHp"]) <= 0
    ):
        print("Przegrales!")
        break
    roundtick(char1, char2, char3, enemy1, enemy2, enemy3)
