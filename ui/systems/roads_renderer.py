import pygame

# each road representation
# the keys are alphabetical to remove differences between dlr and rld for example
# r - right, l - left, u - up, d - down
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

    # loading the roads assets right at the start of the game
    def loadRoadImages(self):
        for key in roadsImages:
            roadsImages[key] = pygame.image.load(roadsImages[key])

    # creates only once, when dirty, the surface for the roads
    def createRoadsSurface(self, roadNodes, roadConnections):
        # gets the grid consisting of road key strings as in "roadsImages"
        grid = self.parseRoads(roadNodes, roadConnections)

        self.carsSurface = pygame.Surface(
            (self.mapWidth, self.mapHeight), pygame.SRCALPHA
        )

        # dimensions of a cell
        cellWidth = self.mapWidth / self.gridColumns
        cellHeight = self.mapHeight / self.gridRows

        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                # world positions
                worldX = cellWidth * x
                worldY = cellHeight * y

                # converted to screen space
                screenX = (worldX - self.camera.x) * self.camera.zoom
                screenY = (worldY - self.camera.y) * self.camera.zoom

                # getting the right image or None
                img = roadsImages.get(grid[y][x], None)
                if img is not None:
                    # added 1 to fenceCellWidth and fenceCellHeight to solve visual gaps between cells
                    scaled_img = pygame.transform.scale(
                        img,
                        (
                            cellWidth * self.camera.zoom + 1,
                            cellHeight * self.camera.zoom + 1,
                        ),
                    )
                    # blitting on the cached surface
                    self.carsSurface.blit(scaled_img, (screenX, screenY))

        return grid

    # draws the cached surface on screen, using the camera parameters, each frame
    def draw(self):
        # screen position
        screenX = -self.camera.x * self.camera.zoom
        screenY = -self.camera.y * self.camera.zoom

        if self.carsSurface is not None:
            # scaling using the camera zoom
            scaledCarsSurface = pygame.transform.scale(
                self.carsSurface,
                (self.mapWidth * self.camera.zoom, self.mapHeight * self.camera.zoom),
            )
            # blitting on screen
            self.screen.blit(scaledCarsSurface, (screenX, screenY))

    # converting the roadNodes and roadConnections into a grid table with road keys
    def parseRoads(self, roadNodes, roadConnections):
        # initializing the grid
        grid = [["" for _ in range(self.gridColumns)] for _ in range(self.gridRows)]
        for i in range(0, len(roadConnections)):
            nodeX = roadNodes[i].x
            nodeY = roadNodes[i].y
            # for each neighbour, check the direction in which it should go, then populate that
            # path adding the direction's key
            for neighbour in roadConnections[i]:
                neighX = roadNodes[neighbour].x
                neighY = roadNodes[neighbour].y
                if neighX > nodeX:
                    for x in range(nodeX, neighX):
                        grid[nodeY][x] += "r"
                elif neighX < nodeX:
                    for x in range(neighX + 1, nodeX + 1):
                        grid[nodeY][x] += "l"
                if neighY < nodeY:
                    for y in range(neighY + 1, nodeY + 1):
                        grid[y][nodeX] += "u"
                elif neighY > nodeY:
                    for y in range(nodeY, neighY):
                        grid[y][nodeX] += "d"

        # then, sort them to differentiate between rld and dlr, for example
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j]:
                    grid[i][j] = "".join(sorted(grid[i][j]))
        return grid
