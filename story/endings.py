"""
story/endings.py
The two endings of HOLLOWGATE.
"""
from engine import ui, art


def show(player, ending):
    if ending == "resolve":
        _resolve_ending(player)
    else:
        _corruption_ending(player)


def _resolve_ending(player):
    ui.clear()
    ui.print_art(art.ENDING_RESOLVE_ART)
    ui.narrate(
        [
            f"{player.name} brings the crown down against the stone floor "
            "of the chamber, and it doesn't crack like porcelain this "
            "time - it crumbles, all at once, like something that was "
            "only ever pretending to be solid.",

            "The heart above you falters. Just once. Just enough.",

            f"You don't remember the whole climb back up. You remember "
            "the stairs getting easier, the torches lighting themselves "
            "ahead of you instead of behind, and the gate - the actual "
            "gate, the one at the top - standing open onto a sky you'd "
            "half-convinced yourself you'd never see get light again.",

            f"Aldenmoor is still dead above you. That much, Hollowgate "
            "never lied about. But you're standing in it, breathing "
            "actual air, and whatever you came down here for, you're "
            f"carrying it back up as {player.name} the {player.cls_display} "
            "- not as anything the gate got to keep a piece of.",

            "The gate will open again in a hundred years. It always "
            "does. That's someone else's descent to make.",

            "THE LONG ASCENSION",
        ],
        chapter_label="ENDING",
    )
    ui.press_enter("[Enter] ...")


def _corruption_ending(player):
    ui.clear()
    ui.print_art(art.ENDING_CORRUPTION_ART)
    ui.narrate(
        [
            f"{player.name} lifts the crown. It's lighter than it looks, "
            "and it fits - not comfortably, exactly, but completely, the "
            "way a wound fits the shape of whatever made it.",

            "The heart above you settles into a new rhythm, and you "
            "realize, distantly, that it's matching yours.",

            "You don't leave. You understand, the way you understand "
            "things down here instead of learning them, that leaving was "
            "never really on the table - not once you'd taken enough of "
            "what this place offers to make it this far.",

            f"Somewhere far above, Aldenmoor stays dead, the gate closes "
            "over the stairs, and the legend adjusts itself without any "
            "fuss: something waits beneath the chapel, now, and it isn't "
            f"the Hollow King anymore. It's {player.name}.",

            "You get everything you came here wanting. Hollowgate is "
            "very good at that part. It just never mentions, until "
            "after, that 'everything' includes the job of keeping the "
            "gate fed for the next hundred years.",

            "THE HOLLOW THRONE",
        ],
        chapter_label="ENDING",
    )
    ui.press_enter("[Enter] ...")
