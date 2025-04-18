import pygame as pg

class States(object):
    player_set = set()
    players = pg.sprite.Group()
    joysticks = None

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        States.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]

    def move_state(self, next_state = None):
        if not next_state: return
        if next_state == "game": 
            if len(States.players) > 0:
                self.done = True
                self.next = next_state
                self.menu.close()
        else:
            self.done = True
            self.next = next_state
            self.menu.close()

    
  
