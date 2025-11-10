import pygame
from core.settings import *


class Camera:
    # x, y - global pixel coordinates
    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.zoom = zoom

    # x must not exceed the right or left bound
    def setX(self, x):
        minX = 0
        maxX = max(0, MAP_WIDTH - SCREEN_WIDTH / self.zoom)
        self.x = max(minX, min(x, maxX))

    # y must not exceed the upper or lower bound
    def setY(self, y):
        minY = 0
        maxY = max(0, MAP_HEIGHT - SCREEN_HEIGHT / self.zoom)
        self.y = max(minY, min(y, maxY))

    # zoom should not zoom out of the map
    def setZoom(self, zoom):
        minZoomX = SCREEN_WIDTH / MAP_WIDTH
        minZoomY = SCREEN_HEIGHT / MAP_HEIGHT
        minZoom = max(minZoomX, minZoomY)
        maxZoom = 2

        self.zoom = max(minZoom, min(zoom, maxZoom))
        self.setX(self.x)
        self.setY(self.y)

    # update to take care of the panning / zooming using user input
    def update(self, dt):
        panSpeed = dt * 600 / self.zoom
        zoom_step = 0.05

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.setX(self.x - panSpeed)
        if keys[pygame.K_RIGHT]:
            self.setX(self.x + panSpeed)
        if keys[pygame.K_UP]:
            self.setY(self.y - panSpeed)
        if keys[pygame.K_DOWN]:
            self.setY(self.y + panSpeed)
        if keys[pygame.K_i]:
            self.setZoom(self.zoom + zoom_step)
        if keys[pygame.K_o]:
            self.setZoom(self.zoom - zoom_step)
