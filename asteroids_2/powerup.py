import asteroid
import player
import projectile
import saucer
import pygame
from math import pi
class Powerup:
    def __init__(self, x, y, type=1, duration=5):
        self.type = type
        if self.type == 1:
            self.sprite = pygame.image.load("textures/power-up-1.png").convert_alpha()
        elif self.type == 2:
            self.sprite = pygame.image.load("textures/power-up-2.png").convert_alpha()
        elif self.type == 3:
            self.sprite = pygame.image.load("textures/power-up-3.png").convert_alpha()
        else:
            print("powerup type not recognised!")
        self.duration = duration
        self.p_x = x
        self.p_y = y
        self.mask = None
        self.mask_width = None
        self.mask_height = None
        self.facing_angle_rad = 0


    def duration_update(self, dt):
        self.duration -= dt
        if self.duration <= 0:
            return False
        else:
            return True

    def handle_collision(self, colliding_object):
        if isinstance(colliding_object, asteroid.Asteroid):
            pass
        elif isinstance(colliding_object, player.Player):
            return "hit"
        elif isinstance(colliding_object, saucer.Saucer):
                pass
        elif isinstance(colliding_object, projectile.Projectile):
            if colliding_object.friendly:
                return "hit"
        else:
            pass
