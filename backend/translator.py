from backend.graph import Graph
from backend.car import Car
from ui.car_ui import CarUI
import numpy as np


class Translator:
    def __init__(self, coord_map : dict):
        self.coord_map = coord_map
    def translate(self, car : Car):
        crt_node_coords = np.array(self.coord_map[car.crt_node])
        next_node_coords = np.array(self.coord_map[car.next_node])

        direction_vector = next_node_coords - crt_node_coords
        position = crt_node_coords + direction_vector * car.progress
        direction_vector = np.array(direction_vector)
        direction_vector = direction_vector / np.linalg.norm(direction_vector)
        speed = direction_vector * car.speed
        carUI = CarUI(car.id, position[0], position[1], speed[0], speed[1])
        return carUI
