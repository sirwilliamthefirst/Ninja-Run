import pygame as pg
import data.constants as c  # Import constants
import os

ATTACK_INTERVAL = 20
ATTACK_LENGTH = 20
IDLE_FRAMES = 1
ATTACK_FRAMES = 3
PREPARE_FRAMES = 1

class Samurai(pg.sprite.Sprite):
     # Class variable to hold shared images
    idle_images = []
    preparing_images = []
    attacking_images = []

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image_index = 0
        self.is_attacking = False

        if not Samurai.idle_images:
            self.load_images()

        self.rect = self.idle_images[0].get_rect()
        self.rect.topleft = [pos_x, pos_y]
        
        # Initial state
        self.state = "idle"
        self.image = self.idle_images[0]  # Default to first idle image

        # State timing control
        self.state_time = 0
        self.state_duration = {"idle": 1000, "preparing": 500, "attacking": 300}  # frames for each state


    def update(self):
        """ Update the enemy state and animation. """
        self.state_time += 1

        # Handle state transitions
        if self.state == "idle":
            self.handle_idle_state()
        elif self.state == "preparing":
            self.handle_preparing_state()
        elif self.state == "attacking":
            self.handle_attacking_state()
        self.shift(c.PLATFORM_SPEED, 0)

    def handle_idle_state(self):
        if self.state_time >= self.state_duration["idle"]:
            # Transition to preparing state
            self.state = "preparing"
            self.state_time = 0  # Reset timer
            self.image_index = 0  # Reset animation to first frame
            return
        # Animation for idle state
        self.image = self.idle_images[self.image_index]
        self.image_index = (self.image_index + 1) % len(self.idle_images)

    def handle_preparing_state(self):
        if self.state_time >= self.state_duration["preparing"]:
            # Transition to attacking state
            self.state = "attacking"
            self.state_time = 0
            self.image_index = 0
            self.is_attacking = True
            return
        # Animation for preparing state
        self.image = self.preparing_images[self.image_index]
        self.image_index = (self.image_index + 1) % len(self.preparing_images)

    def handle_attacking_state(self):
        self.is_attacking = True
        if self.state_time >= self.state_duration["attacking"]:
            # Transition back to idle state
            self.state = "idle"
            self.state_time = 0
            self.image_index = 0
            self.is_attacking = False
            return
        # Animation for attacking state
        self.image = self.attacking_images[self.image_index]
        self.image_index = (self.image_index + 1) % len(self.attacking_images)

    def load_images(self):

        for i in range(IDLE_FRAMES):
            self.idle_images.append(pg.image.load(os.path.join(c.ASSETS_PATH, f'enemy/samurai/Idle__{i}.png')).convert_alpha())

        for i in range(PREPARE_FRAMES):
            self.preparing_images.append(pg.image.load(os.path.join(c.ASSETS_PATH, f'enemy/samurai/Prepare__{i}.png')).convert_alpha())

        for i in range(ATTACK_FRAMES):
            self.attacking_images.append(pg.image.load(os.path.join(c.ASSETS_PATH, f'enemy/samurai/Attack__{i}.png')).convert_alpha())

    def shift(self, x, y):
        self.pos_x += x
        self.pos_y += y

        self.rect.bottom = self.pos_y
        self.rect.x = self.pos_x