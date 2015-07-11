import pygame
import time  # time.sleep(0.005) and fps
from constants import GameConstants
from load_levels import Levels
from draw import Draw
import highscores


class Bricknoid:

    def __init__(self):
        pygame.init()
        self.constants = GameConstants()
        self.drawer = Draw()
        pygame.display.set_caption("Bricknoid v3.0")
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.last_time_fps_is_checked = time.time()
        # change the variable to load a specific level first
        # variable (level, score, lives)
        self.init_game(self.constants.NEW_GAME)

    def init_game(self, game):
        self.level = game[0]
        self.score = game[1]
        self.lives = game[2]
        self.state = self.constants.STATES["BALL_IN_PADDLE"]

        self.paddle = pygame.Rect(
            self.constants.CENTER_COORDS[0] - self.constants.PADDLE_WIDTH / 2,
            self.constants.PADDLE_Y,
            self.constants.PADDLE_WIDTH,
            self.constants.PADDLE_HEIGHT
            )
        self.ball = pygame.Rect(
            self.constants.CENTER_COORDS[0] - self.constants.PADDLE_WIDTH / 2,
            self.constants.PADDLE_Y - self.constants.BALL_DIAMETER,
            self.constants.BALL_DIAMETER,
            self.constants.BALL_DIAMETER
        )
        self.init_ball_vel = self.constants.INIT_BALL_VEL
        self.ball_vel = [
            self.init_ball_vel[0],
            self.init_ball_vel[1]
            ]
        self.ball_vel[0] *= self.constants.BALL_VEL_COEF
        self.ball_vel[1] *= self.constants.BALL_VEL_COEF
        self.last_ball_pos = [self.ball.left, self.ball.top]

        self.levels = Levels()
        self.levels.load_level(self.level)

        self.add_bricks_to_game(self.levels.return_loaded_level())

    # level
    def add_bricks_to_game(self, level):
        y_ofs = 35
        # y_ofs = constants.V_OFFSET
        self.bricks = []
        for i in range(len(level)):
            # x_ofs = 35
            x_ofs = self.constants.MIN_BRICKS_X + 35
            for j in range(len(level[i])):
                if level[i][j] is 'x':
                    self.bricks.append(pygame.Rect(
                        x_ofs, y_ofs,
                        self.constants.BRICK_WIDTH,
                        self.constants.BRICK_HEIGHT
                    ))
                x_ofs += self.constants.BRICK_WIDTH + 10
            y_ofs += self.constants.BRICK_HEIGHT + 5

    def check_exit(self, running, keys={113: 0}):
        for event in pygame.event.get():
            if event.type is pygame.QUIT or keys[pygame.K_q]:
                running[0] = False

    def get_input_for_menu(self, running):
        while running[0]:
            self.clock.tick(70)
            self.drawer.menu()
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            self.check_exit(running, keys)
            if not running[0]:
                return
            if keys[pygame.K_n]:
                return
            if keys[pygame.K_i]:
                self.drawer.instructions()
                pygame.display.flip()
                while running[0]:
                    self.clock.tick(70)
                    keys = pygame.key.get_pressed()
                    self.check_exit(running, keys)
                    if keys[pygame.K_ESCAPE]:
                        break

    def check_input(self, running):
        keys = pygame.key.get_pressed()
        self.check_exit(running, keys)
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 10
            if self.paddle.left < self.constants.MIN_PADDLE_X:
                self.paddle.left = self.constants.MIN_PADDLE_X

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 10
            if self.paddle.left > self.constants.MAX_PADDLE_X:
                self.paddle.left = self.constants.MAX_PADDLE_X

        if keys[pygame.K_SPACE] and \
                self.state is self.constants.STATES["BALL_IN_PADDLE"]:
            self.ball_vel = [5, -5]
            self.state = self.constants.STATES["PLAYING"]

        elif keys[pygame.K_RETURN] and \
                self.state is self.constants.STATES["WON"]:
            self.level += 1
            self.lives += 1
            self.init_game((self.level, self.score, self.lives))

        elif keys[pygame.K_RETURN] and \
                self.state is self.constants.STATES["GAME_OVER"]:
            self.init_game(self.constants.NEW_GAME)

        elif keys[pygame.K_ESCAPE]:
            self.drawer.menu()
            pygame.display.flip()
            self.get_input_for_menu(running)

    def move_ball(self):
        self.last_ball_pos = [self.ball.left, self.ball.top]
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= self.constants.MIN_BALL_X:
            self.ball.left = self.constants.MIN_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= self.constants.MAX_BALL_X:
            self.ball.left = self.constants.MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < self.constants.MIN_BALL_Y:
            self.ball.top = self.constants.MIN_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def decide_new_direction_and_remove_brick(self, brick):
        delta_x = -self.last_ball_pos[0] + self.ball.left
        delta_y = -self.last_ball_pos[1] + self.ball.top

        top_middle = (brick.left + self.constants.BRICK_WIDTH / 2,
                      brick.top)
        left_middle = (brick.left,
                       brick.top + self.constants.BRICK_HEIGHT / 2)
        down_middle = (brick.left + self.constants.BRICK_WIDTH / 2,
                       brick.top + self.constants.BRICK_HEIGHT)
        right_middle = (brick.left + self.constants.BRICK_WIDTH,
                        brick.top + self.constants.BRICK_HEIGHT / 2)

        top_middle_delta = ((top_middle[0] - self.ball.left) ** 2 +
                            (top_middle[1] - self.ball.top) ** 2) ** 0.5
        left_middle_delta = ((left_middle[0] - self.ball.left) ** 2 +
                             (left_middle[1] - self.ball.top) ** 2) ** 0.5
        down_middle_delta = ((down_middle[0] - self.ball.left) ** 2 +
                             (down_middle[1] - self.ball.top) ** 2) ** 0.5
        right_middle_delta = ((right_middle[0] - self.ball.left) ** 2 +
                              (right_middle[1] - self.ball.top) ** 2) ** 0.5

        self.bricks.remove(brick)

        if delta_x > 0 and delta_y > 0:
            if top_middle_delta < left_middle_delta:
                self.ball_vel[1] *= -1
            else:
                self.ball_vel[0] *= -1
                self.ball.left -= 25
                self.ball.top += 25
                if self.check_for_bricks():
                    self.ball_vel[1] *= -1
                self.ball.left += 25
                self.ball.top -= 25
        if delta_x < 0 and delta_y > 0:
            if top_middle_delta < right_middle_delta:
                self.ball_vel[1] *= -1
            else:
                self.ball_vel[0] *= -1
                self.ball.left += 25
                self.ball.top += 25
                if self.check_for_bricks():
                    self.ball_vel[1] *= -1
                self.ball.left -= 25
                self.ball.top -= 25
        if delta_x > 0 and delta_y < 0:
            if down_middle_delta < left_middle_delta:
                self.ball_vel[1] *= -1
            else:
                self.ball_vel[0] *= -1
                self.ball.left -= 25
                self.ball.top -= 25
                if self.check_for_bricks():
                    self.ball_vel[1] *= -1
                self.ball.left += 25
                self.ball.top += 25
        if delta_x < 0 and delta_y < 0:
            if down_middle_delta < right_middle_delta:
                self.ball_vel[1] *= -1
            else:
                self.ball_vel[0] *= -1
                self.ball.left += 25
                self.ball.top -= 25
                if self.check_for_bricks():
                    self.ball_vel[1] *= -1
                self.ball.left -= 25
                self.ball.top += 25

    def check_for_bricks(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                return True

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.decide_new_direction_and_remove_brick(brick)
                self.score += 5
                break

        if not len(self.bricks):
            self.state = self.constants.STATES["WON"]

        if self.ball.colliderect(self.paddle):
            self.ball.top = \
                self.constants.PADDLE_Y - self.constants.BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.ball_vel[0] = abs(self.ball_vel[0])
            elif keys[pygame.K_LEFT]:
                self.ball_vel[0] = -abs(self.ball_vel[0])

        # if the ball hits the ground
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = self.constants.STATES["BALL_IN_PADDLE"]
            else:
                self.state = self.constants.STATES["GAME_OVER"]

    def show_stats(self, fps=''):
        msg = \
            "LEVEL: " + str(self.level + 1) + \
            " SCORE: " + str(self.score) + \
            " LIVES: " + str(self.lives) + \
            " fps: " + str(fps)
        pygame.display.set_caption(msg)
        # if self.drawer.font:
        #     self.drawer.print_on_screen(
        #         "LEVEL: " + str(self.level + 1) +
        #         " SCORE: " + str(self.score) +
        #         " LIVES: " + str(self.lives) +
        #         " fps: " + str(fps),
        #       self.constants.WHITE, self.constants.CENTER_COORDS[0] - 175, 5)

    def check_state(self):
        if self.state is self.constants.STATES["PLAYING"]:
            pass
            # self.move_ball_with_collision()
            self.move_ball()
            self.handle_collisions()
        elif self.state is self.constants.STATES["BALL_IN_PADDLE"]:
            self.ball.left = self.paddle.left + self.paddle.width / 2
            self.ball.top = self.paddle.top - self.ball.height
            self.drawer.show_message("PRESS SPACE TO START")
        elif self.state is self.constants.STATES["GAME_OVER"]:
            self.drawer.show_message("GAME OVER. PRESS ENTER TO RESTART")
            if highscores.check_if_highscore(str(self.score)):
                highscores.insert_highscore(str(self.score), "martin")
        elif self.state is self.constants.STATES["WON"]:
            self.drawer.show_message(
                "YOU WON! PRESS ENTER TO PLAY THE NEXT LEVEL"
            )
        elif self.state is self.constants.STATES["WON"] and \
                self.level is self.levels.return_number_of_levels() + 1:
            self.drawer.show_message(
                "CONGRATULATIONS, YOU'VE COMPLETED THE GAME!!"
            )
            if highscores.check_if_highscore(str(self.score)):
                highscores.insert_highscore(str(self.score), "martin")

    def print_current_state(self):
        # drawing
        self.drawer.screen.fill(self.constants.BLACK)
        self.drawer.paddle(self.paddle)
        self.drawer.ball(self.ball)
        self.drawer.bricks(self.bricks)
        self.show_stats(self.fps)
        self.check_state()
        pygame.display.flip()

    def calculate_fps(self, fps):
        if time.time() - self.last_time_fps_is_checked > 1:
            self.last_time_fps_is_checked = time.time()
            self.fps = fps
            fps = 0
        return fps

    def run(self):
        running = [True]

        self.drawer.menu()
        pygame.display.flip()
        self.get_input_for_menu(running)

        fps = 0
        while running[0]:
            self.clock.tick(60)

            fps += 1
            fps = self.calculate_fps(fps)

            self.print_current_state()
            self.check_input(running)

if __name__ == "__main__":
    Bricknoid().run()
