from enum import Enum
import pygame
from pygame._sdl2 import controller
from data.api.supabase_client import LeaderboardClient
import pygame_menu

class Game_States(Enum):
    GAME = "game"
    MENU = "menu"
    LEADERBOARD = "leaderboard"


class States(object):
    player_set = set()
    players = pygame.sprite.Group()
    joysticks = None
    pvp_flag = False
    leaderboard = LeaderboardClient()
    username = None
    new_user_menu = None
    new_user_flow_active = False

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        States.joysticks = []
        
        for x in range(controller.get_count()):
            try:
                States.joysticks.append(x)    
            except Exception as e:
                print(f"⚠ Controller subsystem unavailable: {e}")

    def move_state(self, next_state: str = None):
        if not next_state:
            return
        if next_state == Game_States.GAME.value:
            if len(States.players) > 0:
                self.done = True
                self.next = next_state
                self.menu.close()
        else:
            self.done = True
            self.next = next_state
            self.menu.close()

    @staticmethod
    def login():
        if States.leaderboard.sign_in_with_oauth():
            States.username = States.leaderboard.get_username()
            if States.username is None:
                print("New user flow")
                # Pop up a menu to ask for profile name
                def set_profile_name(value, id):
                    # Save the username to the backend
                    # You may need to implement a method in LeaderboardClient to set the username
                    try:
                        # This assumes you have a method to set the username in your backend
                        States.leaderboard.set_username(value, id)
                        print(f"Username set to {value}")
                        if States.new_user_menu:
                            States.new_user_menu.disable()
                    except Exception as e:
                        print(f"Error setting username: {e}")

                # Create a popup menu for username input
                theme = pygame_menu.Theme(
                    background_color=(0, 0, 0, 180),
                    title_background_color=(30, 30, 30),
                    title_font_size=30,
                    widget_font_size=24,
                )
                States.new_user_menu = pygame_menu.Menu(
                    "Create Profile", 400, 250, theme=theme, position=(50,50,True)
                )
                States.new_user_menu.add.label("Enter your profile name:")
                States.new_user_menu.add.text_input("Name: ", onchange=None, textinput_id="name")
                States.new_user_menu.add.button("Submit", lambda: set_profile_name(
                    States.new_user_menu.get_input_data()["name"], States.leaderboard.get_user_id()
                ))
                States.new_user_menu.add.button("Cancel", lambda: States.new_user_menu.disable())
                # To show the menu, you must call States.new_user_menu.mainloop(screen) in your main loop
                # or integrate it into your state update/draw logic.
        else:
            print("Login failed!")
        
    @staticmethod
    def logout():
        States.leaderboard.sign_out()
        States.username = None