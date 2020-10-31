import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = (800, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pg.init()
pg.font.init()


class Ball():
    def __init__(self, coord, vel, rad=15, color=None):
        if color == None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1., g=2.):
        self.vel[1] += int(g * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 2 ** 2 and self.coord[1] > SCREEN_SIZE[1] - 2 * self.rad:
            self.is_alive = False

    def check_walls(self):
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i], 0.8, 0.9)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i], 0.8, 0.9)

    def flip_vel(self, axis, coef_norm=1, coef_par=1):
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
    def __init__(self, coord=[30, SCREEN_SIZE[1] // 2],
                 min_pow=20, max_pow=50):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        end_pos = [self.coord[0] + int(self.power * np.cos(self.angle)),
                   self.coord[1] + int(self.power * np.sin(self.angle))]
        pg.draw.line(screen, RED, self.coord, end_pos, 5)

    def strike(self):
        vel = [int(self.power * np.cos(self.angle)), int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coord), vel)

    def move(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])


class Target:
    def __init__(self):
        self.points = 0
        self.is_alive = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 30)
        self.color = RED

    def draw(self):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def is_hit(self, obj, points=1):
        """
        Попадание шарика в цель.
        """
        if (self.x - obj.coord[0]) ** 2 + (self.y - obj.coord[1]) ** 2 <= (2 * self.r) ** 2:
            self.points += points
            return True
        else:
            return False


class Manager:
    def __init__(self):
        self.number_of_targets = 1
        self.gun = Gun()
        self.table = Table()
        self.balls = []
        self.targets = [Target() for i in range(self.number_of_targets)]
        self.dead_balls = []

    def end_round_card(self):
        screen.fill(BLACK)
        text_surface = myfont.render('Вы уничтожили цель за ' + str(len(self.dead_balls)) + ' выстрелов', True, WHITE)
        screen.blit(text_surface, (400, 300))
        pg.display.flip()

    def process(self, events, screen):
        done = self.handle_events(events)
        self.move()
        self.draw(screen)
        self.check_alive()
        return done

    def draw(self, screen):
        screen.fill(BLACK)
        for ball in self.balls:
            ball.draw(screen)
        self.gun.draw(screen)
        for target in self.targets:
            target.draw()

    def move(self):
        for ball in self.balls:
            ball.move()
        self.gun.move()

    def check_alive(self):
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                self.dead_balls.append(i)
                self.balls.pop(i)

        for i, target in enumerate(self.targets):
            if not target.is_alive:
                self.targets.pop(i)
            for ball in self.balls:
                if target.is_hit(ball):
                    target.is_alive = False

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coord[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coord[1] += 5
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        if len(self.targets) == 0:
            done = True
        return done


screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun")
clock = pg.time.Clock()
myfont = pg.font.SysFont('Comic Sans MS', 30)

def round():
    mgr = Manager()
    done = False
    while not done:
        done = mgr.process(pg.event.get(), screen)
        pg.display.flip()
        clock.tick(15)
    mgr.end_round_card()
    clock.tick(0.2)
    round()

round()
