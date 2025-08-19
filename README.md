# Ninja Run
You are a ninja jumping through the trees! Do you best to not fall, and dodge (or kill 😈) your enemies! See how long you can survive for!

# Version 2.1.1: 
## Whats new
- Added Google Login
- Added Leaderboard for Highscores
### Minor fixes
- Fixed leaderboard access
- Added instructions to main menu

## Changes
- 

# Controls:
## Keyboard
Move: Arrow Keys

Attack: A

Jump: Space

Menu Select: Enter

Menu Join: Space

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
