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
    def cleanup(self):
        print('cleaning up Game state stuff')
        States.player_set.clear()
        States.players.empty()
        
    def startup(self):
        print('starting Game state stuff')
        #look for joysticks
        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        for player in States.players:
            player.unfreeze()
        #create sprites and groups
        #self.players = pg.sprite.Group()
        #self.player1 = Player(c.SCREEN_WIDTH/2, c.SCREEN_HEIGHT/2, self.joysticks[0] if self.joysticks and self.joysticks[0] else None)
        #self.moving_sprites.add(self.player1)

        #get map
        self.stage = MapBuilder(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GRID_UNITS_X, 3) 

        # Timing
        self.last_map_update = pygame.time.get_ticks()

    def get_event(self, events):
        return
        #print(events)
        #for event in events:
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                #if self.player1.get_controller_id() == None:
                    #self.doubleJumpers.append(self.player1)
                
                

            
        
    def update(self, screen, dt):
        self.draw(screen)
        current_time = pygame.time.get_ticks()
    
        if current_time - self.last_map_update > c.MAP_UPDATE_INTERVAL:
            self.stage.update()
            #for player in self.doubleJumpers:
                #player.doubleJump()
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
  