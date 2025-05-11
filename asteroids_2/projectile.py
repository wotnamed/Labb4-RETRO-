from math import sin, cos, atan, sqrt, pi
import pygame
import player
import asteroid


class Projectile:
    """
    The class used to represent projectiles within the game.

    Attributes
    ----------
    size : int
        Indicates the size of the projectile (1 or 2), which in turn determines the sprite of the instance.
    velocity : float
        Indicates the speed of the projectile which is used when updating its position.
    p_x : float
        Determines the projectile's x position within the game world.
    p_y : float
        Determines the projectile's y position within the game world.
    facing_angle_rad : float
        Determines which direction the projectile's sprite is pointing.
    owner : object
        Determines what object summoned the projectile.
    sprite : pygame surface
        The image representing the projectile.
    traveling_angle_rad : float
        The angle the projectile is traveling in.
    mask : pygame mask
        The object's mask.
    mask_width : float
        The object's mask's width.
    mask_height : float
        The object's mask's height.
    owner_traveling_angle_rad : float
        The angle the object that summoned the projectile was traveling in at the time of its summon.
    owner_velocity
        The velocity the owner was traveling at (old code?).
    owner_vector : Tuple of floats
        Describes the previous vector of the projectile owner.
    additional_velocity : float
        Value that describes the velocity of the projectile relative to its origin.
    friendly : bool
        Boolean which indicates if the projectile is friendly to the player or not.
    duration : float
        Value that describes the projectile's remaining time in this world.

    Methods
    -------
    position_update(dt: float) -> None
        updates the projectile's position.
    calculate_angle(x: float, y: float) -> float
        calculates an angle based on a vector specified in x and y
    new_position_update(dt: float) -> None
        Updates the projectile's position based on its additional vector, as well as the origin vector from the owner.
    handle_collision(colliding_object: object) -> str
        Returns a reaction by the projectile when said projectile has been fed a collision.
    duration_update(dt: float) -> bool
        Subtracts dt from 'duration', and if duration <= 0 returns False.
    """

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
        """
        Updates the position of the projectile based on its angle and velocity, as well as the amount time passed (dt).
        Parameters
        ----------
        dt : float
            Delta time to update position in relation to

        Returns
        -------
        None

        Raises
        None
        """
        self.p_x += cos(self.facing_angle_rad) * self.velocity * dt
        self.p_y -= sin(self.facing_angle_rad) * self.velocity * dt

    def calculate_angle(self, x, y):
        """
        Calculates and returns an angle based on an input vector specified in x and y floats.

        Parameters
        ----------
        x : float
            An x value within a coordinate system
        y : float
            A y value within a coordinate system

        Returns
        -------
        float
            an angle specified in radians

        Raises
        ------
        None
        """
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
        """
        A new and refined method to update a projectile's position which accurately accounts for the summoner's vector.

        Parameters
        ----------
        dt : float
            The delta time since last tick.

        Returns
        -------
        None

        Raises
        ------
        None
        """
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
        """
        A method that handles collisions for the projectile based on the provided colliding_object.

        Parameters
        ----------
        colliding_object : object
            An object (preferably derived from one of the game's classes) to be reacted upon.

        Returns
        -------
        str
            The outcome of the collision to be fed to the collision handler in the game.

        Raises
        ------
        None
        """
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
        """
            Updates the remaining duration of the projectile.
            Parameters
            ----------
            dt : float
                The time passed during the game tick, and the value to be subtracted from duration.

            Returns
            -------
            bool
                False equates to that there is no remaining duration for the projectile.

            Raises
            ------
            None
            """
        self.duration -= dt
        if self.duration <= 0:
            return False
        else:
            return True

