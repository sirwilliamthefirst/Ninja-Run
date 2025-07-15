from enum import Enum
import pygame
from pygame._sdl2 import controller
from data.api.supabase_client import LeaderboardClient

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
    user = None

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        States.joysticks = [
            controller.Controller(x) for x in range(controller.get_count())
        ]

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

    def login():
        States.leaderboard.sign_in_with_oauth()
        username = States.leaderboard.get_username()
        if username is None:
            print("New user flow")
        # Here you would typically show a login dialog or redirect to a login screen
        # and handle the authentication process.

