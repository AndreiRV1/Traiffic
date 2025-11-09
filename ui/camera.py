from core.settings import *


class Camera:

    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.zoom = zoom

    def setX(self, x):
        minX = 0
        maxX = max(0, MAP_WIDTH - SCREEN_WIDTH / self.zoom)
        self.x = max(minX, min(x, maxX))

    def setY(self, y):
        minY = 0
        maxY = max(0, MAP_HEIGHT - SCREEN_HEIGHT / self.zoom)
        self.y = max(minY, min(y, maxY))

    def setZoom(self, zoom):
        minZoomX = SCREEN_WIDTH / MAP_WIDTH
        minZoomY = SCREEN_HEIGHT / MAP_HEIGHT
        minZoom = max(minZoomX, minZoomY)
        maxZoom = 2

        self.zoom = max(minZoom, min(zoom, maxZoom))
        self.setX(self.x)
        self.setY(self.y)
