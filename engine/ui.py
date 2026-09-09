"""
engine/ui.py
Core display, input, and text-flow utilities for HOLLOWGATE.
Built to run safely in a plain Windows Command Prompt window:
ASCII-only output, no cursor tricks, no required external deps.
"""

import os
import sys
import time
import textwrap

try:
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init()
    COLOR = True
except Exception:
    COLOR = False

    class _NoColor:
        def __getattr__(self, _name):
            return ""

    Fore = _NoColor()
    Style = _NoColor()

WIDTH = 78
FAST_MODE = os.environ.get("HOLLOWGATE_FAST") == "1"

_SPEEDS = {"instant": 0.0, "fast": 0.006, "normal": 0.015}
_speed_name = "normal"

JOURNAL = []


def set_speed(name):
    global _speed_name
    if name in _SPEEDS:
        _speed_name = name


def clear():
    if FAST_MODE:
        return
    os.system("cls" if os.name == "nt" else "clear")


def color(text, fg):
    if not COLOR or not fg:
        return text
    return f"{fg}{text}{Style.RESET_ALL}"


def hr(char="=", width=WIDTH):
    print(char * width)


def banner(title, subtitle=None):
    print()
    hr("=")
    print(color(title.center(WIDTH), Fore.YELLOW))
    if subtitle:
        print(color(subtitle.center(WIDTH), Fore.LIGHTBLACK_EX))
    hr("=")
    print()


def print_art(art, centered=True, pad_top=0, pad_bottom=1):
    lines = art.strip("\n").split("\n")
    if centered:
        maxlen = max((len(l) for l in lines), default=0)
        pad = max(0, (WIDTH - maxlen) // 2)
        lines = [(" " * pad) + line for line in lines]
    for _ in range(pad_top):
        print()
    print("\n".join(lines))
    for _ in range(pad_bottom):
        print()


def type_out(text, fg=None, delay=None, end="\n"):
    if delay is None:
        delay = 0.0 if FAST_MODE else _SPEEDS.get(_speed_name, 0.015)
    if delay <= 0:
        print(color(text, fg))
        return
    prefix = fg if (fg and COLOR) else ""
    suffix = Style.RESET_ALL if (fg and COLOR) else ""
    sys.stdout.write(prefix)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(suffix + end)
    sys.stdout.flush()


def press_enter(msg="Press [Enter] to continue..."):
    input(color(f"\n{msg}", Fore.LIGHTBLACK_EX))


def spaced_transition(lines=16):
    press_enter("[Enter] ...")
    step = 0.0 if FAST_MODE else 0.02
    for _ in range(lines):
        print()
        if step:
            time.sleep(step)
    clear()


def menu(title, options, allow_back=False, back_label="Back"):
    display = list(options)
    if allow_back:
        display = display + [back_label]
    while True:
        if title:
            print()
            print(color(title, Fore.CYAN))
        for i, opt in enumerate(display, 1):
            print(f"  [{i}] {opt}")
        raw = input(color("> ", Fore.CYAN)).strip()
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= len(display):
                if allow_back and n == len(display):
                    return None
                return n - 1
        print(color("  (enter a number from the list)", Fore.RED))


def confirm(prompt):
    while True:
        raw = input(f"{prompt} (y/n) > ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False


def log_journal(chapter, text):
    JOURNAL.append((chapter, text))


def show_journal():
    clear()
    if not JOURNAL:
        banner("YOUR JOURNAL")
        print("Nothing written yet.")
        press_enter("[Enter] Back")
        return

    page_size = 5
    pages = [JOURNAL[i:i + page_size] for i in range(0, len(JOURNAL), page_size)]
    p = len(pages) - 1
    while True:
        clear()
        banner("YOUR JOURNAL", f"page {p + 1} of {len(pages)}")
        start = p * page_size
        for offset, (chap, text) in enumerate(pages[p]):
            tag = f"[{chap}] " if chap else ""
            wrapped = textwrap.fill(
                f"{start + offset + 1}. {tag}{text}",
                width=WIDTH - 2, subsequent_indent="    ",
            )
            print(wrapped)
            print()
        opts = []
        if p > 0:
            opts.append("Previous page")
        if p < len(pages) - 1:
            opts.append("Next page")
        opts.append("Back to game")
        idx = menu("", opts)
        picked = opts[idx]
        if picked == "Previous page":
            p -= 1
        elif picked == "Next page":
            p += 1
        else:
            return


def narrate(beats, chapter_label="", art=None):
    if isinstance(beats, str):
        beats = [beats]
    i = 0
    logged = set()
    n = len(beats)
    while i < n:
        clear()
        if chapter_label:
            print(color(chapter_label, Fore.YELLOW))
            print(color("-" * min(WIDTH, len(chapter_label)), Fore.YELLOW))
            print()
        if art and i == 0:
            print_art(art)
        wrapped = textwrap.fill(beats[i], width=WIDTH)
        type_out(wrapped)
        if i not in logged:
            log_journal(chapter_label, beats[i])
            logged.add(i)
        print()
        raw = input(
            color("[Enter] Continue   [R] Reread   [J] Journal\n> ", Fore.LIGHTBLACK_EX)
        ).strip().lower()
        if raw == "r":
            continue
        if raw == "j":
            show_journal()
            continue
        i += 1


def hp_bar(current, maximum, width=24, label="HP"):
    current_disp = max(0, current)
    ratio = (current_disp / maximum) if maximum else 0
    filled = min(width, int(width * ratio))
    bar = "#" * filled + "-" * (width - filled)
    if ratio > 0.5:
        c = Fore.GREEN
    elif ratio > 0.2:
        c = Fore.YELLOW
    else:
        c = Fore.RED
    return f"{label:<7}[{color(bar, c)}] {current_disp}/{maximum}"


def res_bar(current, maximum, width=24, label="MP"):
    ratio = (current / maximum) if maximum else 0
    filled = min(width, int(width * ratio))
    bar = "#" * filled + "-" * (width - filled)
    return f"{label:<7}[{color(bar, Fore.CYAN)}] {current}/{maximum}"
