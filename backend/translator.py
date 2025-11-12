from backend.graph import Graph
from backend.car import Car
from ui.data.car_ui import CarUI
import numpy as np


class Translator_follow:
    def __init__(self, coord_map : dict):
        self.coord_map = coord_map
    def translate(self, cars):
        carsUI = list()
        for car in cars:
            crt_node_coords = np.array(self.coord_map[int(car.crt_node)])
            next_node_coords = np.array(self.coord_map[int(car.next_node)])
            direction_vector = next_node_coords - crt_node_coords
            position = crt_node_coords + direction_vector * car.progress / car.crt_cost
            direction_vector = np.array(direction_vector)
            speed = direction_vector * car.speed
            carUI = CarUI(car.id, position[0], position[1], speed[0], speed[1])
            carsUI.append(carUI)
        return carsUI
    
class Translator:
    def translate(self, cars):
        carsUI = list()
        for car in cars:
            carUI = CarUI(car.id,car.position[0],car.position[1],car.facing[0],car.facing[1])
            carsUI.append(carUI)
        return carsUI

