import sys
import pygame as pg
import data.constants as c  # Import constants
import data.control as control
import data.states as states


settings = {
    'size':(c.SCREEN_WIDTH, c.SCREEN_HEIGHT),
    'fps' :c.FPS
}
  
app = control.Control(**settings)
state_dict = {
    'menu': states.Menu(),
    'game': states.Game()
}
pg.init()
pg.font.init()  # Initialize the font module
pg.joystick.init()

#I think this may be a bug with pygame but, joystick events are not tracked until they are placed in an object.. so we do that here
for i in range(pg.joystick.get_count()):
    joystick = pg.joystick.Joystick(i)  # Access the first joystick
    print(f"Joystick initialized: {joystick.get_name()}")

pg.display.set_caption('Ninja Run')
app.setup_states(state_dict, 'menu')
app.main_game_loop()
pg.quit()
sys.exit()