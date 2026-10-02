"""Generate the game's sound effects as 16-bit mono WAV files.

Kept in the repo so the assets are reproducible and nothing is copied from
a third party.  Uses only the standard library (no numpy dependency).

Usage:
    python tools/generate_sounds.py
"""
import array
import math
import os
import struct
import wave

SAMPLE_RATE = 44100
ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
)


def envelope(i, total, attack=0.02, release=0.35):
    """Simple attack/release shape so effects don't click."""
    t = i / total
    if t < attack:
        return t / attack
    if t > 1.0 - release:
        return max(0.0, (1.0 - t) / release)
    return 1.0


def tone(duration, start_hz, end_hz, volume=0.35, harmonics=(1.0, 0.35, 0.15)):
    """A swept tone.  end_hz may equal start_hz for a steady pitch."""
    total = int(SAMPLE_RATE * duration)
    samples = array.array("h")
    phase = 0.0
    for i in range(total):
        t = i / total
        freq = start_hz + (end_hz - start_hz) * t
        phase += 2.0 * math.pi * freq / SAMPLE_RATE
        value = sum(amp * math.sin(phase * (n + 1)) for n, amp in enumerate(harmonics))
        value *= volume * envelope(i, total)
        samples.append(int(max(-1.0, min(1.0, value)) * 32767))
    return samples


def write_wav(name, samples):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    path = os.path.join(ASSETS_DIR, name)
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(samples.tobytes())
    print(f"wrote {path} ({len(samples)} samples, {len(samples)/SAMPLE_RATE:.2f}s)")


def main():
    # Task 4: jump - short upward blip
    write_wav("jump.wav", tone(0.12, 320.0, 760.0, volume=0.30))
    # Task 4: scoring - bright two-note ding
    score = tone(0.09, 880.0, 900.0, volume=0.26)
    score.extend(tone(0.13, 1320.0, 1340.0, volume=0.26))
    write_wav("score.wav", score)
    # Task 4: game over - descending buzz
    write_wav("game_over.wav", tone(0.55, 520.0, 110.0, volume=0.34,
                                    harmonics=(1.0, 0.5, 0.3)))


if __name__ == "__main__":
    main()