import pygame

from rendering.systems.cars_renderer import CarsRenderer
from rendering.systems.environment_renderer import EnvironmentRenderer
from rendering.systems.roads_renderer import RoadsRenderer
from rendering.systems.traffic_lights_renderer import TrafficLightsRenderer


# Contains and controlls all the renderers
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
        self.trafficLightsRenderer = TrafficLightsRenderer(
            camera, screen, mapWidth, mapHeight, gridRows, gridColumns
        )
        # dirty means that the roads' cached surface or the environment's cached surface must change
        # this happens at the start, or when the user modifies the road structure
        # note that the background grass will never change and the cars do not use cached
        # surfaces because they change every frame, therefore isDirty does not apply to them
        self.dirty = True
        self.environmentRenderer.createBackgroundGrass()

    def draw(self, state):
        # fills the screen with something
        self.screen.fill((0, 0, 0))
        if self.dirty:
            self.dirty = False
            # if dirty, create the cached surfaces
            grid = self.roadsRenderer.createRoadsSurface(
                state.roadNodes, state.roadConnections
            )
            self.environmentRenderer.createBackgroundDecorations(grid)

        # draw in this order:
        # 1. the grass - environmentRenderer
        # 2. the fences and the other decorations - environmentRenderer
        # 3. the roads - roadsRenderer
        # 4. the cars - carsRenderer

        self.environmentRenderer.draw()
        self.roadsRenderer.draw()
        self.carsRenderer.draw(state.cars)
        self.trafficLightsRenderer.draw(state.trafficLights)
