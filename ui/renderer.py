import pygame

roadsImages = {
    "r": "./assets/road_s_r.png",
    "l": "./assets/road_s_l.png",
    "u": "./assets/road_s_u.png",
    "d": "./assets/road_s_d.png",
    # 2way
    "lr": "./assets/road_s_rl.png",
    "ru": "./assets/road_s_ru.png",
    "dr": "./assets/road_s_rd.png",
    "du": "./assets/road_s_ud.png",
    "lu": "./assets/road_s_lu.png",
    "dl": "./assets/road_s_ld.png",
    # 3 way
    "dlr": "./assets/road_s_rld.png",
    "dlu": "./assets/road_s_lud.png",
    "lru": "./assets/road_s_rlu.png",
    "dru": "./assets/road_s_rud.png",
    # 4 way
    "dlru": "./assets/road_s_rlud.png",
}

carsImages = [
    "./assets/green_car.png",
    "./assets/blue_car.png",
    "./assets/red_car.png",
    "./assets/orange_car.png",
]


class Renderer:
    def __init__(self, camera, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.camera = camera
        self.screen = screen
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.gridRows = gridRows
        self.gridColumns = gridColumns
        self.loadRoadImages()
        self.loadCarImages()

    def loadRoadImages(self):
        for key in roadsImages:
            roadsImages[key] = pygame.image.load(roadsImages[key])

    def loadCarImages(self):
        for index in range(0, len(carsImages)):
            carsImages[index] = pygame.image.load(carsImages[index])

    def draw_world(self, state):
        self.screen.fill((75, 175, 63))
        self.drawRoads(
            self.camera,
            self.gridRows,
            self.gridColumns,
            state.roadNodes,
            state.roadConnections,
        )
        self.drawCars(self.camera, self.gridRows, self.gridColumns, state.cars)

    def drawRoads(self, camera, gridRows, gridColumns, roadNodes, roadConnections):
        grid = self.parseRoads(gridRows, gridColumns, roadNodes, roadConnections)

        cellWidth = self.mapWidth / gridColumns
        cellHeight = self.mapHeight / gridRows

        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                worldX = cellWidth * j
                worldY = cellHeight * i
                screenX = (worldX - camera.x) * camera.zoom
                screenY = (worldY - camera.y) * camera.zoom
                img = roadsImages.get(grid[i][j], None)
                if img is not None:
                    scaled_img = pygame.transform.scale(
                        img,
                        (cellWidth * camera.zoom + 1, cellHeight * camera.zoom + 1),
                    )
                    self.screen.blit(scaled_img, (screenX, screenY))

    def parseRoads(self, gridRows, gridColumns, roadNodes, roadConnections):
        grid = [["" for _ in range(gridColumns)] for _ in range(gridRows)]
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

    def drawCars(self, camera, gridRows, gridColumns, cars):
        cellWidth = self.mapWidth / gridColumns
        cellHeight = self.mapHeight / gridRows

        for car in cars:
            worldX = car.x * cellWidth
            worldY = car.y * cellHeight
            screenX = (worldX - camera.x) * camera.zoom
            screenY = (worldY - camera.y) * camera.zoom
            img = carsImages[car.id % len(carsImages)]
            if img is not None:
                scaled_img = pygame.transform.scale(
                    img, (cellWidth * camera.zoom, cellHeight * camera.zoom)
                )
                rotated_img = pygame.transform.rotate(scaled_img, car.get_direction())
                self.screen.blit(rotated_img, (screenX, screenY))
