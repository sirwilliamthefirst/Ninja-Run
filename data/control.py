import pygame as pg
import sys
import data.states.states as states
  
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock() 
        self.fps = 60
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.done = True
        self.state.get_event(events)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
            
  
  
