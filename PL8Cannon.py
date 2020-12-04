import pygame as pg
import sys
import numpy as np
import yaml
from random import randint

SCREEN_SIZE = (1600, 900)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pg.init()
pg.font.init()

all_sprites = pg.sprite.Group()

class MainMenu:
    def __init__(self):
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.leaderboard = LeaderBoard(self.screen)
        self.manager = Manager(self.screen)
        self.font = pg.font.SysFont('ariel', 100)
        self.margin = 20

    def button_with_text(self, text, x, y, event=None):
        text = self.font.render(text, True, (219, 100, 0))  # 254, 111, 94
        text_rect = pg.Rect((x - text.get_width() // 2 - self.margin,
                             y - text.get_height() // 2 - self.margin),
                            (text.get_width() + 2 * self.margin,
                             text.get_height() + 2 * self.margin))
        #  pg.draw.rect(self.screen, (254, 111, 94), text_rect)
        self.screen.blit(text, (x - text.get_width() // 2,
                                y - text.get_height() // 2))
        if event is not None:
            if event.type == pg.MOUSEBUTTONDOWN and text_rect.collidepoint(event.pos):
                return True

    def run(self):
        while True:
            for event in pg.event.get():
                self.screen.fill((22, 105, 122))
                if self.button_with_text('Начать',
                                         self.screen.get_width() // 2, self.screen.get_height() * 7 / 24, event):
                    self.manager.clock.tick(0.7)
                    self.manager.run()
                if self.button_with_text('Таблица лидеров',
                                         self.screen.get_width() // 2, self.screen.get_height() * 11 / 24, event):
                    self.leaderboard.run()
                if self.button_with_text('Выход',
                                         self.screen.get_width() // 2, self.screen.get_height() * 15 / 24, event):
                    pg.quit()
                    sys.exit()
            pg.display.flip()


class LeaderBoard:
    def __init__(self, screen):
        self.screen = screen
        self.alive = False
        self.score_display: pg.Surface
        self.font = pg.font.SysFont('ariel', 40)
        self.score_dict = {}

    def load_scores(self):
        self.score_dict = yaml.load('Leaderboard', Loader=yaml.FullLoader)

    def update_scores(self):
        yaml.dump(self.score_dict, 'Leaderboard', sort_values=True)

    def display_scores(self):
        for i, key, value in enumerate(self.score_dict.items()):
            self.score_display = self.font.render(str(i) + '. ' + key + ' ' + str(value), True, (171, 215, 235))
            self.screen.blit(self.score_display, (0, i * self.score_display.get_height() + i * 10 + 20))
        self.screen.flip()

    def run(self):
        self.alive = True
        while self.alive:
            self.update_scores()
            self.display_scores()


class Ball(pg.sprite.Sprite):
    def __init__(self, screen, FPS, coord=[0, 0], vel=[0, 0], color=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Resources/Shell.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        self.FPS = FPS
        self.screen = screen
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord.copy()
        self.vel = vel.copy()
        self.is_alive = True

    def draw(self):
        self.screen.blit(self.image, (self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h))

    def move(self, t_step=1., g=5.):
        t_step /= self.FPS // 30
        self.vel[1] += int(g * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 1 and self.coord[1] >= self.screen.get_height() - self.r:
            self.is_alive = False


class Gun:
    def __init__(self, screen, area, coord=[30, SCREEN_SIZE[1] // 2],
                 min_pow=20, max_pow=100, FPS=30):
        self.area = area
        self.screen = screen
        self.FPS = FPS
        self.coord = coord.copy()
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = self.min_pow
        self.vel = int(100 * 30 // self.FPS)
        self.active = False
        self.fired_vel = [0, 0]

        self.step = 30

    def draw(self):
        end_pos = (self.coord[0] + int(self.power * np.cos(self.angle)),
                   self.coord[1] + int(self.power * np.sin(self.angle)))
        pg.draw.line(self.screen, RED, self.coord, end_pos, 5)

    def power_up(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def fire(self):
        self.fired_vel = [int(self.power * np.cos(self.angle)),
                          int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow

    def move_up(self):
        if self.coord[1] < self.area.y + 2*self.step:
            self.coord[1] = self.area.y + 2*self.step
        self.coord[1] -= self.step

    def move_down(self):
        if self.coord[1] > self.area.y + self.area.h - 2*self.step:
            self.coord[1] = self.area.y + self.area.h - 2*self.step
        self.coord[1] += self.step

    def move_right(self):
        if self.coord[0] > self.area.x + self.area.w - 2*self.step:
            self.coord[0] = self.area.x + self.area.w - 2*self.step
        self.coord[0] += self.step

    def move_left(self):
        if self.coord[0] < self.area.x + 2*self.step:
            self.coord[0] = self.area.x + 2*self.step
        self.coord[0] -= self.step

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])

    def move(self, event):
        pg.key.set_repeat(1, self.vel)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.move_up()
            if event.key == pg.K_DOWN:
                self.move_down()
            if event.key == pg.K_RIGHT:
                self.move_right()
            if event.key == pg.K_LEFT:
                self.move_left()


class Target(pg.sprite.Sprite):
    def __init__(self, screen, area, coord=[0, 0]):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Resources/Aerial_Target.png").convert()
        self.area = area
        self.screen = screen
        self.points = 0
        self.life = 1
        self.coord = coord.copy()
        self.vel = [0, 0]
        self.r = randint(10, 30)
        self.color = RED

        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        self.vel[0] = randint(3, 8)
        self.amp = randint(0, min(abs(self.coord[1] - self.area.h), abs(self.coord[1] - self.area.y)) // 2)
        self.curve = randint(10, 100)

    def draw(self):
        self.screen.blit(self.image, (self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h // 2))

    def pattern(self):
        self.vel[1] = int(self.amp / self.curve * np.cos(self.coord[0] / self.curve) * self.vel[0])
        self.coord[1] += self.vel[1]

    def move(self):
        self.coord[0] += self.vel[0]
        self.pattern()
        self.rect = pg.Rect.move(self.rect, self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h // 2)

        if self.coord[0] > self.screen.get_width() * 27 / 24:
            self.vel[0] = -1 * self.vel[0]
        if self.coord[0] < -1 * self.screen.get_width() * 3 / 24:
            self.vel[0] = -1 * self.vel[0]

    def is_hit(self, obj, points=1):
        """
        Попадание шарика в цель.
        """
        if self.rect.colliderect(obj.rect):
            self.points += points
            return True
        else:
            return False


class ArmouredTarget(Target):
    def __init__(self, gun):
        self.gun = gun
        pass

    def draw(self):
        pass

    def attack(self):
        pass

    def move(self):
        pass


class Projectile(pg.sprite.Sprite):
    def __init__(self, screen, coord=[0, 0], vel=[0, 0]):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Resources/Projectile.png").convert()
        self.coord = coord.copy()
        self.vel = vel.copy()
        self.rect = self.image.get_rect()
        self.alive = True

    def is_hit(self):
        pass



class Manager:
    def __init__(self, screen):
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.text = ''
        self.clock = pg.time.Clock()
        self.round_done = False
        self.screen = screen
        self.ground = pg.Rect((0, self.screen.get_height() * 2 // 3),
                              (self.screen.get_width(), self.screen.get_height() // 3))
        self.sky = pg.Rect((0, 0), (self.screen.get_width(), self.screen.get_height() * 2 // 3))
        self.FPS = 60
        self.number_of_targets = 3
        self.gun = Gun(screen=self.screen, FPS=self.FPS, area=self.ground)
        self.balls = []
        self.dead_balls = []
        self.targets = []

    def init_targets(self):
        for i in range(self.number_of_targets):
            self.targets.append(Target(screen=self.screen,
                                       coord=[randint(0, 0),
                                              randint(0, self.screen.get_height() // 3)],
                                       area=self.sky))

    def end_round_card(self):
        self.screen.fill(BLACK)
        self.dead_balls.extend(self.balls)
        self.text = self.font.render('Вы уничтожили цель за ' + str(len(self.dead_balls)) +
                                     ' выстрелов', True, WHITE)
        self.screen.blit(self.text, (self.screen.get_width() // 2 - self.text.get_width() // 2,
                                     self.screen.get_height() // 2 - self.text.get_height() // 2))
        pg.display.flip()

    def draw(self):
        pg.draw.rect(self.screen, (126, 200, 80), self.ground)
        pg.draw.rect(self.screen, (209, 237, 242), self.sky)

        for ball in self.balls:
            ball.draw()
        self.gun.draw()
        for target in self.targets:
            target.draw()

    def move(self):
        for ball in self.balls:
            ball.move()
        for target in self.targets:
            target.move()

    def check_alive(self):
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                self.dead_balls.append(ball)
                self.balls.pop(i)

        for i, target in enumerate(self.targets):
            if target.life == 0:
                self.targets.pop(i)
            for ball in self.balls:
                if target.is_hit(ball):
                    target.life -= 1

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.gun.fire()
                    ball = Ball(screen=self.screen, FPS=self.FPS, coord=self.gun.coord, vel=self.gun.fired_vel)
                    self.balls.append(ball)
            self.gun.move(event)
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
        if len(self.targets) == 0:
            self.round_done = True

    def round(self):
        self.round_done = False
        self.balls = []
        self.dead_balls = []
        self.init_targets()
        while not self.round_done:
            self.draw()
            self.move()
            self.gun.power_up()
            self.check_alive()
            self.handle_events(events=pg.event.get())
            self.clock.tick(self.FPS)
            pg.display.flip()

    def run(self):
        pg.event.clear()
        self.round()
        self.end_round_card()
        self.targets = []
        self.clock.tick(0.5)
        self.run()


mainmenu = MainMenu()
mainmenu.run()
