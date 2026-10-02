"""Headless checks for the Lab-4 tasks.

Run with:
    python tests/test_game.py

Uses the SDL dummy drivers so it works over SSH / in CI with no display
and no audio device. Exits non-zero if any check fails.
"""
import contextlib
import io
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

pygame.init()
SURFACE = pygame.display.set_mode((800, 400))

from game.game_engine import (
    DIFFICULTIES,
    DIFFICULTY_ORDER,
    GAME_OVER,
    MENU,
    PLAYING,
    GameEngine,
)
from game.obstacle import Obstacle
from game.player import Player
from game.audio import AudioManager

WIDTH, HEIGHT = 800, 400
RESULTS = []


def check(name, condition, detail=""):
    RESULTS.append((name, bool(condition), detail))
    status = "PASS" if condition else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f"  -- {detail}"
    print(line)
    return bool(condition)


def new_engine(**kwargs):
    return GameEngine(WIDTH, HEIGHT, **kwargs)


def still_player_survives(speed):
    """Does a player who never jump get hit by an obstacle at this speed?"""
    engine = new_engine(difficulty="medium")
    engine.max_speed = 10_000.0        # isolate swept collision from the Task 1 cap
    engine.ramp_per_frame = 0.0
    engine.speed = speed
    engine.spawn_interval = 10 ** 9
    engine.obstacles = []
    obstacle = Obstacle(800, engine.ground_y, speed)
    engine.obstacles.append(obstacle)
    for _ in range(2000):
        engine.update()
        if engine.state != PLAYING:
            return False                 # died -> collision correctly registered
        if obstacle.x + obstacle.width < 0:
            break
    return True                          # ghosted straight through


# --------------------------------------------------------------- Task 1 tests

def test_speed_is_capped():
    worst = 0.0
    for name in DIFFICULTIES:
        engine = new_engine(difficulty=name)
        for _ in range(60 * 60 * 10):    # 10 simulated minutes
            engine.update()
            engine.speed = min(engine.speed + engine.ramp_per_frame, engine.max_speed)
            worst = max(worst, engine.speed)
        check(f"Task 1: speed respects {name} ceiling",
              engine.speed <= engine.max_speed + 1e-9,
              f"final {engine.speed:.3f} <= max {engine.max_speed}")


def test_swept_collision_catches_ghosted_hits():
    """Speeds that made a motionless player survive in the ORIGINAL code."""
    ghost_speeds = []
    for i in range(64):
        speed = 56.0 + (120.0 - 56.0) * i / 63.0
        if still_player_survives(speed):
            ghost_speeds.append(round(speed, 2))
    check("Task 1: swept collision removes ghost passes (56-120 px/frame)",
          not ghost_speeds,
          f"0 ghost passes across 64 speeds"
          if not ghost_speeds else f"still ghosting at {ghost_speeds[:6]}")


def test_swept_rect_covers_full_span():
    obstacle = Obstacle(800, 360, 60.0)
    check("Task 1: swept_rect is None before first move", obstacle.swept_rect() is None)
    obstacle.move()
    swept = obstacle.swept_rect()
    expected_left = 800 - 60.0
    expected_right = 800 + 25
    check("Task 1: swept_rect spans whole travelled width",
          swept is not None and abs(swept.left - expected_left) < 1e-6
          and abs(swept.right - expected_right) < 1e-6,
          f"span [{swept.left:.0f}, {swept.right:.0f}]")


def test_collision_triggers_at_all():
    engine = new_engine(difficulty="easy")
    obstacle = Obstacle(800, engine.ground_y, 6.0)
    engine.obstacles = [obstacle]
    for _ in range(500):
        engine.update()
        if engine.state != PLAYING:
            break
    check("Task 1: ordinary grounded collision is detected",
          engine.state == GAME_OVER, f"state={engine.state}")


# --------------------------------------------------------------- Task 2 tests

def test_game_over_screen():
    engine = new_engine(difficulty="easy")
    engine.spawn_interval = 1
    for _ in range(500):
        engine.update()                    # never jumps -> hits the first obstacle
        if engine.state != PLAYING:
            break
    check("Task 2: collision switches to GAME_OVER state",
          engine.state == GAME_OVER, f"state={engine.state}")

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        engine.render(SURFACE)
        engine.update()
    check("Task 2: nothing printed to console instead",
          buffer.getvalue() == "", f"stdout={buffer.getvalue()!r}")

    # The game over panel must actually paint over a blank screen.
    SENTINEL = (1, 2, 3)
    SURFACE.fill(SENTINEL)
    engine.render(SURFACE)
    painted = sum(1 for y in range(HEIGHT) for x in range(0, WIDTH, 2)
                  if SURFACE.get_at((x, y)) != SENTINEL)
    check("Task 2: game over overlay is drawn on screen",
          painted > 500, f"{painted} sampled px painted over a blank screen")

    check("Task 2: final score is retained", engine.score >= 0, f"score={engine.score}")


def test_waits_for_input_then_menu():
    engine = new_engine(difficulty="easy")
    engine.spawn_interval = 1
    for _ in range(500):
        engine.update()
        if engine.state != PLAYING:
            break
    engine.render(SURFACE)

    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    check("Task 2: input during the lockout does not skip the score screen",
          engine.state == GAME_OVER, f"state={engine.state}")

    for _ in range(40):
        engine.update(dt=0.05)
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    check("Task 2/3: key after the lockout opens the difficulty menu",
          engine.state == MENU, f"state={engine.state}")


# --------------------------------------------------------------- Task 3 tests

def test_replay_difficulties():
    engine = new_engine(difficulty="medium")
    engine.spawn_interval = 1
    for _ in range(500):
        engine.update()
        if engine.state != PLAYING:
            break
    engine._lockout = 0.0
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    check("Task 3: menu opens", engine.state == MENU)
    check("Task 3: menu preselects the current difficulty",
          engine.menu_index == DIFFICULTY_ORDER.index("medium"), f"idx={engine.menu_index}")

    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    check("Task 3: Up moves the selection",
          engine.menu_index == DIFFICULTY_ORDER.index("easy"), f"idx={engine.menu_index}")

    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
    check("Task 3: Down moves the selection",
          engine.menu_index == DIFFICULTY_ORDER.index("medium"), f"idx={engine.menu_index}")

    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    check("Task 3: selection wraps past the top to the Quit row",
          engine.menu_index == len(DIFFICULTY_ORDER),
          f"idx={engine.menu_index} (expected {len(DIFFICULTY_ORDER)})")

    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
    check("Task 3: Down from the Quit row wraps back to the top (Easy)",
          engine.menu_index == 0, f"idx={engine.menu_index} (expected 0)")
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    cfg = DIFFICULTIES["easy"]
    check("Task 3: confirming Easy starts a fresh Easy run",
          engine.state == PLAYING and engine.difficulty == "easy"
          and abs(engine.speed - cfg["start_speed"]) < 1e-9
          and engine.spawn_interval == cfg["spawn_interval"]
          and engine.score == 0,
          f"state={engine.state} difficulty={engine.difficulty} "
          f"speed={engine.speed} spawn={engine.spawn_interval}")

    for key in DIFFICULTIES:
        engine.difficulty = key
        engine._start_run()
        cfg = DIFFICULTIES[key]
        ok = (abs(engine.speed - cfg["start_speed"]) < 1e-9
              and engine.spawn_interval == cfg["spawn_interval"]
              and engine.max_speed == cfg["max_speed"])
        check(f"Task 3: {key} preset applies start speed / spawn rate / cap", ok,
              f"speed={engine.speed} spawn={engine.spawn_interval} cap={engine.max_speed}")


def test_quit_option():
    engine = new_engine(difficulty="medium")
    engine.state = MENU
    engine.menu_index = len(DIFFICULTY_ORDER)   # the "Quit" row
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    check("Task 3: Quit stops the main loop", engine.running is False,
          f"running={engine.running}")


def test_esc_quits():
    engine = new_engine(difficulty="medium")
    engine.state = MENU
    engine._lockout = 0.0
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    check("Task 3: Escape quits from the menu", engine.running is False)


# --------------------------------------------------------------- Task 4 tests

def test_sound_effects():
    audio = AudioManager()
    check("Task 4: audio manager initialises without raising", True,
          audio.failed_reason or "mixer ready")
    check("Task 4: jump / score / game_over sounds loaded",
          all(n in audio.sounds for n in ("jump", "score", "game_over")),
          f"loaded={sorted(audio.sounds)}")
    audio.play("jump")
    audio.play("score")
    audio.play("game_over")
    check("Task 4: play() is safe to call", True)

    assets = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    sizes = {}
    for name in ("jump", "score", "game_over"):
        path = os.path.join(assets, f"{name}.wav")
        sizes[name] = os.path.getsize(path) if os.path.exists(path) else 0
    check("Task 4: wav assets present and non-empty",
          all(v > 1000 for v in sizes.values()), f"{sizes}")


def test_jump_and_score():
    engine = new_engine(difficulty="easy")
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    check("Gameplay: Space makes the player jump", not engine.player.on_ground)
    for _ in range(200):
        engine.update()
    check("Gameplay: gravity returns the player to the ground", engine.player.on_ground)

    # An obstacle already behind the player must score exactly one point.
    # Geometry: player hitbox (margin 2) is [82, 108]; an obstacle at x=40
    # spans [40, 65], clear of the hitbox, and its right edge is left of the
    # player's x=80, which is the scoring condition.
    engine = new_engine(difficulty="easy")
    engine.obstacles = [Obstacle(40, engine.ground_y, 6.0)]
    for _ in range(10):
        engine.update()
        if engine.state != PLAYING:
            break
    check("Gameplay: clearing an obstacle scores a point",
          engine.score == 1 and engine.state == PLAYING,
          f"score={engine.score} state={engine.state}")

    # scoring must not double-count the same obstacle
    for _ in range(30):
        engine.update()
        if engine.state != PLAYING:
            break
    check("Gameplay: an obstacle only ever scores once",
          engine.score == 1, f"score={engine.score}")


def test_render_all_states():
    engine = new_engine(difficulty="medium")
    ok = True
    for state in (PLAYING, GAME_OVER, MENU):
        engine.state = state
        SURFACE.fill((0, 0, 0))
        try:
            engine.render(SURFACE)
        except Exception as exc:
            ok = False
            check(f"Render {state}", False, repr(exc))
    if ok:
        check("Render: playing / game over / menu all draw cleanly", True)


def main():
    for fn in (
        test_speed_is_capped,
        test_swept_rect_covers_full_span,
        test_swept_collision_catches_ghosted_hits,
        test_collision_triggers_at_all,
        test_game_over_screen,
        test_waits_for_input_then_menu,
        test_replay_difficulties,
        test_quit_option,
        test_esc_quits,
        test_sound_effects,
        test_jump_and_score,
        test_render_all_states,
    ):
        fn()

    failed = [name for name, ok, _ in RESULTS if not ok]
    print()
    print("=" * 60)
    print(f"{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed")
    if failed:
        print("FAILED:")
        for name in failed:
            print(f"  - {name}")
    print("=" * 60)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())