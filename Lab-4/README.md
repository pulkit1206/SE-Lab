# Lab 4: VibeCoding

**Course:** Software Engineering (UE24CS341A) &mdash; Semester 5, Section F
**Student:** PULKIT BHARDWAJ &mdash; USN `PES1UG24CS346`
**Assigned repository:** [`SETAPESU26/39_endless-runner`](https://github.com/SETAPESU26/39_endless-runner) (original commit `5e73071`)
**AI tool:** opencode (Claude `big-pickle`), used as a CLI pair-programming agent
**Date:** 02 October 2026

> Per the handout, **no pull request was opened against `SETAPESU26`.** All work here
> is in the student's own account.

---

## Deliverables

| # | Deliverable | Location |
| --- | --- | --- |
| a | Videos (before and after) | [`videos/`](videos/) &mdash; `before.mp4`, `after.mp4` |
| b | Updated code | [`code/`](code/) |
| c | Chat history as doc/pdf | [`chat-history/`](chat-history/) &mdash; `.pdf` (5 pp), `.doc`, `.html` |
| &mdash; | Supporting evidence | [`evidence/`](evidence/) |

---

## The bug

`GameEngine.update()` moved every obstacle and *then* tested
`obstacle.rect().colliderect(player.rect())` &mdash; a single sample per frame. The
player is 30 px wide at `x=80` and obstacles are 25 px wide, so an obstacle overlaps
only while its `x` lies in the open interval `(55, 110)`: a **55 px wide** window.
Any per-frame step of 55 px or more can step clean over that window, and `speed` was
climbing by 0.003 every frame with **no ceiling**, so this state was guaranteed to be
reached rather than merely possible.

Measured on the unmodified original:

- tunneling begins at **56 px/frame**, matching the 55 px geometry exactly
- **10&ndash;30 %** of obstacles ghost through the player at a given high speed
- **1447 speeds** in 56&ndash;120 px/frame at which a player who **never jumps** is not
  killed at all &mdash; see `evidence/02-ghost-pass-speeds-original.txt`

## The fix

1. **Swept (continuous) collision** &mdash; `Obstacle` records `prev_x` on each `move()`
   and exposes `swept_rect()`, the whole horizontal span covered in that frame. The
   engine tests that span against the player hitbox, so an obstacle cannot slip
   between two samples **at any speed**.
2. **Speed ceiling** &mdash; each difficulty has a `max_speed`; the ramp saturates.
3. **Fairness** &mdash; collision uses `Player.hitbox(margin=2)`; drawing is unchanged.

Plus the three remaining tasks: an on-screen **game over** panel with final and best
score, a **replay menu** offering Easy / Medium / Hard / Quit, and **sound effects**
for jump, scoring and death that degrade to silence when no audio device exists.

## Verification

`code/tests/test_game.py` runs **34 headless checks, all passing**. The decisive
regression sweeps the 64 speeds from 56 to 120 px/frame that previously let a
motionless player survive, and confirms every one now registers a hit:

```
[PASS] Task 1: swept collision removes ghost passes (56-120 px/frame) -- 0 ghost passes across 64 speeds
```

## The two videos

Both are exactly 10.000 s / 600 frames at 60 fps, produced by driving the game's own
`render()` into an offscreen surface and piping raw frames to ffmpeg, so they are
deterministic and do not depend on screen-recording timing.

They are tied together deliberately by **the same speed value, 57.24 px/frame**:

| Video | What happens |
| --- | --- |
| `before.mp4` | Original code unmodified. Player does not jump at 57.24 px/frame &mdash; **243 ghost crossings**, obstacles pass straight through, no collision, game continues. Then at normal speed a hit lands and the game simply **freezes** with no overlay, only a console print. |
| `after.mp4` | Same 57.24 px/frame, player stops jumping &mdash; the hit is **caught in 0.1 s**. Then the game over panel, the difficulty menu, and a fresh Easy run restarting at score 0. |

In the before video the ramp is fast-forwarded along the original curve
(`speed += 0.003`/frame reaches 57 after ~4.5 minutes) so the bug is visible inside
10 seconds; the game code itself is untouched.

## Running the game

```bash
cd code
pip install -r requirements.txt
python main.py
python tests/test_game.py      # 34 headless checks
```

| Action | Keys |
| --- | --- |
| Jump | `Space`, `Up`, `W` |
| Game over → menu | any key |
| Move / confirm selection | `Up`/`W`, `Down`/`S` &nbsp;·&nbsp; `Enter` |
| Quit from menu | `Esc` or `Q` |

## Evidence files

| File | Contents |
| --- | --- |
| `evidence/01-bug-measurement-original-code.txt` | Tunnel rate vs. speed on the original code |
| `evidence/02-ghost-pass-speeds-original.txt` | The 1447 speeds where a motionless player survives |
| `evidence/03-test-results-fixed-code.txt` | Full 34-check run on the fixed code |
| `evidence/04-code-diff.txt` | Diff from `5e73071` to the Lab-4 commit |