import pygame as pg
import numpy as math
from pygame.draw import *
from random import randint
from random import choice

pg.init()
pg.font.init()


class Variables:
    """
    A class of variables needed to start the game.
    """
    def __init__(self):
        self.timer = 0
        self.number_of_stars = 3
        self.number_of_balls = 10

        self.total_gametime = 20  # Time the game goes on for in seconds
        self.FPS = 50

        # The list of colors used
        self.RED = (255, 0, 0, 255)
        self.BLUE = (0, 0, 255, 255)
        self.YELLOW = (255, 255, 0, 255)
        self.GREEN = (0, 255, 0, 255)
        self.MAGENTA = (255, 0, 255, 255)
        self.CYAN = (0, 255, 255, 255)
        self.BLACK = (30, 30, 30, 255)
        self.WHITE = (255, 255, 255, 255)
        self.BROWN = (210, 105, 30, 255)

        self.COLORS = [self.RED, self.BLUE, self.YELLOW, self.GREEN, self.MAGENTA, self.CYAN]


var = Variables()


class InputBox:
    """
    Class creating a name writing box.
    """
    def __init__(self, x, y, w, h, text=''):
        self.name_recorded = False
        self.name = ''
        self.text = text
        self.rect = pg.Rect(x, y, w, h)
        self.color = var.WHITE  # The non-active color
        self.txt_surface = mm.myfont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        The thing that handles the events like writing and deactivating the inputbox.
        :param event:
        :return:
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = var.CYAN if self.active else var.WHITE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.name = self.text
                    self.name_recorded = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = mm.myfont.render(self.text, True, self.color)

    def update(self):
        """
        A procedure to update the size of the inputbox.
        :return: None
        """
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        """
        A procedure to display the text on the screen.
        :object screen: pg.Surface
        :return: None
        """
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class MainMenu:
    """
    Launches mainmenu and handles the events associated with it.
    """
    def __init__(self):
        self.leaderboard = False
        self.endcard = False
        self.username = ''
        self.screen_width = 1200
        self.screen_height = 900
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.myfont = pg.font.SysFont('Comic Sans MS', 50)
        self.endgamefont = pg.font.SysFont('Comic Sans MS', 100)
        self.text1 = self.myfont.render("Welcome to BALLBREAKER", True, var.CYAN)
        self.text2 = self.myfont.render("Please, enter your name:", True, var.CYAN)
        self.text3 = self.myfont.render("Leaderboard", True, var.CYAN)

    def leaderboard_in_main_menu(self, event):
        """
        Displays the leaderboard in main menu.
        :param event:
        :return: None
        """
        # Check if the mouse was clicked inside the "Leaderboard" Rect.
        if event.type == pg.MOUSEBUTTONDOWN and pg.Rect(self.screen_width // 2 - 130, self.screen_height // 2 - 10,
                                                        260, 55).collidepoint(event.pos[0], event.pos[1]):
            self.screen.fill(var.BLACK)
            # Opens the 'Leaderboard' file.
            with open('Leaderboard.txt', 'r') as file:
                # Writes out line for line the file.
                for i, line in enumerate(file.readlines()):
                    self.text_leaderboard = self.myfont.render(line, True, var.GREEN)
                    self.screen.blit(self.text_leaderboard, (self.screen_width//10, self.screen_height//10 + i*55))
            pg.display.update()

    def draw_main_menu(self, x, y, w, h):
        """
        Draws the main menu and handles the inputbox and leaderboard
        (x, y) - the position of the left top corner of the input box
        w - width of the input box
        h - height of the input box
        :param x: int
        :param y: int
        :param w: int
        :param h: int
        :return: None
        """
        input_box = InputBox(x, y, w, h)
        done = False
        while not done:
            for event in pg.event.get():
                # Checks for exit inside main menu
                if event.type == pg.QUIT:
                    pg.quit()
                input_box.handle_event(event)
                # Checks for the end of writing
                if input_box.name_recorded:
                    done = True
                    self.username = input_box.name
                input_box.update()

                # Checks if the player entered the leaderboard
                if event.type == pg.MOUSEBUTTONDOWN and pg.Rect(self.screen_width // 2 - 130, self.screen_height // 2 - 10,
                                                                260, 55).collidepoint(event.pos[0], event.pos[1]):
                    self.screen.fill(var.BLACK)
                    with open('Leaderboard.txt', 'r') as file:
                        # Writes out the 'Leaderboard.txt' line by line
                        for i, line in enumerate(file.readlines()):
                            self.text_leaderboard = self.myfont.render(str(line.strip()), True, var.GREEN)
                            self.screen.blit(self.text_leaderboard,
                                             (self.screen_width // 10, self.screen_height // 10 + i * 55))
                    self.leaderboard = True
                # Checks if the player exits the leaderboard
                if event.type == pg.MOUSEBUTTONUP:
                    self.leaderboard = False

            if not self.leaderboard:
                # Draws the main menu
                self.screen.fill(var.BLACK)
                input_box.draw(self.screen)

                pg.draw.rect(self.screen, var.BROWN, (self.screen_width//2 - 230, self.screen_height//2 - 310,
                                                      self.text1.get_width() + 20, 55))
                pg.draw.rect(self.screen, var.BROWN, (self.screen_width//2 - 230 + 15, self.screen_height//2 - 210,
                                                      self.text2.get_width() + 20, 55))
                pg.draw.rect(self.screen, var.BROWN, (self.screen_width//2 - 130 + 25, self.screen_height//2 - 10,
                                                      self.text3.get_width() + 20, 55))
                self.screen.blit(self.text1, (self.screen_width//2 - 230 + 10, self.screen_height//2 - 300))
                self.screen.blit(self.text2, (self.screen_width//2 - 230 + 25, self.screen_height//2 - 200))
                self.screen.blit(self.text3, (self.screen_width//2 - 130 + 35, self.screen_height//2))

            pg.display.flip()
            pg.time.Clock().tick(var.FPS)
            pg.display.update()

    def draw_endcard(self):
        self.text_endcard1 = self.endgamefont.render("GAME OVER", True, var.RED)
        self.text_endcard2 = self.endgamefont.render("YOUR SCORE " + self.username + ":", True, var.RED)
        self.endcardscore = self.endgamefont.render(str(c.counter), True, var.RED)
        self.text_label = self.endgamefont.render("Noobie", True, var.WHITE)

        if c.counter > 50 and c.counter < 100:
            self.text_label = self.endgamefont.render("Rookie", True, var.GREEN)
        elif c.counter > 100 and c.counter < 200:
            self.text_label = self.endgamefont.render("Amateur", True,  var.YELLOW)
        elif c.counter > 200 and c.counter < 300:
            self.text_label = self.endgamefont.render("Ball Master", True, var.MAGENTA)
        elif c.counter > 300:
            self.text_label = self.endgamefont.render("Ball Breaker", True, var.RED)

        self.screen.fill(var.BLACK)
        self.screen.blit(self.text_endcard1, (self.screen_width//10, self.screen_height//10))
        self.screen.blit(self.text_endcard2, (self.screen_width//10, self.screen_height//5))
        self.screen.blit(self.endcardscore, (self.screen_width//10 + self.text_endcard2.get_width() + 10,
                                             self.screen_height // 5))
        self.screen.blit(self.text_label, (self.screen_width//2 - self.text_label.get_width(), self.screen_height // 2))

        pg.display.flip()
        pg.time.Clock().tick(var.FPS)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                gh.finished = True


mm = MainMenu()


class BaseTarget:
    """
    Creates a base Target.
    """
    def __init__(self):
        self.vx = choice([-1, 1]) * randint(1, 5)  # Speed of the target in the x direction
        self.vy = choice([-1, 1]) * randint(1, 5)  # Speed of the target in the y direction
        self.x = randint(100, 1100)  # Initial x coordinate of the target
        self.y = randint(100, 900)  # Initial y coordinate of the target
        self.color = var.COLORS[randint(0, 5)]  # The colour of the target


class Ball(BaseTarget):
    """
    Class, which defines Ball as an object.
    """

    def __init__(self):
        super().__init__()
        self.r = randint(20, 100)  # The radius of the target

        circle(mm.screen, self.color, (self.x, self.y), self.r)

    def draw_ball(self):
        """
        Procedure that draws the ball
        :return: None
        """
        circle(mm.screen, self.color, (self.x, self.y), self.r)

    def motion_ball(self):
        """
        Procedure handling ball's motion
        :return: None
        """
        self.x, self.y = self.x + self.vx, self.y + self.vy
        circle(mm.screen, self.color, (self.x, self.y), self.r)

        if mm.screen_width - self.x <= self.r or self.x <= self.r:
            self.vx = -self.vx
        if mm.screen_height - self.y <= self.r or self.y < self.r:
            self.vy = -self.vy

    def catch_the_ball(self, event):
        """
        Method, registering the catching of the ball.
        :param event: берёт событие MOUSEBUTTONDOWN
        :return: bool
        """
        x, y = event.pos
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= self.r ** 2:
            return True
        else:
            return False


class Star(BaseTarget):
    """
    Class that defines Star as an object.
    """

    def __init__(self):
        super().__init__()
        self.r = 100
        self.color = var.COLORS[3]

    def draw_star(self):
        """
        Procedure that draws the star.
        :return: None
        """
        point_list = []
        num_points = 8
        for i in range(num_points * 2):
            self.r = 100
            if i % 2 == 0:
                self.r = self.r // 2
            ang = i * math.pi / num_points + var.timer * math.pi / 20
            x = self.x + int(math.cos(ang) * self.r)
            y = self.y + int(math.sin(ang) * self.r)
            point_list.append((x, y))

        pg.draw.polygon(mm.screen, self.color, point_list)
        pg.draw.circle(mm.screen, var.RED, (self.x, self.y), self.r // 2)

    def motion_star(self, timer):
        """
        Method handling star's motion.
        :param timer: int
        :return: None
        """
        # Describes star's reflection
        if mm.screen_width - self.x <= self.r or self.x <= self.r:
            self.vx = -self.vx
        if mm.screen_height - self.y <= self.r or self.y < self.r:
            self.vy = -self.vy

        self.x, self.y = self.x + self.vx, self.y + self.vy
        # Describes the special behaviour. The star changes velocity every 40 ticks of the clock
        if timer % 40 == 0:
            self.vx = choice([-1, 1]) * randint(4, 8)  # Speed of the ball in the x direction
            self.vy = choice([-1, 1]) * randint(4, 8)  # Speed of the ball in the y direction

    def catch_the_star(self, event):
        """
        Method, registering if the star was caught.
        :param event:
        :return: bool
        """
        x, y = event.pos
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= (self.r // 2) ** 2:
            return True
        else:
            return False


star_pool = [Star() for i in range(var.number_of_stars)]
ball_pool = [Ball() for k in range(var.number_of_balls)]


class GameHandler:
    """
    Class handling the playable part of the game.
    """
    def __init__(self):
        self.timer = 0
        self.clock = pg.time.Clock()
        self.finished = False

    def motion_processor(self):
        """
        Procedure processing motion of the targets.
        :return:
        """
        for star in star_pool:
            star.draw_star()
            star.motion_star(var.timer)
        for ball in ball_pool:
            ball.draw_ball()
            ball.motion_ball()

    def target_creator(self):
        """
        Procedure adding targets, after they were hit.
        :return: None
        """
        if len(ball_pool) < var.number_of_balls:
            ball_pool.append(Ball())
        if len(star_pool) < var.number_of_stars:
            star_pool.append(Star())


gh = GameHandler()


class Counter:
    """
    A counting class.
    """
    def __init__(self):
        self.counter = 0
        self.counter_surface = mm.myfont.render(str(self.counter), False, (0, 0, 255))

    def count_updater(self):
        """
        Displays the current score.
        :return: None
        """
        self.counter_surface = mm.myfont.render(str(self.counter), False, (0, 0, 255))
        mm.screen.blit(self.counter_surface, (mm.screen_width//2, mm.screen_height//10))

    def main_loop_event_checker(self, event):
        """
        Method processing hits.
        :param event:
        :return: None
        """
        if event.type == pg.QUIT:
            gh.finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for i, star in enumerate(star_pool):
                if star.catch_the_star(event):
                    self.counter += 10
                    star_pool.pop(i)
            for i, ball in enumerate(ball_pool):
                if ball.catch_the_ball(event):
                    self.counter += 1
                    ball_pool.pop(i)


c = Counter()


class LeaderBoardUpdate:
    """
    Class handling the file to game data transition and back.
    """
    def __init__(self):
        self.sorted = False
        self.updated = False
        self.score_dict = {}
        self.number_of_scores = 0

    def leaderboard_reader(self):
        """
        Procedure reading the file and organising it into 2 lists.
        :return: None
        """
        with open('Leaderboard.txt') as file:
            for line in file.readlines():
                line = line.split()
                self.score_dict.update({line[1]: int(line[3])})
            self.number_of_scores = len(self.score_dict)

    def leaderboard_update(self, username):
        """
        Method updating the leaderboard.
        :param username: str
        :return: None
        """
        if len(self.score_dict) < 11 or (username in self.score_dict and self.score_dict.value(username) < c.counter):
            self.score_dict.update({username: c.counter})
        elif c.counter > self.score_dict.get(list(self.score_dict)[10]):
            self.score_dict.update({list(self.score_dict)[10]: c.counter})
        # Сортировка имён
        self.score_dict = sorted(self.score_dict.items(), key=lambda x: x[1], reverse=True)
        # Сортировка закончена

        with open('Leaderboard.txt', 'wt') as file:
            file.write(str(1) + '. ' + self.score_dict[0][0] + ' - ' + str(self.score_dict[0][1]))
            for i in range(1, len(self.score_dict)):
                file.write('\n' + str(i) + '. ' + self.score_dict[i][0] + ' - ' + str(self.score_dict[i][1]))


lb = LeaderBoardUpdate()


mm.draw_main_menu(mm.screen_width//2 - 100, mm.screen_height//2 - 100, 500, 50)


while not gh.finished:
    if not mm.endcard:
        gh.target_creator()
        gh.motion_processor()
        c.count_updater()
        var.timer += 1
        pg.display.update()
        gh.clock.tick(var.FPS)
        mm.screen.fill(var.BLACK)
        for event in pg.event.get():
            c.main_loop_event_checker(event)
    if var.timer == var.total_gametime * var.FPS:
        mm.draw_endcard()
        mm.endcard = True

pg.quit()

lb.leaderboard_reader()
lb.leaderboard_update(mm.username)
