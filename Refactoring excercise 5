import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((750, 1060))

colour_dict = {
    'BLACK': (0, 0, 0),
    'ORANGE': (200, 113, 55),
    'LIGHT_BLUE': (135, 205, 222),
    'EVEN_LIGHTER_BLUE': (213, 255, 230),
    'GREY': (153, 153, 153),
    'LIGHTER_ORANGE': (222, 170, 135),
    'MUDDISH_GREEN': (128, 102, 0),
    'DARKER_MUDDISH_GREEN': (85, 68, 0),
    'LIGHTER_MUDDISH_GREEN': (141, 124, 56),
    'TOXIC_GREEN': (136, 170, 0),
    'ORANGISH_WHITE': (255, 204, 170),
}


def draw_background():
    """
    Функция рисует фон.
    """
    background = pygame.Surface((750, 1060))
    rect(background, colour_dict['DARKER_MUDDISH_GREEN'], (0, 0, 750, 479))  # Раскрашивает верхнюю полуплоскость
    rect(background, colour_dict['LIGHTER_MUDDISH_GREEN'], (0, 479, 750, 2))  # Рисует границу между полуплоскостями
    rect(background, colour_dict['MUDDISH_GREEN'], (0, 481, 750, 580))  # Раскрашивает нижнюю полуплоскость
    rect(background, colour_dict['BLACK'], (0, 0, 750, 1060), 3)  # Верхняя граница

    screen.blit(background, (0, 0))


def draw_window():
    """
    Функция рисует окно.
    """
    rect(screen, colour_dict['EVEN_LIGHTER_BLUE'], (410, 30, 330, 430))  # Стекло

    rect(screen, colour_dict['LIGHT_BLUE'], (429, 45, 134, 110))
    rect(screen, colour_dict['LIGHT_BLUE'], (588, 45, 134, 110))
    rect(screen, colour_dict['LIGHT_BLUE'], (429, 170, 134, 275))
    rect(screen, colour_dict['LIGHT_BLUE'], (588, 170, 134, 275))
    # Рама


def draw_tail(x, y):
    """
    Функция рисует хвост
    :param x: положение
    :param y: положение
    """

    serf1 = pygame.Surface((750, 1060), pygame.SRCALPHA)
    ellipse(serf1, colour_dict['ORANGE'], (120 - 120, 610 - 610, 350, 100))
    ellipse(serf1, colour_dict['BLACK'], (120 - 120, 610 - 610, 350, 100), 3)  # Граница хвоста
    serf1 = pygame.transform.rotate(serf1, -30)  # Вращение дополнительной поверхности с хвостом
    screen.blit(serf1, (x - 120, y - 80))


def draw_front_paw_right(x, y):
    """
    Фнкция рисует правую лапку
    :param x: положение
    :param y: положение
    """

    serf2 = pygame.Surface((750, 1060), pygame.SRCALPHA)  # Создание дополнительной поверхности для правой передней лапы
    ellipse(serf2, colour_dict['BLACK'], (120 - 2, 698, 124, 69))
    ellipse(serf2, colour_dict['ORANGE'], (120, 700, 120, 65))  # Прорисовка правой передней лапы
    serf2 = pygame.transform.rotate(serf2, -65)  # Вращение дополнительной поверхности с правой передней лапой
    screen.blit(serf2, (x - 410, y - 410))


def draw_head(x, y, k):
    """
    Функция, рисующая голову.

    x, y - определяют положение
    k - определяет размер
    """
    ellipse(screen, colour_dict['BLACK'],
            (int(x - k * 102), int(y - k * 92), int(k * 204), int(k * 184)))
    ellipse(screen, colour_dict['ORANGE'],
            (int(x - k * 100), int(y - k * 90), int(k * 200), int(k * 180)))  # Раскрашивает голову


def draw_body(x, y, k):
    """
    Функция, рисующая тело.

    x, y - определяют положение
    k - определяет размер
    """
    ellipse(screen, colour_dict['BLACK'],
            (int(x + k * 13), int(y - k * 107), int(k * 444), int(k * 249)))
    ellipse(screen, colour_dict['ORANGE'],
            (int(x + k * 15), int(y - k * 105), int(k * 440), int(k * 245)))  # Раскрашивает тела


def draw_front_paw_left(x, y, k):
    """
    Функция, рисующая перёднюю лапу.

    x, y - определяют положение
    k - определяет размер
    """
    ellipse(screen, colour_dict['BLACK'], (int(x + k * 3), int(y + k * 88), int(k * 124), int(k * 69)))
    # ободок передней лапы
    ellipse(screen, colour_dict['ORANGE'], (int(x + k * 5), int(y + k * 90), int(k * 120), int(k * 65)))
    # раскрашивает передню лапу


def draw_back_paw(x, y, k):
    """
    Функция, рисующая заднюю лапу.

    x, y - определяют положение
    k - определяет размеры
    """
    circle(screen, colour_dict['BLACK'], (int(x + k * 390), int(y + k * 90)), int(k * 80))  # ободок круга задней лапы
    circle(screen, colour_dict['ORANGE'], (int(x + k * 390), int(y + k * 90)),
           int(k * 78))  # раскраска круга задней лапы

    ellipse(screen, colour_dict['BLACK'], (int(x + k * 438), int(y + k * 103), int(k * 59), int(k * 129)))
    # ободок эллипса задней лапы
    ellipse(screen, colour_dict['ORANGE'], (int(x + k * 440), int(y + k * 105), int(k * 55), int(k * 125)))
    # раскраска эллипса задней лапы


def draw_eyes(x, y, k):
    """
    Функция, рисующая глаза.

    x, y - определяют положение
    k - определеяет размеры
    """
    circle(screen, colour_dict['TOXIC_GREEN'], (int(x - k * 40), int(y + k * 10)), int(k * 30))  # Левый глаз
    ellipse(screen, colour_dict['BLACK'], (int(x - k * 30), int(y - k * 17), int(k * 8), int(k * 53)))  # Левый зрачок
    circle(screen, colour_dict['BLACK'], (int(x - k * 40), int(y + k * 10)), int(k * 31), 1)  # Центр левого зрачка

    circle(screen, colour_dict['TOXIC_GREEN'], (int(x + k * 50), int(y + k * 10)), int(k * 30))  # Правый глаз
    ellipse(screen, colour_dict['BLACK'], (int(x + k * 60), int(y - k * 17), int(k * 8), int(k * 53)))  # Правый зрачок
    circle(screen, colour_dict['BLACK'], (int(x + k * 50), int(y + k * 10)), int(k * 31), 1)  # Центр правого зрачка


def draw_mouth(x, y, k):
    """
    Функция, рисующая рот и нос.

    x, y - определяют положение
    k - определяет размеры
    """
    polygon(screen, colour_dict['BLACK'], [[int(x - k * 8), int(y + k * 41)], [int(x + k * 14), int(y + k * 41)],
                                           [int(x + k * 3), int(y + k * 54)]])
    polygon(screen, colour_dict['ORANGISH_WHITE'],
            [[int(x - k * 6), int(y + k * 43)], [int(x + k * 12), int(y + k * 43)],
             [int(x + k * 3), int(y + k * 52)]])  # Закрашивает нос
    line(screen, colour_dict['BLACK'], (int(x + k * 3), int(y + k * 54)), (int(x + k * 3), int(y + k * 75)), 2)
    line(screen, colour_dict['BLACK'], (int(x - k * 10), int(y + k * 75)), (int(x + k * 16), int(y + k * 75)), 2)

    line(screen, colour_dict['BLACK'], (int(x - k * 20), int(y + k * 70)), (int(x - k * 120), int(y + k * 50)), 1)
    line(screen, colour_dict['BLACK'], (int(x - k * 20), int(y + k * 65)), (int(x - k * 120), int(y + k * 45)), 1)
    line(screen, colour_dict['BLACK'], (int(x - k * 20), int(y + k * 60)), (int(x - k * 120), int(y + k * 40)), 1)
    # Правые усы
    line(screen, colour_dict['BLACK'], (int(x + k * 26), int(y + k * 70)), (int(x + k * 126), int(y + k * 50)), 1)
    line(screen, colour_dict['BLACK'], (int(x + k * 26), int(y + k * 65)), (int(x + k * 126), int(y + k * 45)), 1)
    line(screen, colour_dict['BLACK'], (int(x + k * 26), int(y + k * 60)), (int(x + k * 126), int(y + k * 40)), 1)
    # Левые усы


def draw_ears(x, y, k):
    """
    Функция, рисующая уши.

    x, y - определяют положение
    k - определяет размер
    """
    polygon(screen, colour_dict['ORANGE'], [[int(x + k * 42), int(y - k * 71)], [int(x + k * 92), int(y - k * 101)],
                                            [int(x + k * 82), int(y - k * 33)]])
    polygon(screen, colour_dict['ORANGE'], [[int(x - k * 105), int(y - k * 95)], [int(x - k * 52), int(y - k * 68)],
                                            [int(x - k * 89), int(y - k * 28)]])
    # Закрашивает внешнюю часть ушей
    polygon(screen, colour_dict['LIGHTER_ORANGE'],
            [[int(x - k * 96), int(y - k * 82)], [int(x - k * 60), int(y - k * 67)],
             [int(x - k * 86), int(y - k * 40)]])
    polygon(screen, colour_dict['LIGHTER_ORANGE'],
            [[int(x + k * 51), int(y - k * 71)], [int(x + k * 84), int(y - k * 91)],
             [int(x + k * 78), int(y - k * 47)]])
    # Закрашивает внутрюннюю часть уха
    polygon(screen, colour_dict['BLACK'], [[int(x - k * 105), int(y - k * 95)], [int(x - k * 52), int(y - k * 68)],
                                           [int(x - k * 89), int(y - k * 28)]], 2)
    polygon(screen, colour_dict['BLACK'], [[int(x + k * 42), int(y - k * 71)], [int(x + k * 92), int(y - k * 101)],
                                           [int(x + k * 82), int(y - k * 33)]], 2)
    # Ободок внешней части ушей
    polygon(screen, colour_dict['BLACK'], [[int(x - k * 96), int(y - k * 82)], [int(x - k * 60), int(y - k * 67)],
                                           [int(x - k * 86), int(y - k * 40)]], 2)
    polygon(screen, colour_dict['BLACK'], [[int(x + k * 51), int(y - k * 71)], [int(x + k * 84), int(y - k * 91)],
                                           [int(x + k * 78), int(y - k * 47)]], 2)
    # Ободок внутренней части ушей


def draw_cat(x, y, k):
    """
    Функция, рисующая кота.

    Рисующие функции расположены послойно.
    Пример: правая передняя лапа рисуется под головой ->
    функция, рисующая лапу расположена раньше.

    x, y - координаты центра головы кота.
    """

    draw_front_paw_right(x, y)
    draw_body(x, y, k)
    draw_head(x, y, k)
    draw_tail(x, y)
    draw_back_paw(x, y, k)
    draw_front_paw_left(x, y, k)
    draw_eyes(x, y, k)
    draw_mouth(x, y, k)
    draw_ears(x, y, k)


def draw_ball_of_strings(x, y):
    """
    Функция рисует клубок ниток

    x, y - положение центра клубка
    """
    circle(screen, colour_dict['BLACK'], (x, y), 87)
    circle(screen, colour_dict['GREY'], (x, y), 85)
    # Закрашивает клубок
    arc(screen, colour_dict['BLACK'], (x - 50, y - 50, 100, 100), 0, 1.8, 3)
    arc(screen, colour_dict['BLACK'], (x - 50, y - 50, 90, 90), 2.2, 3, 3)
    arc(screen, colour_dict['BLACK'], (x - 70, y - 70, 120, 120), 1.2, 2.6, 3)
    arc(screen, colour_dict['BLACK'], (x - 70, y - 50, 150, 120), 3, 0.3, 3)
    aalines(screen, colour_dict['BLACK'], False,
            [[x - 85, y], [x - 95, y + 30], [x - 155, y - 15], [x - 195, y + 20],
             [x - 255, y - 30], [x - 275, y + 40], [x - 295, y + 5]])
    # Выбившаяся нить


x_cat_pos = 120
y_cat_pos = 610
scale = 1  # Не менять! (draw_tail, и draw_front_paw_right не имеют возможности менять размер)

x_ball_pos = 455
y_ball_pos = 930

draw_background()
draw_window()
draw_cat(x_cat_pos, y_cat_pos, scale)
draw_ball_of_strings(x_ball_pos, y_ball_pos)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
