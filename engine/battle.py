"""
engine/battle.py
The grid-based tactical battle system that powers every fight in the game.
"""

import random

from . import ui, dice
from .entities import Ability

GRID_W = 7
GRID_H = 4

DIRECTIONS = [("North", (0, -1)), ("South", (0, 1)), ("East", (1, 0)), ("West", (-1, 0))]


def grid_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


class Grid:
    def __init__(self, obstacles=None):
        self.obstacles = set(obstacles or [])

    def in_bounds(self, x, y):
        return 0 <= x < GRID_W and 0 <= y < GRID_H

    def blocked(self, x, y):
        return (x, y) in self.obstacles


def _hp_tier(hp, maxhp):
    r = hp / maxhp if maxhp else 0
    if r <= 0:
        return "Defeated"
    if r > 0.75:
        return "Unharmed"
    if r > 0.5:
        return "Wounded"
    if r > 0.25:
        return "Bloodied"
    return "Near Death"


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(player, enemies, grid, log, arena_name, art=None):
    ui.clear()
    ui.hr("=")
    print((" " + arena_name + " ").center(ui.WIDTH, "="))
    ui.hr("=")
    if art:
        ui.print_art(art, pad_bottom=1)

    occupied = {player.pos: "@"}
    for e in enemies:
        if e.is_alive():
            occupied[e.pos] = e.symbol

    header = "      " + "".join(f"  {c + 1} " for c in range(GRID_W))
    print(header)
    sep = "    " + "+---" * GRID_W + "+"
    print(sep)
    for y in range(GRID_H):
        row_label = chr(ord('A') + y)
        row = f" {row_label}  |"
        for x in range(GRID_W):
            if (x, y) in grid.obstacles:
                cell = " # "
            else:
                cell = f" {occupied.get((x, y), '.')} "
            row += cell + "|"
        print(row)
        print(sep)
    print()

    print(ui.hp_bar(player.hp, player.max_hp, label=player.name[:7]))
    print(ui.res_bar(player.res, player.max_res, label=player.res_name[:7]))
    print()
    for e in enemies:
        if e.is_alive():
            tier = _hp_tier(e.hp, e.max_hp)
            print(ui.hp_bar(e.hp, e.max_hp, label=e.name[:7]) + f"  ({tier})")
    print()
    ui.hr("-")
    for line in log[-6:]:
        print(line)
    ui.hr("-")


# ---------------------------------------------------------------------------
# Combat resolution
# ---------------------------------------------------------------------------

def resolve_attack(attacker, defender, ability, log):
    d20 = dice.d20()

    if d20 == 1:
        log.append(f"{attacker.name} attacks with {ability.name}... and fumbles badly.")
        return

    hit_bonus = attacker.effective_hit_bonus()
    total = d20 + hit_bonus
    target_ac = defender.effective_ac()
    crit = (d20 == 20)
    hit = crit or total >= target_ac

    if not hit:
        log.append(f"{attacker.name} uses {ability.name} ({total} vs AC {target_ac}) - MISS.")
        return

    dmg, _detail = dice.roll(ability.dice)
    dmg += attacker.buff_dmg

    note = ""
    if ability.extra.get("bonus_if_charging") and getattr(defender, "charging", False):
        dmg = int(dmg * 1.5)
        note = " (bonus - they never saw it coming!)"
    if ability.extra.get("execute_threshold") and defender.max_hp and \
            defender.hp <= defender.max_hp * ability.extra["execute_threshold"]:
        crit = True

    if crit:
        dmg = dmg * 2
        note += " CRITICAL HIT!"

    dmg = max(1, dmg)
    defender.take_damage(dmg)
    log.append(f"{attacker.name} uses {ability.name} ({total} vs AC {target_ac}) - HIT for {dmg} damage!{note}")

    if ability.extra.get("poison_turns") and defender.is_alive():
        defender.status["poison"] = ability.extra["poison_turns"]
        defender.status["poison_dice"] = ability.extra["poison_dice"]
        log.append(f"{defender.name} is poisoned!")

    if ability.extra.get("weaken_hit") and defender.is_alive():
        defender.status["weaken"] = ability.extra.get("weaken_turns", 1)
        defender.weaken_hit = ability.extra["weaken_hit"]
        log.append(f"{defender.name} is slowed by the frost!")

    if not defender.is_alive():
        log.append(f"{defender.name} falls.")


def apply_self_ability(user, ability, log):
    if ability.kind == "heal":
        amt, _detail = dice.roll(ability.extra["heal_dice"])
        user.heal(amt)
        log.append(f"{user.name} uses {ability.name} and recovers {amt} HP!")
        return

    if ability.kind == "buff":
        turns = ability.extra.get("turns", 2)
        if "buff_def" in ability.extra:
            user.status["def_buff"] = turns
            user.status["def_buff_amt"] = ability.extra["buff_def"]
            user.def_bonus += ability.extra["buff_def"]
        if "buff_hit" in ability.extra:
            user.status["hit_buff"] = turns
            user.status["hit_buff_amt"] = ability.extra["buff_hit"]
            user.buff_hit += ability.extra["buff_hit"]
        if "buff_dmg" in ability.extra:
            user.status["dmg_buff"] = turns
            user.status["dmg_buff_amt"] = ability.extra["buff_dmg"]
            user.buff_dmg += ability.extra["buff_dmg"]
        if "shield" in ability.extra:
            amt, _detail = dice.roll(ability.extra["shield"])
            user.shield += amt
            log.append(f"A ward absorbs the next {amt} damage.")
        log.append(f"{user.name} uses {ability.name}!")


def tick_status(entity, log):
    if not entity.is_alive():
        return

    if entity.status.get("poison", 0) > 0:
        amt, _detail = dice.roll(entity.status.get("poison_dice", "1d4"))
        entity.take_damage(amt)
        log.append(f"{entity.name} takes {amt} poison damage.")
        entity.status["poison"] -= 1
        if entity.status["poison"] <= 0:
            entity.status.pop("poison", None)
            entity.status.pop("poison_dice", None)
            log.append(f"The poison in {entity.name}'s blood fades.")
        if not entity.is_alive():
            return

    if entity.status.get("def_buff", 0) > 0:
        entity.status["def_buff"] -= 1
        if entity.status["def_buff"] <= 0:
            entity.def_bonus -= entity.status.pop("def_buff_amt", 0)
            entity.status.pop("def_buff", None)
            log.append(f"{entity.name}'s guard relaxes.")

    if entity.status.get("hit_buff", 0) > 0:
        entity.status["hit_buff"] -= 1
        if entity.status["hit_buff"] <= 0:
            entity.buff_hit -= entity.status.pop("hit_buff_amt", 0)
            entity.status.pop("hit_buff", None)

    if entity.status.get("dmg_buff", 0) > 0:
        entity.status["dmg_buff"] -= 1
        if entity.status["dmg_buff"] <= 0:
            entity.buff_dmg -= entity.status.pop("dmg_buff_amt", 0)
            entity.status.pop("dmg_buff", None)

    if entity.status.get("weaken", 0) > 0:
        entity.status["weaken"] -= 1
        if entity.status["weaken"] <= 0:
            entity.status.pop("weaken", None)
            entity.weaken_hit = 0


# ---------------------------------------------------------------------------
# Player turn
# ---------------------------------------------------------------------------

def player_turn(player, alive_enemies, grid, can_flee, log):
    while True:
        options = ["Move", "Attack", "Ability", "Item", "Info"]
        if can_flee:
            options.append("Flee")
        idx = ui.menu("What do you do?", options)
        choice = options[idx]

        if choice == "Move":
            if _do_move(player, grid, alive_enemies, log):
                return "continue"
            continue

        if choice == "Attack":
            if _do_ability(player, player.basic(), alive_enemies, grid, log):
                return "continue"
            continue

        if choice == "Ability":
            ab = _choose_ability(player)
            if ab is None:
                continue
            if ab.cost > player.res:
                print(f"Not enough {player.res_name}.")
                ui.press_enter()
                continue
            if _do_ability(player, ab, alive_enemies, grid, log):
                return "continue"
            continue

        if choice == "Item":
            if _use_item(player, log):
                return "continue"
            continue

        if choice == "Info":
            _show_info(player, alive_enemies)
            continue

        if choice == "Flee":
            chance = 0.4 + 0.1 * player.move_range
            if random.random() < chance:
                log.append(f"{player.name} slips away into the dark.")
                return "fled"
            log.append(f"{player.name} tries to flee, but can't break away!")
            return "continue"


def _do_move(player, grid, enemies, log):
    remaining = player.move_range
    moved = False
    while remaining > 0:
        occupied = {e.pos for e in enemies if e.is_alive()}
        labels = [d[0] for d in DIRECTIONS]
        stop_label = "Stop here" if moved else "Cancel"
        idx = ui.menu(
            f"Move where? ({remaining} step{'s' if remaining != 1 else ''} left)",
            labels + [stop_label],
        )
        if idx == len(labels):
            break
        dx, dy = DIRECTIONS[idx][1]
        nx, ny = player.pos[0] + dx, player.pos[1] + dy
        if not grid.in_bounds(nx, ny):
            print("The wall stops you there.")
            ui.press_enter()
            continue
        if grid.blocked(nx, ny):
            print("Something blocks the way.")
            ui.press_enter()
            continue
        if (nx, ny) in occupied:
            print("That space is occupied.")
            ui.press_enter()
            continue
        player.pos = (nx, ny)
        moved = True
        remaining -= 1
    return moved


def _choose_ability(player):
    opts = [a.blurb(player.res_name) for a in player.abilities]
    idx = ui.menu("Choose an ability:", opts, allow_back=True, back_label="Back")
    if idx is None:
        return None
    return player.abilities[idx]


def _do_ability(player, ability, alive_enemies, grid, log):
    if ability.kind in ("heal", "buff"):
        apply_self_ability(player, ability, log)
        player.res -= ability.cost
        return True

    in_range = [e for e in alive_enemies if grid_distance(player.pos, e.pos) <= ability.range]
    if not in_range:
        print(f"No target within range {ability.range} for {ability.name}.")
        ui.press_enter()
        return False

    player.res -= ability.cost

    if ability.kind == "aoe_attack":
        for e in in_range:
            resolve_attack(player, e, ability, log)
        return True

    if len(in_range) == 1:
        target = in_range[0]
    else:
        names = [f"{e.name} ({e.hp}/{e.max_hp} HP)" for e in in_range]
        tidx = ui.menu("Choose a target:", names)
        target = in_range[tidx]

    resolve_attack(player, target, ability, log)
    return True


def _use_item(player, log):
    items = [(k, v) for k, v in player.inventory.items() if v > 0]
    if not items:
        print("You have nothing to use.")
        ui.press_enter()
        return False
    labels = [f"{k} x{v}" for k, v in items]
    idx = ui.menu("Use which item?", labels, allow_back=True)
    if idx is None:
        return False
    key = items[idx][0]
    if key == "Healing Potion":
        amt, _detail = dice.roll("2d8+4")
        player.heal(amt)
        player.inventory[key] -= 1
        log.append(f"{player.name} drinks a Healing Potion and recovers {amt} HP.")
        return True
    if key == "Elixir":
        player.hp = player.max_hp
        player.status = {}
        player.inventory[key] -= 1
        log.append(f"{player.name} drinks the Elixir. Every wound closes at once.")
        return True
    return False


def _show_info(player, enemies):
    ui.clear()
    ui.banner(f"{player.name} the {player.cls_display}")
    print(ui.hp_bar(player.hp, player.max_hp))
    print(ui.res_bar(player.res, player.max_res, label=player.res_name))
    print(f"Armor Class: {player.effective_ac()}   Move: {player.move_range} tile(s)/turn")
    print()
    print("Abilities:")
    for a in player.abilities:
        print(f"  - {a.blurb(player.res_name)}")
    if player.status:
        print("\nActive effects:", ", ".join(player.status.keys()))
    print("\nEnemies:")
    for e in enemies:
        if e.is_alive():
            print(f"  - {e.name}: {_hp_tier(e.hp, e.max_hp)} ({e.hp}/{e.max_hp} HP)")
    ui.press_enter()


# ---------------------------------------------------------------------------
# Enemy AI
# ---------------------------------------------------------------------------

def _move_toward(mover, target_pos, grid, blocked_positions, steps):
    for _ in range(max(1, steps)):
        dx = _clamp(target_pos[0] - mover.pos[0], -1, 1)
        dy = _clamp(target_pos[1] - mover.pos[1], -1, 1)
        if dx == 0 and dy == 0:
            break
        if abs(target_pos[0] - mover.pos[0]) >= abs(target_pos[1] - mover.pos[1]):
            order = [(dx, 0), (0, dy)]
        else:
            order = [(0, dy), (dx, 0)]
        moved = False
        for ddx, ddy in order:
            if ddx == 0 and ddy == 0:
                continue
            nx, ny = mover.pos[0] + ddx, mover.pos[1] + ddy
            if grid.in_bounds(nx, ny) and not grid.blocked(nx, ny) and (nx, ny) not in blocked_positions:
                mover.pos = (nx, ny)
                moved = True
                break
        if not moved:
            break


def _move_away(mover, target_pos, grid, blocked_positions, steps):
    for _ in range(max(1, steps)):
        dx = -_clamp(target_pos[0] - mover.pos[0], -1, 1)
        dy = -_clamp(target_pos[1] - mover.pos[1], -1, 1)
        if dx == 0 and dy == 0:
            dx = random.choice([-1, 1])
        order = [(dx, 0), (0, dy)]
        moved = False
        for ddx, ddy in order:
            if ddx == 0 and ddy == 0:
                continue
            nx, ny = mover.pos[0] + ddx, mover.pos[1] + ddy
            if grid.in_bounds(nx, ny) and not grid.blocked(nx, ny) and (nx, ny) not in blocked_positions:
                mover.pos = (nx, ny)
                moved = True
                break
        if not moved:
            break


def enemy_turn(enemy, player, all_enemies, grid, log):
    if not enemy.is_alive():
        return

    others = {e.pos for e in all_enemies if e is not enemy and e.is_alive()} | {player.pos}

    if enemy.charging:
        _execute_special(enemy, player, log)
        enemy.charging = False
        return

    if enemy.ai == "boss":
        _boss_ai(enemy, player, grid, others, log)
        return

    dist = grid_distance(enemy.pos, player.pos)

    if enemy.ai == "aggressive":
        if dist > enemy.atk_range:
            _move_toward(enemy, player.pos, grid, others - {player.pos}, enemy.speed)
            dist = grid_distance(enemy.pos, player.pos)
        if dist <= enemy.atk_range:
            resolve_attack(enemy, player, enemy.basic_ability, log)

    elif enemy.ai == "ranged":
        if dist <= 1 and enemy.speed > 0:
            _move_away(enemy, player.pos, grid, others - {player.pos}, 1)
            dist = grid_distance(enemy.pos, player.pos)
        elif dist > enemy.atk_range:
            _move_toward(enemy, player.pos, grid, others - {player.pos}, enemy.speed)
            dist = grid_distance(enemy.pos, player.pos)
        if dist <= enemy.atk_range:
            resolve_attack(enemy, player, enemy.basic_ability, log)
        else:
            log.append(f"{enemy.name} can't find an angle to strike.")


def _boss_ai(enemy, player, grid, others, log):
    enemy.turn_count += 1

    for step in enemy.enrage_steps:
        if not step["done"] and enemy.hp <= enemy.max_hp * step["threshold"]:
            step["done"] = True
            enemy.hit_bonus += step.get("hit_bonus", 0)
            enemy.speed = step.get("speed", enemy.speed)
            if "dmg_dice" in step:
                enemy.dmg_dice = step["dmg_dice"]
                enemy.basic_ability.dice = step["dmg_dice"]
            if "cooldown" in step:
                enemy.special_cooldown = step["cooldown"]
            log.append(f"*** {step['message']} ***")

    if enemy.special and not enemy.charging and enemy.turn_count % enemy.special_cooldown == 0:
        enemy.charging = True
        log.append(f">> {enemy.special['telegraph']}")
        return

    dist = grid_distance(enemy.pos, player.pos)
    if dist > enemy.atk_range:
        _move_toward(enemy, player.pos, grid, others - {player.pos}, enemy.speed)
        dist = grid_distance(enemy.pos, player.pos)
    if dist <= enemy.atk_range:
        resolve_attack(enemy, player, enemy.basic_ability, log)


def _execute_special(enemy, player, log):
    special = enemy.special
    log.append(f">>> {enemy.name} unleashes {special['name']}! <<<")
    if special["kind"] == "aoe_radius":
        if grid_distance(enemy.pos, player.pos) <= special["radius"]:
            amt, _detail = dice.roll(special["dice"])
            player.take_damage(amt)
            log.append(f"You're caught in it for {amt} damage!")
        else:
            log.append("You were far enough away - it misses you completely!")
    elif special["kind"] == "single":
        temp = Ability("special", special["name"], 0, special["dice"], 99, "attack", "")
        resolve_attack(enemy, player, temp, log)


# ---------------------------------------------------------------------------
# Battle loop
# ---------------------------------------------------------------------------

def run_battle(player, enemies, arena_name="Battle", art=None, obstacles=None,
               player_start=(1, 1), can_flee=True):
    grid = Grid(obstacles)
    player.pos = player_start
    log = [f"You enter {arena_name}."]

    while True:
        alive = [e for e in enemies if e.is_alive()]
        if not alive:
            render(player, enemies, grid, log, arena_name, art)
            return "victory"
        if not player.is_alive():
            render(player, enemies, grid, log, arena_name, art)
            return "defeat"

        tick_status(player, log)
        player.regen()
        if not player.is_alive():
            render(player, enemies, grid, log, arena_name, art)
            return "defeat"

        render(player, enemies, grid, log, arena_name, art)
        result = player_turn(player, alive, grid, can_flee, log)
        if result == "fled":
            return "fled"

        alive = [e for e in enemies if e.is_alive()]
        if not alive:
            render(player, enemies, grid, log, arena_name, art)
            return "victory"

        for e in alive:
            if not e.is_alive():
                continue
            tick_status(e, log)
            if not e.is_alive():
                continue
            enemy_turn(e, player, enemies, grid, log)
            if not player.is_alive():
                render(player, enemies, grid, log, arena_name, art)
                return "defeat"


def battle_with_retry(player, make_enemies_fn, arena_name, art=None, obstacles=None,
                       player_start=(1, 1), can_flee=True, death_text=None):
    while True:
        enemies = make_enemies_fn()
        outcome = run_battle(player, enemies, arena_name, art, obstacles, player_start, can_flee)
        if outcome in ("victory", "fled"):
            return outcome

        ui.clear()
        ui.banner("YOU HAVE FALLEN")
        ui.type_out(death_text or (
            "Darkness closes in around you... but Hollowgate isn't finished "
            "with you yet. Not like this."
        ))
        again = ui.menu("", ["Rise and fight again", "Give up and return to the title screen"])
        if again != 0:
            return "quit"
        player.full_restore()
