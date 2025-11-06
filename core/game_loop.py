# core/game_loop.py
import pygame
from backend.simulation import Simulation
from ui.renderer import Renderer


class GameLoop:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.simulation = Simulation()
        self.renderer = Renderer(screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update backend simulation
            self.simulation.update(dt)

            # Draw UI from simulation state
            state = self.simulation.export_ui_state()
            self.renderer.draw_world(state)

            pygame.display.flip()
