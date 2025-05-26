import pygame as pg
from data.player.player import Player
from ..map import *
from pygame.locals import *
from .states import Game_States, States
import pygame_menu
from data.api.client import APIClient
 

class Menu(States):


    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        self.menu = None
        self.visible_switch = 50
        self.visible_counter = 0 
        self.text_dict = {}

    def cleanup(self):
        print('cleaning up Main Menu state stuff')
    def startup(self):
        print('starting Main Menu state stuff')
        mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0) # transparent background

                )
        self.menu = pygame_menu.Menu('Ninja Run', c.SCREEN_WIDTH, c.SCREEN_HEIGHT,
                       theme=mytheme)
        States.pvp_flag = False
        self.player_enter_btn = self.menu.add.label("Press Enter/Start to join")
        self.game_start_btn = self.menu.add.label("")
        self.make_menu_buttons(self.menu)
        self.in_use_colors = set()

    def get_event(self, events):
        self.menu.update(events)
        for event in events:
            if event.type == pg.QUIT:
                self.quit = True
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 7 and not States.player_set.__contains__(event.instance_id):
                    self.add_player(event.instance_id)
                    if(len(States.players) > 0):
                        self.make_menu_buttons(self.menu)
                        self.menu.force_surface_update()


            if event.type == pg.KEYDOWN:
                if not States.player_set.__contains__("Keyboard") and event.key == pg.K_RETURN:
                    self.add_player()
                    if(len(States.players) > 0):
                        self.make_menu_buttons(self.menu)
                        self.menu.force_surface_update()

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
        if len(States.players) == 0: # If this is the second player, get available colors
            self.available_colors = Player.get_available_colors()
            print(f"Available colors: {self.available_colors}")
         # Get colors already in use
        decide_color = next((color for color in self.available_colors if color not in self.in_use_colors), None)
        if decide_color is not None:
            self.in_use_colors.add(decide_color)
        else:
            decide_color = "default"
        joystick = None
        if joystick_id != None:
            States.player_set.add(joystick_id)
            joystick = next(stick for stick in States.joysticks if joystick_id == stick.get_id())
        else:
            States.player_set.add("Keyboard")
        num_players = len(States.players)
        x, y = getattr(c, f"PLAYER{num_players+1}_MENU_POS")
        States.players.add(Player(x, y, joystick, freeze=True, player_num=num_players+1, color=decide_color))

    def start_pvp(self):
        States.pvp_flag = True
        self.move_state(Game_States.GAME.value)

    def make_menu_buttons(self, menu):
        menu.clear()
        if len(States.players) == 1:
            menu.add.button('Play', lambda: self.move_state(Game_States.GAME.value))
        elif len(States.players) > 1:
            menu.add.button('Play (Co-op)', lambda: self.move_state(Game_States.GAME.value))
            pvp_button = menu.add.button("PVP", lambda: self.start_pvp())
            pvp_button.set_font(c.PVP_FONT_PATH, 30, (120, 6, 6), (255,255,255), (120, 6, 6), (255,255,255), None, False)  # Change the font color to red
        menu.add.button('Leaderboard', lambda: self.move_state("leaderboard")) #placeholder
        menu.add.button('Settings') #placeholder
        menu.add.button('Quit', pygame_menu.events.EXIT)


class Leaderboard(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.menu = None
        self.visible_switch = 50
        self.visible_counter = 0 
        self.text_dict = {}

    def cleanup(self):
        print('cleaning up Leaderboard menu state stuff')
    def startup(self):
        mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0) # transparent background

                )
        self.menu = pygame_menu.Menu('Leaderboard', c.SCREEN_WIDTH, c.SCREEN_HEIGHT,
                       theme=mytheme)

        #NOTE Get entries
        leaderboard_data= APIClient.get_scores()
        if "error" in leaderboard_data:
            self.menu.add.label("Error fetching leaderboard data")
        else:
            self.leaderboard_table = self.menu.add.table()
            self.leaderboard_table.add_row(["Name","Score"], cell_padding=[20,20,5,5])
            for item in sorted(leaderboard_data, key=lambda x: x['score'], reverse=True)[:5]:
                self.leaderboard_table.add_row([item['name'], item['score']], cell_padding=[20,20,5,5])


        self.menu.add.button('Back', lambda: self.move_state("menu"))


    def get_event(self, events):
        self.menu.update(events)
       
    def update(self, screen, dt):
        self.draw(screen)
        
    def draw(self, screen):
        screen.fill((0,0,0))
        self.menu.draw(screen)


       
