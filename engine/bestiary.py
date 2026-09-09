"""
engine/bestiary.py
Enemy templates for HOLLOWGATE. Each make_* function returns a *fresh*
Enemy instance (important for retries after defeat).
"""

from .entities import Enemy, Ability


def make_husk():
    return Enemy("husk", "Husk", 16, 11, 3, "1d6+1", atk_range=1, speed=1,
                  ai="aggressive", symbol="h")


def make_gatekeeper():
    return Enemy("gatekeeper", "The Gatekeeper", 32, 12, 4, "1d8+2", atk_range=1,
                  speed=1, ai="aggressive", flee_ok=False, symbol="G")


def make_drowned_wretch():
    return Enemy("wretch", "Drowned Wretch", 18, 11, 4, "1d6+2", atk_range=2,
                  speed=1, ai="ranged", symbol="w")


def make_bound_tome():
    return Enemy("tome", "The Bound Tome", 38, 12, 5, "1d8+3", atk_range=3,
                  speed=0, ai="ranged", flee_ok=False, symbol="T")


def make_bone_stalker():
    return Enemy("stalker", "Bone Stalker", 20, 13, 5, "1d6+3", atk_range=1,
                  speed=2, ai="aggressive", symbol="b")


def make_gardener():
    special = {
        "name": "Bloom of Thorns",
        "telegraph": "The Gardener's roots coil and writhe - thorns are about to erupt around it!",
        "kind": "aoe_radius",
        "radius": 2,
        "dice": "3d6+2",
        "cooldown": 4,
    }
    enrage = [
        {"threshold": 0.5, "hit_bonus": 1, "cooldown": 3,
         "message": "The Gardener's roots blacken and lash out faster!", "done": False},
    ]
    return Enemy("gardener", "The Gardener", 60, 14, 6, "2d6+2", atk_range=1, speed=1,
                 ai="boss", special=special, enrage_steps=enrage, flee_ok=False, symbol="Y")


def make_hollow_king():
    special = {
        "name": "Ruin",
        "telegraph": "The Hollow King raises his shattered crown - the air itself begins to crack!",
        "kind": "aoe_radius",
        "radius": 2,
        "dice": "4d6+4",
        "cooldown": 4,
    }
    enrage = [
        {"threshold": 0.6, "hit_bonus": 1, "cooldown": 3, "speed": 2,
         "message": "Cracks race up the Hollow King's arm. He moves faster now.",
         "done": False},
        {"threshold": 0.3, "hit_bonus": 1, "cooldown": 2, "dmg_dice": "2d10+3",
         "message": "What's left of him is mostly rage. This ends soon, one way or another.",
         "done": False},
    ]
    return Enemy("hollowking", "The Hollow King", 95, 15, 7, "2d8+3", atk_range=1, speed=1,
                 ai="boss", special=special, enrage_steps=enrage, flee_ok=False, symbol="K")


def make_mirror_self(player):
    """Its stats are drawn directly from the player's own build."""
    ultimate = player.ultimate()
    basic = player.basic()
    hp = max(20, int(player.max_hp * 0.85))
    e = Enemy("mirror", f"{player.name}'s Reflection", hp, player.ac,
              player.hit_bonus, basic.dice, atk_range=basic.range,
              speed=player.move_range, ai="boss", flee_ok=False, symbol="@")
    e.special = {
        "name": f"Mirrored {ultimate.name}",
        "telegraph": f"Your reflection copies your stance exactly - it's about to unleash {ultimate.name}!",
        "kind": "single",
        "dice": ultimate.dice,
        "cooldown": 5,
    }
    e.special_cooldown = 5
    return e
