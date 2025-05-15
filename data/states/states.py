from enum import Enum
import pygame 
import pygame_menu

class Game_States(Enum):
        GAME = "game"
        MENU = "menu"
        LEADERBOARD = "leaderboard"
class States(object):
    player_set = set()
    players = pygame.sprite.Group()
    joysticks = None

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        States.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    def move_state(self, next_state : str = None):
        if not next_state: return
        if next_state == Game_States.GAME.value: 
            if len(States.players) > 0:
                self.done = True
                self.next = next_state
                self.menu.close()
        else:
            self.done = True
            self.next = next_state
            self.menu.close()

    
  
