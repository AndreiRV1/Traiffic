from backend.graph import Graph
import numpy as np
import random

class Car:
    id_crt = 0
    def __init__(self, position,facing):
        self.id = self.id_crt
        self.id_crt +=1
        self.speed = 0
        self.friction = 0.00005

        self.accelerate_step = 0.0005
        self.max_speed = 0.1
        self.steer_step = 0.1

        self.position = np.array(position)
        self.facing = np.array(facing)

    def move(self,accelerate: int, steer:bool, dt):
        if accelerate not in [-1,0,1]:
            accelerate = 0
        if steer not in [-1,0,1]:
            steer = 0
        acceleration = accelerate * self.accelerate_step
        self.speed += acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed

        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        if self.speed > 0:
            self.speed -= self.friction

        if self.speed < 0:
            self.speed += self.friction

        angle_to_steer = 0
        if self.speed > 0:
            angle_to_steer = self.steer_step * steer
        rotation_matrix = np.array([
        [np.cos(angle_to_steer), -np.sin(angle_to_steer)],
        [np.sin(angle_to_steer),  np.cos(angle_to_steer)]
        ])
        self.facing = rotation_matrix @ self.facing
        self.position = self.position + (self.facing * self.speed)


# Function will update current instance of car, returning 0  when car reached destination and 1 else
    def update(self, dt : float):
        return 1