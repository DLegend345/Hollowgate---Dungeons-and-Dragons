"""
engine/entities.py
Ability, Combatant, and Player definitions, plus the four playable
class kits (Warrior, Rogue, Mage, Cleric).
"""


class Ability:
    def __init__(self, key, name, cost, dice_notation, range_, kind, desc, extra=None):
        self.key = key
        self.name = name
        self.cost = cost
        self.dice = dice_notation
        self.range = range_
        self.kind = kind  # attack | aoe_attack | heal | buff
        self.desc = desc
        self.extra = extra or {}

    def blurb(self, res_name):
        cost_txt = f"{self.cost} {res_name}" if self.cost else "Free"
        if self.kind in ("heal", "buff"):
            rng_txt = "self"
        else:
            rng_txt = f"range {self.range}"
        return f"{self.name}  [{cost_txt}, {rng_txt}] - {self.desc}"


class Combatant:
    """Shared HP/AC/status machinery for both Player and Enemy."""

    def __init__(self, name, max_hp, ac, hit_bonus):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.ac = ac                 # base armor class, never mutated directly
        self.hit_bonus = hit_bonus
        self.buff_hit = 0
        self.buff_dmg = 0
        self.def_bonus = 0
        self.weaken_hit = 0
        self.shield = 0
        self.status = {}
        self.pos = (0, 0)

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount):
        amount = max(0, amount)
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
        self.hp = max(0, self.hp - amount)

    def effective_ac(self):
        return self.ac + self.def_bonus

    def effective_hit_bonus(self):
        return self.hit_bonus + self.buff_hit - self.weaken_hit


# ---------------------------------------------------------------------------
# Class kits — index 0 is always the free basic attack, index -1 the ultimate
# ---------------------------------------------------------------------------

def _warrior_kit():
    return [
        Ability("attack", "Strike", 0, "1d8+3", 1, "attack",
                "A solid, dependable blow with your blade."),
        Ability("cleave", "Cleave", 6, "1d6+2", 1, "aoe_attack",
                "A wide swing that catches every foe beside you."),
        Ability("shieldwall", "Shield Wall", 8, None, 0, "buff",
                "Brace behind your shield. +6 Defense for 2 turns.",
                extra={"buff_def": 6, "turns": 2}),
        Ability("reckoning", "Reckoning", 14, "3d6+5", 1, "attack",
                "Every wound you've taken returns as one devastating blow."),
    ]


def _rogue_kit():
    return [
        Ability("attack", "Quick Strike", 0, "1d6+4", 1, "attack",
                "Fast, precise, and hard to see coming."),
        Ability("backstab", "Backstab", 8, "2d6+4", 1, "attack",
                "Bonus damage against a foe that isn't watching you.",
                extra={"bonus_if_charging": True}),
        Ability("poisonblade", "Poison Blade", 10, "1d4+2", 1, "attack",
                "A shallow cut laced with something foul.",
                extra={"poison_turns": 3, "poison_dice": "1d4"}),
        Ability("assassinate", "Assassinate", 16, "2d8+6", 1, "attack",
                "A killing stroke. Always a critical hit against the badly wounded.",
                extra={"execute_threshold": 0.25}),
    ]


def _mage_kit():
    return [
        Ability("attack", "Firebolt", 0, "1d8+3", 3, "attack",
                "A bolt of raw flame flung from your palm."),
        Ability("frostnova", "Frost Nova", 8, "1d6+2", 2, "aoe_attack",
                "Frost bursts outward, biting every enemy nearby and slowing them.",
                extra={"weaken_hit": 2, "weaken_turns": 1}),
        Ability("barrier", "Arcane Barrier", 6, None, 0, "buff",
                "A shimmering ward that absorbs the next hits against you.",
                extra={"shield": "2d6+6"}),
        Ability("meteor", "Meteor", 20, "2d8+4", 4, "aoe_attack",
                "You call down fire from somewhere that isn't the sky."),
    ]


def _cleric_kit():
    return [
        Ability("attack", "Smite", 0, "1d6+3", 1, "attack",
                "A blow wreathed in pale light."),
        Ability("heal", "Heal", 8, None, 0, "heal",
                "Warm light knits your wounds closed.",
                extra={"heal_dice": "2d8+6"}),
        Ability("bless", "Bless", 6, None, 0, "buff",
                "Conviction sharpens your every strike. +3 to hit, +2 damage, 3 turns.",
                extra={"buff_hit": 3, "buff_dmg": 2, "turns": 3}),
        Ability("judgment", "Judgment", 18, "3d6+6", 2, "attack",
                "Light given weight and edge."),
    ]


CLASS_DATA = {
    "warrior": {
        "display": "Warrior",
        "title": "The Ironclad",
        "hp": 44, "res_name": "Stamina", "res_max": 20, "res_regen": 4,
        "hit_bonus": 5, "ac": 15, "move_range": 1,
        "kit": _warrior_kit,
        "potions": 2,
        "symbol": "W",
        "tagline": "Heavy armor. Heavier grudges. Hard to put down.",
        "hook": (
            "You fought in a war that ended without a victory worth the name. "
            "Hollowgate doesn't care who wins - it only asks who's still standing "
            "when it's over. That, you can do."
        ),
    },
    "rogue": {
        "display": "Rogue",
        "title": "The Shade",
        "hp": 30, "res_name": "Focus", "res_max": 24, "res_regen": 5,
        "hit_bonus": 7, "ac": 14, "move_range": 2,
        "kit": _rogue_kit,
        "potions": 2,
        "symbol": "R",
        "tagline": "Fast, precise, and always one step out of reach.",
        "hook": (
            "You owe a debt that death itself didn't cancel. Something down here "
            "is worth more than the price of getting it. You've stolen from worse "
            "places than this."
        ),
    },
    "mage": {
        "display": "Mage",
        "title": "The Arcanist",
        "hp": 30, "res_name": "Mana", "res_max": 28, "res_regen": 5,
        "hit_bonus": 6, "ac": 13, "move_range": 1,
        "kit": _mage_kit,
        "potions": 2,
        "symbol": "M",
        "tagline": "Thin armor, thinner patience, devastating range.",
        "hook": (
            "You have a theory: that death is a puzzle, not a wall. Hollowgate is "
            "the only place in the world old enough, and cruel enough, to test it."
        ),
    },
    "cleric": {
        "display": "Cleric",
        "title": "The Warden",
        "hp": 36, "res_name": "Faith", "res_max": 26, "res_regen": 5,
        "hit_bonus": 5, "ac": 14, "move_range": 1,
        "kit": _cleric_kit,
        "potions": 1,
        "symbol": "C",
        "tagline": "Steady hands, stubborn hope, a light that won't gutter out.",
        "hook": (
            "You made a promise at a deathbed that your faith says you shouldn't "
            "be able to keep. You came to keep it anyway."
        ),
    },
}


class Player(Combatant):
    def __init__(self, name, cls_key):
        data = CLASS_DATA[cls_key]
        super().__init__(name, data["hp"], data["ac"], data["hit_bonus"])
        self.cls_key = cls_key
        self.cls_display = data["display"]
        self.cls_title = data["title"]
        self.res_name = data["res_name"]
        self.max_res = data["res_max"]
        self.res = self.max_res
        self.res_regen = data["res_regen"]
        self.move_range = data["move_range"]
        self.abilities = data["kit"]()
        self.hook = data["hook"]
        self.symbol = data["symbol"]
        self.inventory = {"Healing Potion": data["potions"]}
        self.alignment = 0
        self.chapters_cleared = 0

    def basic(self):
        return self.abilities[0]

    def ultimate(self):
        return self.abilities[-1]

    def regen(self):
        self.res = min(self.max_res, self.res + self.res_regen)

    def full_restore(self):
        self.hp = self.max_hp
        self.res = self.max_res
        self.status = {}
        self.shield = 0
        self.buff_hit = 0
        self.buff_dmg = 0
        self.def_bonus = 0
        self.weaken_hit = 0

    def level_up(self, hp_gain, res_gain, log=None):
        self.max_hp += hp_gain
        self.hp = min(self.max_hp, self.hp + hp_gain)
        self.max_res += res_gain
        self.res = self.max_res
        if log is not None:
            log.append(
                f"You feel steadier. Max HP +{hp_gain}, Max {self.res_name} +{res_gain}."
            )


class Enemy(Combatant):
    def __init__(self, key, name, max_hp, ac, hit_bonus, dmg_dice, atk_range=1,
                 speed=1, ai="aggressive", special=None, enrage_steps=None,
                 flee_ok=True, symbol="e"):
        super().__init__(name, max_hp, ac, hit_bonus)
        self.key = key
        self.dmg_dice = dmg_dice
        self.atk_range = atk_range
        self.speed = speed
        self.ai = ai
        self.special = special
        self.special_cooldown = special.get("cooldown", 4) if special else None
        self.charging = False
        self.turn_count = 0
        self.enrage_steps = enrage_steps or []
        self.flee_ok = flee_ok
        self.symbol = symbol
        self.basic_ability = Ability("basic", "Attack", 0, dmg_dice, atk_range, "attack", "")
