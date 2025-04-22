"""
This module initializes the display and creates dictionaries of resources.
Also contained are various constants used throughout the program.
"""


from enum import Enum
import os
import pygame 

#Setup Display 4/3 Aspect
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))

WIDTH_SCALE = SCREEN_WIDTH/800
HEIGHT_SCALE = SCREEN_HEIGHT/600

WINDOW_TITLE = "Ninja Run"
FPS = 60 

# Player Appearance
SPRITE_WIDTH = 50 * WIDTH_SCALE # Adjust ratios if needed
SPRITE_HEIGHT = 44 * HEIGHT_SCALE

#Define Map stuff 
GRID_SIZE = 120 * WIDTH_SCALE
GRID_UNITS_X = int(SCREEN_WIDTH // GRID_SIZE) 
GRID_UNITS_Y = int(SCREEN_HEIGHT / GRID_SIZE) #REPLACE Y WITH PERLIN NOISE VALUES
MAP_UPDATE_INTERVAL = 10
PLATFORM_WIDTH = 50 * WIDTH_SCALE #32
PLATFORM_AVRG_WIDTH = 80 * WIDTH_SCALE#32
PLATFORM_SPEED = -5 * WIDTH_SCALE #Negative because they move to the left -1 is good for tesing -5 is good tho i think
PLATFORM_WIDTH_DEVIATION = 20 * WIDTH_SCALE
PLATFORM_MIN_WIDTH = 45 * WIDTH_SCALE 
PLATFORM_HEIGHT = 20 * HEIGHT_SCALE  #4
TREE_WIDTH = 50 * WIDTH_SCALE
TREE_HEIGHT = SCREEN_HEIGHT
PLATFORM_PROBABILITY = 0.85 #Threshhold for random num generator to determine number of platforms
GENERATIONALGO = "forest"

BRANCH_NUM_LOWER = 3
BRANCH_NUM_HIGHER = 6
BRANCH_NUM_DEVIATION = 3 
BRANCH_MIN_SPACING = 40  * HEIGHT_SCALE#CAUTION: If to big, can cause infinite loop
 
BRANCH_HEIGHT_MEAN = int(500 * HEIGHT_SCALE)
BRANCH_HEIGHT_BOUND = int(100 * HEIGHT_SCALE)
BRANCH_HEIGHT_SCALE = int(200 * HEIGHT_SCALE)
BRANCH_HEIGHT_SKEW = int(-4 * HEIGHT_SCALE)



BACKGROUND_IMAGE_DIMENSIONS = [928 * WIDTH_SCALE, 600 * HEIGHT_SCALE] #Width and Height of background image file, used for moving background
BACKGROUND_SCROLL_SPEED = 5 * WIDTH_SCALE #Sets speed at which background moves


# Player Physics
BASE_SPEED = 5 * WIDTH_SCALE
MAX_SPEED = 5 * WIDTH_SCALE
GRAVITY = 0.8 * HEIGHT_SCALE
MAX_GRAVITY = 20 * HEIGHT_SCALE
AIRBORN_SHIFT = 0.7 * WIDTH_SCALE
VERTICLE_SHIFT = 0.4 * HEIGHT_SCALE
JUMP = -10 * HEIGHT_SCALE
DRAG_SPEED = 0.7 * WIDTH_SCALE
ATTACK_RATE = 25
COYOTE_TIME = 10


SPAWN_TREE = 3

# Tolerances and thresholds
FALL_THRU_TOLERENCE = 0.9 #how much to push down on the stick to fall thru a platform
DEADZONE = -100 #where the player dies if off the map


#assets path
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath( __file__ )))
ASSETS_PATH = os.path.join(BASE_PATH, "assets")

#Screen positions, Divided into 4:3 Aspect (x, y) * (WIDTH, HEIGHT)
SCREEN_COORDINATES = {
    "Top": {
        0: (0.0, 0.0),
        1: (0.125, 0.0),
        2: (0.25, 0.0),
        3: (0.375, 0.0),
        4: (0.5, 0.0),
        5: (0.625, 0.0),
        6: (0.75, 0.0),
        7: (0.875, 0.0),
        8: (1.0, 0.0),
    },
    "Upper_Center": {
        0: (0.0, 0.25),
        1: (0.125, 0.25),
        2: (0.25, 0.25),
        3: (0.375, 0.25),
        4: (0.5, 0.25),
        5: (0.625, 0.25),
        6: (0.75, 0.25),
        7: (0.875, 0.25),
        8: (1.0, 0.25),
    },
    "Middle": {
        0: (0.0, 0.5),
        1: (0.125, 0.5),
        2: (0.25, 0.5),
        3: (0.375, 0.5),
        4: (0.5, 0.5),
        5: (0.625, 0.5),
        6: (0.75, 0.5),
        7: (0.875, 0.5),
        8: (1.0, 0.5),
    },
    "Lower_Center": {
        0: (0.0, 0.75),
        1: (0.125, 0.75),
        2: (0.25, 0.75),
        3: (0.375, 0.75),
        4: (0.5, 0.75),
        5: (0.625, 0.75),
        6: (0.75, 0.75),
        7: (0.875, 0.75),
        8: (1.0, 0.75),
    },
    "Bottom": {
        0: (0.0, 1.0),
        1: (0.125, 1.0),
        2: (0.25, 1.0),
        3: (0.375, 1.0),
        4: (0.5, 1.0),
        5: (0.625, 1.0),
        6: (0.75, 1.0),
        7: (0.875, 1.0),
        8: (1.0, 1.0),
    },
}

SCREEN_POSITIONS = {
    key: {inner_key: (x * SCREEN_WIDTH, y * SCREEN_HEIGHT) for inner_key, (x, y) in sub_dict.items()}
    for key, sub_dict in SCREEN_COORDINATES.items()
}

PLAYER1_MENU_POS = SCREEN_POSITIONS["Lower_Center"][1]
PLAYER2_MENU_POS = SCREEN_POSITIONS["Lower_Center"][7]
MAX_PLAYERS = 2




class DeathType(Enum):
    FALL = "fall"
    ENEMY = "enemy"

class Actions(Enum):
    MOVE_X = "x_axis"
    MOVE_Y = "y_axis"
    JUMP_PRESS = "jump_press"
    JUMP_HOLD = "jump_hold"
    DASH = "dash"
    ATTACK = "attack"

DEFAULT_KEY_MAP = {
    Actions.JUMP_PRESS: pygame.K_SPACE,
    Actions.MOVE_X: [pygame.K_LEFT, pygame.K_RIGHT],
    Actions.MOVE_Y: [pygame.K_UP, pygame.K_DOWN],
    Actions.ATTACK: pygame.K_a,
    Actions.DASH: pygame.K_s
}

DEFAULT_JOY_MAP = {
    Actions.JUMP_PRESS: 0,
    Actions.MOVE_X: 0,
    Actions.MOVE_Y: 1,
    Actions.ATTACK: 2,
    Actions.DASH: 1
}
