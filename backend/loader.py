from backend.graph import Graph

import string

class Loader:
    def __init__(self, path : string):
        with open(path, "r") as file:
            num_edges = int(file.readline())
            self.graph = Graph()
            for i in range(0,num_edges):
                edge = list(file.readline().split())
                edge[2] = float(edge[2])
                self.graph.add_multiple_edges(edge)
            self.coord_map = dict()
            for i in range(0,len(self.graph.adj_list)):
                coords = tuple(float(x) for x in file.readline().split())
                self.coord_map[list(self.graph.adj_list.keys())[i]] = coords
            self.spawners = list(file.readline().split())