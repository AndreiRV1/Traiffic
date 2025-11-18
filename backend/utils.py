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
        car1.crashed = True
        car2.crashed = True
        return True
    return False


def get_road_bounds(graph, coord_map, margin, car_radius):
    """
    Returns padded road bounds for each edge.
    Adds car_radius to ensure collision triggers even for tiny overshoots.
    """
    bounds = []
    for start_node, neighbors in graph.adj_list.items():
        x1, y1 = coord_map[int(start_node)]
        for end_node, _ in neighbors:
            x2, y2 = coord_map[int(end_node)]

            x_min = min(x1, x2) - margin - car_radius
            x_max = max(x1, x2) + margin + car_radius
            y_min = min(y1, y2) - margin - car_radius
            y_max = max(y1, y2) + margin + car_radius

            bounds.append({"x_min": x_min, "x_max": x_max,
                           "y_min": y_min, "y_max": y_max})
    return bounds


def check_street_collision(car, road_bounds):
    """
    Checks if a car is outside all padded road bounds.
    Returns True if off-road.
    """
    x, y = car.position
    for road in road_bounds:
        if road["x_min"] <= x <= road["x_max"] and road["y_min"] <= y <= road["y_max"]:
            return False  # still on some road
    print(f"Car {car.id} went off the street! at ({x:.2f},{y:.2f})")
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
