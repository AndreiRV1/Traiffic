from core import settings
import pygame


class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_roads(self, screen, nodes, connections):
        road_color = (100, 100, 100)
        width = 8

        for conn in connections:
            node_a = nodes[conn.a]
            node_b = nodes[conn.b]
            posxa = node_a.x * settings.SCREEN_WIDTH
            posya = node_a.y * settings.SCREEN_HEIGHT
            posxb = node_b.x * settings.SCREEN_WIDTH
            posyb = node_b.y * settings.SCREEN_HEIGHT
            pygame.draw.line(screen, road_color, (posxa, posya), (posxb, posyb), width)

    def draw_car(self, car, image):
        angle = car.facing_angle()
        rotated_car = pygame.transform.rotate(image, angle + 90)

        posx = car.x * settings.SCREEN_WIDTH
        posy = car.y * settings.SCREEN_HEIGHT
        rect = rotated_car.get_rect(center=(posx, posy))
        self.screen.blit(rotated_car, rect.topleft)

    def draw_world(self, state):
        self.screen.fill((0, 0, 0))
