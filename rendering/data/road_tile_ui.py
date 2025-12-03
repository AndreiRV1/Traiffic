class RoadTileUI:
    def __init__(self):
        # set if a car can move in that direction, not dependant on the road way
        self.goesToTop = False
        self.goesToRight = False
        self.goesToBottom = False
        self.goesToLeft = False

        # set if there is a road in that direction, next to this tile, but a car can't go there
        self.adjacentToTop = False
        self.adjacentToRight = False
        self.adjacentToBottom = False
        self.adjacentToLeft = False

        # set if there is a road in that direction, next to this tile
        self.adjacentToTopRight = False
        self.adjacentToBottomRight = False
        self.adjacentToBottomLeft = False
        self.adjacentToTopLeft = False

    def isARoad(self):
        return (
            self.goesToTop or self.goesToRight or self.goesToBottom or self.goesToLeft
        )

    def isAdjacentDirectlyToAnyRoad(self):
        return (
            self.adjacentToTop
            or self.adjacentToRight
            or self.adjacentToBottom
            or self.adjacentToLeft
        )

    def isAdjacentToAnything(self):
        return (
            self.adjacentToTop
            or self.adjacentToRight
            or self.adjacentToBottom
            or self.adjacentToLeft
            or self.adjacentToTopRight
            or self.adjacentToBottomRight
            or self.adjacentToBottomLeft
            or self.adjacentToTopLeft
        )

    def getEncoding(self):
        goesTo = ""
        if self.goesToTop:
            goesTo += "t"
        if self.goesToRight:
            goesTo += "r"
        if self.goesToBottom:
            goesTo += "b"
        if self.goesToLeft:
            goesTo += "l"

        adjacentToDirectly = ""
        if self.adjacentToTop:
            adjacentToDirectly += "t"
        if self.adjacentToRight:
            adjacentToDirectly += "r"
        if self.adjacentToBottom:
            adjacentToDirectly += "b"
        if self.adjacentToLeft:
            adjacentToDirectly += "l"

        adjancentToDiagonally = ""
        if self.adjacentToTopRight:
            adjancentToDiagonally += "tr"
        if self.adjacentToBottomRight:
            adjancentToDiagonally += "br"
        if self.adjacentToBottomLeft:
            adjancentToDiagonally += "bl"
        if self.adjacentToTopLeft:
            adjancentToDiagonally += "tl"

        return goesTo + "-" + adjacentToDirectly + "-" + adjancentToDiagonally

    def __repr__(self):
        return self.getEncoding()
