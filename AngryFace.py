import pygame
import sys
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 800))

circle(screen, (205, 205, 0, 255), (400, 400), 250, 0)  # The Face
polygon(screen, (0, 0, 0), [(300, 560), (300, 600), (500, 560), (500, 600)], 0)  # The Bow-tie
polygon(screen, (0, 0, 0), [(270, 530), (270, 510), (530, 510), (530, 530)], 0)  # The Mouth
circle(screen, (139, 0, 0), (270, 350), 50, 0)  # Left Eye ball
circle(screen, (139, 0, 0), (530, 350), 35, 0)  # Right Eye ball
circle(screen, (0, 0, 0), (270, 350), 15, 0)  # Left iris
circle(screen, (0, 0, 0), (530, 350), 15, 0)  # Right iris
polygon(screen, (0, 0, 0), [(240, 240), (240, 200), (330, 340), (330, 380)], 0)  # Left eyebrow
polygon(screen, (0, 0, 0), [(560, 240), (560, 200), (470, 350), (470, 390)], 0)  # Right eyebrow

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
sys.exit()

