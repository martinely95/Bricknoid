import pygame
import time  # time.sleep(0.005) and fps
import sys


SCREEN_SIZE = 1280, 720
PLAY_AREA = 640, 480
H_OFFSET = (SCREEN_SIZE[0] - PLAY_AREA[0]) / 2
V_OFFSET = (SCREEN_SIZE[1] - PLAY_AREA[1]) / 2
CENTER_COORDS = (H_OFFSET + PLAY_AREA[0] / 2, V_OFFSET + PLAY_AREA[1] / 2)

# object dimensions
BRICK_WIDTH = 60
BRICK_HEIGHT = 15
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 12
BALL_DIAMETER = 10
BALL_RADIUS = BALL_DIAMETER / 2

# MAX_PADDLE_X = PLAY_AREA[0] - PADDLE_WIDTH
# MAX_BALL_X = PLAY_AREA[0] - BALL_DIAMETER
# MAX_BALL_Y = PLAY_AREA[1] - BALL_DIAMETER
MAX_PADDLE_X = SCREEN_SIZE[0] - H_OFFSET - PADDLE_WIDTH
MIN_PADDLE_X = H_OFFSET
MAX_BALL_X = SCREEN_SIZE[0] - H_OFFSET - BALL_DIAMETER
MAX_BALL_Y = SCREEN_SIZE[1] - V_OFFSET - BALL_DIAMETER
MIN_BALL_X = H_OFFSET + BALL_DIAMETER
MIN_BALL_Y = V_OFFSET - BALL_DIAMETER


# paddle y coordinate ??????
# PADDLE_Y = PLAY_AREA[1] - PADDLE_HEIGHT - 10
PADDLE_Y = V_OFFSET + PLAY_AREA[1] - PADDLE_HEIGHT - 10

# color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BRICK_COLOR = (0, 255, 0)  # GREEN

# state constants
STATES = {  # upon integration in v3.0
    "BALL_IN_PADDLE": 0,
    "PLAYING": 1,
    "WON": 2,
    "GAME_OVER": 3,
    "CHANGING_LEVEL": 4
}
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
STATE_CHANGING_LEVEL = 4

# game constants
NEW_GAME = (0, 0, 3)
INIT_BALL_VEL = (1, -1)
BALL_VEL_COEF = 1


class Bricknoid:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Bricknoid v2.0")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        # change the variable to load a specific level first
        # variable (level, score, lives)
        self.init_game(NEW_GAME)

    # def init_game(self, thelevel, thescore, thelives):
    def init_game(self, game):
        self.level = game[0]
        self.score = game[1]
        self.lives = game[2]
        self.state = STATE_BALL_IN_PADDLE

        self.paddle = pygame.Rect(
            CENTER_COORDS[0] - PADDLE_WIDTH / 2,
            PADDLE_Y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
            )
        self.ball = pygame.Rect(
            CENTER_COORDS[0] - PADDLE_WIDTH / 2,
            PADDLE_Y - BALL_DIAMETER,
            BALL_DIAMETER,
            BALL_DIAMETER
        )
        self.init_ball_vel = INIT_BALL_VEL
        self.ball_vel = [
            self.init_ball_vel[0],
            self.init_ball_vel[1]
            ]
        self.ball_vel[0] *= BALL_VEL_COEF
        self.ball_vel[1] *= BALL_VEL_COEF
        self.last_ball_pos = [self.ball.left, self.ball.top]
        # masivi edno drugo tuka
        if self.level == 0:
            self.create_bricks()
        elif self.level == 1:
            self.create_bricks1()
        elif self.level == 2:
            self.create_bricks2()
        elif self.level == 3:
            self.create_bricks3()
        elif self.level == 4:
            self.create_bricks4()
        elif self.level == 5:
            self.create_bricks5()
        elif self.level == 6:
            self.create_bricks6()
        elif self.level == 7:
            self.create_bricks7()
        elif self.level == 8:
            self.create_bricks8()
        elif self.level == 9:
            self.create_bricks9()

    ################################################################
    ################################################################
    def menu(self):
        if self.font:
            self.screen.fill(BLACK)
            font_surface = self.font.render(
                "New game(n)",
                False,
                WHITE)
            self.screen.blit(
                font_surface, (CENTER_COORDS[0] - 100, CENTER_COORDS[1] - 150)
                )
            font_surface = self.font.render(
                "Instructions(i)",
                False,
                WHITE)
            self.screen.blit(
                font_surface, (CENTER_COORDS[0] - 100, CENTER_COORDS[1] - 100)
                )
            font_surface = self.font.render(
                "High scores(h) - not ready",
                False,
                WHITE)
            self.screen.blit(
                font_surface, (CENTER_COORDS[0] - 100, CENTER_COORDS[1] - 50)
                )
            font_surface = self.font.render(
                "Quit(q)",
                False,
                WHITE)
            self.screen.blit(
                font_surface, (CENTER_COORDS[0] - 100, CENTER_COORDS[1])
                )
            pygame.display.flip()

    def instructions(self):
        if self.font:
            self.screen.fill(BLACK)
            font_surface = self.font.render(
                "Press the left arrow to move the platform to the left.",
                False,
                WHITE)
            self.screen.blit(
                font_surface, (CENTER_COORDS[0] - 250, CENTER_COORDS[1] - 100)
                )
            font_surface = self.font.render(
                "Press the right arrow to move the platform to the right.",
                False,
                WHITE)
            self.screen.blit(
                font_surface, (CENTER_COORDS[0] - 250, CENTER_COORDS[1] - 50)
                )
            pygame.display.flip()

    def check_exit(self, keys={113: 0}):
        for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    sys.exit()

    def get_input_for_menu(self):
        while True:
            self.menu()
            keys = pygame.key.get_pressed()
            self.check_exit(keys)
            if keys[pygame.K_n]:
                return
            if keys[pygame.K_i]:
                self.instructions()
                while 1:
                    keys = pygame.key.get_pressed()
                    self.check_exit(keys)
                    if keys[pygame.K_ESCAPE]:
                        break
    # here is all the code to create the bricks for different levels

    # level 1
    def create_bricks(self):
        # y_ofs = 35
        y_ofs = V_OFFSET
        self.bricks = []
        for i in range(7):
            # x_ofs = 35
            x_ofs = H_OFFSET + 35
            for j in range(8):
                self.bricks.append(pygame.Rect(
                    x_ofs, y_ofs,
                    BRICK_WIDTH,
                    BRICK_HEIGHT
                ))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 5

    # level 2
    def create_bricks1(self):
        y_ofs = 35
        self.bricks = []
        for i in range(7):
            x_ofs = 45
            for j in range(8):
                if (j % 2 == 0):
                    self.bricks.append(pygame.Rect(
                        x_ofs, y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                    x_ofs += (BRICK_WIDTH + 20) * 2
            y_ofs += BRICK_HEIGHT + 5

    # level 3
    def create_bricks2(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8):
            x_ofs = 35
            if i % 2 == 1:
                for j in range(8):
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                    x_ofs += BRICK_WIDTH + 10
                y_ofs += (BRICK_HEIGHT + 5) * 2

    # level 4
    def create_bricks3(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8):
            x_ofs = 10
            if i % 2 == 1:
                for j in range(10):
                    if j % 2 == 1:
                        self.bricks.append(pygame.Rect(
                            x_ofs, y_ofs,
                            BRICK_WIDTH,
                            BRICK_HEIGHT
                        ))
                        x_ofs += (BRICK_WIDTH + 10) * 2
                y_ofs += (BRICK_HEIGHT + 5) * 2

    # level 5
    def create_bricks4(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8):
            x_ofs = 35
            for j in range(8):
                if j == i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5

    # level 6
    def create_bricks5(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8):
            x_ofs = 35
            for j in range(8):
                if j != i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5

    # level 7
    def create_bricks6(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8, 0, -1):
            x_ofs = 35
            for j in range(8):
                if j == i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5

    # level 8
    def create_bricks7(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8, 0, -1):
            x_ofs = 35
            for j in range(8):
                if j == i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5
        for i in range(8, 0, -1):
            x_ofs = 35
            for j in range(8):
                if j == i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5

    # level 9
    def create_bricks8(self):
        y_ofs = 35
        self.bricks = []
        for i in range(8):
            x_ofs = 35
            for j in range(8):
                if j == i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5
        for i in range(8):
            x_ofs = 35
            for j in range(8):
                if j == i:
                    self.bricks.append(pygame.Rect(
                        x_ofs,
                        y_ofs,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    ))
                x_ofs += (BRICK_WIDTH + 10)
            y_ofs += BRICK_HEIGHT + 5

    # level 10
    def create_bricks9(self):
        y_ofs = 35
        self.bricks = []
        for i in range(16):
            x_ofs = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(
                    x_ofs,
                    y_ofs,
                    BRICK_WIDTH,
                    BRICK_HEIGHT
                ))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 5

    ###########################################################
    ###########################################################

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= 10
            if self.paddle.left < MIN_PADDLE_X:
                self.paddle.left = MIN_PADDLE_X

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 10
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [5, -5]
            self.state = STATE_PLAYING

        elif keys[pygame.K_RETURN] and self.state == STATE_WON:
            self.level += 1
            self.lives += 1
            self.init_game((self.level, self.score, self.lives))

        elif keys[pygame.K_RETURN] and self.state == STATE_GAME_OVER:
            self.init_game(NEW_GAME)

    # move_ball_with_collision(self):
    # broi gi edno po edno v zavisimost otkade idva topkata

    def move_ball(self):
        self.last_ball_pos = [self.ball.left, self.ball.top]
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= MIN_BALL_X:
            self.ball.left = MIN_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < MIN_BALL_Y:
            self.ball.top = MIN_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                # # точки на блокчето:
                # (x_1, y_1) = (brick.left, brick.top)
                # (x_2, y_2) = (brick.left + brick.width, brick.top)
                # (x_3, y_3) = (brick.left, brick.top + brick.height)
                # (x_4, y_4) = (brick.left + brick.width,
                #               brick.top + brick.height)
                # # уравнение на горната част на блокчето:
                # k_1 = (y_2 - y_1)/(x_2 - x_1)
                # b_1 = (x_2*y_1 - y_2*x_1)/(x_2 - x_1)
                # # уравнение на долната част на блокчето:
                # k_2 = (y_4 - y_3)/(x_4 - x_3)
                # b_2 = (x_4*y_3 - y_4*x_3)/(x_4 - x_3)
                # # уравнение на лявата част на блокчето:
                # # k_3 = (y_3 - y_1)/(x_3 - x_1)
                # k_3 = 1
                # b_3 = x_3
                # # b_3 = (x_3*y_1 - y_3*x_1)/(x_3 - x_1)
                # # уравнение на дясната част на блокчето:
                # # k_4 = (y_4 - y_2)/(x_4 - x_4)
                # k_4 = 1
                # b_4 = x_4
                # # b_4 = (x_4*y_2 - y_4*x_2)/(x_4 - x_2)
                # # уравнение на топчето:
                # k_t = (self.last_ball_pos[1] -
                #        self.ball.top
                #        )/(
                #        self.last_ball_pos[0] -
                #        self.ball.left)
                # b_t = (self.last_ball_pos[0]*self.ball.top -
                #        self.last_ball_pos[1]*self.ball.left
                #        )/(
                #        self.last_ball_pos[0] -
                #        self.ball.left)
                # # print(brick.left/top/height/wight)
                # # width + 10; height+5
                # # посоката след сблъсъка се решава от това
                # # коя права е пресякло топчето;
                # # дали правата на долната част на
                # # правоъгълничето или правата на лявата му част
                # self.score += 3
                # if (
                #     self.last_ball_pos[0] - self.ball.left > 0 and
                #     self.last_ball_pos[1] - self.ball.top > 0
                #      ):
                #     # ако идва от югоизток
                #     if (
                #         brick.top <=
                #         (k_3*b_t - b_3*k_t)/(k_3 - k_t) <=
                #         brick.top + brick.height
                #          ):
                #         self.ball_vel[0] = -self.ball_vel[0]
                #     elif (
                #         brick.left <=
                #         (b_t - b_2)/(k_2 - k_t) <=
                #         brick.left + brick.width
                #          ):
                #         self.ball_vel[1] = -self.ball_vel[1]
                #     else:
                #         self.ball_vel[1] = -self.ball_vel[1]
                # elif (
                #     self.last_ball_pos[0] - self.ball.left < 0 and
                #     self.last_ball_pos[1] - self.ball.top < 0
                #      ):
                #     # ако идва от СЗ
                #     if (
                #         brick.top <=
                #         (k_3*b_t - b_3*k_t)/(k_3 - k_t) <=
                #         brick.top + brick.height
                #          ):
                #         self.ball_vel[0] = -self.ball_vel[0]
                #     elif (
                #         brick.left <=
                #         (b_t - b_1)/(k_1 - k_t) <=
                #         brick.left + brick.width
                #          ):
                #         self.ball_vel[1] = -self.ball_vel[1]
                #     else:
                #         self.ball_vel[1] = -self.ball_vel[1]
                # elif (
                #     self.last_ball_pos[0] - self.ball.left > 0 and
                #     self.last_ball_pos[1] - self.ball.top < 0
                #      ):
                #     # ако идва от СИ
                #     if (
                #         brick.top <=
                #         (k_4*b_t - b_4*k_t)/(k_4 - k_t) <=
                #         brick.top + brick.height
                #          ):
                #         self.ball_vel[0] = -self.ball_vel[0]
                #     elif (
                #         brick.left <=
                #         (b_t - b_1)/(k_1 - k_t) <=
                #         brick.left + brick.width
                #          ):
                #         self.ball_vel[1] = -self.ball_vel[1]
                #     else:
                #         self.ball_vel[1] = -self.ball_vel[1]
                # elif (
                #     self.last_ball_pos[0] - self.ball.left < 0 and
                #     self.last_ball_pos[1] - self.ball.top > 0
                #      ):
                #     # ако идва от ЮЗ
                #     if (
                #         brick.top <=
                #         (k_3*b_t - b_3*k_t)/(k_3 - k_t) <=
                #         brick.top + brick.height
                #          ):
                #         self.ball_vel[0] = -self.ball_vel[0]
                #     elif (
                #         brick.left <=
                #         (b_t - b_2)/(k_2 - k_t) <=
                #         brick.left + brick.width
                #          ):
                #         self.ball_vel[1] = -self.ball_vel[1]
                #     else:
                #         self.ball_vel[1] = -self.ball_vel[1]
                # # ball.top ball.left brick.top brick.left
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]

        # if the ball hits the ground
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self, fps=''):
        if self.font:
            font_surface = self.font.render(
                "LEVEL: " + str(self.level + 1) +
                " SCORE: " + str(self.score) +
                " LIVES: " + str(self.lives) +
                " fps: " + str(fps),
                False,
                WHITE)
            self.screen.blit(font_surface, (205, 5))

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, WHITE)
            x = (PLAY_AREA[0] - size[0])
            y = (PLAY_AREA[1] - size[1]) / 1
            self.screen.blit(font_surface, (x, y))

    def run(self):
        self.menu()
        self.get_input_for_menu()

        last_time = time.time()
        fps = 0
        last_fps = 0
        while 1:
            current_time = time.time()
            fps += 1
            tdelta = - last_time + current_time
            if tdelta > 1:
                last_time = time.time()
                last_fps = fps
                fps = 0
            self.check_exit()

            self.clock.tick(70)  # bavi fps-a
            self.screen.fill(BLACK)
            self.check_input()

            if self.state == STATE_PLAYING:
                pass
                # self.move_ball_with_collision()
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO START")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO RESTART")
            elif self.state == STATE_WON:
                self.show_message(
                    "YOU WON! PRESS ENTER TO PLAY THE NEXT LEVEL"
                )
            elif self.state == STATE_WON and self.level == 9:
                self.show_message(
                    "CONGRATULATIONS, YOU'VE COMPLETED THE GAME!!"
                )
            # draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # draw ball
            pygame.draw.circle(
                self.screen,
                WHITE,
                (
                    int(self.ball.left + BALL_RADIUS),
                    int(self.ball.top + BALL_RADIUS)
                ),
                int(BALL_RADIUS))

            self.draw_bricks()

            self.show_stats(last_fps)

            pygame.display.flip()

            # have this here for cascading block drawing
            # self.draw_bricks()


if __name__ == "__main__":
    Bricknoid().run()
