import pygame as pg

class States(object):
    player_set = set()
    players = pg.sprite.Group()
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

    
  
