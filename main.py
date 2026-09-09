"""
main.py - HOLLOWGATE
A one-shot ASCII dungeon crawler for the Windows Command Prompt.
Run this with `python main.py`, or just double-click Launch Hollowgate.bat.
"""
import sys

from engine import ui, entities, art
from story import chapter1, chapter2, chapter3, chapter4, chapter5, endings

CLASS_KEYS = ["warrior", "rogue", "mage", "cleric"]

DEFAULT_NAMES = {
    "warrior": "Kael",
    "rogue": "Wren",
    "mage": "Isolde",
    "cleric": "Brother Ambrose",
}

HOW_TO_PLAY_TEXT = """
HOLLOWGATE is a turn-based dungeon crawl. Every menu is a numbered list -
type the number of your choice and press Enter.

STORY:
  Narration appears one passage at a time. After each one you can:
    [Enter]  continue
    [R]      reread the passage you just read
    [J]      open your Journal, which remembers everything said so far

BATTLES:
  Fights happen on a small grid. You and your enemies are letters on a
  map ('@' is always you). Each turn you choose ONE action:
    Move    - move up to your class's move speed, one tile per step
    Attack  - your class's free basic attack (needs to be in range)
    Ability - a special move that costs Stamina/Focus/Mana/Faith
    Item    - drink a potion or other consumable
    Info    - check your stats, abilities, and the battlefield
    Flee    - try to escape (not available in boss fights)

  Attacks work like tabletop dice: you roll a d20 plus your bonus against
  the enemy's Armor Class. A natural 20 is always a critical hit; a
  natural 1 always misses. If you hit, you roll damage dice for the
  amount.

  Bosses sometimes 'charge up' a big attack and warn you a turn ahead of
  time. Watch the log - repositioning during the warning can save you.

  If you fall in battle, Hollowgate isn't finished with you: you can
  rise and try that fight again with full health, no questions asked.

CLASSES:
  Warrior - tanky, melee, strong single-target and group damage
  Rogue   - fast, high burst, moves 2 tiles per turn
  Mage    - fragile, ranged spells, area damage
  Cleric  - balanced, self-healing and buffs

Good luck down there.
"""


def title_screen():
    ui.clear()
    ui.print_art(art.TITLE_ART)
    ui.press_enter("[Enter] ...")


def main_menu():
    idx = ui.menu("MAIN MENU", ["New Game", "How to Play", "Credits", "Quit"])
    return ["new", "how", "credits", "quit"][idx]


def how_to_play():
    ui.clear()
    ui.banner("HOW TO PLAY")
    print(HOW_TO_PLAY_TEXT)
    ui.press_enter()


def show_credits():
    ui.clear()
    ui.banner("CREDITS")
    print("HOLLOWGATE")
    print()
    print("A one-shot ASCII dungeon crawler.")
    print("Written for a command prompt near you.")
    print()
    print("Built with Python, dice, and entirely too much ASCII art.")
    ui.press_enter()


def choose_speed():
    ui.clear()
    ui.banner("TEXT SPEED")
    idx = ui.menu(
        "How should narration text appear?",
        ["Normal (typewriter)", "Fast (typewriter, quicker)", "Instant (no typewriter)"],
    )
    ui.set_speed(["normal", "fast", "instant"][idx])


def choose_class():
    ui.clear()
    ui.banner("CHOOSE YOUR CLASS")
    for k in CLASS_KEYS:
        d = entities.CLASS_DATA[k]
        print(f"{d['display']} - {d['title']}")
        print(f"  {d['tagline']}")
        print(
            f"  HP {d['hp']}  |  {d['res_name']} {d['res_max']}  |  "
            f"AC {d['ac']}  |  Move {d['move_range']} tile(s)/turn"
        )
        print()
    idx = ui.menu("Who are you, down here?", [entities.CLASS_DATA[k]["display"] for k in CLASS_KEYS])
    chosen = CLASS_KEYS[idx]

    ui.clear()
    portrait = getattr(art, f"PORTRAIT_{chosen.upper()}")
    ui.print_art(portrait)
    print(entities.CLASS_DATA[chosen]["hook"])
    ui.press_enter()
    return chosen


def ask_name(cls_key):
    default = DEFAULT_NAMES[cls_key]
    raw = input(f"\nWhat do they call you down here? [{default}] > ").strip()
    return raw if raw else default


PROLOGUE_BEATS = [
    "The town of Aldenmoor has been dead for longer than anyone alive "
    "can confirm. Once a century, the gate beneath its ruined chapel "
    "opens anyway - and something in the world always finds someone "
    "willing to walk through it.",

    "The stories don't agree on what's down there. They agree on one "
    "thing: it gives you whatever you came for. It just never mentions "
    "the cost until you're already standing at the bottom, holding it.",

    "Tonight, the gate is open. You are the one standing in front of it.",
]


def play_game():
    choose_speed()
    cls_key = choose_class()
    name = ask_name(cls_key)
    player = entities.Player(name, cls_key)

    ui.narrate(PROLOGUE_BEATS, chapter_label="PROLOGUE", art=art.PROLOGUE_ART)
    ui.spaced_transition()

    alignment = 0
    for chapter in (chapter1, chapter2, chapter3, chapter4):
        result = chapter.run(player)
        if result == "quit":
            return
        alignment += result
        player.alignment = alignment

    ending = chapter5.run(player, alignment)
    if ending == "quit":
        return

    endings.show(player, ending)
    ui.clear()
    ui.banner("THANK YOU FOR PLAYING HOLLOWGATE")
    ui.press_enter("[Enter] Return to the title screen...")


def main():
    title_screen()
    while True:
        choice = main_menu()
        if choice == "new":
            play_game()
        elif choice == "how":
            how_to_play()
        elif choice == "credits":
            show_credits()
        elif choice == "quit":
            ui.clear()
            print("The gate closes behind you.\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThe gate closes.\n")
        sys.exit(0)
