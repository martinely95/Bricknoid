import pygame
from constants import GameConstants


class Draw:

    def __init__(self):
        self.constants = GameConstants()
        if pygame.display.get_caption():
            self.screen = pygame.display.get_surface()
        else:
            self.screen = pygame.display.set_mode(self.constants.SCREEN_SIZE)
        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

    def print_on_screen(self, text, color, hpos, vpos=50):
        font_surface = self.font.render(text, False, color)
        self.screen.blit(font_surface, (hpos, vpos))

    def menu(self):
        if self.font:
            self.screen.fill(self.constants.BLACK)
            self.print_on_screen(
                "New game/ continue(n)",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 100,
                self.constants.CENTER_COORDS[1] - 150)
            self.print_on_screen(
                "Instructions(i)",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 100,
                self.constants.CENTER_COORDS[1] - 100)
            self.print_on_screen(
                "High scores(h) - not ready",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 100,
                self.constants.CENTER_COORDS[1] - 50)
            self.print_on_screen(
                "Quit(q)",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 100,
                self.constants.CENTER_COORDS[1])

    def instructions(self):
        if self.font:
            self.screen.fill(self.constants.BLACK)
            self.print_on_screen(
                "Press the left arrow to move the platform to the left.",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 250,
                self.constants.CENTER_COORDS[1] - 100)
            self.print_on_screen(
                "Press the right arrow to move the platform to the right.",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 250,
                self.constants.CENTER_COORDS[1] - 50)
            self.print_on_screen(
                "Press 'Esc' during play time to go to main menu.",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 250,
                self.constants.CENTER_COORDS[1])
            self.print_on_screen(
                "Press 'Esc' to go back.",
                self.constants.WHITE,
                self.constants.CENTER_COORDS[0] - 250,
                self.constants.CENTER_COORDS[1] + 50)

    def bricks(self, bricks):
        for brick in bricks:
            pygame.draw.rect(self.screen, self.constants.BRICK_COLOR, brick)

    def show_message(self, msg):
        if self.font:
            size = self.font.size(msg)
            font_surface = self.font.render(msg, False, self.constants.WHITE)
            x = self.constants.CENTER_COORDS[0] - size[0] / 2
            y = self.constants.CENTER_COORDS[1]
            self.screen.blit(font_surface, (x, y))

    def paddle(self, paddle):
        pygame.draw.rect(
                self.screen,
                self.constants.BLUE,
                paddle)

    def ball(self, ball):
        pygame.draw.circle(
                self.screen,
                self.constants.WHITE,
                (
                    int(ball.left + self.constants.BALL_RADIUS),
                    int(ball.top + self.constants.BALL_RADIUS)
                ),
                int(self.constants.BALL_RADIUS))
    # def level(self):
