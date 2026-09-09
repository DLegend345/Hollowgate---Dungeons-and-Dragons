"""
story/chapter1.py - THE GATE BELOW
"""
from engine import ui, battle, bestiary, art

LABEL = "CHAPTER I - THE GATE BELOW"


def run(player):
    ui.narrate(
        [
            "The stair spirals down past torches that haven't burned in a "
            "hundred years, and yet burn now. Your breath fogs in air that "
            "shouldn't be this cold this far underground.",

            "Somewhere below you, something exhales. Long, and slow, and "
            "not remotely human.",

            "This is Hollowgate. You already knew that stairs, once "
            "started, don't allow much room for changing your mind.",
        ],
        chapter_label=LABEL,
        art=art.CH1_BG,
    )

    ui.narrate([
        "A shape peels itself off the wall ahead - stooped, wrong at the "
        "joints, wearing the ragged shreds of clothes decades out of "
        "fashion. A husk. One of the ones who came before you, and stayed.",
    ], chapter_label=LABEL)

    def make_husk_fight():
        h = bestiary.make_husk()
        h.pos = (5, 1)
        return [h]

    outcome = battle.battle_with_retry(
        player, make_husk_fight, "The Gate Below",
        art=art.HUSK_ART, player_start=(1, 2),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "It drops. Whatever was left of the person it used to be doesn't "
        "so much as flicker in its eyes as they go dark. You're not sure "
        "that's a mercy. You're not sure it isn't, either.",
    ], chapter_label=LABEL)

    # --- Interaction / alignment choice -----------------------------------
    ui.clear()
    ui.print_art(art.CH1_INTERACTION)
    ui.narrate([
        "Further on, rubble half-buries a second husk - pinned, not dead, "
        "one hand still twitching toward the light of your torch. Beneath "
        "the grime you can just make out a chain around its neck: an "
        "amulet, old silver, the kind pilgrims wore when they still came "
        "here hoping for something other than a door out.",
    ], chapter_label=LABEL)

    idx = ui.menu(
        "What do you do?",
        [
            "Pull the rubble off and free it, amulet and all",
            "Take the amulet - it can't use it anymore - and move on",
        ],
    )
    if idx == 0:
        ui.narrate([
            "You heave the stone aside. The husk doesn't thank you - it "
            "can't - but it drags itself upright and staggers off into "
            "the dark on legs that shouldn't still work, amulet swinging "
            "at its throat. Small mercies. You'll take them where you "
            "find them, down here.",
        ], chapter_label=LABEL)
        alignment = 2
    else:
        ui.narrate([
            "You crouch, unclasp the chain, and pull. The husk's hand "
            "closes weakly around empty air where the amulet used to be. "
            "You tell yourself it doesn't need it anymore. You almost "
            "believe it. The silver is warm in your pocket the rest of "
            "the way down, warmer than metal should be.",
        ], chapter_label=LABEL)
        alignment = -2

    ui.narrate([
        "The passage opens into a wide chamber. At its center stands a "
        "thing built from centuries of stolen keys and the bones of "
        "everyone who ever needed one - the Gatekeeper, and it has "
        "already noticed you.",
    ], chapter_label=LABEL)

    def make_gatekeeper_fight():
        g = bestiary.make_gatekeeper()
        g.pos = (5, 1)
        return [g]

    outcome = battle.battle_with_retry(
        player, make_gatekeeper_fight, "The Gatekeeper's Chamber",
        art=art.GATEKEEPER_ART, player_start=(1, 2), can_flee=False,
        death_text=(
            "The Gatekeeper's weight comes down on you like a closing "
            "door. Darkness - but not the final kind. Not yet."
        ),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "The Gatekeeper collapses into a pile of keys that were never "
        "going to open anything, for anyone, ever again. Somewhere far "
        "below, you feel - rather than hear - a lock disengage.",

        "You gained ground tonight. You also learned that Hollowgate "
        "notices when something dies inside it. You'd better keep moving.",
    ], chapter_label=LABEL)

    ui.spaced_transition()
    return alignment

