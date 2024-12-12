import pygame as pg

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.collidable = False

    def is_collidable(self):
        return self.collidable