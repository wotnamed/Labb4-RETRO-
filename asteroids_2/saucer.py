from math import sin, cos, radians, degrees, atan, sqrt, pi
import pygame
import projectile
import asteroid
import player
import random


class Saucer:
    def __init__(self, x, y, enemy, tick_per_fire):
        self.facing_angle_rad = 0
        self.mass = 1
        self.traveling_angle_rad = 0
        self.thrust_force = 100
        self.velocity = 0
        self.p_x = x
        self.p_y = y
        self.steering_modifier = 1
        self.rotational_energy = 0
        self.rotational_velocity = 0
        self.sprite = pygame.image.load("textures/sauces_90.png").convert_alpha()
        self.prev_x_v = 0
        self.prev_y_v = 0
        self.prev_tick_shot = False
        self.mask = None
        self.mask_width = None
        self.mask_height = None
        self.target = enemy
        self.shot_chance = tick_per_fire

    def calculate_angle(self, x, y):
        if x != 0:
            return atan(y/x)
        elif x == 0 and y > 0:
            return pi/2
        elif x == 0 and y < 0:
            return 3*pi/2

    def update(self, dt):
        self.aim_at_target()
        if self.dice_roll(dt=dt, share=self.shot_chance):
            return "fire"
        if dt < 5:
            self.movement(0.1, dt)

    def dice_roll(self, dt, share=1000):
        roll = random.randint(1, int(share))
        if roll == share:
            return True
        else:
            return False

    def calculate_velocity(self, x, y):
        return sqrt(x**2 + y**2)

    def calculate_delta_velocity(self, input, dt):
        return self.thrust_force/self.mass * input * dt

    def calculate_x_component(self, angle, velocity):
        return cos(angle)*velocity

    def calcuate_y_component(self, angle, velocity):
        return sin(angle)*velocity

    def flip(self, number):
        return -number

    def movement(self, input, dt):
        dv = self.calculate_delta_velocity(input, dt)
        dx = self.prev_x_v + self.calculate_x_component(self.facing_angle_rad, dv) * dt
        dy = self.prev_y_v + self.calcuate_y_component(self.facing_angle_rad, dv) * dt
        self.velocity = self.calculate_velocity(dx, dy)
        self.prev_x_v = dx
        self.prev_y_v = dy
        self.p_x += dx
        self.p_y -= dy
        self.traveling_angle_rad = self.calculate_angle(dx, self.flip(dy))


    def aim_at_target(self):
        # set facing_angle_rad to point at target
        target_x = self.target.p_x
        target_y = self.target.p_y
        dx = target_x-self.p_x
        dy = target_y-self.p_y
        if dx > 0:
            self.facing_angle_rad = self.calculate_angle(dx, -dy)
        else:
            self.facing_angle_rad = self.calculate_angle(dx, -dy) + pi


    def handle_collision(self, colliding_object):
        if isinstance(colliding_object, projectile.Projectile):
            if not colliding_object.friendly:
                pass
            else:
                return "death"
        if isinstance(colliding_object, asteroid.Asteroid):
            return "death"
        if isinstance(colliding_object, player.Player):
            return "death"
        else:
            pass
