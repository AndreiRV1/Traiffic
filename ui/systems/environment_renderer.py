import math
import random
import pygame

# different grass images
environmentGrassImages = [
    "./assets/environment/grass_0.png",
    "./assets/environment/grass_1.png",
    "./assets/environment/grass_2.png",
    "./assets/environment/grass_3.png",
    "./assets/environment/grass_4.png",
    "./assets/environment/grass_5.png",
    "./assets/environment/grass_6.png",
    "./assets/environment/grass_7.png",
    "./assets/environment/grass_8.png",
]

# weights for the grass images to make them more visually pleasing
environmentGrassWeights = [12, 30, 12, 3, 3, 1, 3, 3, 1]

# fence images
environmentFenceImages = [
    "./assets/environment/fence.png",
    "./assets/environment/fence_end.png",
]

# other decorations images
environmentDecorationsImages = [
    "./assets/environment/stone_0.png",
    "./assets/environment/stone_1.png",
    "./assets/environment/stone_2.png",
    "./assets/environment/stone_3.png",
    "./assets/environment/stone_4.png",
    "./assets/environment/mushroom_0.png",
    "./assets/environment/mushroom_1.png",
    "./assets/environment/log_0.png",
    "./assets/environment/log_1.png",
    "./assets/environment/log_2.png",
    "./assets/environment/flower_0.png",
    "./assets/environment/flower_1.png",
    "./assets/environment/flower_2.png",
    "./assets/environment/bush_0.png",
    "./assets/environment/bush_1.png",
    "./assets/environment/bush_2.png",
    "./assets/environment/bush_3.png",
]


class EnvironmentRenderer:
    def __init__(self, camera, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.camera = camera
        self.screen = screen
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.gridRows = gridRows
        self.gridColumns = gridColumns
        self.backgroundGrass = None
        self.backgroundDecorations = None
        self.loadEnvironmentImages()

    # loading the grass, fences and other decorations right at the start of the game
    def loadEnvironmentImages(self):
        for index in range(0, len(environmentGrassImages)):
            environmentGrassImages[index] = pygame.image.load(
                environmentGrassImages[index]
            )
        for index in range(0, len(environmentDecorationsImages)):
            environmentDecorationsImages[index] = pygame.image.load(
                environmentDecorationsImages[index]
            ).convert_alpha()

        # using conver_alpha because they use transparency
        for index in range(0, len(environmentFenceImages)):
            environmentFenceImages[index] = pygame.image.load(
                environmentFenceImages[index]
            ).convert_alpha()

    # creates only once, when dirty, the surface for the grass
    def createBackgroundGrass(self):
        self.backgroundGrass = pygame.Surface(
            (self.mapWidth, self.mapHeight), pygame.SRCALPHA
        )

        cellWidth = self.mapWidth / self.gridColumns
        cellHeight = self.mapHeight / self.gridRows

        # grass looks better if the tiles are half the size of a normal tile
        newCellWidth = self.camera.zoom * int(round(cellWidth / 2))
        newCellHeight = self.camera.zoom * int(round(cellHeight / 2))

        for y in range(0, self.gridRows * 2):
            for x in range(0, self.gridColumns * 2):
                # getting a random grass tile using the weights
                img = random.choices(
                    environmentGrassImages, weights=environmentGrassWeights, k=1
                )[0]

                # scaling does not use camera parameters because this is only making the
                # grass surface, it will not put it on screen
                scaled_img = pygame.transform.scale(img, (newCellWidth, newCellHeight))
                self.backgroundGrass.blit(
                    scaled_img, (x * newCellWidth, y * newCellHeight)
                )

    # creates only once, when dirty, the surface for the decorations
    def createBackgroundDecorations(self, roadsGrid):
        self.backgroundDecorations = pygame.Surface(
            (self.mapWidth, self.mapHeight), pygame.SRCALPHA
        )

        cellWidth = self.mapWidth / self.gridColumns
        cellHeight = self.mapHeight / self.gridRows

        # fence creation (looks best when half the size of a cell)
        fenceCellWidth = self.camera.zoom * int(round(cellWidth / 2))
        fenceCellHeight = self.camera.zoom * int(round(cellHeight / 2))
        for y in range(0, self.gridRows * 2):
            for x in range(0, self.gridColumns * 2):
                img = None
                # computing the x and y of the big cell
                initX = math.floor(x / 2)
                initY = math.floor(y / 2)
                yGood = 0 <= initY + 1 < len(roadsGrid)
                if yGood and 1 <= initX < len(roadsGrid[initY + 1]) - 1 and y % 2 == 1:
                    # the text of the big cell underneath this big one
                    sDown = roadsGrid[initY + 1][initX]
                    if "l" in sDown and "r" in sDown:
                        img = environmentFenceImages[0]  # fence part
                    if "l" in sDown and "r" not in sDown and x % 2 == 1:
                        img = environmentFenceImages[1]  # fence end
                    elif "l" in sDown and "r" not in sDown and x % 2 == 0:
                        img = environmentFenceImages[0]  # fence part

                if img is not None:
                    # added 1 to fenceCellWidth and fenceCellHeight to solve visual gaps between cells
                    scaled_img = pygame.transform.scale(
                        img, (fenceCellWidth + 1, fenceCellHeight + 1)
                    )

                    # blitting on the cached texture
                    self.backgroundDecorations.blit(
                        scaled_img, (x * fenceCellWidth, y * fenceCellHeight)
                    )

        # other decorations creation (looks best the full cell size)
        availablePos = []

        # getting avaliable positions, that are not adjacent to a road
        for y in range(0, self.gridRows):
            for x in range(0, self.gridColumns):
                if roadsGrid[y][x] != "":
                    continue
                if x > 0 and roadsGrid[y][x - 1] != "":
                    continue
                if x + 1 < len(roadsGrid[0]) and roadsGrid[y][x + 1] != "":
                    continue
                if y > 0 and roadsGrid[y - 1][x] != "":
                    continue
                if y + 1 < len(roadsGrid) and roadsGrid[y + 1][x] != "":
                    continue
                availablePos.append([x, y])

        # getting uniformily distributed positions across the map, using a stepper
        step = len(availablePos) // 32
        chosenPos = []
        for i in range(0, 32):
            start = i * step
            end = min((i + 1) * step, len(availablePos))
            if start >= len(availablePos):
                break
            # using a random offset to achieve randomness
            idx = random.randint(start, end - 1)
            chosenPos.append(availablePos[idx])

        for pos in chosenPos:
            # for each position, blit an image to the background decorations, without using the camera parameters
            img = random.choice(environmentDecorationsImages)
            # added 1 to cellWidth and cellHeight to solve visual gaps between cells
            scaled_img = pygame.transform.scale(img, (cellWidth + 1, cellHeight + 1))
            self.backgroundDecorations.blit(
                scaled_img, (pos[0] * cellWidth, pos[1] * cellHeight)
            )

    # draws both the surfaces on screen, using the camera parameters, each frame
    def draw(self):
        # getting screen x, y using the camera parameters
        screenX = -self.camera.x * self.camera.zoom
        screenY = -self.camera.y * self.camera.zoom

        if self.backgroundGrass is not None:
            # scaling to match the zoom
            scaledBackgroundGrass = pygame.transform.scale(
                self.backgroundGrass,
                (self.mapWidth * self.camera.zoom, self.mapHeight * self.camera.zoom),
            )
            # bliting on screen
            self.screen.blit(scaledBackgroundGrass, (screenX, screenY))

        if self.backgroundDecorations is not None:
            # scaling to match the zoom
            scaledBackgroundDecorations = pygame.transform.scale(
                self.backgroundDecorations,
                (self.mapWidth * self.camera.zoom, self.mapHeight * self.camera.zoom),
            )
            # bliting on screen
            self.screen.blit(scaledBackgroundDecorations, (screenX, screenY))
