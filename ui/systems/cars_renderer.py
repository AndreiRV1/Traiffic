import pygame

carsImages = [
    "./assets/cars/green_car.png",
    "./assets/cars/blue_car.png",
    "./assets/cars/red_car.png",
    "./assets/cars/orange_car.png",
]


class CarsRenderer:
    def __init__(self, camera, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.camera = camera
        self.screen = screen
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.gridRows = gridRows
        self.gridColumns = gridColumns
        self.loadCarImages()

    def loadCarImages(self):
        for index in range(0, len(carsImages)):
            carsImages[index] = pygame.image.load(carsImages[index])

    def draw(self, cars):
        cellWidth = self.mapWidth / self.gridColumns
        cellHeight = self.mapHeight / self.gridRows

        for car in cars:
            worldX = car.x * cellWidth
            worldY = car.y * cellHeight
            screenX = (worldX - self.camera.x) * self.camera.zoom
            screenY = (worldY - self.camera.y) * self.camera.zoom
            img = carsImages[car.id % len(carsImages)]
            if img is not None:
                scaled_img = pygame.transform.scale(
                    img, (cellWidth * self.camera.zoom, cellHeight * self.camera.zoom)
                )
                rotated_img = pygame.transform.rotate(scaled_img, car.get_direction())
                self.screen.blit(rotated_img, (screenX, screenY))
