from math import sin, cos, atan, sqrt, pi
import pygame
import player
import asteroid

class Projectile:
    def __init__(self, owner, x=None, y=None, velocity=300, angle=None, duration=2, size=1):
        self.size = size
        if velocity is not None:
            self.velocity = owner.velocity*29.82 + velocity
        else:
            self.velocity = owner.velocity*29.82 + 200
        if x is not None and y is not None:
            self.p_x = x
            self.p_y = y
        else:
            self.p_x = owner.p_x
            self.p_y = owner.p_y
        if angle is not None:
            self.facing_angle_rad = angle
        else:
            self.facing_angle_rad = owner.facing_angle_rad
        self.owner = owner

        if self.size == 1:
            self.sprite = pygame.image.load("textures/projectile_90.png").convert_alpha()
        elif self.size == 2:
            self.sprite = pygame.image.load("textures/projectile_large.png")
        self.traveling_angle_rad = 0
        self.mask = None
        self.mask_width = None
        self.mask_height = None
        self.owner_traveling_angle_rad = owner.traveling_angle_rad
        self.owner_velocity = owner.velocity
        self.owner_vector = (self.owner.prev_x_v, self.owner.prev_y_v)
        self.additional_velocity = velocity
        if isinstance(owner, player.Player):
            self.friendly = True
        else:
            self.friendly = False
        self.duration = duration

    def position_update(self, dt):
        self.p_x += cos(self.facing_angle_rad) * self.velocity * dt
        self.p_y -= sin(self.facing_angle_rad) * self.velocity * dt

    def calculate_angle(self, x, y):
        if x != 0:
            if x > 0:
                return atan(y/x)
            if x < 0:
                return atan(y/x) + pi
        elif x == 0 and y > 0:
            return pi/2
        elif x == 0 and y < 0:
            return 3*pi/2

    def new_position_update(self, dt):
        #  add initial velocity at facing angle as well as ship traveling vector
        if self.owner_traveling_angle_rad == None or 0:
            sub1 = self.owner_velocity * 29.82
            sub2 = 0
        else:
            sub1 = cos(self.owner_traveling_angle_rad) * self.owner_velocity * 29.82
            sub2 = sin(self.owner_traveling_angle_rad) * self.owner_velocity * 29.82
        sub3 = cos(self.facing_angle_rad) * self.additional_velocity
        sub4 = sin(self.facing_angle_rad) * self.additional_velocity
        vector_x = (sub3 + self.owner_vector[0]/dt) #+sub1
        vector_y = -(sub4 + self.owner_vector[1]/dt) #  +sub2
        self.velocity = sqrt(vector_x**2 + vector_y**2)
        self.traveling_angle_rad = self.calculate_angle(vector_x, -vector_y)
        self.p_x += cos(self.traveling_angle_rad) * self.velocity * dt
        self.p_y -= sin(self.traveling_angle_rad) * self.velocity * dt

    def handle_collision(self, colliding_object):
        if isinstance(colliding_object, asteroid.Asteroid):
            return "hit"
        elif isinstance(colliding_object, player.Player):
            if self.friendly is True:
                pass
            else:
                return "hit"
        else:
            pass

    def duration_update(self, dt):
        self.duration -= dt
        if self.duration <= 0:
            return False
        else:
            return True

