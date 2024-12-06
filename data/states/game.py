import pygame as pg
from .states import States
from ..player import Player
import data.tools as tools
from ..map import *
from pygame.locals import *
import data.constants as c  # Import constants

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.map_spawn_counter = 0
        self.unit_size = c.SCREEN_WIDTH/c.GRID_UNITS_X
    def cleanup(self):
        print('cleaning Game state')
        States.player_set.clear()
        States.players.empty()
        self.map_spawn_counter = 0

        
    def startup(self):
        print('starting Game state')
        #look for joysticks
        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
    
        #get map
        self.stage = MapBuilder(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GRID_UNITS_X) 
        self.stage.generate(c.GENERATIONALGO)
        #self.stage.generate() #USe this for random stage select... at some point, make a stage select screen and build there


        for player in States.players:
            spawn_tree = self.stage.get_tree(c.SPAWN_TREE)
            spawn_branch = spawn_tree.get_middle_branch()
            x, y = spawn_branch.get_top_center()
            print(player.rect.bottom, spawn_branch.get_top_center())
            player.unfreeze()
            player.move(x, y)
            print(player.rect.x, player.rect.bottom)

        # Timing
        self.last_map_update = pygame.time.get_ticks()

    def get_event(self, events):
        return
          
    def update(self, screen, dt):
        self.draw(screen)
        current_time = pygame.time.get_ticks()
    
        if current_time - self.last_map_update > c.MAP_UPDATE_INTERVAL:
            self.stage.update()

            if self.map_spawn_counter >= self.unit_size:
                tree = self.stage.create_tree()
                self.map_spawn_counter = 0
                # TODO: SPAWN ENEMIES
            self.map_spawn_counter += abs(c.PLATFORM_SPEED)


            States.players.update()
            for player in States.players:
                tools.collisionHandler.handle_verticle_collision(player, self.stage.get_map())
                player.drag()
            self.last_map_update = current_time
            if all(player.is_dead() for player in States.players):
                self.done = True
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.stage.draw(screen)
        States.players.draw(screen)
  