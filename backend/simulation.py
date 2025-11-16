from ui.data.car_ui import CarUI 
from ui.data.road_node_ui import *
from backend.translator import Translator
#from backend.translator import Translator_follow
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
        self.spawn_interval = 1.0
        self.time_since_last_spawn = 0.0
        self.road_bounds = get_road_bounds(self.graph, self.coord_map, margin=1.0)
#        self.translator_follow = Translator_follow(self.coord_map)

    def update(self, dt):
        #if self.cars.__len__() == 0:
        #    # Adds one car at a time
        #    source, destination = random.sample(self.spawners,2)
        #    path = self.graph.traverse(source,destination)
        #    source = int(source)
        #    destination = int(destination)
        #    coords = path_to_coords(path,self.coord_map)
        #    new_car = Car_follow(self.coord_map[source],self.graph,coords)
        #    self.cars.append(new_car)
        self.time_since_last_spawn += dt
        if self.time_since_last_spawn >= self.spawn_interval:
            self.time_since_last_spawn = 0.0
            self.spawn_car()
        for car in self.cars:
            if not car.update(dt, all_cars = self.cars, road_bounds = self.road_bounds) or car.crashed == True:
                self.cars.remove(car)

    #Car spawner method for easier testing
    def spawn_car(self):
        source, destination = random.sample(self.spawners,2)
        path = self.graph.traverse(source,destination)
        source = int(source)
        destination = int(destination)
        coords = path_to_coords(path,self.coord_map)
        if not coords:
            return
        new_car = Car_follow(self.coord_map[source],self.graph,coords)
        self.cars.append(new_car)

    def export_ui_state(self):
        roadNodes = [ RoadNodeUI (0, 0),RoadNodeUI(3, 3),RoadNodeUI(0, 3),RoadNodeUI(20, 3),RoadNodeUI(3, 14),]
        roadConnections = [[int(t[0]) for t in self.graph.adj_list[key]] for key in sorted(self.graph.adj_list.keys())]
        cars = self.translator.translate(self.cars)
        return UIState(roadNodes, roadConnections, cars)
