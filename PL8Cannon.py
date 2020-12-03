import pygame as pg
import sys
import numpy as np
from random import randint

SCREEN_SIZE = (800, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pg.init()
pg.font.init()


class Ball:
    def __init__(self, screen, coord=[0, 0], vel=[0, 0], r=15, color=None):
        self.screen = screen
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord.copy()
        self.vel = vel.copy()
        self.r = r
        self.is_alive = True

    def draw(self):
        pg.draw.circle(self.screen, self.color, self.coord, self.r)

    def move(self, t_step=1., g=2.):
        self.vel[1] += int(g * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 1 and self.coord[1] >= self.screen.get_height() - self.r:
            self.is_alive = False

    def check_walls(self):
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.r:
                self.coord[i] = self.r
                self.flip_vel(n[i], 0.8, 0.9)
            elif self.coord[i] > SCREEN_SIZE[i] - self.r:
                self.coord[i] = SCREEN_SIZE[i] - self.r
                self.flip_vel(n[i], 0.8, 0.9)

    def flip_vel(self, axis, coef_norm=1.0, coef_par=1.0):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_norm = vel.dot(n) * n
        vel_par = vel - vel_norm
        ans = -vel_norm * coef_norm + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()


class Table:
    pass


class Gun:
    def __init__(self, screen, coord=[30, SCREEN_SIZE[1] // 2],
                 min_pow=20, max_pow=50):
        self.screen = screen

        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = self.min_pow
        self.vel = 100
        self.active = False
        self.fired_vel = [0, 0]

        self.step = 5

    def draw(self):
        end_pos = (self.coord[0] + int(self.power * np.cos(self.angle)),
                   self.coord[1] + int(self.power * np.sin(self.angle)))
        pg.draw.line(self.screen, RED, self.coord, end_pos, 5)

    def power_up(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def fire(self):
        self.fired_vel = [int(self.power * np.cos(self.angle)), int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow

    def move_up(self):
        self.coord[1] -= self.step

    def move_down(self):
        self.coord[1] += self.step

    def move_right(self):
        self.coord[0] += self.step

    def move_left(self):
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


class Target:
    def __init__(self, screen, coord=[0, 0]):
        self.screen = screen
        self.points = 0
        self.is_alive = 1
        self.coord = coord
        self.r = randint(10, 30)
        self.color = RED

    def draw(self):
        pg.draw.circle(self.screen, self.color, self.coord, self.r)

    def is_hit(self, obj, points=1):
        """
        Попадание шарика в цель.
        """
        if (self.coord[0] - obj.coord[0]) ** 2 + (self.coord[1] - obj.coord[1]) ** 2 <= (obj.r + self.r) ** 2:
            self.points += points
            return True
        else:
            return False


class Manager:
    def __init__(self):
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.text = ''
        self.clock = pg.time.Clock()
        self.round_done = False

        self.FPS = 30
        self.number_of_targets = 1
        self.gun = Gun(screen=self.screen)
        self.table = Table()
        self.balls = []
        self.dead_balls = []
        self.targets = []

    def init_targets(self):
        for i in range(self.number_of_targets):
            self.targets.append(Target(screen=self.screen,
                                       coord=[randint(self.screen.get_width() * 9 // 10, self.screen.get_width()),
                                              randint(0, self.screen.get_height())]))

    def end_round_card(self):
        self.screen.fill(BLACK)
        self.dead_balls.extend(self.balls)
        self.text = self.font.render('Вы уничтожили цель за ' + str(len(self.dead_balls)) +
                                     ' выстрелов', True, WHITE)
        self.screen.blit(self.text, (self.screen.get_width() // 2 - self.text.get_width() // 2,
                                     self.screen.get_height() // 2 - self.text.get_height() // 2))
        pg.display.flip()

    def draw(self):
        self.screen.fill(BLACK)
        for ball in self.balls:
            ball.draw()
        self.gun.draw()
        for target in self.targets:
            target.draw()

    def move(self):
        for ball in self.balls:
            ball.move()

    def check_alive(self):
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                self.dead_balls.append(ball)
                self.balls.pop(i)

        for i, target in enumerate(self.targets):
            if not target.is_alive:
                self.targets.pop(i)
            for ball in self.balls:
                if target.is_hit(ball):
                    target.is_alive = False

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
                    ball = Ball(screen=self.screen, coord=self.gun.coord, vel=self.gun.fired_vel)
                    self.balls.append(ball)
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
        self.round()
        self.end_round_card()
        self.targets = []
        self.clock.tick(0.5)
        self.run()


manager = Manager()

manager.run()
