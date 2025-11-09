import pygame

from ui.systems.cars_renderer import CarsRenderer
from ui.systems.environment_renderer import EnvironmentRenderer
from ui.systems.roads_renderer import RoadsRenderer


class Renderer:
    def __init__(self, camera, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.screen = screen
        self.environmentRenderer = EnvironmentRenderer(
            camera, screen, mapWidth, mapHeight, gridRows, gridColumns
        )
        self.carsRenderer = CarsRenderer(
            camera, screen, mapWidth, mapHeight, gridRows, gridColumns
        )
        self.roadsRenderer = RoadsRenderer(
            camera, screen, mapWidth, mapHeight, gridRows, gridColumns
        )
        self.dirty = True
        self.environmentRenderer.createBackgroundGrass()

    def draw(self, state):
        self.screen.fill((0, 0, 0))
        if self.dirty:
            self.dirty = False
            grid = self.roadsRenderer.createCarsSurface(
                state.roadNodes, state.roadConnections
            )
            self.environmentRenderer.createBackgroundDecorations(grid)

        self.environmentRenderer.draw()
        self.roadsRenderer.draw()
        self.carsRenderer.draw(state.cars)
