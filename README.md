# Hollowgate - Dungeons and Dragons (5 chapters)
Dungeons and Dragons adventure in command prompt, with grid based movement, bosses, classes, and biomes. 
A one-shot ASCII dungeon crawler for the Windows Command Prompt.

*"Some doors are not meant to open."*

Once a century, a gate beneath the dead town of Aldenmoor opens. It
grants whoever survives the descent whatever they came for - it just
never mentions the cost until you're already holding it. Tonight, the
gate is open, and you're standing in front of it.

## How to launch

**Easiest way:** Double-click **`Launch Hollowgate.bat`**. It will open
a Command Prompt window, check that Python is installed, quietly install
the one small optional dependency (`colorama`, for color), and start the
game. Nothing else is required.

If double-clicking doesn't work (some systems block `.bat` files from
unfamiliar sources), open Command Prompt yourself, `cd` into this
folder, and run:

```
python main.py
```

**Requirements:** Python 3.8 or newer. Get it from
[python.org/downloads](https://www.python.org/downloads/) if you don't
already have it - during installation, check "Add python.exe to PATH".
`colorama` is optional; the game runs fine without it, just without
color.

## What's in the box

- **4 playable classes**: Warrior, Rogue, Mage, and Cleric, each with a
  distinct kit of 4 abilities, its own resource (Stamina / Focus / Mana
  / Faith), and its own movement speed and armor class.
- **5 chapters**, each with its own background art, its own monsters,
  an interactive story beat, and a chapter-ending fight.
- **A grid-based tactical battle system** - move around a small
  battlefield, flank, kite, and manage range instead of just mashing
  attack. Bosses telegraph their big attacks a turn in advance.
- **A branching ending** - the choices you make across the game (and
  the choice you make at the very end) lead to one of two very
  different final chapters.
- **A journal** - press `J` after any story passage to reread anything
  you've read so far, or `R` to reread just the passage in front of you.
- **A lot of hand-drawn ASCII art** - class portraits, monsters, bosses,
  backgrounds, and story-interaction art, all built from plain ASCII so
  it renders correctly in a stock Command Prompt window.

## Controls

Every menu in the game is a numbered list. Type the number of your
choice and press Enter. That's the whole control scheme.

Full instructions (including how the dice-based combat works) are also
available from the in-game **How to Play** menu.

## Notes

- The game is entirely self-contained in this folder - `main.py` plus
  the `engine/` and `story/` folders. Don't separate them.
- There's no save file. It's meant to be played start to finish in one
  sitting (roughly 20-40 minutes depending on how much you explore the
  Journal and how many retries a boss costs you).
- Dying in a fight doesn't end your run - Hollowgate just makes you try
  that fight again. The only way to actually stop partway is to choose
  to give up when offered, or close the window.

Good luck down there.

