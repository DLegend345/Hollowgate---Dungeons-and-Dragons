"""
story/chapter5.py - THE HEART OF THE DEPTHS
"""
from engine import ui, battle, bestiary, art

LABEL = "CHAPTER V - THE HEART OF THE DEPTHS"


def run(player, alignment):
    ui.narrate(
        [
            "The passage ends without warning, opening onto a chamber "
            "vast enough to swallow the sound of your own footsteps. At "
            "its center, something enormous rises out of the floor and "
            "the ceiling both, pulsing in a slow, patient rhythm.",

            "It's a heart, or it's wearing the idea of one. It's the "
            "thing every floor of Hollowgate has been built around, and "
            "wrapped around, and fed.",
        ],
        chapter_label=LABEL,
        art=art.CH5_BG,
    )

    if alignment >= 3:
        ui.narrate([
            "Everything you refused to take from this place seems to "
            "have added up to something. You feel lighter than you have "
            "any right to feel, this deep down - steadier, clearer, like "
            "the dark down here has less of a grip on you than it should.",
        ], chapter_label=LABEL)
        player.buff_dmg += 2
        player.heal(int(player.max_hp * 0.25))
        tag = "resolve"
    elif alignment <= -3:
        ui.narrate([
            "Everything you took from this place is still with you, and "
            "it's woken up down here, closer to whatever it came from. "
            "Something in your chest runs hotter than it should. You feel "
            "dangerous. You're not sure that's the same thing as feeling "
            "strong.",
        ], chapter_label=LABEL)
        player.buff_hit += 2
        tag = "corruption"
    else:
        ui.narrate([
            "You've taken some things and refused others, and standing "
            "here now, you're not sure any of it tipped the scale one "
            "way or the other. Whatever you are when this is over, you "
            "haven't decided yet. Maybe that's the point.",
        ], chapter_label=LABEL)
        player.shield += 10
        tag = "balanced"

    ui.narrate([
        "A figure detaches from the base of the heart - crowned, "
        "cracked down the middle like old porcelain, wearing the "
        "unmistakable shape of someone who made this exact descent a "
        "very long time ago, and never found the stairs back up. The "
        "Hollow King has been waiting longer than the gate has been a "
        "legend.",
    ], chapter_label=LABEL)

    def make_boss():
        k = bestiary.make_hollow_king()
        k.pos = (5, 1)
        return [k]

    outcome = battle.battle_with_retry(
        player, make_boss, "The Heart of the Depths",
        art=art.HOLLOWKING_ART, player_start=(1, 2), can_flee=False,
        death_text=(
            "The Hollow King's crown catches the last of your strength "
            "and doesn't even seem to notice spending it. But he's had "
            "centuries of practice losing people who came back anyway."
        ),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "The Hollow King comes apart the way old porcelain comes apart - "
        "all at once, and completely. What's left of the crown rolls to "
        "a stop at your feet, cracked clean through, still faintly warm.",

        "The heart above you keeps beating. It was never really about "
        "him. He was just the last person foolish enough to stand this "
        "close to it and call that a victory.",
    ], chapter_label=LABEL)

    ui.clear()
    ui.print_art(art.CH5_INTERACTION)

    if tag == "resolve":
        flavor = (
            "Everything about tonight has been pointing here. You already "
            "know, standing over the crown, which choice actually feels "
            "like yours."
        )
    elif tag == "corruption":
        flavor = (
            "You can feel exactly how easy the crown would be to lift. "
            "Everything you've taken tonight has been leading, quietly, "
            "toward this."
        )
    else:
        flavor = (
            "Nothing about tonight has decided this for you. Whatever "
            "you choose now, it'll be the first thing down here that's "
            "entirely your own."
        )

    ui.narrate([
        "The heart offers you the same thing it offered him, and the "
        "one before him, and however many came before that: stay, take "
        "the crown, and everything you came here wanting is yours, for "
        "as long as you're willing to keep this place fed. Or walk away, "
        "and leave with nothing but your own name, still yours.",
        flavor,
    ], chapter_label=LABEL)

    idx = ui.menu(
        "The crown is waiting. What do you do?",
        [
            "Shatter the crown and walk back up, whatever it costs you",
            "Take the crown, and everything that comes with it",
        ],
    )

    ui.spaced_transition()
    return "resolve" if idx == 0 else "corruption"
