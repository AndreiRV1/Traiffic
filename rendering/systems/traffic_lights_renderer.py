import math
import random
import pygame


# traffic lights images
trafficLightsImages = [
    "./assets/traffic_lights/traffic_light_off.png",
    "./assets/traffic_lights/traffic_light_on.png",
]


class TrafficLightsRenderer:
    def __init__(self, camera, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.camera = camera
        self.screen = screen
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.gridRows = gridRows
        self.gridColumns = gridColumns
        self.loadTrafficLightsImages()

    # loading the traffic lights images
    def loadTrafficLightsImages(self):
        trafficLightsImages[0] = pygame.image.load(
            trafficLightsImages[0]
        ).convert_alpha()
        trafficLightsImages[1] = pygame.image.load(
            trafficLightsImages[1]
        ).convert_alpha()

    # called every frame, uses the traffic lights data given by the simulation
    def draw(self, trafficLights):
        cellWidth = self.mapWidth / self.gridColumns
        cellHeight = self.mapHeight / self.gridRows

        for trafficLight in trafficLights:
            offsetX = trafficLight.x
            offsetY = trafficLight.y
            rotation = 0

            if trafficLight.direction == 0:
                offsetY -= 1
            if trafficLight.direction == 1:
                offsetX += 1
                rotation = 90
            if trafficLight.direction == 2:
                offsetY += 1
            if trafficLight.direction == 3:
                offsetX -= 1
                rotation = 90

            # world x, y positions
            worldX = offsetX * cellWidth
            worldY = offsetY * cellHeight

            # conversion to screen x, y positions using the camera parameters
            screenX = (worldX - self.camera.x) * self.camera.zoom
            screenY = (worldY - self.camera.y) * self.camera.zoom

            # choosing a random colored car
            img = trafficLightsImages[0 if trafficLight.isGreen == True else 1]

            # scaliong the image using the camera parameters
            scaled_img = pygame.transform.scale(
                img,
                (
                    cellWidth * self.camera.zoom,
                    cellHeight * self.camera.zoom,
                ),
            )
            rotated_img = pygame.transform.rotate(scaled_img, rotation)

            # blitting directly on screen
            self.screen.blit(rotated_img, (screenX, screenY))
