import pygame

class Player:
    def __init__(self, x, ground_y, width=30, height=40):
        self.x = x
        self.ground_y = ground_y
        self.width = width
        self.height = height
        self.y = ground_y - height
        self.vy = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False

    def update(self):
        self.vy += self.gravity
        self.y += self.vy

        ground_level = self.ground_y - self.height
        if self.y >= ground_level:
            self.y = ground_level
            self.vy = 0
            self.on_ground = True

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def hitbox(self, margin=0):
        """Collision box, optionally inset for a fairer feel.

        Drawing still uses rect(); only collision uses this, so the player
        can be slightly generous near obstacle edges without changing the
        look of the game.
        """
        margin = max(0, min(margin, (self.width - 1) // 2, (self.height - 1) // 2))
        return pygame.Rect(self.x + margin, self.y + margin,
                           self.width - 2 * margin, self.height - 2 * margin)