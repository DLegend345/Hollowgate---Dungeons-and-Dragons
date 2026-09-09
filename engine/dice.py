"""
engine/dice.py
Tiny dice-notation roller used everywhere combat math happens.
"""

import random
import re

_DICE_RE = re.compile(r"^(\d+)d(\d+)([+-]\d+)?$")


def roll(notation):
    if not notation:
        return 0, "0"
    m = _DICE_RE.match(notation.replace(" ", ""))
    if not m:
        raise ValueError(f"Bad dice notation: {notation!r}")
    num, sides, mod = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    rolls = [random.randint(1, sides) for _ in range(num)]
    total = sum(rolls) + mod
    parts = "+".join(str(r) for r in rolls)
    if mod:
        parts += f"{'+' if mod > 0 else ''}{mod}"
    return max(0, total), parts


def d20():
    return random.randint(1, 20)
