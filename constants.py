"""
This module initializes the display and creates dictionaries of resources.
Also contained are various constants used throughout the program.
"""

import os
import pygame 

#Setup Display
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))

WINDOW_TITLE = "Ninja Run"
FPS = 60 

#Define Map stuff 
GRID_SIZE = 20
GRID_UNITS_X = int(SCREEN_WIDTH / GRID_SIZE)
GRID_UNITS_Y = SCREEN_HEIGHT / GRID_SIZE #REPLACE Y WITH PERLIN NOISE VALUES
MAP_UPDATE_INTERVAL = 10
PLAYER_START_CORD = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
PLATFORM_WIDTH = 75 #32
PLATFORM_HEIGHT = 12 #4
PLATFORM_PROBABILITY = 0.85 #Threshhold for random num generator to determine number of platforms
GENERATIONALGO = "random"

BACKGROUND_IMAGE_DIMENSIONS = [928, 600] #Width and Height of background image file, used for moving background
BACKGROUND_SCROLL_SPEED = 1 #Sets speed at which background moves


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
ASSETS_PATH = os.path.dirname(os.path.realpath( __file__ ))
ASSETS_PATH = os.path.join(ASSETS_PATH, "assets")
