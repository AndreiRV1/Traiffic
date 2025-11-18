from backend.graph import Graph
from backend.car import Car
import numpy as np
import random
#from backend.utils import signed_angle,round,PID
from backend.utils import PID, signed_angle, check_collision, check_street_collision


class Car_follow(Car):
    '''
    PID enabled car that follows certain path
    '''
    def __init__(self,position, graph : Graph, path: list):
        self.graph = graph
        self.path = path
        self.crt_node = 1
        self.target = self.path[1]
        self.destination = self.path[self.path.__len__()-1]
        facing = self.path[1] - self.path[0]
        self.pid_speed = PID(Kp=1.5, Ki=-0.02, Kd=0.5)
        self.pid_steer = PID(Kp=10, Ki=-0.02, Kd=0.1)
        self.crashed = False
        print(self.path)
        super().__init__(position,facing)


# Function will update current instance of car, returning 0 when car reached destination and 1 else
    def update(self, dt : float, all_cars, road_bounds):
        dir_to_next = self.target - self.position
        dot = np.dot(self.facing, dir_to_next)
        if dot == 0:
            dot = 1
        dist_to_next = np.linalg.norm(dir_to_next) * np.sign(dot)
        print(dist_to_next)
        print(f"Car {self.id} updating at {self.position}")

        if -1 < dist_to_next < 1:
            print(self.crt_node, self.target)
            self.crt_node +=1
            if self.crt_node >= self.path.__len__():
                return 0
            else:
                self.target = self.path[self.crt_node]
                return 1
        angle = signed_angle(self.facing,dir_to_next,True)
        forward = self.pid_speed.update(dist_to_next, dt)
        steer = self.pid_steer.update(angle, dt)
        # Collision check between cars:
        if all_cars:
            for car2 in all_cars:
                if car2.id != self.id:
                    dist = np.linalg.norm(self.position - car2.position)
                    print(f"Car {self.id} -> {car2.id}: dist {dist}")
                if car2.id != self.id and check_collision(car2,self):
                    self.crashed = True
                    car2.crashed = True
                    return 0
        # Road bounds check
        if road_bounds and check_street_collision(self, road_bounds):
            print("Road bounds reached!!!!!!!!!!!!!!!!!!!!!!")
            self.crashed = True
            return 0
        self.move(forward,steer,dt)
        return 1