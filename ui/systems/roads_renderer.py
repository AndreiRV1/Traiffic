import pygame


roadsImages = {
    # 1 way
    "r": "./assets/roads/road_s_r.png",
    "l": "./assets/roads/road_s_l.png",
    "u": "./assets/roads/road_s_u.png",
    "d": "./assets/roads/road_s_d.png",
    # 2 way
    "lr": "./assets/roads/road_s_rl.png",
    "ru": "./assets/roads/road_s_ru.png",
    "dr": "./assets/roads/road_s_rd.png",
    "du": "./assets/roads/road_s_ud.png",
    "lu": "./assets/roads/road_s_lu.png",
    "dl": "./assets/roads/road_s_ld.png",
    # 3 way
    "dlr": "./assets/roads/road_s_rld.png",
    "dlu": "./assets/roads/road_s_lud.png",
    "lru": "./assets/roads/road_s_rlu.png",
    "dru": "./assets/roads/road_s_rud.png",
    # 4 way
    "dlru": "./assets/roads/road_s_rlud.png",
}


class RoadsRenderer:
    def __init__(self, camera, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.camera = camera
        self.screen = screen
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.gridRows = gridRows
        self.gridColumns = gridColumns
        self.carsSurface = None
        self.loadRoadImages()

    def loadRoadImages(self):
        for key in roadsImages:
            roadsImages[key] = pygame.image.load(roadsImages[key])

    def createCarsSurface(self, roadNodes, roadConnections):
        grid = self.parseRoads(roadNodes, roadConnections)

        self.carsSurface = pygame.Surface(
            (self.mapWidth, self.mapHeight), pygame.SRCALPHA
        )

        cellWidth = self.mapWidth / self.gridColumns
        cellHeight = self.mapHeight / self.gridRows

        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                worldX = cellWidth * x
                worldY = cellHeight * y
                screenX = (worldX - self.camera.x) * self.camera.zoom
                screenY = (worldY - self.camera.y) * self.camera.zoom
                img = roadsImages.get(grid[y][x], None)
                if img is not None:
                    scaled_img = pygame.transform.scale(
                        img,
                        (
                            cellWidth * self.camera.zoom + 1,
                            cellHeight * self.camera.zoom + 1,
                        ),
                    )
                    self.carsSurface.blit(scaled_img, (screenX, screenY))

        return grid

    def draw(self):
        screenX = -self.camera.x * self.camera.zoom
        screenY = -self.camera.y * self.camera.zoom

        if self.carsSurface is not None:
            scaledCarsSurface = pygame.transform.scale(
                self.carsSurface,
                (self.mapWidth * self.camera.zoom, self.mapHeight * self.camera.zoom),
            )
            self.screen.blit(scaledCarsSurface, (screenX, screenY))

    def parseRoads(self, roadNodes, roadConnections):
        grid = [["" for _ in range(self.gridColumns)] for _ in range(self.gridRows)]
        for i in range(0, len(roadConnections)):
            nodeX = roadNodes[i].x
            nodeY = roadNodes[i].y
            for neighbour in roadConnections[i]:
                neighX = roadNodes[neighbour].x
                neighY = roadNodes[neighbour].y
                if neighX > nodeX:
                    grid[nodeY][nodeX] += "r"
                    for x in range(nodeX + 1, neighX):
                        grid[nodeY][x] += "r"
                elif neighX < nodeX:
                    grid[nodeY][nodeX] += "l"
                    for x in range(neighX + 1, nodeX):
                        grid[nodeY][x] += "l"

                if neighY < nodeY:
                    grid[nodeY][nodeX] += "u"
                    for y in range(neighY + 1, nodeY):
                        grid[y][nodeX] += "u"
                elif neighY > nodeY:
                    grid[nodeY][nodeX] += "d"
                    for y in range(nodeY + 1, neighY):
                        grid[y][nodeX] += "d"

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j]:
                    grid[i][j] = "".join(sorted(grid[i][j]))
        return grid
