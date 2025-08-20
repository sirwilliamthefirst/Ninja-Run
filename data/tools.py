"""
This module contains the fundamental Control class.
Also contained here are resource loading functions.
"""

"""
A very basic base class that contains some commonly used functionality.
"""

import os
import pygame as pg
import math

EPSILON = 0.1


class collisionHandler:

    def check_collision(one, two):
        """
        This is a callback function to be used with sprite group collision methods.
        It initially checks if two sprites have overlapping rectangles. If this is
        True, it will check if their masks collide and return the result.  If the
        rectangles were not colliding, the mask check is not performed.
        """
        return pg.sprite.collide_rect(one, two)  # and pg.sprite.collide_mask(one,two)

    """
    Iterate over all tiles to check if player collides
    """

    def handle_verticle_collision(player, tiles):
        if player.get_fall_thru():
            return

        dy = math.ceil(player.get_dy())
        on_tile = False

        sorted_tiles = sorted(
            tiles,
            key=lambda tile: (
                abs(tile.get_rect().top - player.rect.bottom)
                if player.rect.right > tile.get_rect().left
                and player.rect.left < tile.get_rect().right
                else float("inf")
            ),
        )

        collision_left_bound = (player.rect.centerx + player.rect.left) / 2
        collision_right_bound = (player.rect.centerx + player.rect.right) / 2
        for tile in sorted_tiles:
            tile_rect = tile.get_rect()
            # Check if the player is falling and intersecting with the top of the tile
            if (
                (player.rect.bottom) <= tile_rect.top <= player.rect.bottom + dy
                and collision_right_bound >= tile_rect.left
                and collision_left_bound <= tile_rect.right
            ):
                if (
                    dy >= 0
                ):  # Only check for collisions if the player is moving downwards
                    # Land on the tile
                    player.rect.bottom = tile_rect.top
                    player.land()
                    on_tile = True
                    return

        if not on_tile:
            player.fall()


class sprite_loader:

    def load_sprites(folder_path, file_prefix, frames, width=None, height=None):
        sprites_sequence = []
        for i in range(frames):
            image = pg.image.load(
                os.path.join(folder_path, f"{file_prefix}__{i}.png")
            ).convert_alpha()
            if width and height:
                image = pg.transform.scale(image, (width, height))
            sprites_sequence.append(image)
        return sprites_sequence


def drawTextRightJustified(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    rect = img.get_rect(topright = (x, y))
    screen.blit(img, rect)


class HealthBar():
    def __init__(self, x, y, w, h, value, max_value = None, barC = "blue", backC = "red"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.barC = barC
        self.backC = backC
        self.value = value
        self.max_value = max_value if max_value else value

    def draw(self, surface):
        #calculate health ratio
        ratio = self.value / self.max_value
        pg.draw.rect(surface, self.backC, (self.x, self.y, self.w, self.h))
        pg.draw.rect(surface, self.barC, (self.x, self.y, self.w * ratio, self.h))

    def move(self, x,y):
        self.x = x
        self.y = y
    
    def transform(self, w, h):
        self.w = w
        self.h = h

    def set_value(self, value):
        self.value = value