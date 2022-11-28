import pygame, sys
import math, random
import json
pygame.init()
resolution = (1920, 1080)
window = pygame.display.set_mode(resolution)

BLACK = (0, 0, 0)
GREEN = (46, 131, 9)

class Player:
    def __init__(self):
        self.recoil_type = "y"
        self.hp = 3
        self.ammo_dmg = 22
        self.enemy_spawn_cooldown = pygame.time.get_ticks()
        self.crosshair_roloading = 20
        self.max_ammo = 50
        self.active = False
        self.reload_index = pygame.time.get_ticks()
        self.reload_speed = 2100
        self.player_magazine = 50
        self.last_fr = pygame.time.get_ticks()
        self.last_a = pygame.time.get_ticks()
        self.last_b = pygame.time.get_ticks()
        self.recoil_multiplier = 4
        self.ergo = 10
        self.max_recoil = 200
        self.x_collision_enabled = True
        self.shooting = False
        self.gun_type = "auto"
        self.full_accuracy = False
        self.fire_rate = 70
        self.last = pygame.time.get_ticks()
        self.cross_cooldown = 50
        self.crosshair = 20
        self.x = 0
        self.sprinting = False
        self.stamina = 100
        self.y = 0
        self.image = pygame.image.load("img/player.png")
        self.ak = pygame.image.load("img/Ak47.png")
        self.p90 = pygame.image.load("img/p90.png")
        self.bar = pygame.image.load("img/fast_acces.png")
        self.flash = pygame.image.load("img/MuzzleFlash.png")
        self.bar_object = self.bar.get_rect()
        self.bar_object.x = 830
        self.bar_object.y = 1010
        self.current_gun_object = self.ak.get_rect()
        self.bar = pygame.transform.scale(self.bar, [250, 70])
        self.ak = pygame.transform.scale(self.ak, [82, 24])
        self.p90 = pygame.transform.scale(self.p90, [60, 32])
        self.image = pygame.transform.scale(self.image, [128, 128])
        self.player_object = self.image.get_rect()
        self.width = self.image.get_height()
        self.height = self.image.get_width()
        self.start = pygame.math.Vector2(self.x)
        self.end = self.start
        self.speed = 4
        self.y_aim = 0
        self.last_pos = [0, 0]
        self.gun = pygame.Surface((70, 40)).convert_alpha()
        self.angle = 0
        self.current_gun = self.p90
        self.inventory = {}
        self.load_gun_stats("FN-P90")

    def load_gun_stats(self, gun):
        f = open("assets/rifles.json")
        f = json.load(f)
        self.gun = pygame.image.load(f[gun][6])
        self.current_gun_object = self.gun.get_rect()
        self.gun = pygame.transform.scale(self.gun, f[gun][7])
        self.current_gun = self.gun
        self.max_ammo = f[gun][0]
        self.ergo = f[gun][2]
        self.gun_type = f[gun][5]
        self.recoil_multiplier = f[gun][1]
        self.fire_rate = f[gun][4]
        self.max_recoil = f[gun][3]
        self.ammo_dmg = f[gun][8]

    def per_tick(self, keys, angle):
        if angle < 50:
            self.recoil_type = "y"
        else:
            self.recoil_type = "x"
        self.end = self.start
        self.player_object.x = self.x
        self.player_object.y = self.y
        if self.sprinting == False and self.full_accuracy == False:
            self.speed = 4
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed / 2
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed / 2

        if self.full_accuracy:
            self.speed = 1
        else:
            self.speed = 4

        now = pygame.time.get_ticks()

        self.sprinting = False
        if keys[pygame.K_LSHIFT] and self.full_accuracy == False:
            if self.stamina > 0:
                self.sprinting = True
                self.speed = 8
            if now - self.last >= 200 and self.stamina > 0:
                self.stamina -= 1
                self.last = now

        mouse_presses = pygame.mouse.get_pressed()

        self.mouse_clicked = False
        if mouse_presses[2]:
            self.mouse_clicked = True
            if now - self.last >= self.cross_cooldown and self.crosshair >= 5:
                self.crosshair -= self.ergo / 2
                self.last = now

        if self.crosshair <= 14:
            self.full_accuracy = True
        else:
            self.full_accuracy = False

        if now - self.last_a >= 100 and self.crosshair < 24 and self.mouse_clicked == False:
            self.speed = 4
            self.crosshair += 2
            self.last_a = now
            self.full_accuracy = False

        if self.sprinting == False and now - self.last >= 200 and self.stamina < 100:
            self.last = now
            self.stamina += 1

    def draw(self, bullet, angle):
        self.pos = pygame.mouse.get_pos()
        window.blit(self.image, (self.x, self.y))
        if self.full_accuracy:
            self.y_aim = 35
        else:
            self.y_aim = 40
        if len(guns.bullets) >= 1:
            pass
        else:
            self.angle = angle
        rotimage = pygame.transform.rotate(self.current_gun, self.angle)
        if angle > 90 or angle < -90:
            rotimage = pygame.transform.rotate(self.current_gun, -self.angle)
            rotimage = pygame.transform.flip(rotimage, False, True)

        self.current_gun_object = rotimage.get_rect()
        if self.full_accuracy:
            self.y_aim = 50
        else:
            self.y_aim = 70
        if self.shooting:
            rect = rotimage.get_rect(center=(self.x+55, self.y + self.y_aim))
        else:
            rect = rotimage.get_rect(center=(self.x+60, self.y+self.y_aim))
        window.blit(self.bar, self.bar_object)
        window.blit(rotimage, rect)
        if self.active == True and self.shooting == False and self.full_accuracy == False and self.player_magazine != self.max_ammo:
            pygame.draw.circle(window, BLACK, self.pos, self.crosshair_roloading, width=2)
            self.crosshair_roloading -= 0.1
        else:
            self.crosshair_roloading = 20

        pygame.draw.circle(window, BLACK, self.pos, self.crosshair, width=2)

class Bullet:
    def __init__(self, x, y, player, guns, recoil_type, type="player"):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        if type=="player":
            if player.crosshair <= 50:
                player.crosshair += guns.bullet_count / 2

            guns.bullet_count += 1
            guns.aditional_recoil = guns.bullet_count * player.recoil_multiplier

            if player.full_accuracy == False:
                if random.randint(1, 2) == 1:
                    recoil_a = random.randint(30, 70+guns.aditional_recoil)
                    if recoil_type=="x":
                        mx -= recoil_a
                    else:
                        my -= recoil_a

            if guns.aditional_recoil <= player.max_recoil:
                if recoil_type == "x":
                    mx -= random.randint(5, 10 + guns.aditional_recoil)
                else:
                    my -= random.randint(5, 10+guns.aditional_recoil)
            else:
                if recoil_type == "x":
                    mx -= random.randint(5, player.max_recoil - 20)
                else:
                    my -= random.randint(5, player.max_recoil-20)
        else:
            if recoil_type == "x":
                mx -= random.randint(5, 50)
            else:
                my -= random.randint(5, 50)

        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((7, 4)).convert_alpha()
        self.bullet.fill((189,183,107))
        self.bullet = pygame.transform.rotate(self.bullet, angle)

        if type=="player" and player.shooting:
            player.angle = angle

        self.speed = 40

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed,
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)

class World:
    def __init__(self, player):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.background = pygame.image.load("img/background.png")
#        self.andrew = pygame.image.load("img/andrew.png")
#        self.andrew = pygame.transform.scale(self.andrew, [128, 128])
#        self.target = self.andrew.get_rect()
#        self.target.x = 500
#        self.target.y = 300
        self.hit = 0
        self.edgeR = pygame.Rect((1930, 0), (10, 1080))
        self.edgeB = pygame.Rect((0, 1080), (1920, 10))
        self.edgeT = pygame.Rect((0, 0), (1920, 10))
        self.collide = False
        self.collideB = True
        self.collideT = False
        self.stage = 1
        self.rect_list = []
        self.init_world("first_world.json", 1, 0, player)
        self.x_collision = False

    def init_world(self, world, stage, player_y, player):
        if player.y == player_y:
            pass
        else:
            player.y = player_y
        f = open(f"worlds/{world}", "r")
        self.rect_list = []
        f = json.load(f)
        for a in f["rects"]:
            if a[4] == stage:
                self.rect_list.append(pygame.Rect(a[0], a[1], a[2], a[3]))
        filename = f[f"s{stage}"]
        self.background = pygame.image.load(f"img/{filename}").convert()
        self.background = pygame.transform.scale(self.background, pygame.Vector2(1024 * 2, 576 * 2))
#        self.background = pygame.transform.scale(self.background, [1920, 1080])

    def per_tick(self, player, fps):
        window.blit(self.background, (0, 0))
        if player.player_object.colliderect(self.edgeT):
            self.collideT = True
            self.stage = 1
            self.init_world("first_world.json", 1, 900, player)
        else:
            self.collideT = False

        if player.player_object.colliderect(self.edgeR):
            self.collide = True
        else:
            self.collide = False
        if player.player_object.colliderect(self.edgeB):
            self.collideB = True
            self.stage = 2
            self.init_world("first_world.json", 2, 80, player)
        else:
            self.collideB = False
        bullets_t = len(guns.bullets)
        text = self.font.render(f'Stamina: {player.stamina} Enemies killed: {enemies.enemies_killed} Full Accuracy: {player.full_accuracy} Recoil: {guns.aditional_recoil} SPEED:{player.speed} PX: {player.x} PY: {player.y}, Collide: {self.collide} BCollide: {self.collideB}  TCollide: {self.collideT} Bullets: {bullets_t} Ammo: {player.player_magazine} FPS: {fps}, HP: {player.hp}', True, BLACK, GREEN)
        textRect = text.get_rect()
        window.blit(text, textRect)
        pygame.draw.rect(window, BLACK, self.edgeR)
        pygame.draw.rect(window, BLACK, self.edgeB)
        for rect_obj in self.rect_list:
            for bullet in guns.bullets[:]:
                if rect_obj.collidepoint(bullet.pos):
                    guns.bullets.remove(bullet)
            #pygame.draw.rect(window, (0, 0, 255), rect_obj)
            if player.player_object.colliderect(rect_obj):
                if player.player_object.colliderect(rect_obj) and player.x < rect_obj[0]:
                    player.x -= 10
                if player.player_object.colliderect(rect_obj) and player.x > rect_obj[0]:
                    player.x += 10
                if player.player_object.colliderect(rect_obj) and player.y < rect_obj[0]:
                    player.y -= 10
                if player.player_object.colliderect(rect_obj) and player.y > rect_obj[0]:
                    player.y += 10

class Guns_Mechanic:
    def __init__(self):
        self.aditional_recoil = 0
        self.bullet_count = 0
        self.cooldown_tracker = 0
        self.x = 0
        self.y = 0
        self.size = 0
        self.xval = 0
        self.yval = 0
        self.bullets = []

    def per_tick(self, player):
        for bullet in self.bullets:
            bullet.draw(window)

    def draw(self, player, w):
        for bullet in guns.bullets[:]:
            bullet.update()
            if not window.get_rect().collidepoint(bullet.pos):
                self.bullets.remove(bullet)

class wave:
    def __init__(self):
        self.wave = 0

    def start_wave(self, bg):
        pass

class enemies:
    def __init__(self):
        self.enemies = []
        #self.bandit = [100, 20, 20, 0, 0]
        self.image = pygame.image.load("img/enemy.png")
        self.image = pygame.transform.scale(self.image, [128, 128])
        self.bandit_object = self.image.get_rect()
        self.enemies.append([self.bandit_object, 15, 1])
        self.check = True
        self.blood_img = pygame.image.load("img/blood.png")
        self.enemies_killed = 0
        self.blood = []

    def per_tick(self, player):
        for a in self.enemies:
            try:
                dirvect = pygame.math.Vector2(player.x - a[0].x,
                                              player.y - a[0].y)
                dirvect.normalize()
                dirvect.scale_to_length(2)
                a[0].move_ip(dirvect)
            except:
                pass

    def draw(self, bg):
        for a in self.enemies:
            if a[2] == bg.stage:
                window.blit(self.image, a[0])
        for a in self.blood:
            print(a)
            if a[1] >= 0:
                a[1] -= 1
                window.blit(self.blood_img, a[0])
            else:
                self.blood.remove(a)

    def new_enemy(self, player, stage, x, y, type="inside", hp=100):
        if type == "inside":
            self.rect = pygame.Rect(x, y, 100, 120)
            self.enemies.append([self.rect, hp, stage])
        else:
            self.rect = pygame.Rect(player.x, player.y, 100, 120)
            self.enemies.append([self.rect, hp, stage])

    def collision_check(self, player):
        for a in self.enemies:
            for bullet in guns.bullets[:]:
                if a[0].collidepoint(bullet.pos):
                    guns.bullets.remove(bullet)
                    a[1] -= player.ammo_dmg
                    self.blood.append([bullet.pos, 5])
                    if a[1] <= 0:
                        self.enemies_killed += 1
                        self.enemies.remove(a)
            if player.player_object.colliderect(a[0]):
                self.blood.append([a[0], 5])
                self.enemies.remove(a)
                player.hp -= 1

guns = Guns_Mechanic()
enemies = enemies()

def main():
    run = True
    player = Player()
    bg = World(player)
    clock = pygame.time.Clock()
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    while run:
        pos = pygame.mouse.get_pos()
        mouse_presses = pygame.mouse.get_pressed()
        now = pygame.time.get_ticks()
        if mouse_presses[0]:
            if now - player.last_fr >= player.fire_rate and player.gun_type == "auto" and player.active == False:
                if player.player_magazine <= 0:
                    pass
                else:
                    guns.bullets.append(Bullet(*[player.x + 50, player.y + 30], player, guns, player.recoil_type))
                    player.player_magazine -= 1
                    player.shooting = True
                player.last_fr = now
        if now - player.last_b >= 100 and not mouse_presses[0]:
            if player.crosshair > 26:
                player.crosshair -= 3
            player.shooting = False
            if guns.aditional_recoil > 0:
                guns.aditional_recoil -= 10
                if guns.aditional_recoil < 0:
                    guns.aditional_recoil = 0
            guns.bullet_count = 0
            player.last_b = now
        pygame.time.Clock().tick(144)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and player.gun_type == "semi" and now - player.last_fr >= player.fire_rate and player.active == False:
                if player.player_magazine <= 0:
                    pass
                else:
                    guns.bullets.append(Bullet(*[player.x + 50, player.y + 30], player, guns, "x"))
                    player.player_magazine -= 1
                    player.shooting = True
                player.last_fr = now

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    enemies.new_enemy(player, bg.stage)
                elif event.key == pygame.K_r and player.shooting == False and player.full_accuracy == False and player.player_magazine != player.max_ammo:
                    player.reload_index = now
                    player.active = True
        if now - player.reload_index >= player.reload_speed and player.active == True and player.shooting == False and player.full_accuracy == False and player.player_magazine != player.max_ammo:
            player.player_magazine = player.max_ammo
            player.active = False
        if now - player.enemy_spawn_cooldown >= 1500 and bg.stage == 2:
            player.enemy_spawn_cooldown = now
            x = random.randint(50, 1800)
            y = random.randint(50, 400)
            enemies.new_enemy(player, 2, x, y)

        dir = (pos[0] - player.x, pos[1] - player.y)
        angle = math.degrees(math.atan2(-dir[1], dir[0]))
        keys = pygame.key.get_pressed()
        fps = clock.get_fps()
        fps = round(fps)
        clock.tick()
        bg.per_tick(player, fps)
        player.per_tick(keys, angle)
        enemies.per_tick(player)
        enemies.collision_check(player)
        enemies.draw(bg)
        player.draw(Bullet, angle)
        guns.per_tick(player)
        guns.draw(player, bg)
        pygame.display.update()

main()