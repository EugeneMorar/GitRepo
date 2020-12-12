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


class InputBox:
    """
    Class creating a name writing box.
    """

    def __init__(self, screen, x=0, y=0, w=0, h=0, text=''):
        self.screen = screen
        self.name_recorded = False
        self.name = ''
        self.username = ''
        self.text = text
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 255, 255)  # The non-active color
        self.font = pg.font.SysFont('arial', 65)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        The thing that handles the events like writing and deactivating the inputbox.
        :param event:
        :return:
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (255, 100, 100) if self.active else (255, 255, 255)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.name = self.text
                    self.name_recorded = True
                    self.text = ''
                    self.active = False
                    self.color = (255, 255, 255)
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        """
        A procedure to update the size of the InputBox.
        :return: None
        """
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        """
        A procedure to display the text on the screen.
        :object screen: pygame.Surface
        :return: None
        """
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(self.screen, self.color, self.rect, 2)

    def run(self, event):
        self.draw()
        self.handle_event(event)
        # Checks for the end of writing
        if self.name_recorded:
            self.username = self.name
        self.update()


class MainMenu:
    """
    Класс главного меню, из него вызывается игра.
    """

    def __init__(self):
        self.screen = pg.display.set_mode(SCREEN_SIZE)

        self.username = ''

        self.score = 0

        self.manager = Manager(self.screen)

        self.input_name = InputBox(self.screen,
                                   self.screen.get_width() // 2 - 500 // 2,
                                   self.screen.get_height() * 38 // 48,
                                   500, 70)

        self.font = pg.font.SysFont('ariel', 100)

        self.margin = 20

    def button_with_text(self, text, x, y, event=None):
        """
        Метод для упрощения создания кнопок
        Рисует и возвращает булеан при нажатии
        return: bool
        """
        text = self.font.render(text, True, (219, 100, 0))
        text_rect = pg.Rect((x - text.get_width() // 2 - self.margin,
                             y - text.get_height() // 2 - self.margin),
                            (text.get_width() + 2 * self.margin,
                             text.get_height() + 2 * self.margin))
        self.screen.blit(text, (x - text.get_width() // 2,
                                y - text.get_height() // 2))
        if event is not None:
            if event.type == pg.MOUSEBUTTONDOWN and text_rect.collidepoint(event.pos):
                return True

    def draw(self):
        self.screen.fill((22, 105, 122))
        self.button_with_text('Выход', self.screen.get_width() // 2, self.screen.get_height() * 15 / 24)
        self.button_with_text('Таблица лидеров', self.screen.get_width() // 2, self.screen.get_height() * 11 / 24)
        self.button_with_text('Начать', self.screen.get_width() // 2, self.screen.get_height() * 7 / 24)

    def run(self):
        while True:
            self.draw()
            self.input_name.draw()

            if self.input_name.name_recorded:
                self.username = self.input_name.username

            for event in pg.event.get():
                if self.button_with_text('Начать',
                                         self.screen.get_width() // 2, self.screen.get_height() * 7 / 24, event) and \
                        self.username != '':
                    self.manager.clock.tick(1)
                    self.score = self.manager.run()
                if self.button_with_text('Таблица лидеров',
                                         self.screen.get_width() // 2, self.screen.get_height() * 11 / 24, event):
                    LeaderBoard(self.screen).run(self.username, self.score)
                if self.button_with_text('Выход',
                                         self.screen.get_width() // 2, self.screen.get_height() * 15 / 24, event):
                    pg.quit()
                    sys.exit()
                self.input_name.run(event)

            pg.display.flip()


class LeaderBoard:
    """
    Класс таблицы очков
    """

    def __init__(self, screen):
        self.screen = screen
        self.alive = True
        self.score_display: pg.Surface
        self.font = pg.font.SysFont('ariel', 100)
        self.score_list = []

    def load_scores(self):
        """
        Переписывает все строчки из Leaderboard.yaml в self.score_list
        return: None
        """
        try:
            with open('Leaderboard', 'r') as f:
                self.score_list.extend(yaml.load(f, Loader=yaml.FullLoader))
        except FileNotFoundError:
            pass

    def update_scores(self, username='', score=0):
        """
        Сортирует список очков, добавляет новый элемент (username, score) и обновляет Leaderboard.yaml
        return: None
        """
        if username != '' and score != 0:
            self.score_list.append((str(username), score))
        for p in range(2):
            for i in range(len(self.score_list)):
                for k in range(len(self.score_list)):
                    try:
                        if k != i and self.score_list[i][0] == self.score_list[k][0]:
                            self.score_list[i] = self.score_list[i][0], max(self.score_list[i][1],
                                                                            self.score_list[k][1])
                            self.score_list.pop(k)
                    except IndexError:
                        pass
        self.score_list.sort(key=lambda tup: tup[1], reverse=True)
        while len(self.score_list) > 11:
            self.score_list.pop(11)
        with open('Leaderboard', 'w') as f:
            yaml.dump(self.score_list, f)

    def display_scores(self):
        """
        Отрисовывает таблицу очков
        return: None
        """
        self.screen.fill((0, 0, 0))
        for i, (key, value) in enumerate(self.score_list):
            score_display = self.font.render(str(i + 1) + '. ' + key + ' ' + str(value), True, (171, 215, 235))
            self.screen.blit(score_display, (self.screen.get_width() // 12,
                                             i * score_display.get_height() + i * 10 + 20))
        pg.display.flip()

    def run(self, username, score):
        """
        Главный цикл класса
        return: None
        """
        self.load_scores()
        self.update_scores(username, score)
        self.display_scores()
        while self.alive:
            for event in pg.event.get():
                if mainmenu.button_with_text('Выход', self.screen.get_width() * 10 // 12,
                                             self.screen.get_height() // 2, event):
                    self.alive = False
                pg.display.flip()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


class Ball(pg.sprite.Sprite):
    """
    Класс снаряда которыми стреляет пушка
    """

    def __init__(self, screen, FPS, coord=[0, 0], vel=[0, 0], color=None, coef=1.):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resources/Ball.png").convert()

        self.image = pg.transform.scale(self.image, (int(self.image.get_width() * coef),
                                                     int(self.image.get_height() * coef)))

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
        """
        Отрисовка объекта класса
        return: None
        """
        self.screen.blit(self.image, (self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h // 2))

    def move(self, t_step=1., g=5.):
        """
        Метод обрабатывающий движение объекта
        return: None
        """
        t_step /= self.FPS // 30
        self.vel[1] += int(g * t_step)

        #  Обновляет координаты объекта
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)

        #  Проверяет, что снаряд ушёл за границу экрана
        if self.coord[1] > self.screen.get_height() or \
                self.coord[0] > self.screen.get_width() * 25 / 24 or \
                self.coord[0] < -1 * self.screen.get_width() * 1 / 24:
            self.is_alive = False

        #  Перемещает Rect объекта за объектом
        self.rect = pg.Rect(self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h // 2,
                            self.rect.w, self.rect.h)


class Gun(pg.sprite.Sprite):
    def __init__(self, screen, area, coord=[30, SCREEN_SIZE[1] * 5 // 6],
                 min_pow=10, max_pow=80, FPS=30):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resources/TankFrame_right.png").convert()

        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.area = area

        self.screen = screen

        self.FPS = FPS

        self.coord = coord.copy()

        self.angle = 0

        self.life = 5

        self.min_pow = min_pow

        self.max_pow = max_pow

        self.power = self.min_pow

        self.vel = int(100 * 30 // self.FPS)

        self.active = False

        self.fired_vel = [0, 0]

        self.step = 30

    def draw(self):
        """
        Отрисовывает пушку
        return: None
        """
        self.screen.blit(self.image, (self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h // 2))

    def power_up(self):
        """
        Обрабатывает заряд пушки
        return: None
        """
        if self.active and self.power < self.max_pow:
            self.power += 1

    def fire(self):
        """
        Подсчитывает скорость вылетевшего снаряда
        return: None
        """
        self.fired_vel = [int(self.power * np.cos(self.angle)),
                          int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow

    def move_up(self):
        if self.coord[1] < self.area.y + 2 * self.step:
            self.coord[1] = self.area.y + 2 * self.step
        self.coord[1] -= self.step

    def move_down(self):
        if self.coord[1] > self.area.y + self.area.h - 2 * self.step:
            self.coord[1] = self.area.y + self.area.h - 2 * self.step
        self.coord[1] += self.step

    def move_right(self):
        if self.coord[0] > self.area.x + self.area.w - 2 * self.step:
            self.coord[0] = self.area.x + self.area.w - 2 * self.step
        self.coord[0] += self.step

        self.image = pg.image.load("Resources/TankFrame_right.png").convert()
        self.image.set_colorkey((0, 0, 0))

    def move_left(self):
        if self.coord[0] < self.area.x + 2 * self.step:
            self.coord[0] = self.area.x + 2 * self.step
        self.coord[0] -= self.step

        self.image = pg.image.load("Resources/TankFrame_left.png").convert()
        self.image.set_colorkey((0, 0, 0))

    def set_angle(self, mouse_pos):
        """
        Обновляет угол, под которым производится выстрел
        return: None
        """
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])

    def move(self, event):
        """
        Обрабатывает движение пушки
        return: None
        """
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

        #  Перемещает Rect пушки
        self.rect = pg.Rect(self.coord[0], self.coord[1], self.rect.w, self.rect.h)


class Target(pg.sprite.Sprite):
    """
    Класс целей
    """

    def __init__(self, screen, clock, area, FPS, coord=[0, 0]):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Resources/Aerial_Target.png").convert()
        self.area = area  # area - Rect, в котором допустимо движение цели
        self.screen = screen
        self.FPS = FPS
        self.clock = clock
        self.life = 5
        self.coord = coord.copy()
        self.start_coord = coord.copy()
        self.vel = [0, 0]
        self.time_alive = randint(0, 100)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        self.vel[0] = randint(3, 8)

        # Амплитуда движения цели по оси y
        self.amp = min(abs(self.coord[1] - self.area.h), abs(self.coord[1] - self.area.y)) // 2

        # Величина обратно пропорциональная частоте колебаний
        self.curve = randint(35, 50)

    def draw(self):
        self.screen.blit(self.image, (self.coord[0] - self.rect.w // 2, self.coord[1] - self.rect.h // 2))

    def pattern(self):
        """
        Подсчёт y координаты объекта
        """
        self.coord[1] = self.start_coord[1] + self.amp * np.sin(self.coord[0] / self.curve)

    def move(self):
        self.coord[0] += self.vel[0]
        self.pattern()

        # Обновляет положение Rect объекта
        self.rect = pg.Rect(self.coord[0] - self.rect.w // 2,
                            self.coord[1] - self.rect.h // 2,
                            self.rect.w, self.rect.h)

        # Проверяет границы экрана, обращает скорости целей при столкновении с ним
        if self.coord[0] > self.screen.get_width() * 27 / 24:
            self.vel[0] = -1 * self.vel[0]
        if self.coord[0] < -1 * self.screen.get_width() * 3 / 24:
            self.vel[0] = -1 * self.vel[0]

        self.time_alive += 1

    def is_hit(self, obj):
        """
        Попадание шарика в цель.
        return: bool
        """
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False

    def shell_out(self):
        """
        Возвращает снаряд цели на её координате каждые 2 секунды
        return: bool
        """
        if self.time_alive % (self.FPS * 2) == 0:
            return Shell(self.screen, self.FPS, self.coord)
        else:
            return None


class Plane(Target):
    def __init__(self, screen, clock, area, FPS, coord=[0, 0]):
        super(Plane, self).__init__(screen, clock, area, FPS, coord)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Resources/Plane_right.png").convert()
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() * 3),
                                                     int(self.image.get_height() * 3)))
        self.image.set_colorkey((0, 0, 0))
        self.vel[0] = 3 * self.vel[0]
        self.life = 1
        self.coord[0] = 0

    def pattern(self):
        self.coord[1] = self.start_coord[1]

    def move(self):
        self.coord[0] += self.vel[0]
        self.pattern()

        # Обновляет положение Rect объекта
        self.rect = pg.Rect(self.coord[0] - self.rect.w // 2,
                            self.coord[1] - self.rect.h // 2,
                            self.rect.w, self.rect.h)

        # Проверяет на столкновение с границами экрана
        if self.coord[0] > self.screen.get_width() or \
                self.coord[0] < 0:
            self.life = 0

        self.time_alive += 1

    def shell_out(self):
        """
        Возвращает снаряд цели на её координате каждые 2 секунды
        return: bool
        """
        if self.time_alive % (self.FPS // 10) == 0 and self.coord[0] < self.screen.get_width() * 2 // 3:
            return Shell(self.screen, self.FPS, self.coord)
        else:
            return None


class Shell(Ball):
    """
    Класс снаряда цели
    """

    def __init__(self, screen, FPS, coord=[0, 0], vel=[0, 0]):
        super(Shell, self).__init__(screen, FPS)
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resources/Projectile.png").convert()

        self.image.set_colorkey((0, 0, 0))

        self.screen = screen

        self.FPS = FPS

        self.coord = coord.copy()

        self.vel = vel.copy()

        self.rect = self.image.get_rect()

        self.alive = True

    def has_hit(self, obj):
        """
        Попадание shell в gun.
        """
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False


class Manager:
    """
    Класс игры
    """

    def __init__(self, screen):

        self.clock = pg.time.Clock()

        self.round_done = False

        self.game_over = False

        self.round_number = 1

        self.round_time = 0

        self.score = 0

        self.FPS = 60

        self.screen = screen

        self.ground = pg.Rect((0, self.screen.get_height() * 2 // 3),
                              (self.screen.get_width(), self.screen.get_height() // 3))
        self.sky = pg.Rect((0, 0), (self.screen.get_width(), self.screen.get_height() * 2 // 3))

        self.gun = Gun(screen=self.screen, FPS=self.FPS, area=self.ground)

        self.text = ''
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.health = self.font.render('', True, (0, 0, 0))
        self.bomber_text = self.font.render('INCOMING',
                                            True, BLACK)

        self.balls = []
        self.dead_balls = []
        self.targets = []
        self.shells_in_flight = []

    def init_targets(self):
        """
        Инициирует цели на координаете coord
        """
        for i in range(self.round_number):
            self.targets.append(Target(screen=self.screen,
                                       clock=self.clock,
                                       coord=[randint(0, self.sky.w),
                                              randint(0, self.sky.h // 2)],
                                       FPS=self.FPS,
                                       area=self.sky))

    def end_round_card(self):
        """
        Экран, появляющийся в конце каждого раунда
        """
        self.screen.fill(BLACK)
        self.dead_balls.extend(self.balls)
        if self.gun.life != 0:
            self.text = self.font.render('Вы уничтожили цели за ' + str(len(self.dead_balls)) +
                                         ' выстрелов', True, WHITE)
            self.screen.blit(self.text, (self.screen.get_width() // 2 - self.text.get_width() // 2,
                                         self.screen.get_height() // 2 - self.text.get_height() // 2))
            self.text = self.font.render('Ваше здоровье: ' + str(self.gun.life),
                                         True, WHITE)
            self.screen.blit(self.text, (self.screen.get_width() // 2 - self.text.get_width() // 2,
                                         self.screen.get_height() * 2 // 3 - self.text.get_height() // 2))
        else:
            self.text = self.font.render('GAME OVER', True, WHITE)
            self.screen.blit(self.text, (self.screen.get_width() // 2 - self.text.get_width() // 2,
                                         self.screen.get_height() // 2 - self.text.get_height() // 2))
        pg.display.flip()

    def draw(self):
        # Отрисовка фона
        pg.draw.rect(self.screen, (126, 200, 80), self.ground)
        pg.draw.rect(self.screen, (209, 237, 242), self.sky)

        # Отрисовка хп
        self.screen.blit(self.health, (0, 0))

        # Отрисовка предупреждения
        if (self.round_time / self.FPS + 1) % (self.round_number * 10) > 7:
            pg.draw.rect(self.screen, (255, 100, 100),
                         pg.Rect((self.screen.get_width() - self.bomber_text.get_width() - 5,
                                  self.screen.get_height() // 40),
                                 (self.bomber_text.get_width(),
                                  self.bomber_text.get_height())))
            self.screen.blit(self.bomber_text, (self.screen.get_width() - self.bomber_text.get_width() - 5,
                                                self.screen.get_height() // 40))

        # Отрисовка снарядов пушки
        for ball in self.balls:
            ball.draw()

        # Отрисовка пушки
        self.gun.draw()

        # Отрисовка целей
        for target in self.targets:
            target.draw()

        # Отрисовка снарядов целей
        for shell in self.shells_in_flight:
            shell.draw()

    def move(self):
        for ball in self.balls:
            ball.move()
        for target in self.targets:
            target.move()
        for shell in self.shells_in_flight:
            shell.move()

    def check_alive(self):
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                self.dead_balls.append(ball)
                self.balls.pop(i)

        for i, target in enumerate(self.targets):
            if target.life <= 0:
                self.targets.pop(i)
                self.score += 1
            for ball in self.balls:
                if target.is_hit(ball):
                    target.life -= ball.rect.w // 24  # Урон цели зависит от размера снаряда пушки
                    ball.is_alive = False

        for i, shell in enumerate(self.shells_in_flight):
            if shell.has_hit(self.gun):
                self.gun.life -= 1  # Количество хп, снимаемое при попадании снаряда цели - 1
                shell.alive = False
            if not shell.alive:
                self.shells_in_flight.pop(i)

        if self.gun.life <= 0:
            self.round_done = True
            self.game_over = True

        if (self.round_time / self.FPS + 1) % (self.round_number * 10) == 0:
            self.targets.append((Plane(screen=self.screen,
                                       clock=self.clock,
                                       coord=[0, self.sky.h // 4],
                                       FPS=self.FPS,
                                       area=self.sky)))

    def targets_attack(self):
        """
        Инициирует снаряды целей
        """
        for target in self.targets:
            if target.shell_out() is not None:
                self.shells_in_flight.append(target.shell_out())

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    self.gun.active = True

            # Инициирует снаряд пушки по нажатию лкм или пкм
            if event.type == pg.MOUSEBUTTONUP:
                self.gun.fire()
                if event.button == 1:
                    ball = Ball(screen=self.screen, FPS=self.FPS,
                                coord=self.gun.coord, vel=self.gun.fired_vel)
                    self.balls.append(ball)
                elif event.button == 3:
                    self.gun.fired_vel = [self.gun.fired_vel[0] * 2, self.gun.fired_vel[1] * 2]
                    ball = Ball(screen=self.screen, FPS=self.FPS,
                                coord=self.gun.coord, vel=self.gun.fired_vel,
                                coef=0.3)
                    self.balls.append(ball)

            self.gun.move(event)

            # Преобразование здоровья целей и пушки в pygame.Surface
            health_text = 'Здоровье пушки: ' + str(self.gun.life)
            self.health = self.font.render(health_text, True, (255, 0, 0))

        # Смена угла выстрела пушки
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        # Заканчивает раунд при отсутствии целей
        if len(self.targets) == 0:
            self.round_done = True

    def round(self):
        self.round_done = False
        self.round_time = 0
        self.balls = []
        self.dead_balls = []
        self.init_targets()
        while not self.round_done:
            self.draw()
            self.move()
            self.gun.power_up()
            self.targets_attack()
            self.check_alive()
            self.handle_events(events=pg.event.get())
            self.clock.tick(self.FPS)
            self.round_time += 1
            pg.display.flip()
        self.round_number += 1

    def run(self):
        pg.event.clear()
        self.round()
        self.end_round_card()
        self.targets = []
        self.gun.life = 5
        self.clock.tick(0.5)
        if not self.game_over:
            self.run()
        else:
            return self.score


mainmenu = MainMenu()
mainmenu.run()
