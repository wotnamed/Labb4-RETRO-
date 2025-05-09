import random
from math import sin, cos, atan, sqrt, pi
import pygame

class Asteroid:
    def __init__(self, mother=None, size=None, traveling_angle_rad=None, velocity=None, rotational_velocity=None, x=None, y=None):
        if mother is not None:
            if mother.size == 3:
                self.size = 2
                self.sprite = pygame.image.load("textures/asteroid_medium.png").convert_alpha()
            elif mother.size == 2:
                self.size = 1
                self.sprite = pygame.image.load("textures/asteroid_small.png").convert_alpha()
            elif mother.size == 1:
                print("Daughter asteroid can't be created from size 1 asteroid!")
            else:
                print("Mother size unrecognized.")
            self.facing_angle_rad = random.randint(0, 6)
            self.traveling_angle_rad = random.randint(-1,1)*mother.traveling_angle_rad
            self.velocity = mother.velocity * 2
            self.rotational_velocity = random.randint(-2, 2)*mother.rotational_velocity
            self.p_x = mother.p_x
            self.p_y = mother.p_y
        elif mother is None:
            self.size = size
            if self.size == 3:
                self.sprite = pygame.image.load("textures/asteroid_large.png").convert_alpha()
            elif self.size == 2:
                self.sprite = pygame.image.load("textures/asteroid_medium.png").convert_alpha()
            elif self.size == 1:
                self.sprite = pygame.image.load("textures/asteroid_small.png").convert_alpha()
            else:
                print("Asteroid size unrecognized.")
            self.facing_angle_rad = random.randint(0, 6)
            if traveling_angle_rad:
                self.traveling_angle_rad = traveling_angle_rad
            else:
                self.traveling_angle_rad = random.randint(0, 7)
            if velocity:
                self.velocity = velocity
            else:
                self.velocity = random.randint(10,20)
            if rotational_velocity:
                self.rotational_velocity = rotational_velocity
            else:
                self.rotational_velocity = random.randint(-2, 2)
            self.p_x = x
            self.p_y = y
        self.mask = None
    def position_update(self, dt):
        self.p_x += cos(self.traveling_angle_rad) * self.velocity * dt
        self.p_y -= sin(self.traveling_angle_rad) * self.velocity * dt
        self.facing_angle_rad += self.rotational_velocity * dt
        if self.facing_angle_rad > 2*pi:
            self.facing_angle_rad -= 2*pi
        if self.facing_angle_rad < 0:
            self.facing_angle_rad = 2*pi + self.facing_angle_rad

    def handle_collision(self, colliding_object):
        if not isinstance(colliding_object, Asteroid):
            if self.size <= 1:
                return "death"
            else:
                return "split"
        else:
            pass

