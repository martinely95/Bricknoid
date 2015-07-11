class GameConstants:

    def __init__(self):
        # screen
        self.SCREEN_SIZE = 960, 540
        self.CENTER_COORDS = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / 2)

        # objects
        self.BRICK_WIDTH = 60
        self.BRICK_HEIGHT = 15
        self.PADDLE_WIDTH = 120
        self.PADDLE_HEIGHT = 12
        self.BALL_DIAMETER = 10
        self.BALL_RADIUS = self.BALL_DIAMETER / 2

        self.MIN_BRICKS_X = self.SCREEN_SIZE[0] / 5
        self.MAX_PADDLE_X = self.SCREEN_SIZE[0] - self.PADDLE_WIDTH
        self.MIN_PADDLE_X = 0
        self.MAX_BALL_X = self.SCREEN_SIZE[0] - self.BALL_DIAMETER
        self.MAX_BALL_Y = self.SCREEN_SIZE[1] - self.BALL_DIAMETER
        self.MIN_BALL_X = self.BALL_DIAMETER
        self.MIN_BALL_Y = self.BALL_DIAMETER

        self.PADDLE_Y = self.SCREEN_SIZE[1] - self.PADDLE_HEIGHT - 10

        # colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.BRICK_COLOR = (0, 255, 0)  # GREEN

        # states
        self.STATES = {  # upon integration in v3.0
            "BALL_IN_PADDLE": 0,
            "PLAYING": 1,
            "WON": 2,
            "GAME_OVER": 3,
            "CHANGING_LEVEL": 4
        }

        # game
        self.NEW_GAME = (1, 0, 3)
        self.INIT_BALL_VEL = (1, -1)
        self.BALL_VEL_COEF = 1
