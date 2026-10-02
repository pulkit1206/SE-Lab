"""Sound effects for the runner (Lab-4 Task 4).

The mixer is optional: on a machine with no audio device (CI, a container,
a remote shell) the game must still run, so every failure path simply
disables sound instead of raising.
"""
import os

import pygame

ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
)

SOUND_NAMES = ("jump", "score", "game_over")


class AudioManager:
    def __init__(self, enabled=True):
        self.available = False
        self.sounds = {}
        self.failed_reason = None
        if enabled:
            self._start()

    def _start(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error as exc:
            self.failed_reason = f"mixer unavailable: {exc}"
            return
        except Exception as exc:  # defensive: some drivers raise non-pygame errors
            self.failed_reason = f"mixer init failed: {exc}"
            return

        for name in SOUND_NAMES:
            path = os.path.join(ASSETS_DIR, f"{name}.wav")
            if not os.path.exists(path):
                self.failed_reason = f"missing asset {path}"
                continue
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error as exc:
                self.failed_reason = f"could not load {name}.wav: {exc}"
        self.available = bool(self.sounds)

    def play(self, name):
        if not self.available:
            return
        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass