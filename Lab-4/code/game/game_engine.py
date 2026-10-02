import pygame
from .player import Player
from .obstacle import Obstacle
from .audio import AudioManager

# Game Engine

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)
BLACK = (0, 0, 0)
PANEL = (18, 22, 34)
ACCENT = (255, 214, 92)
GREY = (170, 175, 190)

# Screen states (Task 2 + Task 3)
PLAYING = "playing"
GAME_OVER = "game_over"
MENU = "menu"

# Collision is tested against a player box inset by this many pixels on each
# side. Slightly forgiving near edges, which keeps high-speed hits feeling fair.
HITBOX_MARGIN = 2

# Seconds that must pass after game over before a key press opens the menu,
# so the key that killed you cannot skip the score screen instantly.
INPUT_LOCKOUT = 0.45

# Difficulty presets (Task 3). max_speed is the fairness ceiling from Task 1.
DIFFICULTIES = {
    "easy": {
        "label": "Easy",
        "start_speed": 4.0,
        "spawn_interval": 115,
        "ramp_per_frame": 0.0015,
        "max_speed": 13.0,
        "blurb": "A gentle warm-up",
    },
    "medium": {
        "label": "Medium",
        "start_speed": 6.0,
        "spawn_interval": 70,
        "ramp_per_frame": 0.003,
        "max_speed": 19.0,
        "blurb": "The original pace",
    },
    "hard": {
        "label": "Hard",
        "start_speed": 9.5,
        "spawn_interval": 46,
        "ramp_per_frame": 0.005,
        "max_speed": 26.0,
        "blurb": "Fast and relentless",
    },
}
DIFFICULTY_ORDER = ["easy", "medium", "hard"]

# Key names, normalised by pygame.key.name().lower() -- see _handle_key.
JUMP_KEYS = ("space", "up", "w")
MENU_UP_KEYS = ("up", "w")
MENU_DOWN_KEYS = ("down", "s")
CONFIRM_KEYS = ("return", "enter", "space")
QUIT_KEYS = ("escape", "q")


class GameEngine:
    def __init__(self, width, height, difficulty="medium", audio=None):
        self.width = width
        self.height = height
        self.ground_y = height - 40
        self.audio = audio if audio is not None else AudioManager()

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 56, bold=True)
        self.heading_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 18)

        self.state = PLAYING
        self.menu_index = 1
        self.best_score = 0
        self.running = True
        self._lockout = 0.0

        if difficulty not in DIFFICULTIES:
            difficulty = "medium"
        self.difficulty = difficulty
        self._start_run()

    # ------------------------------------------------------------------ setup

    def _start_run(self):
        """Begin a fresh run using the current difficulty's settings."""
        cfg = DIFFICULTIES[self.difficulty]
        self.player = Player(80, self.ground_y)

        # Task 1: speed still ramps, but it now has a ceiling per difficulty.
        self.speed = cfg["start_speed"]
        self.ramp_per_frame = cfg["ramp_per_frame"]
        self.max_speed = cfg["max_speed"]
        self.spawn_interval = cfg["spawn_interval"]

        self._spawn_timer = 0
        self.obstacles = []
        self.distance = 0
        self.score = 0
        self.state = PLAYING

    @property
    def game_over(self):
        """Kept for compatibility with the original engine's public flag."""
        return self.state == GAME_OVER

    # ------------------------------------------------------------------ input

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return
        if event.type == pygame.KEYDOWN:
            self._handle_key(event.key)

    def _handle_key(self, key):
        # pygame only defines lowercase letter constants (K_w, not K_W), so the
        # key is normalised by name instead. This also handles Shift+W, since
        # the physical key reports the same name either way.
        name = pygame.key.name(key).lower()

        if self.state == PLAYING:
            if name in JUMP_KEYS:
                self.player.jump()
                if not self.player.on_ground:
                    self.audio.play("jump")
            return

        if self._lockout > 0:
            return

        if self.state == GAME_OVER:
            # Task 2: the game waits here for input instead of printing.
            self.state = MENU
            self.menu_index = DIFFICULTY_ORDER.index(self.difficulty)
            return

        if self.state == MENU:
            if name in MENU_UP_KEYS:
                self.menu_index = (self.menu_index - 1) % (len(DIFFICULTY_ORDER) + 1)
            elif name in MENU_DOWN_KEYS:
                self.menu_index = (self.menu_index + 1) % (len(DIFFICULTY_ORDER) + 1)
            elif name in CONFIRM_KEYS:
                self._confirm_menu()
            elif name in QUIT_KEYS:
                self.running = False

    def _confirm_menu(self):
        if self.menu_index < len(DIFFICULTY_ORDER):
            self.difficulty = DIFFICULTY_ORDER[self.menu_index]
            self._start_run()          # Task 3: replay on the chosen difficulty
        else:
            self.running = False       # Exit

    def handle_input(self):
        # Retained for API compatibility. Input is edge-triggered and handled
        # in handle_event; nothing to poll here.
        pass

    # ------------------------------------------------------------------ update

    def update(self, dt=0.0):
        if self._lockout > 0:
            self._lockout = max(0.0, self._lockout - dt)

        if self.state != PLAYING:
            return

        # Task 1: ramp, then clamp. The original had no ceiling at all.
        self.speed = min(self.speed + self.ramp_per_frame, self.max_speed)
        self.player.update()

        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.obstacles.append(Obstacle(self.width, self.ground_y, self.speed))

        for obstacle in self.obstacles:
            obstacle.move()
            obstacle.speed = self.speed

        # Task 1: swept (continuous) collision test. Each obstacle is tested
        # across the whole horizontal span it travelled this frame, so a fast
        # obstacle can no longer jump clean over the player's hitbox between
        # two samples.
        if self._check_collisions():
            self._end_run()
            return

        for obstacle in self.obstacles:
            if not obstacle.scored and obstacle.x + obstacle.width < self.player.x:
                obstacle.scored = True
                self.score += 1
                self.audio.play("score")

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]
        self.distance += self.speed

    def _check_collisions(self):
        hitbox = self.player.hitbox(margin=HITBOX_MARGIN)
        for obstacle in self.obstacles:
            swept = obstacle.swept_rect()
            if swept is not None and swept.colliderect(hitbox):
                return True
        return False

    def _end_run(self):
        self.state = GAME_OVER
        self._lockout = INPUT_LOCKOUT
        self.best_score = max(self.best_score, self.score)
        self.audio.play("game_over")

    # ----------------------------------------------------------------- render

    def render(self, screen):
        pygame.draw.line(screen, BROWN, (0, self.ground_y),
                         (self.width, self.ground_y), 4)

        pygame.draw.rect(screen, WHITE, self.player.rect())
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, DARK_GREEN, obstacle.rect())

        screen.blit(self.font.render(f"Score: {self.score}", True, BLACK), (10, 8))
        info = f"Speed: {self.speed:.1f} / {self.max_speed:.0f}   -   {DIFFICULTIES[self.difficulty]['label']}"
        screen.blit(self.small_font.render(info, True, BLACK), (10, 40))

        if self.state == GAME_OVER:
            self._render_game_over(screen)
        elif self.state == MENU:
            self._render_menu(screen)

    def _dim(self, screen, alpha=165):
        veil = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        veil.fill((0, 0, 0, alpha))
        screen.blit(veil, (0, 0))

    def _panel(self, screen, width, height):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (self.width // 2, self.height // 2)
        pygame.draw.rect(screen, PANEL, rect)
        pygame.draw.rect(screen, ACCENT, rect, 3)
        return rect

    def _blit_centered(self, screen, surface, cx, y):
        screen.blit(surface, (cx - surface.get_width() // 2, y))

    def _render_game_over(self, screen):
        # Task 2: a real game-over screen with the final score.
        self._dim(screen)
        panel = self._panel(screen, 460, 200)
        cx = panel.centerx

        self._blit_centered(screen, self.big_font.render("GAME OVER", True, ACCENT),
                            cx, panel.y + 22)
        self._blit_centered(
            screen, self.heading_font.render(f"Final score: {self.score}", True, WHITE),
            cx, panel.y + 92)
        self._blit_centered(
            screen, self.small_font.render(f"Best: {self.best_score}", True, GREY),
            cx, panel.y + 130)
        self._blit_centered(
            screen,
            self.small_font.render("Press any key to continue...", True, ACCENT),
            cx, panel.y + 160)

    def _render_menu(self, screen):
        # Task 3: pick a difficulty to replay, or exit.
        self._dim(screen)
        panel = self._panel(screen, 480, 268)
        cx = panel.centerx

        self._blit_centered(
            screen, self.heading_font.render("Play again", True, ACCENT),
            cx, panel.y + 18)
        self._blit_centered(
            screen,
            self.small_font.render("Choose a difficulty  (Up/Down, Enter)", True, GREY),
            cx, panel.y + 56)

        options = list(DIFFICULTY_ORDER) + [None]  # None renders as "Quit"
        y = panel.y + 88
        for i, key in enumerate(options):
            selected = i == self.menu_index
            if selected:
                row = pygame.Rect(panel.x + 40, y - 6, panel.width - 80, 36)
                pygame.draw.rect(screen, (44, 52, 74), row)

            marker = ">" if selected else " "
            label = DIFFICULTIES[key]["label"] if key else "Quit"
            color = ACCENT if selected else WHITE
            screen.blit(self.menu_font.render(f"{marker}  {label}", True, color),
                        (panel.x + 52, y))

            if key:
                blurb = self.small_font.render(DIFFICULTIES[key]["blurb"], True, GREY)
                screen.blit(blurb, (panel.x + 104, y + 6))
            y += 42