import pygame as pg
from data.constants import Actions, DEFAULT_KEY_MAP, DEFAULT_JOY_MAP # Import constants

class input_handler():
    def __init__(self, joystick : pg.Joystick | None = None, 
                 keyboard_mapping : dict[Actions, int] = DEFAULT_KEY_MAP,
                 joystick_mapping : dict[Actions, int] = DEFAULT_JOY_MAP):
        self.joystick = joystick
        self.keys = None
        self.pressed_keys = None
        self.j_state = None
        self.j_pressed = None
        self.old_keys = None
        self.old_j_state = None
        self.control_map = keyboard_mapping if not joystick else joystick_mapping 
        
        pass

    def get_inputs(self) -> dict[Actions, float]: 
        action_dict = {}
        if not self.joystick:
            self.old_keys = self.keys
            self.keys = pg.key.get_pressed()
            self.pressed_keys = [key for key in self.keys if self.old_keys[key]] 
            button_state = self.keys
            pressed_state = self.pressed_keys

        else:
            self.old_j_state = self.j_state
            self.j_state = {i: self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())}
            self.j_pressed = [key for key, value in self.j_state.items() if value and key in self.old_j_state]
            button_state = self.j_state
            pressed_state = self.j_pressed
        
        axis = self.get_axis()
        action_dict[Actions.MOVE_X] = axis[0]
        action_dict[Actions.MOVE_Y] = axis[1]
        action_dict[Actions.JUMP_HOLD] = pressed_state[self.control_map[Actions.JUMP_HOLD]]
        action_dict[Actions.ATTACK] = button_state[self.control_map[Actions.ATTACK]] 
        action_dict[Actions.DASH] = button_state[self.control_map[Actions.DASH]] 

        return action_dict

    def get_axis(self) -> tuple[int, int]:
        if self.joystick:
            return (self.joystick.get_axis(0), self.joystick.get_axis(1))
        else:
           return self.keys[pg.K_RIGHT] - self.keys[pg.K_LEFT]


    
