"""
story/chapter2.py - THE SUNKEN ARCHIVE
"""
from engine import ui, battle, bestiary, art

LABEL = "CHAPTER II - THE SUNKEN ARCHIVE"


def run(player):
    ui.narrate(
        [
            "Water finds you before the room does - ankle-deep, black, "
            "and utterly still except where your boots disturb it. Shelves "
            "rise on every side, floor to ceiling, packed with books that "
            "have been rotting for longer than books should exist.",

            "This was a library, once. Or it wanted to be. Hollowgate "
            "remembers everything that's ever been written about it, and "
            "it apparently didn't like most of it.",
        ],
        chapter_label=LABEL,
        art=art.CH2_BG,
    )

    ui.narrate([
        "Something surfaces between two shelves - a shape built from wet "
        "cloth and old ink, mouth working around words that come out as "
        "bubbles instead of sound. A Drowned Wretch. It doesn't want to "
        "talk. It wants an audience, and it isn't picky about consent.",
    ], chapter_label=LABEL)

    def make_wretch_fight():
        w = bestiary.make_drowned_wretch()
        w.pos = (5, 1)
        return [w]

    outcome = battle.battle_with_retry(
        player, make_wretch_fight, "The Sunken Archive",
        art=art.WRETCH_ART, player_start=(1, 2),
    )
    if outcome == "quit":
        return "quit"

    # --- Interaction / alignment choice: the sealed door -------------------
    ui.clear()
    ui.print_art(art.CH2_INTERACTION)
    ui.narrate([
        "Past the last shelf, a door blocks the only dry path forward. No "
        "handle, no keyhole - just a question carved deep into the wood, "
        "in a language that somehow reads perfectly clearly anyway:",

        "\"A starving wolf finds a lamb, alone, too far from the flock to "
        "cry for help. What does the wolf do?\"",

        "There's no visible mechanism. You get the sense the door isn't "
        "asking what the wolf does. It's asking what you'd do, standing "
        "where the wolf is standing.",
    ], chapter_label=LABEL)

    idx = ui.menu(
        "How do you answer?",
        [
            "\"The wolf still has to eat something else, tonight.\"",
            "\"The wolf takes the lamb. That's what wolves are for.\"",
        ],
    )
    if idx == 0:
        ui.narrate([
            "The carving shifts, resettles, and the door swings inward "
            "without a sound. Whatever judged your answer seems, if not "
            "satisfied, at least willing to let you pass. You don't feel "
            "like you won an argument. You feel like you were tested for "
            "something else entirely.",
        ], chapter_label=LABEL)
        alignment = 2
    else:
        ui.narrate([
            "The door doesn't argue. It simply opens, the way something "
            "opens when it already suspected your answer and isn't "
            "disappointed. Somewhere in the dark ahead, you think you "
            "hear something that might almost be approval.",
        ], chapter_label=LABEL)
        alignment = -2

    ui.narrate([
        "Beyond the door, one book waits on a lectern, larger than the "
        "rest, chained shut with iron gone soft and wet with rot. As you "
        "approach, the chains creak - and pull taut on their own.",
    ], chapter_label=LABEL)

    def make_tome_fight():
        t = bestiary.make_bound_tome()
        t.pos = (5, 1)
        return [t]

    outcome = battle.battle_with_retry(
        player, make_tome_fight, "The Bound Tome's Alcove",
        art=art.TOME_ART, player_start=(1, 2), can_flee=False,
        death_text=(
            "The Bound Tome finds one more page to write you into, and "
            "the ink is cold. But Hollowgate isn't finished with your "
            "story yet."
        ),
    )
    if outcome == "quit":
        return "quit"

    ui.narrate([
        "The Tome's pages stop turning. Whatever grief was bound into it "
        "unravels into damp, ordinary paper, and for the first time since "
        "you stepped through the gate, the archive is quiet.",

        "You press on, deeper, past shelves that finally hold nothing "
        "but water and dust. Somewhere ahead, the passage begins to "
        "slope downward again.",
    ], chapter_label=LABEL)

    ui.spaced_transition()
    return alignment
