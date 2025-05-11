import pygame
import player
import projectile
import asteroid
import saucer
import powerup
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
        self.font_3 = None
        self.object_list = []
        self.level = 0  # default should be 1
        self.score = 0
        self.scene = 0
        self.sfx_1 = None
        self.sfx_2 = None
        self.sfx_3 = None
        self.sfx_4 = None
        self.sfx_5 = None
        self.sfx_6 = None
        self.game_time = 0

    # Will initialise the beginning of the game, create all essential objects etc.
    def random_spawn_saucer(self, count, safe_distance=10000):
        z = 0
        while z < count:
            x = random.randint(0, self.window_size)
            y = random.randint(0, self.window_size)
            if ((x - self.window_size / 2) * (x - self.window_size / 2) + (y - self.window_size / 2) * (
                    y - self.window_size / 2)) > safe_distance:
                self.object_list.append(saucer.Saucer(x=x, y=y, enemy=self.ship, tick_per_fire=100-count))
                z += 1
            else:
                pass

    def random_spawn_asteroid(self, count, safe_distance=10000):
        z = 0
        while z < count:
            #  check that asteroid position has a distance more than 200 from middle point
            #  if sqrt(x**2 + y**2) + 1000 > sqrt(2*self.window_size**2)
            x = random.randint(0, self.window_size)
            y = random.randint(0, self.window_size)
            if ((x - self.window_size / 2) * (x - self.window_size / 2) + (y - self.window_size / 2) * (y - self.window_size / 2)) > safe_distance:
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
        self.object_list = []
        self.object_list.append(self.ship)
        print(self.object_list)
        for i in self.object_list:
            if not isinstance(i, player.Player):
                try:
                    index = self.object_list.index(i)
                    del self.object_list[index]
                except ValueError:
                    print("projectile not in object list! (level_init)")
        print(self.object_list)
        self.ship.reset(self.window_size, 3)
        self.sfx_4.play()
        if level <= 10:
            self.random_spawn_asteroid(level + 3)
        if level > 10:
            self.random_spawn_saucer(level-10)

    def setup(self):
        self.level = 11
        self.score = 0
        self.sfx_1 = pygame.mixer.Sound('sfx/laserShoot.wav')
        self.sfx_2 = pygame.mixer.Sound('sfx/asteroidExplosion.wav')
        self.sfx_3 = pygame.mixer.Sound('sfx/playerExplosion.wav')
        self.sfx_4 = pygame.mixer.Sound('sfx/newLevel.wav')
        self.sfx_5 = pygame.mixer.Sound('sfx/saucerShoot.wav')
        self.sfx_6 = pygame.mixer.Sound('sfx/powerupActivated.wav')
        self.ship = player.Player(self.window_size/2,self.window_size/2)
        self.font_1 = pygame.font.SysFont('Comic Sans MS', 10)
        self.font_2 = pygame.font.Font('freesansbold.ttf', 16)
        self.font_3 = pygame.font.Font('freesansbold.ttf', 12)
        self.level_init(self.level)

    def main(self):
        clock = pygame.time.Clock()
        pygame.init()
        pygame.mixer.init()
        # CREATE A CANVAS
        canvas = pygame.display.set_mode((self.window_size, self.window_size))
        # TITLE OF CANVAS
        pygame.display.set_caption("baka!")
        pygame.display.set_icon(pygame.image.load('textures/icon.png'))

        # SETUP GAME OBJECTS
        self.setup()
        # GAME LOOP
        while not self.exit:
            pygame.display.update()
            self.dt = clock.tick(70) / 1000
            self.draw(canvas)
            self.handle_events(canvas)
            self.game_time += self.dt

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
        self.random_powerup_spawn(average_ticks_per_spawn=1000, duration=10)
        self.react_to_user_input(keys)
        self.ship.tick(self.dt)
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
                outcome = i.update(self.dt)
                if outcome == "fire":
                    self.object_list.append(projectile.Projectile(i, velocity=300, duration=2, angle=i.facing_angle_rad+0.2*random.randint(-1, 1)))
                    self.sfx_5.play()
                saucer_count += 1
            if isinstance(i, powerup.Powerup):
                if not i.duration_update(self.dt):
                    index = self.object_list.index(i)
                    del self.object_list[index]

        if asteroid_count == 0 and saucer_count == 0:
            self.level += 1
            self.level_init(self.level)

        self.collision_checking(threshold=1000)

    def random_powerup_spawn(self, average_ticks_per_spawn, duration):
        if random.randint(1, average_ticks_per_spawn) == 1:
            self.object_list.append(powerup.Powerup(x=random.randint(1, self.window_size), y=random.randint(1, self.window_size), type=random.randint(1,3), duration=duration))
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

    def collision_checking(self, threshold):
        #  I use masks for collision detection. This essentially means that we need to do a pseudo-render here.
        for i in self.object_list:
            image = pygame.transform.rotate(i.sprite, degrees(i.facing_angle_rad))
            i.mask = pygame.mask.from_surface(image)
            mask_image_1 = i.mask.to_surface()
            i.mask_width = int(mask_image_1.get_width())
            i.mask_height = int(mask_image_1.get_height())
        for i in self.object_list:
            for e in self.object_list:
                if e.mask is not None and i.mask is not None and e != i and (i.p_x-e.p_x)**2+(i.p_y-e.p_y)<threshold:
                    if i.mask.overlap(e.mask, ((e.p_x - e.mask_width/2) - (i.p_x - i.mask_width/2), (e.p_y - e.mask_height/2) - (i.p_y - i.mask_height/2))):
                        outcome = i.handle_collision(e)
                        try:
                            main.collision_handler(outcome, i)
                        except ValueError:
                            pass

    def collision_handler(self, result, i):
        if isinstance(i, player.Player):
            match result:
                case "death":
                    self.sfx_3.play()
                    self.ship.lives -= 1
                    self.ship.reset(self.window_size, invincibility_duration=3)
                        #  Trigger ship invincibility for 3 seconds and reset ship position (reset())
        if isinstance(i, projectile.Projectile):
            match result:
                case "hit":
                    try:
                        index = self.object_list.index(i)
                        del self.object_list[index]
                    except ValueError:
                        print("projectile not in object list! (collision_handler)")
        if isinstance(i, asteroid.Asteroid):
            if result == "death":
                index = self.object_list.index(i)
                del self.object_list[index]
                self.score += 10
                self.sfx_2.play()
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
        if isinstance(i, powerup.Powerup):
            match result:
                case "hit":
                    if i.type == 1:
                        if self.ship.powerup_1:
                            self.score += 200
                        self.ship.powerup_1 = True
                    elif i.type == 2:
                        if self.ship.powerup_2:
                            self.score += 200
                        self.ship.powerup_2 = True
                    elif i.type == 3:
                        self.ship.powerup_3 += 1
                        self.ship.lives += 1
                    index = self.object_list.index(i)
                    del self.object_list[index]
                    self.sfx_6.play()


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
        if self.ship.powerup_1:
            text = "Big shot"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 315))
        if self.ship.powerup_2:
            text = "Front splitter"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 330))
        if self.ship.powerup_3 > 0:
            text = f"Extra life (x{self.ship.powerup_3})"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 345))

    def ship_stat_gui(self, canvas):
        buffer = "coordinates = (" + str(self.ship.p_x) + ", " + str(self.ship.p_y) + ")"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 10))
        buffer = "facing_angle_rad = " + str(self.ship.facing_angle_rad)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 25))
        buffer = "traveling_angle_rad = " + str(self.ship.traveling_angle_rad)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 40))
        buffer = "rotational_energy = " + str(self.ship.rotational_energy)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 55))
        buffer = "rotational_velocity = " + str(self.ship.rotational_velocity)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 70))
        buffer = "previous_vector = (" + str(self.ship.prev_x_v) + ", " + str(self.ship.prev_y_v) + ")"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 85))
        buffer = "velocity = " + str(self.ship.velocity)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 100))
        buffer = "score: " + str(self.score)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 115))
        buffer = "level: " + str(self.level)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 130))
        buffer = "lives: " + str(self.ship.lives)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 145))
        buffer = "dt: " + str(self.dt)
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 160))
        buffer = f"fps: {(1 / self.dt):.1f}" if self.dt > 0 else "undefined"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 175))
        buffer = "entities: " + str(len(self.object_list))
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (20, 190))

    def game_screen_gui(self, canvas):
        self.ship_powerup_gui(canvas)
        self.ship_stat_gui(canvas)


    def draw(self, canvas):
        canvas.fill((0, 0, 0))
        for i in self.object_list:
            image = pygame.transform.rotate(i.sprite, degrees(i.facing_angle_rad))
            #  we need to copy the original sprite and not alter it, as rotating a sprite changes its sprite
            canvas.blit(image, (i.p_x - int(image.get_width() / 2), i.p_y - int(image.get_height() / 2)))
            #  here we center where we render the image on its center, to avoid artifacts when rotating images.
        self.game_screen_gui(canvas)


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
            if not self.ship.powerup_1:
                self.object_list.append(projectile.Projectile(self.ship, duration=2))
                if self.ship.powerup_2:
                    self.object_list.append(projectile.Projectile(self.ship, duration=2, angle=(self.ship.facing_angle_rad-0.1)))
                    self.object_list.append(projectile.Projectile(self.ship, duration=2, angle=(self.ship.facing_angle_rad+0.1)))
            elif self.ship.powerup_1:
                self.object_list.append(projectile.Projectile(self.ship, duration=2, size=2))
                if self.ship.powerup_2:
                    self.object_list.append(projectile.Projectile(self.ship, duration=2, angle=(self.ship.facing_angle_rad-0.1)))
                    self.object_list.append(projectile.Projectile(self.ship, duration=2, angle=(self.ship.facing_angle_rad+0.1)))
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