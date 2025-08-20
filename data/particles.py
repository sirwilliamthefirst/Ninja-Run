import pygame
from random import randint
from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        pos: list[int],
        color: str,
        direction: pygame.math.Vector2,
        speed: int,
    ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 1000
        self.size = 4

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(
            surface=self.image,
            color=self.color,
            center=(self.size / 2, self.size / 2),
            radius=self.size / 2,
        )
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_pos(self):
        if (
            self.pos[0] < -50
            or self.pos[0] > SCREEN_WIDTH + 50
            or self.pos[1] < -50
            or self.pos[1] > SCREEN_HEIGHT + 50
        ):
            self.kill()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_pos()
        self.check_alpha()

class HealthParticles(Particle):
    def __init__(self, groups: pygame.sprite.Group, pos: list[int], color: str, direction: pygame.math.Vector2, speed: int):
        super().__init__(groups, pos, color, direction, speed)
        self.life

        
class ExplodingParticle(Particle):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        pos: list[int],
        color: str,
        direction: pygame.math.Vector2,
        speed: int,
    ):
        super().__init__(groups, pos, color, direction, speed)
        self.t0 = pygame.time.get_ticks()
        self.lifetime = randint(1000, 1200)
        self.exploding = False
        self.size = 4
        self.max_size = 50
        self.inflate_speed = 500
        self.fade_speed = 3000

    def explosion_timer(self):
        if not self.exploding:
            t = pygame.time.get_ticks()
            if t - self.t0 > self.lifetime:
                self.exploding = True

    def inflate(self, dt):
        self.size += self.inflate_speed * dt
        # self.create_surf()

    def check_size(self):
        if self.size > self.max_size:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.explosion_timer()
        if self.exploding:
            self.inflate(dt)
            self.fade(dt)

        self.check_pos()
        self.check_size()
        self.check_alpha()


class FloatingParticle(Particle):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        pos: list[int],
        color: str,
        direction: pygame.math.Vector2,
        speed: int,
    ):
        super().__init__(groups, pos, color, direction, speed)


class KunaiProjectile(Particle):
    """A kunai projectile that can be thrown by the player"""

    def __init__(self, x: float, y: float, vx: float, vy: float):
        # Create a simple kunai projectile using the particle system
        pos = [x, y]
        direction = pygame.math.Vector2(vx, vy).normalize()
        speed = (vx ** 2 + vy ** 2) ** 0.5

        # Create a temporary group for the kunai
        temp_group = pygame.sprite.Group()
        super().__init__(temp_group, pos, "silver", direction, speed)

        # Kunai-specific properties
        self.size = 8
        self.alpha = 255
        self.fade_speed = 0  # Don't fade
        self.lifetime = 3.0  # 3 seconds
        self.age = 0.0

        # Create kunai-shaped surface
        self.create_kunai_surf()

    def create_kunai_surf(self):
        """Create a kunai-shaped surface"""
        self.image = pygame.Surface((self.size * 2, self.size * 3)).convert_alpha()
        self.image.set_colorkey("black")

        # Draw kunai shape (simple triangle with handle)
        points = [
            (self.size, 0),  # Tip
            (0, self.size * 2),  # Left edge
            (self.size * 2, self.size * 2),  # Right edge
        ]
        pygame.draw.polygon(self.image, "silver", points)

        # Draw handle
        handle_rect = pygame.Rect(self.size - 2, self.size * 2, 4, self.size)
        pygame.draw.rect(self.image, "brown", handle_rect)

        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        """Update kunai position and age"""
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
            return

        # Move kunai
        self.move(dt)

        # Check if off screen
        self.check_pos()

    def check_pos(self):
        """Check if kunai is off screen"""
        if (
            self.pos[0] < -50
            or self.pos[0] > SCREEN_WIDTH + 50
            or self.pos[1] < -50
            or self.pos[1] > SCREEN_HEIGHT + 50
        ):
            self.kill()
