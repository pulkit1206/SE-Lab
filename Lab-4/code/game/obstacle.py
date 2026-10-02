import pygame

class Obstacle:
    def __init__(self, x, ground_y, speed, width=25, height=40):
        self.x = x
        self.width = width
        self.height = height
        self.y = ground_y - height
        self.speed = speed
        self.scored = False
        # Position before the current frame's move(). Lets the engine run a
        # swept collision test over the whole span the obstacle travelled,
        # instead of sampling only its end position. See swept_rect().
        self.prev_x = x

    def move(self):
        self.prev_x = self.x
        self.x -= self.speed

    def swept_rect(self):
        """Horizontal span covered during the last move(), both ends included.

        Returns None before the obstacle has moved, so an obstacle that has
        only ever been drawn at its spawn point never registers a phantom hit.
        """
        if self.prev_x == self.x:
            return None
        left = min(self.x, self.prev_x)
        right = max(self.x, self.prev_x) + self.width
        return pygame.Rect(left, self.y, right - left, self.height)

    def off_screen(self):
        return self.x + self.width < 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)