import numpy as np
import pygame as pg
from pygame.draw import *

pg.init()

FPS = 30
screen = pg.display.set_mode((800, 600))

screen.fill((255, 175, 128))


def log(x, y, k):
    surface_log = pg.Surface((800, 600))

    surface_log.set_colorkey((0, 0, 0))

    rect(screen, (0, 200, 64), (x, y, 16 * k, 50 * k))
    rect(surface_log, (0, 200, 64), (x, y - 55 * k, 16 * k, 50 * k))
    rect(surface_log, (0, 200, 64), (x + 2 * k, y - 80 * k, 10 * k, 20 * k))
    rect(surface_log, (0, 200, 64), (x + 4 * k, y - 95 * k, 8 * k, 10 * k))

    screen.blit(surface_log, (0, 0))


def leaves(x, y, k):
    surface_leaves_right = pg.Surface((800, 600))
    surface_leaves_left = pg.Surface((800, 600))

    surface_leaves_left.set_colorkey((0, 0, 0))
    surface_leaves_right.set_colorkey((0, 0, 0))

    arc(surface_leaves_right, (0, 200, 64), (x + 20 * k, y - 40 * k, 60 * k, 50 * k), 0, np.pi, 2)
    arc(surface_leaves_right, (0, 200, 64), (x + 20 * k, y - 80 * k, 40 * k, 25 * k), 0, np.pi, 2)

    arc(surface_leaves_left, (0, 200, 64), (x - 65 * k, y - 40 * k, 60 * k, 50 * k), 0, np.pi, 2)
    arc(surface_leaves_left, (0, 200, 64), (x - 45 * k, y - 80 * k, 40 * k, 25 * k), 0, np.pi, 2)

    ellipse(surface_leaves_right, (0, 200, 64), [x + 40 * k, y - 35 * k, 10 * k, 30 * k])
    ellipse(surface_leaves_right, (0, 200, 64), [x + 50 * k, y - 35 * k, 8 * k, 25 * k])
    ellipse(surface_leaves_right, (0, 200, 64), [x + 62 * k, y - 32 * k, 6 * k, 20 * k])
    ellipse(surface_leaves_right, (0, 200, 64), [x + 30 * k, y - 33 * k, 8 * k, 25 * k])

    ellipse(surface_leaves_left, (0, 200, 64), [x - 24 * k, y - 35 * k, 10 * k, 30 * k])
    ellipse(surface_leaves_left, (0, 200, 64), [x - 50 * k, y - 35 * k, 8 * k, 25 * k])
    ellipse(surface_leaves_left, (0, 200, 64), [x - 58 * k, y - 32 * k, 6 * k, 20 * k])
    ellipse(surface_leaves_left, (0, 200, 64), [x - 36 * k, y - 33 * k, 8 * k, 25 * k])

    ellipse(surface_leaves_right, (0, 200, 64), [x + 36 * k, y - 77 * k, 8 * k, 20 * k])
    ellipse(surface_leaves_right, (0, 200, 64), [x + 50 * k, y - 75 * k, 6 * k, 15 * k])
    ellipse(surface_leaves_right, (0, 200, 64), [x + 26 * k, y - 73 * k, 5 * k, 15 * k])

    ellipse(surface_leaves_left, (0, 200, 64), [x - 36 * k, y - 77 * k, 8 * k, 20 * k])
    ellipse(surface_leaves_left, (0, 200, 64), [x - 20 * k, y - 75 * k, 6 * k, 15 * k])
    ellipse(surface_leaves_left, (0, 200, 64), [x - 26 * k, y - 77 * k, 5 * k, 15 * k])

    screen.blit(surface_leaves_left, (0, 0))
    screen.blit(surface_leaves_right, (0, 0))


def panda(x, y, k):
    circle(screen, (0, 0, 0), (x + 24 * k, y - 35 * k), k * 18)
    circle(screen, (0, 0, 0), (x - 28 * k, y - 33 * k), k * 20)

    rect(screen, (0, 0, 0), (x - 14 * k, y, 18 * k, 56 * k))

    ellipse(screen, (255, 255, 255), [x, y, 100 * k, 60 * k])

    rect(screen, (0, 0, 0), (x + 12 * k, y, 18 * k, 70 * k))

    circle(screen, (255, 255, 255), (x, y), k * 43)

    rect(screen, (0, 0, 0), (x - 12 * k, y + 60 * k, 42 * k, 18 * k))

    ellipse(screen, (0, 0, 0), [x + 80 * k, y + 30 * k, 18 * k, 49 * k])

    circle(screen, (0, 0, 0), (x - 34 * k, y + 10 * k), k * 11)
    circle(screen, (0, 0, 0), (x, y + 13 * k), k * 11)
    circle(screen, (0, 0, 0), (x - 20 * k, y + 32 * k), k * 7)


def palm(x, y, k):
    log(x, y, k)

    leaves(x, y, k)


palm(200, 300, 3)
palm(50, 400, 1)
palm(600, 200, 2)

panda(500, 300, 2)
panda(300, 500, 1)

pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

pg.quit()

