import numpy as np

def path_to_coords(path:list, coord_map):
    '''
    Function converts a list of nodes into a list 
    of their coordinates using the map
    '''
    coord_list = list()
    for node in path:
        coord_list.append(np.array(coord_map[node]))
    return coord_list

def signed_angle(v1, v2, degrees=False):
    '''
    Function computes the angle between vectors
    and keeps sign orientation
    '''
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    dot = np.dot(v1, v2)
    cross = np.cross(v1, v2)
    angle = np.arctan2(cross, dot)
    
    if degrees:
        angle = np.degrees(angle)
    return angle

def check_collision(car1, car2):
    '''
    Function checks if two cars collide
    Each car is viewed as a circle with radius
    specified in constructor
    '''
    distance = np.linalg.norm(car1.position - car2.position)
    if distance < car1.radius_detect + car2.radius_detect:
        print("Collision detected!!!!!!!!!")
        car1.crash = True
        car2.crash = True
        return True
    return False

def get_road_bounds(graph, coord_map, margin):
    '''
    Returns a list of road bounds from the graph and coordinates map.
    Each road bound is a dict: {x_min, x_max, y_min, y_max}
    '''
    margin = 0.3
    bounds = []
    for start_node, neighbors in graph.adj_list.items():
        x1, y1 = coord_map[int(start_node)]
        for end_node, _ in neighbors:
            x2, y2 = coord_map[int(end_node)]
            x_min = min(x1, x2) - margin
            x_max = max(x1, x2) + margin
            y_min = min(y1, y2) - margin
            y_max = max(y1, y2) + margin
            bounds.append({"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max})
    return bounds


def check_street_collision(car, road_bounds):
    '''
    Checks if a car collides with a road bound
    '''
    x, y = car.position
    r = car.radius_detect
    for road in road_bounds:
        print(f"Car {car.id} at ({x:.2f},{y:.2f}) checking road bound {road}")
        if road["x_min"] - r <= x <= road["x_max"] + r and road["y_min"] - r <= y <= road["y_max"] + r:
            return False
    print(f"Car {car.id} went off the street!")
    return True


class PID:
    '''
    Simple PID controller for input management
    '''
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.prev_error = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative
