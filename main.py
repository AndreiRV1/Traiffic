import pygame
from core.game_loop import GameLoop
from core import settings


def main():
    pygame.init()
    pygame.display.set_caption(settings.WINDOW_TITLE)

    # create screen
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # create game
    game = GameLoop(screen, clock)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
