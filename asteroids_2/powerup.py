import asteroid
import player
import projectile
import saucer
import pygame


class Powerup:
    """
    Class which handles the Powerup game object. The Powerup is used to grant the player various upgrades, as well as extra lives.

    Attributes
    ----------
    type : int
        The type of powerup.
    sprite : pygame surface
        The image representing the powerup.
    duration : float
        A variable used to indicate the time remaining until the powerup de-spawns.
    p_x : int
        The x position of the object within the game world.
    p_y : int
        The y position of the object within the game world.
    mask : pygame mask
        The object's "mask" derived from its surface. Is used for collision checking.
    mask_width : float
        Variable used for collision detection.
    mask_height : float
        Variable used for collision detection.
    facing_angle_rad
        Variable used to describe the object's rotation. (Required for rendering object)

    Methods
    -------
    duration_update(dt: float) -> bool
        Subtracts the powerups duration with the time passed during the tick. Returns False if duration <= 0.
    handle_collision(colliding_object : object) -> str
        Checks what object has been collided with and acts accordingly.
    """
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
        """
        Updates the remaining duration of the powerup.
        Parameters
        ----------
        dt : float
            The time passed during the game tick, and the value to be subtracted from duration.

        Returns
        -------
        bool

        Raises
        ------
        None
        """
        self.duration -= dt
        if self.duration <= 0:
            return False
        else:
            return True

    def handle_collision(self, colliding_object):
        """
        Handles collisions for the powerup, and how the powerup reacts to said collisions.
        Parameters
        ----------
        colliding_object : object
            The object which the reaction of the powerup will be based on.

        Returns
        -------
        str

        Raises
        ------
        None
        """
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
