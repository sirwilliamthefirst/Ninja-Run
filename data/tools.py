"""
This module contains the fundamental Control class.
Also contained here are resource loading functions.
"""

"""
A very basic base class that contains some commonly used functionality.
"""

import os
import pygame 
import math

EPSILON = 0.1

class pixelFinder():
    
    def get_pixel_position(row: str, column: int, screen_width: int, screen_height: int):
        x_multiplier, y_multiplier = POSITIONS[row][column]
        return int(x_multiplier * screen_width), int(y_multiplier * screen_height)


class collisionHandler():

    def check_collision(one, two):
        """
        This is a callback function to be used with sprite group collision methods.
        It initially checks if two sprites have overlapping rectangles. If this is
        True, it will check if their masks collide and return the result.  If the
        rectangles were not colliding, the mask check is not performed.
        """
        return pygame.sprite.collide_rect(one,two) and pg.sprite.collide_mask(one,two)
    

    """
    Iterate over all tiles to check if player collides
    """
    def handle_verticle_collision(player, tiles):
        if player.get_fall_thru():
            #print("FALL!")
            return
        
        dy = math.ceil(player.get_dy())
        on_tile = False

        sorted_tiles = sorted(
        tiles,
        key=lambda tile: abs(tile.get_rect().top - player.rect.bottom) if player.rect.right > tile.get_rect().left and player.rect.left < tile.get_rect().right else float('inf')
    )
        #print([abs(tile[1].top - player.rect.bottom) for tile in sorted_tiles])

        for tile in sorted_tiles:
            tile_rect = tile.get_rect()
            # Check if the player is falling and intersecting with the top of the tile
            if (player.rect.bottom) <= tile_rect.top <= player.rect.bottom + dy and player.rect.right >= tile_rect.left and player.rect.left <= tile_rect.right:
                if dy >= 0:  # Only check for collisions if the player is moving downwards
                    # Land on the tile
                    player.rect.bottom = tile_rect.top
                    player.land()
                    on_tile = True
                    return
        
        if not on_tile:
            player.fall()