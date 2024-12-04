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

    def cleanup(self):
        print('cleaning up Main Menu state stuff')
    def startup(self):
        print('starting Main Menu state stuff')
        mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0) # transparent background

                )
        self.menu = pygame_menu.Menu('Ninja Run', c.SCREEN_WIDTH, c.SCREEN_HEIGHT,
                       theme=mytheme)

        self.player_enter_btn = self.menu.add.label("Press Any Button to join")
        #self.menu.add.button('Play', self.set_done)
        #self.menu.add.button('Quit', pygame_menu.events.EXIT)



    def get_event(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.quit = True
            if event.type == pg.JOYBUTTONDOWN and event.button == 7:
                States.player_set.add(event.instance_id)
                num_players = len(States.players)
                x, y = getattr(c, f"PLAYER{num_players+1}_MENU_POS")
                States.players.add(Player(x, y, self.joysticks  if self.joysticks and self.joysticks[0] else None))
            if event.type == pg.KEYDOWN:
                if not States.player_set.__contains__("Keyboard"):
                    States.player_set.add("Keyboard")
                    num_players = len(States.players)
                    x, y = getattr(c, f"PLAYER{num_players+1}_MENU_POS")
                    States.players.add(Player(x, y, freeze=True))
                elif len(States.players) > 0 and event.key == pg.K_RETURN:
                    self.set_done()
        self.menu.update(events)
    def update(self, screen, dt):
        if self.visible_counter >= self.visible_switch:
            if self.player_enter_btn.get_title() == "":
                self.player_enter_btn.set_title("Press Any Button")  # Show the label
            else:
                self.player_enter_btn.set_title("")  # Hide the label
            self.visible_counter = 0
        self.visible_counter += 1
        States.players.update()
        self.draw(screen)
        #print(len(States.player_set))
    def draw(self, screen):
        screen.fill((0,0,0))
        self.menu.draw(screen)
        States.players.draw(screen)
        #self.draw_menu(screen)

    def set_done(self):
        self.done = True
        self.menu.close()
        print("DONE!")
