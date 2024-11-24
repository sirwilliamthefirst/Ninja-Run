import pygame as pg
from ..map import *
from pygame.locals import *
from .states import States
import pygame_menu

class MenuManager:
    def __init__(self):
        pg.font.init()  # Initialize the font module
        self.selected_index = 0
        self.last_option = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,255)
        self.from_bottom = 200
        self.spacer = 75
    def draw_menu(self, screen):
        '''handle drawing of the menu options'''
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (screen.get_rect().centerx, self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])
         
    def update_menu(self):
        self.mouse_hover_sound()
        self.change_selected_option()
         
    def get_event_menu(self, event):
        if event.type == pg.KEYDOWN:
            '''select new index'''
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
                 
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        self.mouse_menu_click(event)
         
    def mouse_hover_sound(self):
        '''play sound when selected option changes'''
        for i,opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                if self.last_option != opt:
                    self.last_option = opt
    def mouse_menu_click(self, event):
        '''select menu option '''
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i,opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break
    def pre_render_options(self):
        '''setup render menu options based on selected or deselected'''
        font_deselect = pg.font.SysFont("arial", 50)
        font_selected = pg.font.SysFont("arial", 70)
 
        rendered_msg = {"des":[],"sel":[]}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, self.deselected_color)
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, self.selected_color)
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend,d_rect))
            rendered_msg["sel"].append((s_rend,s_rect))
        self.rendered = rendered_msg
 
    def select_option(self, i):
        '''select menu option via keys or mouse'''
        if i == len(self.next_list):
            self.quit = True
        else:
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0
 
    def change_selected_option(self, op=0):
        '''change highlighted menu option'''
        for i,opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                self.selected_index = i
        if op:
            self.selected_index += op
            max_ind = len(self.rendered['des'])-1
            if self.selected_index < 0:
                self.selected_index = max_ind
            elif self.selected_index > max_ind:
                self.selected_index = 0

class Menu(States, MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = 'game'
        self.options = ['Play', 'Quit']
        self.next_list = ['game']
        self.pre_render_options()   
        self.menu = None

    def cleanup(self):
        print('cleaning up Main Menu state stuff')
    def startup(self):
        print('starting Main Menu state stuff')
        self.menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input('Name :', default='John Doe')
        #self.menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
        self.menu.add.button('Play', self.set_done)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt):
        self.menu.mainloop(screen)
        return
        #self.update_menu()
        #self.draw(screen)
    def draw(self, screen):
        return
        #screen.fill((0,0,0))
        #self.draw_menu(screen)

