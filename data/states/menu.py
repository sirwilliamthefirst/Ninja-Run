import pygame as pg
import pygame_menu.controls

from data.player.player import Player
from ..map import *
from pygame.locals import *
from .states import States
import pygame_menu

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
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

        self.player_enter_btn = self.menu.add.label("Press Enter/Start to join")
        self.game_start_btn = self.menu.add.label("")
        self.menu.add.button('Play', lambda: self.move_state("game"))
        self.menu.add.button('Leaderboard') #placeholder
        self.menu.add.button('Settings') #placeholder
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def get_event(self, events):
        self.menu.update(events)
        for event in events:
            if event.type == pg.QUIT:
                self.quit = True
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 7:
                    self.add_player(event.instance_id)

            if event.type == pg.KEYDOWN:
                if not States.player_set.__contains__("Keyboard") and event.key == pg.K_RETURN:
                    self.add_player()

    def update(self, screen, dt):
        if self.visible_counter >= self.visible_switch:
            if self.player_enter_btn.get_title() == "":
                self.player_enter_btn.set_title("Press Enter/Start to join")  # Show the label
            else:
                self.player_enter_btn.set_title("")  # Hide the label
            self.visible_counter = 0
        self.visible_counter += 1
        States.players.update(dt)
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,0))
        self.menu.draw(screen)
        States.players.draw(screen)
        for label, text in self.text_dict.items():
            x, y = getattr(c, f"{label}_MENU_POS")
            screen.blit(text, (x * 0.8, y *1.1))

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
