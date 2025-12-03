from backend.graph import Graph
import numpy as np

import string

class Loader:
    '''
    Loads from file with defined structure into data structures
    '''
    def __init__(self, path : string):
        with open(path, "r") as file:

            num_nodes = int(file.readline())
            self.coord_map = dict()
            for i in range(0,num_nodes):
                coords = tuple(float(x) for x in file.readline().split())
                self.coord_map[i] = coords
                
            num_edges = int(file.readline())
            self.graph = Graph()
            for i in range(0,num_edges):
                edge = list(file.readline().split())
                dist_vect = np.array(self.coord_map[int(edge[0])]) - np.array(self.coord_map[int(edge[1])])
                distance = abs(dist_vect[0] + dist_vect[1])
                edge.append(float(distance))
                self.graph.add_multiple_edges(edge)
            self.spawners = list(file.readline().split())
            self.destinations = list(file.readline().split())
            try:
                num_trafficlights = int(file.readline())
            except:
                num_trafficlights = 0

            self.trafficlights = list()
            crt_light = -1
            for i in range(0,num_trafficlights):
                light_list = [int(x) for x in list(file.readline().split())]
                if light_list[0] != crt_light:
                    light_list.append(False)
                    crt_light = light_list[0]
                else:
                    light_list.append(True)
                self.trafficlights.append(light_list)