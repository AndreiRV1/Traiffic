from rendering.data.road_tile_transform_ui import RoadTileTransformUI


class RoadsHelper:
    def __init__(self, coreRoadsImages):
        self.coreRoadsImages = coreRoadsImages
        self.cache = {}
        self.buildTransformCache()

    def buildTransformCache(self):
        self.cache = {}
        for baseEncoding, _ in self.coreRoadsImages.items():
            for horizontal in [False, True]:
                for vertical in [False, True]:
                    for rotations in range(4):
                        currentEncoding = baseEncoding

                        if horizontal:
                            currentEncoding = self.flipEncodingHorizontally(
                                currentEncoding
                            )
                        if vertical:
                            currentEncoding = self.flipEncodingVertially(
                                currentEncoding
                            )
                        for _ in range(rotations):
                            currentEncoding = self.rotateEncoding90CW(currentEncoding)

                        rotation_degrees = rotations * 90

                        if currentEncoding not in self.cache:
                            self.cache[currentEncoding] = RoadTileTransformUI(
                                baseEncoding, rotation_degrees, horizontal, vertical
                            )

    def getImageTransformation(self, encoding):
        if self.cache == None:
            raise ValueError(f"huh: {encoding}")
        if encoding not in self.cache:
            return self.cache["trbl--trbrbltl"]

        return self.cache[encoding]

    def rotateEncoding90CW(self, encoding):
        parts = encoding.split("-")
        goesTo, adj, adjDiag = parts[0], parts[1], parts[2]

        # rotate goes to
        newGoesTo = (
            goesTo.replace("t", "T")
            .replace("r", "R")
            .replace("b", "B")
            .replace("l", "L")
        )
        newGoesTo = (
            newGoesTo.replace("T", "r")
            .replace("R", "b")
            .replace("B", "l")
            .replace("L", "t")
        )
        newGoesTo = "".join(sorted(newGoesTo, key=lambda x: "trbl".index(x)))

        # rotate adj
        newAdj = (
            adj.replace("t", "T").replace("r", "R").replace("b", "B").replace("l", "L")
        )
        newAdj = (
            newAdj.replace("T", "r")
            .replace("R", "b")
            .replace("B", "l")
            .replace("L", "t")
        )
        newAdj = "".join(sorted(newAdj, key=lambda x: "trbl".index(x)))

        # rotate adj diag
        newAdjDiag = ""
        i = 0
        while i < len(adjDiag):
            if i + 1 < len(adjDiag):
                pair = adjDiag[i : i + 2]
                if pair == "tl":
                    newAdjDiag += "tr"
                elif pair == "tr":
                    newAdjDiag += "br"
                elif pair == "br":
                    newAdjDiag += "bl"
                elif pair == "bl":
                    newAdjDiag += "tl"
                i += 2
            else:
                i += 1

        diagList = []
        i = 0
        while i < len(newAdjDiag):
            if i + 1 < len(newAdjDiag):
                diagList.append(newAdjDiag[i : i + 2])
                i += 2
            else:
                i += 1
        diagOrder = {"tr": 0, "br": 1, "bl": 2, "tl": 3}
        diagList.sort(key=lambda x: diagOrder.get(x, 999))
        newAdjDiag = "".join(diagList)

        return newGoesTo + "-" + newAdj + "-" + newAdjDiag

    def flipEncodingHorizontally(self, encoding):
        parts = encoding.split("-")
        goesTo, adj, adjDiag = parts[0], parts[1], parts[2]

        # flip goes to
        newGoesTo = goesTo.replace("l", "L").replace("r", "R")
        newGoesTo = newGoesTo.replace("L", "r").replace("R", "l")
        newGoesTo = "".join(sorted(newGoesTo, key=lambda x: "trbl".index(x)))

        # flip adj
        newAdj = adj.replace("l", "L").replace("r", "R")
        newAdj = newAdj.replace("L", "r").replace("R", "l")
        newAdj = "".join(sorted(newAdj, key=lambda x: "trbl".index(x)))

        # rotate adj diag
        newAdjDiag = ""
        i = 0
        while i < len(adjDiag):
            if i + 1 < len(adjDiag):
                pair = adjDiag[i : i + 2]
                if pair == "tl":
                    newAdjDiag += "tr"
                if pair == "tr":
                    newAdjDiag += "tl"
                if pair == "bl":
                    newAdjDiag += "br"
                if pair == "br":
                    newAdjDiag += "bl"
                i += 2
            else:
                i += 1

        diagList = []
        i = 0
        while i < len(newAdjDiag):
            if i + 1 < len(newAdjDiag):
                diagList.append(newAdjDiag[i : i + 2])
                i += 2
            else:
                i += 1
        diagOrder = {"tr": 0, "br": 1, "bl": 2, "tl": 3}
        diagList.sort(key=lambda x: diagOrder.get(x, 999))
        newAdjDiag = "".join(diagList)

        return newGoesTo + "-" + newAdj + "-" + newAdjDiag

    def flipEncodingVertially(self, encoding):
        parts = encoding.split("-")
        goesTo, adj, adjDiag = parts[0], parts[1], parts[2]

        # flip goes to
        newGoesTo = goesTo.replace("t", "T").replace("b", "B")
        newGoesTo = newGoesTo.replace("T", "b").replace("B", "t")
        newGoesTo = "".join(sorted(newGoesTo, key=lambda x: "trbl".index(x)))

        # flip adj
        newAdj = adj.replace("t", "T").replace("b", "B")
        newAdj = newAdj.replace("T", "b").replace("B", "t")
        newAdj = "".join(sorted(newAdj, key=lambda x: "trbl".index(x)))

        # rotate adj diag
        newAdjDiag = ""
        i = 0
        while i < len(adjDiag):
            if i + 1 < len(adjDiag):
                pair = adjDiag[i : i + 2]
                if pair == "tl":
                    newAdjDiag += "bl"
                if pair == "bl":
                    newAdjDiag += "tl"
                if pair == "tr":
                    newAdjDiag += "br"
                if pair == "br":
                    newAdjDiag += "tr"
                i += 2
            else:
                i += 1

        diagList = []
        i = 0
        while i < len(newAdjDiag):
            if i + 1 < len(newAdjDiag):
                diagList.append(newAdjDiag[i : i + 2])
                i += 2
            else:
                i += 1
        diagOrder = {"tr": 0, "br": 1, "bl": 2, "tl": 3}
        diagList.sort(key=lambda x: diagOrder.get(x, 999))
        newAdjDiag = "".join(diagList)

        return newGoesTo + "-" + newAdj + "-" + newAdjDiag
