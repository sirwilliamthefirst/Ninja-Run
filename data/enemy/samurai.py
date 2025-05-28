import random
import pygame as pg
import data.constants as c  # Import constants
import os

from .enemy import Enemy

ATTACK_INTERVAL = 20
ATTACK_LENGTH = 20
IDLE_FRAMES = 1
ATTACK_FRAMES = 3
PREPARE_FRAMES = 1
class Samurai(Enemy):
     # Class variable to hold shared images
    idle_images = []
    preparing_images = []
    attacking_images = []
    def __init__(self, pos_x, pos_y, worth=20):
        super().__init__(worth)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image_index = 0

        if not Samurai.idle_images:
            self.load_images()

        self.rect = self.idle_images[0].get_rect()
        self.rect.bottom = pos_y
        self.rect.centerx = pos_x
        
        # Initial state
        self.state = "idle"
        self.image = self.idle_images[0]  # Default to first idle image

        # State timing control
        self.state_time = random.randint(0,40)
        self.state_duration = {"idle": 0.8, "preparing": 0.5, "attacking": 0.15}  # seconds for each state


    def update(self, dt):
        """ Update the enemy state and animation. """
        if(not self.dead):
            self.state_time += dt
            # Handle state transitions
            if self.state == "idle":
                self.handle_idle_state()
            elif self.state == "preparing":
                self.handle_preparing_state()
            elif self.state == "attacking":
                self.handle_attacking_state()
            self.move_ip(c.PLATFORM_SPEED * dt, 0)
        elif(len(self.particle_group) == 0):
            self.kill()
        self.particle_group.update(dt)

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
            return
        # Animation for preparing state
        self.image = self.preparing_images[self.image_index]
        self.image_index = (self.image_index + 1) % len(self.preparing_images)

    def handle_attacking_state(self):
        self.collidable = True
        if self.state_time >= self.state_duration["attacking"]:
            # Transition back to idle state
            self.state = "idle"
            self.state_time = 0
            self.image_index = 0
            self.collidable = False
            return
        # Animation for attacking state
        self.image = self.attacking_images[self.image_index]
        self.image_index = (self.image_index + 1) % len(self.attacking_images)

    def load_images(self):

        for i in range(IDLE_FRAMES):
            image = pg.image.load(os.path.join(c.ASSETS_PATH, f'enemy/samurai/Idle__{i}.png')).convert_alpha()
            image = pg.transform.scale(image, (image.get_width() * c.WIDTH_SCALE, image.get_height() * c.HEIGHT_SCALE))
            self.idle_images.append(image)

        for i in range(PREPARE_FRAMES):
            image = pg.image.load(os.path.join(c.ASSETS_PATH, f'enemy/samurai/Prepare__{i}.png')).convert_alpha()
            image = pg.transform.scale(image, (image.get_width() * c.WIDTH_SCALE, image.get_height() * c.HEIGHT_SCALE))
            self.preparing_images.append(image)

        for i in range(ATTACK_FRAMES):
            image = pg.image.load(os.path.join(c.ASSETS_PATH, f'enemy/samurai/Attack__{i}.png')).convert_alpha()
            image = pg.transform.scale(image, (image.get_width() * c.WIDTH_SCALE, image.get_height() * c.HEIGHT_SCALE))
            self.attacking_images.append(image)

