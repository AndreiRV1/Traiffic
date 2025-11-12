from backend.graph import Graph
from backend.car import Car
import numpy as np
import random
from backend.utils import signed_angle

class Car_follow(Car):
    def __init__(self,position, graph : Graph, path: list):
        self.graph = graph
        self.path = path
        self.crt_node = 1
        self.target = self.path[1]
        self.destination = self.path[self.path.__len__()-1]
        facing = self.path[1] - self.path[0]
        super().__init__(position,facing)


# Function will update current instance of car, returning 0     when car reached destination and 1 else
    def update(self, dt : float):
        distance_to_dest = np.linalg.norm(self.position - self.destination)
        if(distance_to_dest < 0.1):
            return 0
        dir_to_next = self.target - self.position
        dist_to_next = np.linalg.norm(dir_to_next)
        if(dist_to_next < 0.1):
            self.crt_node +=1
            self.target = self.path[self.crt_node]
        dot = np.dot(self.facing,dir_to_next)
        if dot > 0:
            forward = 1
        else:
            forward = -1
        angle = signed_angle(self.facing,dir_to_next)
        print(dot)
        print(angle)
        if angle > 0:
            steer = 1
        else:
            steer = -1
        self.move(forward,steer,dt)
        return 1