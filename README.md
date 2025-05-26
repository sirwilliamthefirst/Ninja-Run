# Ninja Run
You are a ninja jumping through the trees! Do you best to not fall, and dodge (or kill 😈) your enemies! See how long you can survive for!

# Version 2.0: Whats new
-PVP mode + Co-op mode (appear once conditions met)

-Player death animiation + time after death to check score

-Starting platforms

-Samurai Enemy

-Attack button for player

-Adjusted backwards movement to be more responsive

-New logic for double jump momentum calculation

-Score addition text on enemy kill

# Controls:
## Keyboard
Move: Arrow Keys

Attack: A

Jump: Space

## Xbox Controller
Move: Left joystick

Attack: X

Jump: A

## Playstation Controller
Move: Left joystick

Attack: Square

Jump: X

# Running the game
Run `python main.py` to start the game, or build the game and run the .exe (if windows) or .app (for macos)

# Building the game
```bash
pip install -r requirements.txt
pyinstaller --onefile --noconsole --add-data "assets:assets" ninja_run.py
```
