import pygame
from backend.simulation import Simulation
from core.settings import *
from ui.camera import Camera
from ui.renderer import Renderer


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
            dt = self.clock.tick(60) / 1000.0

            # exiting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # update camera
            # press i or o for zoom in or zoom out
            # press the arrow keys to move the camera
            panSpeed = dt * 600 / self.camera.zoom
            zoom_step = 0.05
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.camera.setX(self.camera.x - panSpeed)
            if keys[pygame.K_RIGHT]:
                self.camera.setX(self.camera.x + panSpeed)
            if keys[pygame.K_UP]:
                self.camera.setY(self.camera.y - panSpeed)
            if keys[pygame.K_DOWN]:
                self.camera.setY(self.camera.y + panSpeed)
            if keys[pygame.K_i]:
                self.camera.setZoom(self.camera.zoom + zoom_step)
            if keys[pygame.K_o]:
                self.camera.setZoom(self.camera.zoom - zoom_step)

            # update simulation
            self.simulation.update(dt)

            # draw screen
            state = self.simulation.export_ui_state()
            self.renderer.draw_world(state)

            pygame.display.flip()
