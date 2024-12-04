"""
This module initializes the display and creates dictionaries of resources.
Also contained are various constants used throughout the program.
"""


import os
import pygame 

#Setup Display 4/3 Aspect
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))

WINDOW_TITLE = "Ninja Run"
FPS = 60 

#Define Map stuff 
GRID_SIZE = 120
GRID_UNITS_X = SCREEN_WIDTH // GRID_SIZE
GRID_UNITS_Y = SCREEN_HEIGHT / GRID_SIZE #REPLACE Y WITH PERLIN NOISE VALUES
MAP_UPDATE_INTERVAL = 10
PLAYER_START_CORD = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
PLATFORM_WIDTH = 50 #32
PLATFORM_AVRG_WIDTH = 50 #32
PLATFORM_SPEED = -1 #Negative because they move to the left
PLATFORM_WIDTH_DEVIATION = 20
PLATFORM_HEIGHT = 8 #4
TREE_WIDTH = 50
TREE_HEIGHT = SCREEN_HEIGHT
PLATFORM_PROBABILITY = 0.85 #Threshhold for random num generator to determine number of platforms
GENERATIONALGO = "forest"

BRANCH_AVRG_NUM = 7
BRANCH_NUM_DEVIATION = 3
BRANCH_MIN_SPACING = 20




BACKGROUND_IMAGE_DIMENSIONS = [928, 600] #Width and Height of background image file, used for moving background
BACKGROUND_SCROLL_SPEED = 5 #Sets speed at which background moves


# Player Physics
BASE_SPEED = 5
MAX_SPEED = 5
GRAVITY = 0.8
MAX_GRAVITY = 20
AIRBORN_SHIFT = 0.7
VERTICLE_SHIFT = 0.4
JUMP = -10
DRAG_SPEED = 0.7

# Tolerances and thresholds
FALL_THRU_TOLERENCE = 0.9 #how much to push down on the stick to fall thru a platform

# Player Appearance
SPRITE_WIDTH = 50  # Adjust ratios if needed
SPRITE_HEIGHT = 44

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