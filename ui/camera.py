class Camera:

    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.zoom = zoom

    def setX(self, x):
        minX = 0
        maxX = 250

        if x > maxX:
            x = maxX
        if x < minX:
            x = minX
        self.x = x

    def setY(self, y):
        minY = 0
        maxY = 250

        if y > maxY:
            y = maxY
        if y < minY:
            y = minY
        self.y = y

    def setZoom(self, zoom):
        maxZoom = 4
        minZoom = 0.25

        if zoom > maxZoom:
            zoom = maxZoom
        if zoom < minZoom:
            zoom = minZoom
        self.zoom = zoom
