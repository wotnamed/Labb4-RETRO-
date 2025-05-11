
from math import sin, cos, radians, degrees, atan, sqrt, pi
import pygame
import projectile
import asteroid
import saucer


class Player:
    def __init__(self, x, y, movement="arcade"):
        self.movement_type = movement
        self.lives = 3
        self.facing_angle_rad = 0
        self.mass = 0.2
        self.traveling_angle_rad = 0
        self.thrust_force = 100
        self.velocity = 0
        self.p_x = x
        self.p_y = y
        self.steering_modifier = 5
        self.rotational_energy = 0
        self.rotational_velocity = 0
        self.sprite = pygame.image.load("textures/ship_red_90.png").convert_alpha()
        self.prev_x_v = 0
        self.prev_y_v = 0
        self.prev_tick_shot = True
        self.mask = None
        self.mask_width = None
        self.mask_height = None
        self.invincible = False
        self.invincibility_duration = 0
        self.powerup_1 = False
        self.powerup_2 = False
        self.powerup_3 = 0
        #  consider adding ammunition capacity

    def handle_collision(self, colliding_object):
        if self.invincible == False:
            if isinstance(colliding_object, projectile.Projectile):
                    if colliding_object.friendly:
                        pass
                    else:
                        return "death"
            if isinstance(colliding_object, asteroid.Asteroid):
                return "death"
            if isinstance(colliding_object, saucer.Saucer):
                return "death"
            else:
                pass

    def tick(self, dt):
        if self.invincible:
            self.invincibility_duration -= dt
            if self.invincibility_duration <= 0:
                self.invincible = False

    def steer(self, input, dt):  # This shit works so don't touch it please.
        if self.movement_type == "physics":
            self.rotational_energy = self.rotational_energy + input * dt
            self.rotational_velocity = self.rotational_energy*2/self.mass
            self.facing_angle_rad = self.facing_angle_rad + self.rotational_velocity * dt
            #  keep facing angle within 0 and 2 pi for consistency
            if self.facing_angle_rad > 2*pi:
                self.facing_angle_rad -= 2*pi
            if self.facing_angle_rad < 0:
                self.facing_angle_rad = 2*pi + self.facing_angle_rad
        elif self.movement_type == "arcade":
            self.rotational_velocity = input * self.steering_modifier
            self.facing_angle_rad = self.facing_angle_rad + self.rotational_velocity * dt
            #  keep facing angle within 0 and 2 pi for consistency
            if self.facing_angle_rad > 2 * pi:
                self.facing_angle_rad -= 2 * pi
            if self.facing_angle_rad < 0:
                self.facing_angle_rad = 2 * pi + self.facing_angle_rad

    def calculate_delta_velocity(self, input, dt):
        return self.thrust_force/self.mass * input * dt

    def calculate_x_component(self, angle, velocity):
        return cos(angle)*velocity

    def calcuate_y_component(self, angle, velocity):
        return sin(angle)*velocity

    def flip(self, number):
        return -number

    def calculate_angle(self, x, y):
        if x != 0:
            return atan(y/x)
        elif x == 0 and y > 0:
            return pi/2
        elif x == 0 and y < 0:
            return 3*pi/2

    def calculate_velocity(self, x, y):
        return sqrt(x**2 + y**2)

    def vector_and_position_update(self, input, dt):
        dv = self.calculate_delta_velocity(input, dt)
        dx = self.prev_x_v + self.calculate_x_component(self.facing_angle_rad, dv)*dt
        dy = self.prev_y_v + self.calcuate_y_component(self.facing_angle_rad, dv)*dt
        self.velocity = self.calculate_velocity(dx, dy)
        self.prev_x_v = dx
        self.prev_y_v = dy
        self.p_x += dx
        self.p_y -= dy
        self.traveling_angle_rad = self.calculate_angle(dx, self.flip(dy))

    def set_invincible(self, duration):
        self.invincible = True
        self.invincibility_duration = duration

    def reset(self, window_size=800, invincibility_duration=None):
        self.facing_angle_rad = 0
        self.traveling_angle_rad = 0
        self.velocity = 0
        self.rotational_velocity = 0
        self.rotational_energy = 0
        self.p_x = window_size/2
        self.p_y = window_size/2
        self.prev_y_v = 0
        self.prev_x_v = 0
        if invincibility_duration:
            self.set_invincible(invincibility_duration)

    def calculate_new_vector(self, axis, dt):
        if str(axis) == "x":
            return self.thrust_force / self.mass * dt * cos(self.facing_angle_rad)
        if str(axis) == "y":
            return self.thrust_force / self.mass * dt * sin(self.facing_angle_rad)
        else:
            print('no axis selected!')

    def calculate_position(self, vector_x, vector_y, dt):
        self.p_x = self.p_x + vector_x * dt
        self.p_y = self.p_y + vector_y * dt


