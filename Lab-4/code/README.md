# Project: Real-Time Endless Runner Game

This project is a terminal-based endless runner using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---

## What’s Provided

A partially working version of an endless runner with:

- A player-controlled character that jumps over obstacles with gravity pulling it back down
- Obstacles that spawn at a regular interval and scroll toward the player, gradually speeding up
- Score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

### Controls

| Action | Keys |
| --- | --- |
| Jump | `Space`, `Up`, `W` |
| Game over -> menu | any key |
| Move selection | `Up`/`W`, `Down`/`S` |
| Confirm selection | `Enter` or `Space` |
| Quit from menu | `Esc` or `Q` |

### Running the tests

The checks are headless (SDL dummy drivers), so they work with no display
and no audio device:

```bash
python tests/test_game.py
```

### Sound effects

The three WAV files in `assets/` are generated from source rather than
copied from anywhere, and can be rebuilt at any time:

```bash
python tools/generate_sounds.py
```




## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> The game speeds up forever with no limit, and once it's fast enough obstacles can zip past the player without the hit ever registering. Investigate and enhance collision accuracy (and/or the speed ramp) so it stays fair no matter how long a run lasts.


### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the player collides with an obstacle, then gracefully waits for input instead of just printing to the console.


### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard starting speed/spawn rate), or exit.



### Task 4: Add Sound Feedback

> Add basic sound effects for jumping, passing an obstacle (scoring), and the game-over moment.



---

## Expected Behavior

- Player jumps with `Space`, `Up`, or `W`, and gravity brings it back down to the ground
- Obstacles spawn at a regular interval and scroll from right to left, gradually getting faster
- Score increases by one each time the player clears an obstacle
- Game ends when the player collides with an obstacle

---

## Folder Structure

```
endless-runner-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── player.py
│   └── obstacle.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history

---

## Lab-4 Changes

### Task 1: Refine collision detection

**The bug.** `GameEngine.update()` moved every obstacle first and only then
tested `obstacle.rect().colliderect(player.rect())`. That samples the obstacle
at a *single* position per frame, so once an obstacle travelled further in one
frame than the player's hitbox is wide, it could step clean over the player
between two samples and the hit was never seen. `speed` also had no ceiling,
so this was guaranteed to happen rather than merely possible.

**Measured on the original code.** An obstacle overlaps the player when its `x`
lies in the open interval `(55, 110)` — the player is 30 px wide at `x=80`
and the obstacle is 25 px wide. That interval is 55 px wide, so any per-frame
step at or above 55 px can skip it. A headless sweep over speeds 56–120 found
**1447 speeds at which a player who never jumped was not killed at all**, with
10–30 % of obstacles ghosting through at a given speed. The original ramp
(`speed += 0.003` per frame) passes 56 px/frame after ~4.5 minutes and keeps
climbing forever.

**The fix**, in `game/obstacle.py` and `game/game_engine.py`:

1. *Swept (continuous) collision.* `Obstacle` records `prev_x` on every
   `move()`, and `swept_rect()` returns the entire horizontal span it covered
   during that frame. The engine tests that span against the player's hitbox,
   so a fast obstacle cannot skip over it between samples. This is correct at
   any speed, so it is not a tuning workaround.
2. *A speed ceiling.* Each difficulty has a `max_speed`, so the ramp
   saturates instead of growing without limit.

Collisions are also tested against `Player.hitbox(margin=2)`, a box inset by
2 px, which keeps near-misses fair without changing how the player is drawn.

### Task 2: Game over screen

`render()` used to `print()` the score once. There is now a real state machine
(`PLAYING` / `GAME_OVER` / `MENU`) in `game/game_engine.py`. On a collision the
game dims the screen and shows a **GAME OVER** panel with the final score and
the best score so far, then waits for a key press. A 0.45 s input lockout
stops the very key that caused the death from skipping the score screen.

### Task 3: Replay with difficulty

Pressing any key on the game over screen opens a difficulty menu with
**Easy / Medium / Hard / Quit**, navigable with Up/Down and confirmed with
Enter. Each option applies its own starting speed, spawn interval, ramp rate
and speed ceiling:

| Difficulty | Start speed | Spawn interval | Speed ceiling |
| --- | --- | --- | --- |
| Easy | 4.0 | 115 frames | 13 px/frame |
| Medium | 6.0 | 70 frames | 19 px/frame |
| Hard | 9.5 | 46 frames | 26 px/frame |

Confirming a difficulty calls `_start_run()`, which rebuilds the run from
scratch at score 0. Quit (or `Esc`) sets `engine.running = False`, which ends
the `main.py` loop cleanly.

### Task 4: Sound feedback

`game/audio.py` wraps `pygame.mixer` and plays three effects: `jump` on
take-off, `score` when an obstacle is cleared, and `game_over` on death. Every
failure path (no audio device, missing asset, load error) degrades to silence
instead of raising, so the game still runs over SSH or in a container.

### Verification

`tests/test_game.py` runs 34 headless checks covering all four tasks,
including a direct regression test: the 64 speeds from 56 to 120 px/frame that
let a motionless player survive in the original code now all register a hit.

