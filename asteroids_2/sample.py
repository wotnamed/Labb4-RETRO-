import pygame
import player
import projectile
import asteroid
import saucer
import powerup
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
        self.level = 0  # default should be 1 (see self.setup)
        self.score = 0
        self.scene = 0
        self.sfx_1 = None
        self.sfx_2 = None
        self.sfx_3 = None
        self.sfx_4 = None
        self.sfx_5 = None
        self.sfx_6 = None
        self.game_time = 0
        #  The first value in the list below indicates if the gui is toggled, the other if the gui was toggled last update.
        self.toggle_debug_gui = [0, 0]

    def random_spawn_object(self, count, type, safe_distance=10000):
        z = 0
        while z < count:  # A while loop is used to only generate objects outside a desired area.
            #  Generate a random position
            pos = (random.randint(0, self.window_size), random.randint(0, self.window_size))
            #  Make sure that the object is generated outside the "safe zone", aka a certain distance from the player.
            if ((pos[0] - self.window_size / 2)**2 + (pos[1] - self.window_size / 2)**2) > safe_distance:
                if type == "saucer":
                    self.object_list.append(saucer.Saucer(x=pos[0], y=pos[1], enemy=self.ship, tick_per_fire=100-count))
                elif type == "asteroid":
                    self.object_list.append(asteroid.Asteroid(mother=None, size=3, x=pos[0], y=pos[1]))
                else:
                    print("Type not recognised.")
                z += 1
            else:
                pass

    def level_init(self, level):
        #  clear object list, add and reset ship, play init sound, spawn level appropriate objects.
        self.object_list = []
        self.object_list.append(self.ship)
        self.ship.reset(self.window_size, 3)
        self.sfx_4.play()
        if level <= 10:
            self.random_spawn_object(count=level+3, type="asteroid")
        if level > 10:
            self.random_spawn_object(count=level-10, type="saucer")

    def setup(self):
        #  set level and score, init sounds, init player, init fonts, init first level
        self.level = 1
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
        #  init pygame, define display, run setup, run game loop
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

    def pause_screen(self, canvas):
        canvas.fill((0,0,0))
        canvas.blit(self.font_2.render("This is the pause screen.", True, (255, 255, 255)), (250, 350))
        canvas.blit(self.font_2.render("Press '1' or 'SPACE' to switch back to gameplay.", True, (255, 255, 255)), (250, 365))

    def death_screen(self, canvas, keys):
        #  Show score after the current game has ended and enable replay.
        canvas.fill((0,0,0))
        canvas.blit(self.font_2.render("Death.", True, (255, 255, 255)), (250, 350))
        buffer = f"Score: {self.score}"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)),(250, 365))
        canvas.blit(self.font_2.render("To restart, press 'x'.", True, (185, 255, 255)),(250, 380))
        if keys[pygame.K_x]:
            self.setup()
            self.scene = 0

    def start_screen(self, canvas, keys):
        #  Starting info as well as a pathway to change to game screen
        canvas.fill((0, 0, 0))
        canvas.blit(self.font_2.render("Welcome, dear pilot.", True, (255, 255, 255)), (250, 350))
        canvas.blit(self.font_2.render("You have two types of ship available.", True, (255, 255, 255)), (250, 365))
        canvas.blit(self.font_2.render("The first one has a fixed steering speed.", True, (255, 255, 255)), (250, 380))
        canvas.blit(self.font_2.render("The second one has an unlocked", True, (255, 255, 255)), (250, 395))
        canvas.blit(self.font_2.render("steering computer, with a higher difficulty to boot.", True, (255, 255, 255)), (250, 410))
        canvas.blit(self.font_2.render("To change ship type, press 'C' for 1 and 'V' for 2.", True, (255, 255, 255)), (250, 425))
        canvas.blit(self.font_2.render("Press 'SPACE' to depart.", True, (255, 255, 255)), (250, 440))
        canvas.blit(self.font_2.render("Good luck.", True, (255, 255, 255)), (250, 455))

        canvas.blit(self.font_3.render("Keybindings (game screen):", True, (255,255,255)), (250, 100))
        canvas.blit(self.font_3.render("'W' or 'UP' - Accelerate", True, (255,255,255)), (250, 110))
        canvas.blit(self.font_3.render("'A' or 'LEFT' - Turn left", True, (255,255,255)), (250, 120))
        canvas.blit(self.font_3.render("'D' or 'RIGHT' - Turn right", True, (255,255,255)), (250, 130))
        canvas.blit(self.font_3.render("'SPACE' - Fire projectile", True, (255,255,255)), (250, 140))
        canvas.blit(self.font_3.render("'1' or 'SPACE' - Unpause game", True, (255,255,255)), (250, 150))
        canvas.blit(self.font_3.render("'2' or 'ESCAPE' - Pause game", True, (255,255,255)), (250, 160))
        canvas.blit(self.font_3.render("'Q' - Toggle extra stats", True, (255,255,255)), (250, 170))


        if keys[pygame.K_c]:
            self.ship.movement_type = "arcade"
        elif keys[pygame.K_v]:
            self.ship.movement_type = "physics"

        if self.ship.movement_type == "arcade":
            canvas.blit(self.font_2.render("Type 1 currently selected.", True, (255, 185, 255)), (250, 500))
        elif self.ship.movement_type == "physics":
            canvas.blit(self.font_2.render("Type 2 currently selected.", True, (255, 255, 185)), (250, 500))

    def game_screen(self, keys):
        #  count saucers and asteroids to facilitate "next level logic" (pun intended)
        saucer_count = 0
        asteroid_count = 0
        self.random_powerup_spawn(average_ticks_per_spawn=5000, duration=10)
        #  update player
        self.react_to_user_input(keys)
        self.ship.tick(self.dt)
        #  update game objects
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

        self.collision_checking(threshold=1000)
        #  check if level increase condition is met and if so increase level
        if asteroid_count == 0 and saucer_count == 0:
            self.level += 1
            self.level_init(self.level)

    def random_powerup_spawn(self, average_ticks_per_spawn, duration):
        #  runs every tick and has a specified chance (average_ticks_per_spawn) to spawn powerup with a duration
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
        #  Adjusts a specified entity to be within the game window. Known issue: player flies fast enough to escape.
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
        #  Update mask related data for each object in self.object_list
        for i in self.object_list:
            image = pygame.transform.rotate(i.sprite, degrees(i.facing_angle_rad))
            i.mask = pygame.mask.from_surface(image)
            mask_image_1 = i.mask.to_surface()
            i.mask_width = int(mask_image_1.get_width())
            i.mask_height = int(mask_image_1.get_height())
        #  For every entity, check every other entity for collision if the entities are in relative proximity of each other (threshold specifies relative proximity)
        for i in self.object_list:
            for e in self.object_list:
                if e.mask is not None and i.mask is not None and e != i and (i.p_x-e.p_x)**2+(i.p_y-e.p_y)<threshold:
                    if i.mask.overlap(e.mask, ((e.p_x - e.mask_width/2) - (i.p_x - i.mask_width/2), (e.p_y - e.mask_height/2) - (i.p_y - i.mask_height/2))):
                        #  call the collided entity for its reaction
                        outcome = i.handle_collision(e)
                        try:
                            main.collision_handler(outcome, i)
                        except ValueError:
                            pass

    def collision_handler(self, result, i):
        #  Handles collision reactions based on class
        if isinstance(i, player.Player):
            match result:
                case "death":
                    self.sfx_3.play()
                    self.ship.lives -= 1
                    self.ship.reset(self.window_size, invincibility_duration=3)
        if isinstance(i, projectile.Projectile):
            match result:
                case "hit":
                    try:
                        index = self.object_list.index(i)
                        del self.object_list[index]
                    except ValueError:
                        pass
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
                        if self.ship.powerups[0] >= 1:
                            self.score += 200
                        else:
                            self.ship.powerups[0] += 1
                    elif i.type == 2:
                        if self.ship.powerups[1] >= 10:
                            self.score += 200
                        else:
                            self.ship.powerups[1] += 1
                    elif i.type == 3:
                        self.ship.powerups[2] += 1
                        self.ship.lives += 1
                    index = self.object_list.index(i)
                    del self.object_list[index]
                    self.sfx_6.play()

    def handle_events(self, canvas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
        #  fetch pressed keys
        keys = pygame.key.get_pressed()
        self.scene_switcher(keys)
        if self.scene == 3:
            self.death_screen(canvas, keys)
        if self.scene == 2:
            self.pause_screen(canvas)
        if self.scene == 1:
            self.game_screen(keys)
            self.game_time += self.dt
        if self.scene == 0:
            self.start_screen(canvas, keys)
    
    def ship_powerup_gui(self, canvas):
        if self.ship.invincible:
            text = f"Invincible! ({self.ship.invincibility_duration:.1f})"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 300))
        if self.ship.powerups[0] > 0:
            text = f"Big shot {self.ship.powerups[0]}"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 315))
        if self.ship.powerups[1] > 0:
            text = f"Front splitter {self.ship.powerups[1]}"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 330))
        if self.ship.powerups[2] > 0:
            text = f"Extra life (x{self.ship.powerups[2]})"
            canvas.blit(self.font_2.render(text, True, (85, 85, 255)), (20, 345))

    def ship_stat_gui(self, canvas):
        # Toggleable GUI:
        if self.toggle_debug_gui[0] == 1:
            buffer = f"Position =  ({self.ship.p_x:.1f}, {self.ship.p_y:.1f})"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 5))
            buffer = f"Facing angle = {self.ship.facing_angle_rad:.1f}"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 15))
            buffer = f"Traveling angle = {self.ship.traveling_angle_rad:.1f}" if self.ship.traveling_angle_rad is not None else "Traveling_angle_rad = undefined"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 25))
            buffer = f"Rotational energy = {self.ship.rotational_energy:.1f}"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 35))
            buffer = f"Rotational velocity = {self.ship.rotational_velocity:.1f}"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 45))
            buffer = f"Previous vector = ({self.ship.prev_x_v:.1f}, {self.ship.prev_y_v:.1f})"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 55))
            buffer = f"Velocity = {self.ship.velocity:.1f}"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (150, 65))
            buffer = f"dt: {self.dt}"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (85, 5))
            buffer = f"fps: {(1 / self.dt):.1f}" if self.dt > 0 else "undefined"
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (85, 15))
            buffer = "entities: " + str(len(self.object_list))
            canvas.blit(self.font_3.render(buffer, True, (255, 255, 255)), (85, 25))
        #  Mandatory GUI:
        buffer = f"Score: {self.score}"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (5, 5))
        buffer = f"Level: {self.level}"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (5, 20))
        buffer = f"Lives: {self.ship.lives}"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (5, 35))
        buffer = f"Time: {self.game_time:.1f}"
        canvas.blit(self.font_2.render(buffer, True, (255, 255, 255)), (5, 50))

    def game_screen_gui(self, canvas):
        self.ship_powerup_gui(canvas)
        self.ship_stat_gui(canvas)

    def draw(self, canvas):
        canvas.fill((0, 0, 0))
        for i in self.object_list:
            #  we need to copy the original sprite and not alter it, as rotating a sprite changes its size
            image = pygame.transform.rotate(i.sprite, degrees(i.facing_angle_rad))
            #  here we center where we render the image on its center, to avoid artifacts when rotating images.
            canvas.blit(image, (i.p_x - int(image.get_width() / 2), i.p_y - int(image.get_height() / 2)))
        self.game_screen_gui(canvas)

    def fire_ship_cannon(self, velocity=300):
        if self.ship.powerups[0] == 0:  # if not big shot
            self.object_list.append(projectile.Projectile(self.ship, duration=2, velocity=velocity))
            if self.ship.powerups[1] > 0:  # if front splitter
                in_range = 1
                for i in range(self.ship.powerups[1]):
                    self.object_list.append(
                        projectile.Projectile(self.ship, duration=2, angle=(self.ship.facing_angle_rad - 0.1*in_range), velocity=velocity))
                    self.object_list.append(
                        projectile.Projectile(self.ship, duration=2, angle=(self.ship.facing_angle_rad + 0.1*in_range), velocity=velocity))
                    in_range += 1
        elif self.ship.powerups[0] > 0:  # if big shot
            self.object_list.append(projectile.Projectile(self.ship, duration=2, size=2, velocity=velocity))
            if self.ship.powerups[1] > 0:  # if front splitter
                in_range = 1
                for i in range(self.ship.powerups[1]):
                    self.object_list.append(
                        projectile.Projectile(self.ship, size=2, duration=2, angle=(self.ship.facing_angle_rad - 0.1 * in_range), velocity=velocity))
                    self.object_list.append(
                        projectile.Projectile(self.ship, size=2, duration=2, angle=(self.ship.facing_angle_rad + 0.1 * in_range), velocity=velocity))
                    in_range += 1

    def react_to_user_input(self, keys):
        #  Acceleration / deceleration (deceleration would be engine_input = -1)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            engine_input = 1
        else:
            engine_input = 0
        #  Steering
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steer = 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steer = -1
        elif not keys[pygame.K_LEFT] or not keys[pygame.K_a] or not keys[pygame.K_RIGHT] or not keys[pygame.K_d]:
            steer = 0
        else:
            steer = 0
        #  Fire the ships cannon. prev_tick_shot is used to ensure that the ship doesn't fire once per tick.
        if keys[pygame.K_SPACE] and self.ship.prev_tick_shot is False:
            self.fire_ship_cannon()
            self.sfx_1.play()
            self.ship.prev_tick_shot = True  #default: True
        elif not keys[pygame.K_SPACE]:
            self.ship.prev_tick_shot = False
        #  Feed input into ship
        self.ship.steer(steer, self.dt)
        self.ship.vector_and_position_update(engine_input, self.dt)
        #  Toggle debug GUI
        if keys[pygame.K_q]:
            if self.toggle_debug_gui[1] == 0:
                if self.toggle_debug_gui[0] == 0:
                    self.toggle_debug_gui[0] = 1
                elif self.toggle_debug_gui[0] == 1:
                    self.toggle_debug_gui[0] = 0
                self.toggle_debug_gui[1] = 1
        else:
            self.toggle_debug_gui[1] = 0


main = Main()
main.main()