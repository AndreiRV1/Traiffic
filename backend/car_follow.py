from backend.graph import Graph
from backend.car import Car
import numpy as np
import random
#from backend.utils import signed_angle,round,PID
from backend.utils import PID, signed_angle, check_collision, check_street_collision


class Car_follow(Car):
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
        self.time_limit = 4
        self.elapsed_time = 0
        self.isAgressive = False
        super().__init__(position,facing)


# Function will update current instance of car, returning 0 when car reached destination and 1 else
    def update(self, dt : float, all_cars, road_bounds, trafficLights, coordmap):
        lead_car = None
        # Collision check between cars:
        if all_cars:
            for car2 in all_cars:
                if car2.id != self.id and check_collision(car2,self):
                    self.crashed = True
                    car2.crashed = True
                    return 0
        # Road bounds check
        if road_bounds and check_street_collision(self, road_bounds):
            print("Road bounds reached!!!!!!!!!!!!!!!!!!!!!!")
            self.crashed = True
            return 0
        if self.speed > 0 and not self.isAgressive:
            self.elapsed_time = 0
        else:
            self.elapsed_time+=dt
        
        # Intelligent driver approach to speed control
        dir_to_next = self.target - self.position
        dist_to_next = np.linalg.norm(dir_to_next)
        target_speed = 0.25

        if self.crt_node + 1 < len(self.path):
            v1 = self.path[self.crt_node] - self.position
            v2 = self.path[self.crt_node + 1] - self.path[self.crt_node]
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            if norm_v1 > 0 and norm_v2 > 0:
                u1 = v1 / norm_v1
                u2 = v2 / norm_v2
                dot_prod = np.clip(np.dot(u1, u2), -1.0, 1.0)
                angle = np.arccos(dot_prod)
                if angle > 0.5 and norm_v1 < 2.0:
                    target_speed = 0.03 # Slow speed for corners
                elif norm_v1 < 5.0:
                    target_speed = 0.08 # Slows before intersection anyways
            if self.shouldYield(all_cars,trafficLights,coordmap):
                target_speed = 0

        forward = self.getAcceleration(target_speed,self.get_closest_lead_car(all_cars))
        # print(self.get_closest_lead_car(all_cars))

        # Pure pursuit for steering control
        target_angle = np.arctan2(dir_to_next[1],dir_to_next[0])
        current_angle = np.arctan2(self.facing[1],self.facing[0])
        delta_angle = target_angle - current_angle
        delta_angle = (delta_angle + np.pi) % (2 * np.pi) - np.pi 

        steer = delta_angle * 2.0

        #Get next lookahead
        if -0.2 < dist_to_next < 0.2:
            return self.getNextPoint(0.5)

        self.move(forward,steer,dt)
        return 1


    # Gets next target point in Pure Pursuit style
    def getNextPoint(self, lookahead):
        if(self.crt_node >= self.path.__len__()-1):
            return 0
        if np.linalg.norm(self.target - self.path[self.crt_node + 1]) < 0.1:
            self.crt_node +=1
            if self.crt_node >= self.path.__len__()-1:
                return 0
        if self.isAgressive:
            self.isAgressive = False
        direction = np.array(self.path[self.crt_node + 1]) - np.array(self.path[self.crt_node])
        direction = direction / np.linalg.norm(direction)
        direction *= lookahead
        self.target += direction
        if(np.linalg.norm(self.target - self.path[self.crt_node + 1]) < lookahead):
            self.target = self.path[self.crt_node + 1]
        return 1

    # Uses Intellident Driver to give acceleration command
    def getAcceleration(self,target_speed,lead_car):
        T = 1.5      # Safe time headway (seconds) - "2 second rule"
        s0 = 3.0     # Minimum stopping distance (meters)
        a = 0.05      # Max acceleration (m/s^2) - roughly matches your self.accelerate_step?
        b = 4.0      # Comfortable deceleration (m/s^2)
        delta = 4    # Acceleration exponent (usually 4)

        v = self.speed
        v0 = target_speed

        if lead_car is None:
            s = 1000.0
            dv = 0.0
        else:
            s = np.linalg.norm(lead_car.position - self.position)
            dv = self.speed - lead_car.speed

        if s <= 0.1: s = 0.1
        s_star = s0 + (v * T) + (v * dv) / (2 * np.sqrt(a * b))
        if target_speed != 0:
            accel_phys = a * (1 - (v / v0)**delta - (s_star / s)**2)
        else:
            if self.speed < 0.000001:
                return 0
            else:
                return -(2.0/self.accelerate_step)
        return accel_phys / self.accelerate_step

    # Gets car ahead
    def get_closest_lead_car(self, all_cars, scan_distance=15.0, fov_deg=5):
        closest_car = None
        min_dist = float('inf')
        fov_rad = np.deg2rad(fov_deg)
        for other_car in all_cars:
            if other_car.id == self.id:
                continue
            vec_to_other = other_car.position - self.position
            dist = np.linalg.norm(vec_to_other)
            if dist > scan_distance:
                continue
            heading_dot = np.dot(self.facing, other_car.facing)
            if heading_dot < 0.5:
                continue
            my_heading_angle = np.arctan2(self.facing[1], self.facing[0])
            angle_to_other = np.arctan2(vec_to_other[1], vec_to_other[0])
            angle_diff = angle_to_other - my_heading_angle
            angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi
            if -fov_rad < angle_diff < fov_rad:
                if dist < min_dist:
                    min_dist = dist
                    closest_car = other_car

        return closest_car


    # Determines if car should yield
    def shouldYield(self, all_cars,trafficLights,coordmap):
        if self.crt_node >= len(self.path):
            return False

        next_node_pos = self.path[self.crt_node]
        my_dist = np.linalg.norm(next_node_pos - self.position)

        if my_dist > 3:
            return False

        wait = False
        isLight = False
        for light in trafficLights:
            if  np.linalg.norm(self.path[self.crt_node] - coordmap[int(light[0])]) < 0.1:
                prev_pos = self.path[self.crt_node - 1]
                curr_pos = self.path[self.crt_node]
                vec = curr_pos - prev_pos
                coming_from = -1
                if abs(vec[0]) > abs(vec[1]):
                    if vec[0] > 0:
                        coming_from = 3
                    else:
                        coming_from = 1
                else:
                    if vec[1] > 0:
                        coming_from = 0
                    else:
                        coming_from = 2
                if int(light[1]) == coming_from and light[2] == True:
                    isLight = True
                    wait = True
                    break
                if int(light[1]) == coming_from:
                    isLight = True
                    break
        if isLight:
            # print("Light")
            return wait
        
        if self.elapsed_time > self.time_limit:
            self.isAgressive = True

        for other in all_cars:
            if other.id == self.id:
                continue
            if other.crt_node>= len(other.path):
                continue

            other_next_node_pos = other.path[other.crt_node]
            if np.linalg.norm(next_node_pos - other_next_node_pos) < 1.5:
                my_prev = self.path[self.crt_node - 1]
                other_prev = other.path[other.crt_node - 1]
                if np.linalg.norm(my_prev - other_prev) < 0.1:
                    continue

                other_dist = np.linalg.norm(other_next_node_pos - other.position)

                if other_dist < 0.7:
                    # print("Other is closer")
                    return True
                if self.isAgressive:
                    print("Is aggressive")
                    return False

                if my_dist < 2 and other_dist < 2:
                    if abs(self.speed) < 0.1 and abs(other.speed) < 0.1:
                        if other.id < self.id:
                            # print("Tie breaker2")
                            return True
                        else:
                            continue

                if abs(my_dist - other_dist) < 1.5:
                    my_angle = np.arctan2(self.facing[1], self.facing[0])
                    other_angle = np.arctan2(other.facing[1], other.facing[0])
                    diff = my_angle - other_angle
                    diff = (diff + np.pi) % (2 * np.pi) - np.pi
                    diff_deg = np.degrees(diff)
                    
                    if 80 < diff_deg < 100:
                        # print("Right hand")
                        return True

        return False
