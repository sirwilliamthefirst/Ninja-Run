from typing import Union
import pygame as pg
from pygame._sdl2 import controller
from data.constants import Actions, DEFAULT_KEY_MAP, DEFAULT_JOY_MAP  # Import constants


class Input_handler:
    def __init__(
        self,
        joystick: Union[controller.Controller, None] = None,
        keyboard_mapping: dict[Actions, int] = DEFAULT_KEY_MAP,
        joystick_mapping: dict[Actions, int] = DEFAULT_JOY_MAP,
    ):
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
            self.pressed_keys = {
                i
                for i, key in enumerate(self.keys)
                if self.old_keys and self.old_keys[i]
            }

            button_state = self.keys
            pressed_state = self.pressed_keys

        else:
            self.old_j_state = self.j_state
            self.j_state = {
                i: self.joystick.get_button(i) for i in range(pg.CONTROLLER_BUTTON_MAX)
            }
            self.j_pressed = {
                i
                for i, key in enumerate(self.j_state)
                if self.old_j_state and self.old_j_state[i]
            }
            # self.j_pressed = {key: value for key, value in self.j_state.items() if self.old_j_state and value}
            button_state = self.j_state
            pressed_state = self.j_pressed

        # Joysticks can return a value between -32768 and 32767. Triggers however can only return a value between 0 and 32768.
        axis = self.get_axis()

        action_dict[Actions.MOVE_X] = axis[0]
        action_dict[Actions.MOVE_Y] = axis[1]

        if (
            Actions.JUMP_PRESS in self.control_map
            and self.control_map[Actions.JUMP_PRESS] in pressed_state
        ):
            action_dict[Actions.JUMP_HOLD] = 1
            action_dict[Actions.JUMP_PRESS] = 0
        elif button_state[self.control_map[Actions.JUMP_PRESS]]:
            action_dict[Actions.JUMP_HOLD] = 0
            action_dict[Actions.JUMP_PRESS] = 1
        else:
            action_dict[Actions.JUMP_HOLD] = 0
            action_dict[Actions.JUMP_PRESS] = 0
        action_dict[Actions.ATTACK] = (
            1 if button_state[self.control_map[Actions.ATTACK]] else 0
        )
        action_dict[Actions.SKILL] = (
            1 if button_state[self.control_map[Actions.SKILL]] else 0
        )

        return action_dict

    def get_axis(self) -> tuple[int, int]:
        if self.joystick:
            return (
                self.joystick.get_axis(pg.CONTROLLER_AXIS_LEFTX) / 32767,
                self.joystick.get_axis(pg.CONTROLLER_AXIS_LEFTY) / 32767,
            )
        else:
            return (
                self.keys[pg.K_RIGHT] - self.keys[pg.K_LEFT],
                self.keys[pg.K_DOWN] - self.keys[pg.K_UP],
            )
