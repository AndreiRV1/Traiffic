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
