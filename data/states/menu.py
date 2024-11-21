import pygame as pg
from ..map import *
from pygame.locals import *
from .states import States

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
    def cleanup(self):
        print('cleaning up Menu state stuff')
    def startup(self):
        print('starting Menu state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
  
