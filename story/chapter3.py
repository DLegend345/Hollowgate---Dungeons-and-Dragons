"""
story/chapter3.py - THE BONE GARDEN
"""
from engine import ui, battle, bestiary, art

LABEL = "CHAPTER III - THE BONE GARDEN"


def run(player):
    ui.narrate(
        [
            "The passage widens into a cavern that shouldn't be able to "
            "support what's growing in it: pale stalks rising out of "
            "bone-white soil, flowering into shapes that are trying, and "
            "failing, to remember what flowers look like.",

            "Everything here used to be someone. The garden isn't shy "
            "about that.",
        ],
        chapter_label=LABEL,
        art=art.CH3_BG,
    )

    ui.narrate([
        "Two shapes detach from the stalks around you - lean, fast, built "
        "from stacked bone and old sinew. Bone Stalkers, and they've "
        "clearly been waiting for something to hunt.",
    ], chapter_label=LABEL)

    def make_stalkers():
        s1 = bestiary.make_bone_stalker()
        s1.pos = (5, 0)
        s2 = bestiary.make_bone_stalker()
        s2.pos = (5, 3)
        return [s1, s2]

    outcome = battle.battle_with_retry(
        player, make_stalkers, "The Bone Garden",
        art=art.STALKER_ART, player_start=(1, 2),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "Both stalkers fold back into the soil they came from. The "
        "garden doesn't mourn them. It just keeps growing.",
    ], chapter_label=LABEL)

    # --- Interaction / alignment choice: the altar --------------------------
    ui.clear()
    ui.print_art(art.CH3_INTERACTION)
    ui.narrate([
        "At the garden's heart stands an altar grown, not built, out of "
        "rib bones curved into a bowl. Something dark pools in it, "
        "thick as oil, and it ripples toward you the moment you get close "
        "- an offer, wordless but unmistakable: power, on loan, in "
        "exchange for something it doesn't bother naming.",

        "You can feel the Gardener stirring somewhere close by, roused "
        "by the noise of the fight. Whatever you decide, you won't have "
        "long to decide it.",
    ], chapter_label=LABEL)

    idx = ui.menu(
        "What do you do?",
        [
            "Refuse the altar and trust your own strength",
            "Drink from the bowl - power now, questions later",
        ],
    )
    if idx == 0:
        ui.narrate([
            "You step back. The dark in the bowl subsides, almost "
            "sullenly, like something used to getting what it wants. "
            "Whatever this costs you later, it won't be this. You feel "
            "steadier for the refusal - a clean breath, a full heal, "
            "nothing more complicated than that.",
        ], chapter_label=LABEL)
        player.heal(player.max_hp)
        alignment = 2
    else:
        ui.narrate([
            "You drink. It tastes like copper and old rain. For a moment "
            "your own hands look wrong to you - too steady, too eager - "
            "and then the feeling passes, leaving something harder "
            "underneath. Power, exactly as promised. You'll worry about "
            "the price later. Everyone always says that.",
        ], chapter_label=LABEL)
        # A permanent passive bonus (not tracked as a timed status effect,
        # so it can never be accidentally overwritten/reverted by a later
        # timed buff like Bless).
        player.buff_hit += 1
        player.buff_dmg += 2
        alignment = -2

    ui.narrate([
        "The ground shudders. Stalks part like a curtain, and the "
        "Gardener steps through them - the oldest, biggest thing this "
        "place has grown, roots thick as your waist trailing from every "
        "limb, patient in the way that only something that's waited "
        "centuries can afford to be.",
    ], chapter_label=LABEL)

    def make_gardener_fight():
        g = bestiary.make_gardener()
        g.pos = (5, 1)
        return [g]

    outcome = battle.battle_with_retry(
        player, make_gardener_fight, "The Heart of the Bone Garden",
        art=art.GARDENER_ART, obstacles={(3, 0), (3, 3)},
        player_start=(1, 2), can_flee=False,
        death_text=(
            "Roots close over you like the garden closing a wound. But "
            "the dark down here has never been very good at keeping "
            "things buried."
        ),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "The Gardener folds in on itself, roots unraveling into ordinary "
        "dirt. For a long moment, the whole cavern is silent - no "
        "rustling stalks, no distant exhale from the dark. Just you, "
        "breathing hard, and a garden finally allowed to just be dead.",

        "Something in you settles too - not healed, exactly, but "
        "tempered. You've survived Hollowgate's first real test.",
    ], chapter_label=LABEL, art=art.LEVEL_UP_ART)

    player.level_up(6, 3)

    ui.narrate([
        "Ahead, the passage narrows again, and the air starts to carry "
        "the faint, wrong smell of glass.",
    ], chapter_label=LABEL)

    ui.spaced_transition()
    return alignment
