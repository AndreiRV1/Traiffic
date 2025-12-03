import pygame

from rendering.data.road_tile_ui import RoadTileUI
from rendering.systems.roads_helper import RoadsHelper

# each road representation
# the keys are alphabetical to remove differences between dlr and rld for example
# r - right, l - left, u - up, d - down
coreRoadsImages = {
    "--": "./assets/roads/--.png",
    "t--": "./assets/roads/t--.png",
    "t-r-tr": "./assets/roads/t-r-tr.png",
    "t-r-": "./assets/roads/t-r-.png",
    "t-rl-trtl": "./assets/roads/t-rl-trtl.png",
    "t-rl-tr": "./assets/roads/t-rl-tr.png",
    "t-rl-": "./assets/roads/t-rl-.png",
    "tb--": "./assets/roads/tb--.png",
    "tb-r-trbr": "./assets/roads/tb-r-trbr.png",
    "tb-r-br": "./assets/roads/tb-r-br.png",
    "tb-r-": "./assets/roads/tb-r-.png",
    "tb-rl-trbrbltl": "./assets/roads/tb-rl-trbrbltl.png",
    "tb-rl-brbltl": "./assets/roads/tb-rl-brbltl.png",
    "tb-rl-brbl": "./assets/roads/tb-rl-brbl.png",
    "tb-rl-trbl": "./assets/roads/tb-rl-trbl.png",
    "tr--": "./assets/roads/tr--.png",
    "tr--tr": "./assets/roads/tr--tr.png",
    "tr-l-tl": "./assets/roads/tr-l-.png",
    "tr-l-trtl": "./assets/roads/tr-l-tr.png",
    "tr-l-": "./assets/roads/tr-l-tr.png",
    "tr-l-tr": "./assets/roads/tr-l-tr.png",
    "tr-bl-brbltl": "./assets/roads/tr-bl-brbltl.png",
    "tr-bl-trbrbltl": "./assets/roads/tr-bl-trbrbltl.png",
    "tr-bl-trbrbl": "./assets/roads/tr-bl-trbrbl.png",
    "tr-bl-trbrtl": "./assets/roads/tr-bl-trbrtl.png",
    "tr-bl-bltl": "./assets/roads/tr-bl-bltl.png",
    "tr-bl-brtl": "./assets/roads/tr-bl-brtl.png",
    "tr-bl-trbl": "./assets/roads/tr-bl-trbl.png",
    "tr-bl-bl": "./assets/roads/tr-bl-bl.png",
    "trl--": "./assets/roads/trl--.png",
    "trl--tr": "./assets/roads/trl--tr.png",
    "trl--trtl": "./assets/roads/trl--trtl.png",
    "trl-b-brbl": "./assets/roads/trl-b-brbl.png",
    "trl-b-trbrbl": "./assets/roads/trl-b-trbrbl.png",
    "trl-b-trbrbltl": "./assets/roads/trl-b-trbrbltl.png",
    "trl-b-trbrtl": "./assets/roads/trl-b-trbrtl.png",
    "trl-b-trbr": "./assets/roads/trl-b-trbr.png",
    "trl-b-trbl": "./assets/roads/trl-b-trbl.png",
    "trl-b-bl": "./assets/roads/trl-b-bl.png",
    "trbl--trbrbltl": "./assets/roads/trbl--trbrbltl.png",
    "trbl--brbltl": "./assets/roads/trbl--brbltl.png",
    "trbl--bltl": "./assets/roads/trbl--bltl.png",
    "trbl--brtl": "./assets/roads/trbl--brtl.png",
    "trbl--tr": "./assets/roads/trbl--tr.png",
    "trbl--": "./assets/roads/trbl--.png",
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
        self.roadsHelper = RoadsHelper(coreRoadsImages)
        self.loadRoadImages()

    # loading the roads assets right at the start of the game
    def loadRoadImages(self):
        for key in coreRoadsImages:
            coreRoadsImages[key] = pygame.image.load(coreRoadsImages[key])

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

                transformation = self.roadsHelper.getImageTransformation(
                    grid[y][x].getEncoding()
                )
                img = coreRoadsImages.get(transformation.coreImageEncoding, None)
                if img is not None:
                    if transformation.mirrorHorizontal:
                        img = pygame.transform.flip(img, True, False)
                    if transformation.mirrorVertical:
                        img = pygame.transform.flip(img, False, True)
                    if transformation.rotation != 0:
                        img = pygame.transform.rotate(img, -transformation.rotation)

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
        grid = [
            [RoadTileUI() for _ in range(self.gridColumns)]
            for _ in range(self.gridRows)
        ]
        for i in range(0, len(roadConnections)):
            nodeX = roadNodes[i].x
            nodeY = roadNodes[i].y
            # for each neighbour, check the direction in which it should go, then populate that
            # path adding the direction's key
            for neighbour in roadConnections[i]:
                neighX = roadNodes[neighbour].x
                neighY = roadNodes[neighbour].y
                if neighX > nodeX:
                    for x in range(nodeX + 1, neighX):
                        grid[nodeY][x].goesToRight = True
                        grid[nodeY][x].goesToLeft = True
                    grid[nodeY][nodeX].goesToRight = True
                    grid[neighY][neighX].goesToLeft = True
                elif neighX < nodeX:
                    for x in range(neighX + 1, nodeX):
                        grid[nodeY][x].goesToRight = True
                        grid[nodeY][x].goesToLeft = True
                    grid[nodeY][nodeX].goesToLeft = True
                    grid[neighY][neighX].goesToRight = True
                if neighY < nodeY:
                    for y in range(neighY + 1, nodeY):
                        grid[y][nodeX].goesToTop = True
                        grid[y][nodeX].goesToBottom = True
                    grid[nodeY][nodeX].goesToTop = True
                    grid[neighY][neighX].goesToBottom = True
                elif neighY > nodeY:
                    for y in range(nodeY + 1, neighY):
                        grid[y][nodeX].goesToTop = True
                        grid[y][nodeX].goesToBottom = True
                    grid[nodeY][nodeX].goesToBottom = True
                    grid[neighY][neighX].goesToTop = True

        for x in range(0, self.gridColumns):
            for y in range(0, self.gridRows):
                r = grid[y][x]
                if not r.isARoad():
                    continue

                if r.goesToTop or r.goesToBottom:
                    if 0 <= x - 1 < self.gridColumns and r.goesToLeft == False:
                        if grid[y][x - 1].goesToTop or grid[y][x - 1].goesToBottom:
                            r.adjacentToLeft = True
                    if 0 <= x + 1 < self.gridColumns and r.goesToRight == False:
                        if grid[y][x + 1].goesToTop or grid[y][x + 1].goesToBottom:
                            r.adjacentToRight = True

                if r.goesToLeft or r.goesToRight:
                    if 0 <= y - 1 < self.gridRows and r.goesToTop == False:
                        if grid[y - 1][x].goesToLeft or grid[y - 1][x].goesToRight:
                            r.adjacentToTop = True
                    if 0 <= y + 1 < self.gridRows and r.goesToBottom == False:
                        if grid[y + 1][x].goesToLeft or grid[y + 1][x].goesToRight:
                            r.adjacentToBottom = True

                if 0 <= x - 1 < self.gridColumns and 0 <= y - 1 < self.gridRows:
                    r1 = grid[y - 1][x - 1]
                    if (
                        r1.isARoad()
                        and (r.goesToLeft or r.adjacentToLeft)
                        and (r.goesToTop or r.adjacentToTop)
                    ):
                        r.adjacentToTopLeft = True

                if 0 <= x - 1 < self.gridColumns and 0 <= y + 1 < self.gridRows:
                    r1 = grid[y + 1][x - 1]
                    if (
                        r1.isARoad()
                        and (r.goesToLeft or r.adjacentToLeft)
                        and (r.goesToBottom or r.adjacentToBottom)
                    ):
                        r.adjacentToBottomLeft = True
                if 0 <= x + 1 < self.gridColumns and 0 <= y - 1 < self.gridRows:
                    r1 = grid[y - 1][x + 1]
                    if (
                        r1.isARoad()
                        and (r.goesToRight or r.adjacentToRight)
                        and (r.goesToTop or r.adjacentToTop)
                    ):
                        r.adjacentToTopRight = True
                if 0 <= x + 1 < self.gridColumns and 0 <= y + 1 < self.gridRows:
                    r1 = grid[y + 1][x + 1]
                    if (
                        r1.isARoad()
                        and (r.goesToRight or r.adjacentToRight)
                        and (r.goesToBottom or r.adjacentToBottom)
                    ):
                        r.adjacentToBottomRight = True

        return grid
