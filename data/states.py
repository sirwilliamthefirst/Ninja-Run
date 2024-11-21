import pygame as pg
from .player import Player
import data.tools as tools
from .map import *
from pygame.locals import *
import data.constants as c  # Import constants
import data.control as control
  
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
  
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
  
class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
        #look for joysticks
        pg.joystick.init()
        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]

        #create sprites and groups
        self.moving_sprites = pg.sprite.Group()
        self.player1 = Player(c.SCREEN_WIDTH/2, c.SCREEN_HEIGHT/2, self.joysticks[0] if self.joysticks and self.joysticks[0] else None)
        self.moving_sprites.add(self.player1)

        #get map
        self.stage = MapBuilder(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GRID_UNITS_X, 3, self.player1) 

        # Timing
        self.last_map_update = pygame.time.get_ticks()

    def get_event(self, event):
        return
    def update(self, screen, dt):
        self.draw(screen)
        current_time = pygame.time.get_ticks()
    
        if current_time - self.last_map_update > c.MAP_UPDATE_INTERVAL:
            self.stage.update()
            self.moving_sprites.update()
            tools.collisionHandler.handle_verticle_collision(self.player1, self.stage.get_map())
        
            self.player1.drag()
            self.last_map_update = current_time
            if self.player1.is_dead():
                self.done = True
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.stage.draw(screen)
        self.moving_sprites.draw(screen)
  