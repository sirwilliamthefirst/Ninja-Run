import random
import pygame

from data import particles 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.collidable = False
        self.dead = False
        self.particle_group = pygame.sprite.Group()

    def is_collidable(self):
        return self.collidable
    
    def kill(self):
        for _ in range(50):
            pos = self.get_random_position_within()
            pixel = self.get_random_pixel()
            color = self.image.get_at(pixel)
            direction = pygame.math.Vector2(random.uniform(-0.2, 0.2), random.uniform(-1, 0))
            direction = direction.normalize()
            speed = random.randint(2, 5)
            particles.Particle(self.particle_group, pos, color, direction, speed)
            print(len(self.particle_group))
        self.image.set_alpha(0)

    def shift(self, x, y):
        self.pos_x += x
        self.pos_y += y

        self.rect.bottom = self.pos_y
        self.rect.x = self.pos_x