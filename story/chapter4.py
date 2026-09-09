"""
story/chapter4.py - THE MIRROR HALLS
"""
from engine import ui, battle, bestiary, art

LABEL = "CHAPTER IV - THE MIRROR HALLS"

_MEMORY_BEATS = {
    "warrior": (
        "The glass shows you a field after a battle that already ended "
        "without you. You see yourself walking it, looking for a reason "
        "the fighting mattered, and not finding one. Your reflection "
        "looks back at you instead of at the field. It looks like it's "
        "still looking for the reason. It looks like it might not need "
        "to find one anymore."
    ),
    "rogue": (
        "The glass shows you the debt - a face you owe something to that "
        "doesn't get owed things anymore, not the way the living do. You "
        "see yourself trying to pay it anyway, into an account that "
        "might not exist. Your reflection isn't trying. Your reflection "
        "looks like it already spent the payment on itself."
    ),
    "mage": (
        "The glass shows you the theory, laid out the way you always "
        "imagined it: death, solved, like an equation with the last "
        "variable finally filled in. You see yourself reaching for the "
        "answer. Your reflection is already holding it, and it isn't "
        "sharing."
    ),
    "cleric": (
        "The glass shows you the deathbed, the promise, the moment you "
        "said yes to something your faith says shouldn't be kept. You "
        "see yourself still trying to keep it. Your reflection has "
        "stopped trying and started demanding - as if the promise owes "
        "it something now, instead of the other way around."
    ),
}


def run(player):
    ui.narrate(
        [
            "The hall ahead is lined, floor to ceiling, with mirrors that "
            "don't quite agree on what they're reflecting. In some of "
            "them you're taller. In others, older. In one, near the "
            "middle, you aren't moving at all, and it takes you an "
            "uncomfortably long moment to be sure that one's the fake.",
        ],
        chapter_label=LABEL,
        art=art.CH4_BG,
    )

    ui.clear()
    ui.print_art(art.CH4_INTERACTION)
    ui.narrate([
        _MEMORY_BEATS.get(player.cls_key, _MEMORY_BEATS["warrior"]),
        "The reflection raises a hand. You feel, more than decide, that "
        "it's waiting to see what you do with yours.",
    ], chapter_label=LABEL)

    idx = ui.menu(
        "What do you do?",
        [
            "Let it go - lower your hand, and mean it",
            "Match it - raise your hand back, and accept what it's showing you",
        ],
    )
    if idx == 0:
        ui.narrate([
            "You lower your hand. Something in the glass ripples, "
            "displeased, like a door closing on a room it wanted you to "
            "stay in. It's not gone. But for now, it's just a reflection "
            "again - nothing more, nothing that gets to decide anything "
            "about who you are.",
        ], chapter_label=LABEL)
        alignment = 2
    else:
        ui.narrate([
            "You raise your hand back, matching it exactly, and for a "
            "moment the glass isn't glass at all - it's a door, and "
            "you're both standing in the frame. Something passes between "
            "you that you don't have a word for yet. You have a feeling "
            "you're about to find out what it costs.",
        ], chapter_label=LABEL)
        alignment = -2

    ui.narrate([
        "Every mirror in the hall shatters at once, inward, and the glass "
        "gathers itself into a single shape standing where the reflections "
        "used to be - built from your own silhouette, moving the way you "
        "move, armed with everything you know how to use.",
    ], chapter_label=LABEL)

    def make_mirror_fight():
        m = bestiary.make_mirror_self(player)
        m.pos = (5, 1)
        return [m]

    outcome = battle.battle_with_retry(
        player, make_mirror_fight, "The Shattered Hall",
        art=art.MIRROR_ART, player_start=(1, 2), can_flee=False,
        death_text=(
            "It knows exactly how this ends, because it's watched you "
            "get here the same way you did. But it hasn't seen everything "
            "yet."
        ),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "The reflection comes apart into ordinary broken glass, and for "
        "just a second before it does, its face isn't wearing your "
        "expression anymore. It's wearing something almost like relief.",

        "Beyond the ruined hall, the passage slopes down one final time, "
        "toward a warmth that has no business being this far underground.",
    ], chapter_label=LABEL)

    ui.spaced_transition()
    return alignment
