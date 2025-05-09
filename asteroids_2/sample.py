import pygame
import player
import projectile
import asteroid
import saucer
from math import sqrt
from numpy import degrees
import random


class Main:
    def __init__(self):
        self.dt = 0
        self.window_size = 800
        self.exit = False
        self.ship = None
        self.font_1 = None
        self.font_2 = None
        self.object_list = []
        self.level = 0  # default should be 1
        self.score = 0
        self.scene = 0
        self.sfx_1 = None
        self.sfx_2 = None
        self.sfx_3 = None
        self.sfx_4 = None
        self.sfx_5 = None

    # Will initialise the beginning of the game, create all essential objects etc.
    def random_spawn_saucer(self, count):
        z = 0
        while z < count:
            x = random.randint(0, self.window_size)
            y = random.randint(0, self.window_size)
            if x <= (self.window_size / 2 - 200) or x >= (self.window_size / 2 + 200) and y <= (
                    self.window_size / 2 - 200) or y >= (self.window_size / 2 + 200):
                self.object_list.append(saucer.Saucer(x=x, y=y, enemy=self.ship, tick_per_fire=100-count))
                z += 1
            else:
                pass

    def random_spawn_asteroid(self, count):
        z = 0
        while z < count:
            #  check that asteroid position has a distance more than 200 from middle point
            #  if sqrt(x**2 + y**2) + 1000 > sqrt(2*self.window_size**2)
            x = random.randint(0, self.window_size)
            y = random.randint(0, self.window_size)
            if x <= (self.window_size/2 - 200) or x >= (self.window_size/2 + 200) and y <= (self.window_size/2 - 200) or y >= (self.window_size/2 + 200):
            #  if sqrt(x ** 2 + y ** 2) + 1000 > sqrt(2 * self.window_size ** 2):
                self.object_list.append(asteroid.Asteroid(mother=None, size=3, x=x, y=y))
                z += 1
            else:
                pass

    # define safe distance
    # random x and y
    # check delta x and delta y from asteroid to player
    # if delta x^2 + delta y^2 > safe distance

    def level_init(self, level):
        for i in self.object_list:
            if isinstance(i, projectile.Projectile):
                try:
                    index = self.object_list.index(i)
                    del self.object_list[index]
                except ValueError:
                    print("projectile not in object list! (level_init)")
        self.ship.reset(self.window_size, 3)
        self.sfx_4.play()
        if level <= 10:
            self.random_spawn_asteroid(level + 3)
        if level > 10:
            self.random_spawn_saucer(level-10)

    def setup(self):
        self.object_list = []
        self.level = 0
        self.score = 0
        self.sfx_1 = pygame.mixer.Sound('sfx/laserShoot.wav')
        self.sfx_2 = pygame.mixer.Sound('sfx/asteroidExplosion.wav')
        self.sfx_3 = pygame.mixer.Sound('sfx/playerExplosion.wav')
        self.sfx_4 = pygame.mixer.Sound('sfx/newLevel.wav')
        self.sfx_5 = pygame.mixer.Sound('sfx/saucerShoot.wav')
        self.ship = player.Player(self.window_size/2,self.window_size/2)
        self.font_1 = pygame.font.SysFont('Comic Sans MS', 10)
        self.font_2 = pygame.font.Font('freesansbold.ttf', 16)
        self.object_list.append(self.ship)
        self.level_init(self.level)

    def main(self):
        clock = pygame.time.Clock()
        pygame.init()
        pygame.mixer.init()
        # CREATE A CANVAS
        canvas = pygame.display.set_mode((self.window_size, self.window_size))
        # TITLE OF CANVAS
        pygame.display.set_caption("baka!")
        # SETUP GAME OBJECTS
        self.setup()
        # GAME LOOP
        while not self.exit:
            pygame.display.update()
            self.dt = clock.tick(70) / 1000
            self.draw(canvas)
            self.handle_events(canvas)


    def pause_screen(self, canvas):
        canvas.fill((0,0,0))
        canvas.blit(self.font_2.render("This is the pause screen.", True, (255, 255, 255)), (250, 350))
        canvas.blit(self.font_2.render("Press '1' or 'SPACE' to switch back to gameplay.", True, (255, 255, 255)), (250, 365))

    def death_screen(self, canvas, keys):
        canvas.fill((0,0,0))
        canvas.blit(self.font_2.render("Death.", True, (255, 255, 255)), (250, 350))
        buffer = "Score: " + str(self.score)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)),(250, 365))
        canvas.blit(self.font_2.render("To restart, press 'x'.", True, (185, 255, 255)),(250, 380))
        if keys[pygame.K_x]:
            self.setup()
            self.scene = 0

    def start_screen(self, canvas, keys):
        canvas.fill((0, 0, 0))
        canvas.blit(self.font_2.render("Welcome, dear pilot.", True, (255, 255, 255)), (250, 350))
        canvas.blit(self.font_2.render("You have two types of ship available.", True, (255, 255, 255)), (250, 365))
        canvas.blit(self.font_2.render("The first one has a fixed steering speed.", True, (255, 255, 255)), (250, 380))
        canvas.blit(self.font_2.render("The second one has an unlocked", True, (255, 255, 255)), (250, 395))
        canvas.blit(self.font_2.render("steering computer, with a higher difficulty to boot.", True, (255, 255, 255)), (250, 410))
        canvas.blit(self.font_2.render("To change ship type, press c for 1 and v for 2.", True, (255, 255, 255)), (250, 425))
        canvas.blit(self.font_2.render("Press 'SPACE' to depart.", True, (255, 255, 255)), (250, 440))
        canvas.blit(self.font_2.render("Good luck.", True, (255, 255, 255)), (250, 455))

        if keys[pygame.K_c]:
            self.ship.movement_type = "arcade"
        elif keys[pygame.K_v]:
            self.ship.movement_type = "physics"

        if self.ship.movement_type == "arcade":
            canvas.blit(self.font_2.render("Type 1 currently selected.", True, (255, 185, 255)), (250, 500))
        elif self.ship.movement_type == "physics":
            canvas.blit(self.font_2.render("Type 2 currently selected.", True, (255, 255, 185)), (250, 500))

    def game_screen(self, keys):
        saucer_count = 0
        asteroid_count = 0
        self.react_to_user_input(keys)
        self.ship.tick(self.dt)
        if self.ship.invincible:
            print("ship is invincible!")
        for i in self.object_list:
            self.border_checking(i, self.window_size)
            if isinstance(i, projectile.Projectile):
                i.new_position_update(self.dt)
                if not i.duration_update(self.dt):
                    index = self.object_list.index(i)
                    del self.object_list[index]
            if isinstance(i, asteroid.Asteroid):
                i.position_update(self.dt)
                asteroid_count += 1
            if isinstance(i, saucer.Saucer):
                forward = i.update(self.dt)
                if forward == "fire":
                    self.object_list.append(projectile.Projectile(i, velocity=300, duration=2))
                    self.sfx_5.play()
                saucer_count += 1

        if asteroid_count == 0 and saucer_count == 0:
            self.level += 1
            self.level_init(self.level)

        self.collision_checking()

    def scene_switcher(self, keys):
        #  scene 0: start screen
        #  scene 1: gameplay
        #  scene 2: pause screen
        #  scene 3: death screen
        if self.scene == 0:
            if keys[pygame.K_SPACE]:
                self.scene = 1
        else:
            if self.ship.lives < 0:
                self.scene = 3
            elif keys[pygame.K_ESCAPE] or keys[pygame.K_2]:
                self.scene = 2
            elif keys[pygame.K_SPACE] or keys[pygame.K_1]:
                self.scene = 1

    def border_checking(self, entity, window_size):
        if entity.p_x > window_size:
            entity.p_x -= window_size
        elif entity.p_x < 0:
            entity.p_x += window_size
        if entity.p_y > window_size:
            entity.p_y -= window_size
        elif entity.p_y < 0:
            entity.p_y += window_size

    def collision_checking(self):
        #  I use masks for collision detection. This essentially means that we need to do a pseudo-render here.
        for i in self.object_list:
            image = pygame.transform.rotate(i.sprite, degrees(i.facing_angle_rad))
            i.mask = pygame.mask.from_surface(image)
            mask_image_1 = i.mask.to_surface()
            i_mask_width = int(mask_image_1.get_width())
            i_mask_height = int(mask_image_1.get_height())
            for e in self.object_list:
                image = pygame.transform.rotate(e.sprite, degrees(e.facing_angle_rad))
                e.mask = pygame.mask.from_surface(image)
                mask_image_2 = e.mask.to_surface()
                e_mask_width = int(mask_image_2.get_width())
                e_mask_height = int(mask_image_2.get_height())
                if e.mask is not None and i.mask is not None:
                    if i.mask.overlap(e.mask, ((e.p_x - e_mask_width/2) - (i.p_x - i_mask_width/2), (e.p_y - e_mask_height/2) - (i.p_y - i_mask_height/2))):
                        if e == i:
                            pass
                        else:
                            tat = i.handle_collision(e)
                            try:
                                main.collision_handler(tat, i)
                            except ValueError:
                                pass

    def collision_handler(self, result, i):
        if isinstance(i, player.Player):
            match result:
                case "death":
                    self.sfx_3.play()
                    self.ship.lives -= 1
                    self.ship.reset(self.window_size, 3)
                    if self.ship.lives < 1:
                        print("ship is dead.")  # trigger game over
                        #  Trigger ship invincibility for 3 seconds and reset ship position (reset())
                case "powerup":  # trigger powerup in player
                    pass
        if isinstance(i, projectile.Projectile):
            match result:
                case "hit":
                    try:
                        index = self.object_list.index(i)
                        del self.object_list[index]
                    except ValueError:
                        print("projectile not in object list! (collision_handler)")
                    # de-spawn projectile and play sfx (maybe not play sfx since sfx should be played by the object hit?)
        if isinstance(i, asteroid.Asteroid):
            if result == "death":
                index = self.object_list.index(i)
                del self.object_list[index]
                self.score += 10
                self.sfx_2.play()
                # Delete asteroid (i) and maybe trigger explosion animation?
            elif result == "split":
                for f in range(2):
                    self.object_list.append(asteroid.Asteroid(i))
                index = self.object_list.index(i)
                del self.object_list[index]
                self.score += 10
                self.sfx_2.play()
        if isinstance(i, saucer.Saucer):
            if result == "death":
                index = self.object_list.index(i)
                del self.object_list[index]
                self.score += 150
                self.sfx_2.play()
                # spawn in two asteroids with i as mother and delete original asteroid.

    # Runs every frame. What will happen each frame
    def handle_events(self, canvas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

        keys = pygame.key.get_pressed()
        self.scene_switcher(keys)
        if self.scene == 3:
            self.death_screen(canvas, keys)
        if self.scene == 2:
            self.pause_screen(canvas)
        if self.scene == 1:
            self.game_screen(keys)
        if self.scene == 0:
            self.start_screen(canvas, keys)
    
    def ship_powerup_gui(self, canvas):
        if self.ship.invincible:
            text = f"Invincible! ({self.ship.invincibility_duration:.1f})"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 300))
    def game_screen_gui(self, canvas):
        self.ship_powerup_gui(canvas)
        canvas.blit(self.font_1.render("meme", False, (255, 255, 255)), (20, 20))
        buffer = "coordinates = (" + str(self.ship.p_x) + ", " + str(self.ship.p_y) + ")"
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 30))
        buffer = "facing_angle_rad = " + str(self.ship.facing_angle_rad)
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 40))
        buffer = "traveling_angle_rad = " + str(self.ship.traveling_angle_rad)
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 50))
        buffer = "rotational_energy = " + str(self.ship.rotational_energy)
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 60))
        buffer = "rotational_velocity = " + str(self.ship.rotational_velocity)
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 70))
        buffer = "previous_vector = (" + str(self.ship.prev_x_v) + ", " + str(self.ship.prev_y_v) + ")"
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 80))
        buffer = "velocity = " + str(self.ship.velocity)
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (20, 90))
        buffer = "score: " + str(self.score)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (40, 110))
        buffer = "level: " + str(self.level)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (40, 130))
        buffer = "lives: " + str(self.ship.lives)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (40, 150))
        buffer = "dt: " + str(self.dt)
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (725, 10))
        buffer = "fps: " + str(1 / self.dt) if self.dt > 0 else "undefined"
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (725, 20))
        buffer = "entities: " + str(len(self.object_list))
        canvas.blit(self.font_1.render(buffer, False, (255, 255, 255)), (725, 30))

    def draw(self, canvas):
        canvas.fill((0, 0, 0))
        self.game_screen_gui(canvas)
        for i in self.object_list:
            image = pygame.transform.rotate(i.sprite, degrees(i.facing_angle_rad))
            #  we need to copy the original sprite and not alter it, as rotating a sprite changes its sprite
            canvas.blit(image, (i.p_x - int(image.get_width() / 2), i.p_y - int(image.get_height() / 2)))
            #  here we center where we render the image on its center, to avoid artifacts when rotating images.




    def react_to_user_input(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            engine = 1
        #  elif keysPressed[pygame.K_DOWN] or keysPressed[pygame.K_s]:
        #      engine = -1
        else:
            engine = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steer = 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steer = -1
        elif not keys[pygame.K_LEFT] or not keys[pygame.K_a] or not keys[pygame.K_RIGHT] or not keys[pygame.K_d]:
            steer = 0
        else:
            steer = 0

        if keys[pygame.K_SPACE] and self.ship.prev_tick_shot is False:
            self.object_list.append(projectile.Projectile(self.ship, duration=2))
            self.sfx_1.play()
            self.ship.prev_tick_shot = True
        elif not keys[pygame.K_SPACE]:
            self.ship.prev_tick_shot = False

        self.ship.steer(steer, self.dt)
        self.ship.vector_and_position_update(engine, self.dt)
        if keys[pygame.K_q]:
            self.ship.reset(self.window_size)


main = Main()
main.main()