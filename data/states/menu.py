import pygame as pg
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

    def cleanup(self):
        print('cleaning up Main Menu state stuff')
    def startup(self):
        print('starting Main Menu state stuff')
        mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0) # transparent background

                )
        self.menu = pygame_menu.Menu('Ninja Run', c.SCREEN_WIDTH, c.SCREEN_HEIGHT,
                       theme=mytheme)

        self.menu.add.button('Play', self.set_done)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)



    def get_event(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.quit = True
            if event.type == pg.JOYBUTTONDOWN:
                States.player_set.add(event.instance_id)
            if event.type == pg.KEYDOWN:
                States.player_set.add("Keyboard")


        self.menu.update(events)
    def update(self, screen, dt):
        self.draw(screen)
        #print(len(States.player_set))
    def draw(self, screen):
        screen.fill((0,0,0))
        self.menu.draw(screen)
        #self.draw_menu(screen)

    def set_done(self):
        self.done = True
        self.menu.close()
        print("DONE!")
