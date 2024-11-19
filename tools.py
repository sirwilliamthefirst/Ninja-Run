"""
This module contains the fundamental Control class.
Also contained here are resource loading functions.
"""

"""
A very basic base class that contains some commonly used functionality.
"""

import os
import pygame 

class collisionHandler():

    def check_collision(one, two):
        """
        This is a callback function to be used with sprite group collision methods.
        It initially checks if two sprites have overlapping rectangles. If this is
        True, it will check if their masks collide and return the result.  If the
        rectangles were not colliding, the mask check is not performed.
        """
        return pygame.sprite.collide_rect(one,two) and pg.sprite.collide_mask(one,two)
    
    def handle_verticle_collision(player, tiles):
        # Player's current vertical velocity (dy)
        dy = player.get_dy()
        key = pygame.key.get_pressed()
        # Flag to check if the player is on a tile
        on_tile = False

        # Iterate over all tiles to check for collisions
        for tile in tiles:
            # Check if the player is falling and intersecting with the top of the tile
            if player.rect.bottom <= tile[1].top and player.rect.bottom + dy >= tile[1].top and player.rect.right >= tile[1].left and player.rect.left <= tile[1].right :
                if dy >= 0:  # Only check for collisions if the player is moving downwards
                    if player.get_fall_thru():
                        # Allow player to drop through the tile when pressing the down key
                        continue
                    # Land on the tile
                    player.rect.bottom = tile[1].top
                    player.land()
                    on_tile = True
                    break

        # If the player is not on any tile, make them fall
        if not on_tile:
            player.fall()