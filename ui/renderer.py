import pygame

roads = {
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


class Renderer:
    def __init__(self, screen, mapWidth, mapHeight, gridRows, gridColumns):
        self.screen = screen
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.gridRows = gridRows
        self.gridColumns = gridColumns
        self.loadRoadImages()

    def loadRoadImages(self):
        for key in roads:
            roads[key] = pygame.image.load(roads[key])

    def draw_world(self, state):
        self.screen.fill((100, 255, 0))
        self.drawRoads(
            self.gridRows, self.gridColumns, state.roadNodes, state.roadConnections
        )

    def drawRoads(self, gridRows, gridColumns, roadNodes, roadConnections):
        grid = self.parseRoads(gridRows, gridColumns, roadNodes, roadConnections)

        cellWidth = self.mapWidth / gridColumns
        cellHeight = self.mapHeight / gridRows

        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                x = cellWidth * j
                y = cellHeight * i
                img = roads.get(grid[i][j], None)
                if img is not None:
                    scaled_img = pygame.transform.scale(img, (cellWidth, cellHeight))
                    self.screen.blit(scaled_img, (x, y))

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
