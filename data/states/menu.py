import pygame as pg

from data.player.player import Player
from ..map import *
from pygame.locals import *
from .states import States
import pygame_menu


class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        self.options = ['Play', 'Quit']
        self.next_list = ['game']
        self.menu = None
        self.visible_switch = 50
        self.visible_counter = 0 
        self.player_font = pg.font.Font(None, 36)
        self.text_dict = {}

    def cleanup(self):
        print('cleaning up Main Menu state stuff')
    def startup(self):
        print('starting Main Menu state stuff')
        mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0) # transparent background

                )
        self.menu = pygame_menu.Menu('Ninja Run', c.SCREEN_WIDTH, c.SCREEN_HEIGHT,
                       theme=mytheme)

        
        self.player_enter_btn = self.menu.add.label("Press Any Button to join")
        self.game_start_btn = self.menu.add.label("")
        #self.menu.add.button('Play', self.set_done)
        #self.menu.add.button('Quit', pygame_menu.events.EXIT)



    def get_event(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.quit = True
            if event.type == pg.JOYBUTTONDOWN:
                if not States.player_set.__contains__(event.instance_id):
                    self.add_player(event.instance_id)
                elif event.button == 7:
                    self.set_done() 
            if event.type == pg.KEYDOWN:
                if not States.player_set.__contains__("Keyboard"):
                    self.add_player()
                elif len(States.players) > 0 and event.key == pg.K_RETURN:
                    self.set_done()
        self.menu.update(events)
    def update(self, screen, dt):
        if self.visible_counter >= self.visible_switch:
            if self.player_enter_btn.get_title() == "":
                self.player_enter_btn.set_title("Press Any Button to Join")  # Show the label
            else:
                self.player_enter_btn.set_title("")  # Hide the label
            self.visible_counter = 0
        self.visible_counter += 1
        if len(States.players) > 0:
            self.game_start_btn.set_title("Press Enter/Start to start game")
        States.players.update()
        self.draw(screen)
        #print(len(States.player_set))
    def draw(self, screen):
        screen.fill((0,0,0))
        self.menu.draw(screen)
        States.players.draw(screen)
        for label, text in self.text_dict.items():
            x, y = getattr(c, f"{label}_MENU_POS")
            print(x, y)
            screen.blit(text, (x * 0.8, y *1.1))

    def set_done(self):
        self.done = True
        self.menu.close()
        print("DONE!")


    #CAUTION: Does not check if player is already added
    def add_player(self, joystick_id = None):
        joystick = None
        if not joystick_id == None:
            States.player_set.add(joystick_id)
            joystick = next(stick for stick in States.joysticks if joystick_id == stick.get_id())
        else:
            States.player_set.add("Keyboard")
        num_players = len(States.players)
        x, y = getattr(c, f"PLAYER{num_players+1}_MENU_POS")
        States.players.add(Player(x, y, joystick, freeze=True))
