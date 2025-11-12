from ui.data.car_ui import CarUI 
from ui.data.road_node_ui import *
from backend.translator import Translator
from backend.translator import Translator_follow
from backend.car import Car
from backend.car_follow import Car_follow
from backend.loader import Loader
import random
from backend.utils import *

class UIState:
    def __init__ (self, roadNodes, roadConnections, cars): 
        self. roadNodes = roadNodes
        self. roadConnections = roadConnections
        self.cars = cars

class Simulation:
    def __init__(self):
        loader = Loader("./data/predefined_level.traiffic")
        self.graph = loader.graph
        self.coord_map = loader.coord_map
        self.spawners = loader.spawners
        self.cars = []
        self.translator = Translator()
        self.translator_follow = Translator_follow(self.coord_map)

    def update(self, dt):
        if self.cars.__len__() == 0:
            source, destination = random.sample(self.spawners,2)
            path = self.graph.traverse(source,destination)
            source = int(source)
            destination = int(destination)
            coords = path_to_coords(path,self.coord_map)
            new_car = Car_follow(self.coord_map[source],self.graph,coords)
            self.cars.append(new_car)
        for car in self.cars:
            if not car.update(dt):
                self.cars.remove(car)
        
    
    def export_ui_state(self):
        roadNodes = [ RoadNodeUI (0, 0),RoadNodeUI(3, 3),RoadNodeUI(0, 3),RoadNodeUI(20, 3),RoadNodeUI(3, 14),]
        roadConnections = [[int(t[0]) for t in self.graph.adj_list[key]] for key in sorted(self.graph.adj_list.keys())]
        cars = self.translator.translate(self.cars)
        print(self.cars.__len__())
        return UIState(roadNodes, roadConnections, cars)
