import time

import pygame

pygame.init()

class Settings:
    is_game_active = True
    shoot_sound = None
    explosion_sound = None
    score = 0
    is_game_active = True

    @classmethod

    def draw_score(cls, screen, x, y, color):
        f = pygame.font.Font(None, 36)
        score_text = f.render(str(Settings.score), True, color)
        screen.blit(score_text, (x, y))

    @classmethod
    def draw_text(cls, screen, x, y, color, size, text):
        f = pygame.font.Font(None, size)
        score_text = f.render(text, True, color)
        screen.blit(score_text, (x, y))

    def load_and_play_music(cls, path_to_music):
        pygame.mixer.music.load(path_to_music)

    def set_music_volume(cls, volume):
        pygame.mixer.music.set_volume(volume)

WIDTH = 720
HEIGHT = 480

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class GameObjekt():
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = red
        self.size = 20
        self.speed = 5.0
        self.has_image = False
        self.image = None

    def draw(self):
        if not self.has_image:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))
        else:
            self.screen.blit(self.image, (self.x, self.y))

    def add_image(self, path_to_image):
        my_image = pygame.image.load(path_to_image)
        self.image = pygame.transform.scale(my_image,(self.size, self.size))
        self.has_image = True

class Boss(GameObjekt):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.color = green
        self.pattern_x = 1
        self.size = 90

    def move(self):
        self.x += self.speed * self.pattern_x
        if self.x > WIDTH:
            self.pattern_x = -1
        if self.x < 0:
            self.pattern_x = 1

    def shoot(self, projectiles):
        projectile = Projectile(self.x + self.size // 2, self.y - self.size / 2 + 30, screen)
        projectiles.append(projectile)



class Enemy(GameObjekt):
    def __init__(self, x, y, screen):
        super().__init__(x,y,screen)
        self.color = red
        self.pattern_x = 1
        self.start_x = x
        self.speed = 2.5



    def move(self):
        self.x -= self.speed * self.pattern_x
        if self.x <= self.start_x - 40:
            self.pattern_x = -1
        if self.x >= self.start_x + 60:
            self.pattern_x = 1
            self.y += self.speed
            self.speed += 0.2

    def check_end(self):
        if self.y >= HEIGHT - self.size:
            Settings.is_game_active = False

class Explosion(GameObjekt):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.color = red
        self.size = 1

    def expand(self, explosion_list):
        self.size += 6
        self.x -= 3
        self.y -= 3
        if self.size >= 100:
            explosion_list.remove(self)

class Hero(GameObjekt):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.color = green
        self.size = 40
        

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def shoot(self, projectiles):
        projectile = Projectile(self.x + self.size // 2, self.y - self.size / 2 + 30, screen)
        projectiles.append(projectile)



class Projectile(GameObjekt):
    def init(self, x, y, screen):
        super().__init__(x, y, screen)
        self.size = 5
        self.color = blue

    def check_collision(self, enemies, hero, projectile_list, explosion_list, boss_list):
        if self.align == 1:
            for enemy1 in enemies:
                self.check_enemy(enemies, enemy1, explosion_list, projectile_list)
            for boss in boss_list:
                self.enemy(boss_list, boss, explosion_list, projectile_list)

            if 0 >= self.y:
                projectile_list.remove(self)

    def check_enemy(self, enemies, enemy1, explosion_list, projectile_list):
        if enemy1.y - enemy1.size / 2 <= self.y <= enemy1.x + enemy1.size / 2:
            if enemy1.x - enemy1.size / 2 <= self.x <= enemy1.x + enemy1.size / 2:
                enemies.remove(enemy1)
                if type(enemy1) is Boss:
                    Settings.score += 10
                if type(enemy1) is Enemy:
                    Settings.score += 1
                explosion_list.append(Explosion(self.x, self.y, self.screen))
                projectile_list.remove(self)

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))


screen = pygame.display.set_mode((WIDTH,HEIGHT))

fps = 30
clock = pygame.time.Clock()



background_music = pygame.mixer.Sound('music\\background.mp3')
shoot_music = pygame.mixer.Sound('music\\shoot_sound.wav')

enemies = list()
projectiles = list()
explosions = []
projectiles_boss = list()
boss_list = list()
bosses = list()
boss = Boss(0, 10, screen)
boss.add_image('images//boss.png')
bosses.append(boss)

for i in range(550):
    for j in range(6):
        enemy1 = Enemy(40 + i + 20, 80 + j * 40, screen)
        enemies.append(enemy1)

hero = Hero(WIDTH/2,HEIGHT-50,screen)

is_left = False
is_right = False
is_shoot = False

background_image = pygame.image.load('images\\background.png')
scale_background = pygame.transform.scale(background_image,(WIDTH, HEIGHT))

start_ticks_shoot = pygame.time.get_ticks()

background_music.play(-1)
background_music.set_volume(0.1)

while Settings.is_game_active:
    screen.fill(black)
    screen.blit(scale_background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                is_left = True
            if event.key == pygame.K_d:
                is_right = True
            if event.key == pygame.K_SPACE:
                is_shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                is_left = False
            if event.key == pygame.K_d:
                is_right = False
            if event.key == pygame.K_SPACE:
                is_shoot = False

    seconds_from_last_shoot = (pygame.time.get_ticks() - start_ticks_shoot / 1000)

    if is_left:
        hero.move_left()
    if is_right:
        hero.move_right()
    if is_shoot and seconds_from_last_shoot > 1:
        hero.shoot(projectiles)
        start_ticks_shoot = pygame.time.get_ticks()

    for enemy1 in enemies:
        enemy1.move()
        enemy1.draw()
        enemy1.check_end()

    for boss in bosses:
        boss.move()
        boss.draw()
        boss.shoot(projectiles_boss)

    hero.draw()

    for projectile in projectiles:
        projectile.move()
        projectile.check_collision(enemies, boss_list, projectiles, explosions)
        projectile.draw()

    for projectile in projectiles_boss:
        projectile.move()
        projectile.draw()

    for explosion in explosions:
        explosions.expand(explosions)
        explosion.draw()

    Settings.draw_score(screen, 0, 0, green)
    pygame.display.update()
    clock.tick(fps)

screen.fill(black)
Settings.draw_text(screen, 250, 200, red, 50, 'Game Over')
pygame.display.update()
time.sleep(5)
quit()