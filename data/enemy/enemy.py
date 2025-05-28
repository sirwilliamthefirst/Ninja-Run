import random
import pygame

from data import particles


class Enemy(pygame.sprite.Sprite):
    def __init__(self, worth=20):
        super().__init__()
        self.collidable = False
        self.dead = False
        self.particle_group = pygame.sprite.Group()
        self.worth = worth

    def is_collidable(self):
        if not self.dead:
            return self.collidable
        return False

    def is_dead(self):
        return self.dead

    def draw_particles(self, screen):
        self.particle_group.draw(screen)

    def get_rect(self):
        return self.rect

    def get_worth(self):
        return self.worth

    def die(self):
        for _ in range(50):
            pos = self.get_random_position_within()
            pixel = self.get_random_pixel()
            color = self.image.get_at(pixel)
            direction = pygame.math.Vector2(
                random.uniform(-0.2, 0.2), random.uniform(-1, 0)
            )
            direction = direction.normalize()
            speed = random.randint(120, 300)

            particles.Particle(self.particle_group, pos, color, direction, speed)
        self.dead = True
        self.image = self.image.copy()
        self.image.set_alpha(0)

    def move_ip(self, x, y):
        self.rect.move_ip(x, y)

    def get_random_position_within(self):
        random_x = random.randint(self.rect.left, self.rect.right)
        random_y = random.randint(self.rect.top, self.rect.bottom)
        return random_x, random_y

    def get_random_pixel(self):
        size = self.image.get_size()
        random_x = random.randint(0, size[0] - 1)
        random_y = random.randint(0, size[1] - 1)
        return random_x, random_y
