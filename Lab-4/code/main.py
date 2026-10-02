import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
# pre_init must run before init() so the mixer uses the requested buffer size.
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner - Pygame Version")

# Colors
SKY = (200, 220, 240)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT, difficulty="medium")

def main():
    running = True
    while running:
        SCREEN.fill(SKY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.running = False
                continue
            engine.handle_event(event)

        # dt keeps the post-game-over key lockout honest if the frame rate dips.
        dt = clock.get_time() / 1000.0
        engine.update(dt)
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)
        running = engine.running

    pygame.quit()

if __name__ == "__main__":
    main()