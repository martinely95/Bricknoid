import unittest
import pygame
from draw import Draw
from load_levels import Levels


class TestDraw(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.clock.tick(70)  # slow down
        self.drawer = Draw()
        self.constants = self.drawer.constants

    def test_show_menu(self):
        running = True
        while running:
            self.drawer.menu()
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    running = False

    def test_show_instructions(self):
        running = True
        while running:
            self.drawer.instructions()
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    running = False

    def test_show_bricks(self):
        running = True
        self.levels = Levels()
        self.levels.load_level(1)
        level = self.levels.return_loaded_level()
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
        while running:
            self.drawer.bricks(self.bricks)
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_q]:
                    running = False

if __name__ == '__main__':
    unittest.main()
