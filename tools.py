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
        key=lambda tile: abs(tile[1].top - player.rect.bottom) if player.rect.right > tile[1].left and player.rect.left < tile[1].right else float('inf')
    )
        #print([abs(tile[1].top - player.rect.bottom) for tile in sorted_tiles])

        for tile in sorted_tiles:
            # Check if the player is falling and intersecting with the top of the tile
            if (player.rect.bottom) <= tile[1].top <= player.rect.bottom + dy and player.rect.right >= tile[1].left and player.rect.left <= tile[1].right:
                if dy >= 0:  # Only check for collisions if the player is moving downwards
                    # Land on the tile
                    player.rect.bottom = tile[1].top
                    player.land()
                    on_tile = True

                    return
        
        if not on_tile:
            player.fall()