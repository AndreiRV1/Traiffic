import pygame
from core.game_loop import GameLoop
from core import settings


def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption(settings.WINDOW_TITLE)

    # Create the screen
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create and run the game loop
    game = GameLoop(screen, clock)
    game.run()

    # Quit pygame cleanly
    pygame.quit()


if __name__ == "__main__":
    main()
