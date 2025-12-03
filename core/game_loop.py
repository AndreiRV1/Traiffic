import pygame
from backend.simulation import Simulation
from core.settings import *
from rendering.systems.camera import Camera
from rendering.systems.renderer import Renderer


class GameLoop:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.simulation = Simulation()
        self.camera = Camera(0, 0, 1)
        self.renderer = Renderer(
            self.camera,
            screen,
            MAP_WIDTH,
            MAP_HEIGHT,
            GRID_ROWS,
            GRID_COLUMNS,
        )

    def run(self):
        running = True
        while running:
            # delta time between frames - used for movements
            dt = self.clock.tick(60) / 1000.0

            # exiting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # update simulation
            self.simulation.update(dt)

            # update camera based on input
            self.camera.update(dt)

            # update rendering based on simulation state
            state = self.simulation.export_ui_state()
            self.renderer.draw(state)

            pygame.display.flip()
