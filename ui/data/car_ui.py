import math


class CarUI:
    def __init__(self, id, x, y, vx, vy):
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def get_direction(self):
        return math.degrees(math.atan2(-self.vy, self.vx)) - 90
