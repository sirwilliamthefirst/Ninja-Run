import random
import pygame
import numpy
import os
import data.constants as c  # Import constants
import data.particles as particles
from data.player.input_handler import Input_handler
from data.tools import sprite_loader
from pygame._sdl2 import controller

RUN_SPRITE_FRAMES = 10
JUMP_SPRITE_FRAMES = 10
ATTACK_SPRITE_FRAMES = 10

MAX_CHAKRA = 100
STARTING_CHAKRA = 20
CHAKRA_REGEN_RATE = 0.5  # per second


def load_sprites(self):
    # Set run Sprites
    runSprites = sprite_loader.load_sprites(
        os.path.join(c.ASSETS_PATH, f"player_{self.player_num}"),
        "Run",
        RUN_SPRITE_FRAMES,
        c.SPRITE_WIDTH,
        c.SPRITE_HEIGHT,
    )
    jumpSprites = sprite_loader.load_sprites(
        os.path.join(c.ASSETS_PATH, f"player_{self.player_num}"),
        "Jump",
        JUMP_SPRITE_FRAMES,
        c.SPRITE_WIDTH,
        c.SPRITE_HEIGHT,
    )
    attackSprites = sprite_loader.load_sprites(
        os.path.join(c.ASSETS_PATH, f"player_{self.player_num}"),
        "Attack",
        ATTACK_SPRITE_FRAMES,
        c.SPRITE_WIDTH,
        c.SPRITE_HEIGHT,
    )


class Player(
    pygame.sprite.Sprite
):  # maybe make an object class that player inherits that inherits sprites
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        joystick: controller = None,
        freeze: bool = False,
        player_num: int = 1,
        color: str = "default",
    ):
        super().__init__()
        # Find our path
        # self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        self.player_num = player_num
        self.joystick = joystick
        self.input_handler = Input_handler(joystick)
        # Get the sprites
        self.color = color
        self.load_sprites(self.color)
        self.is_airborn = False
        self.is_jumping = False
        self.attacking = False
        self.attack_cooldown = c.ATTACK_RATE
        self.can_doubleJump = True
        self.current_sprite = 0
        self.image = self.sprites["run"][self.current_sprite]  # init as running
        self.rect = self.image.get_rect()
        self.fall_thru = False
        # set position and keep track
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.y_vel = 0
        self.x_vel = 0
        self.rect.topleft = [pos_x, pos_y]
        self.freeze = freeze
        self.dead = False
        self.coyote_timer = 0
        self.done_dying = False
        self.particle_group = pygame.sprite.Group()
        self.chakra = STARTING_CHAKRA

    # Update sprite animation
    def update(self, dt):
        if not self.dead:
            if self.freeze == False:
                self.handle_move(dt)
                self.animate(dt)
                if self.pos_y > c.DEADZONE_Y or self.pos_x < c.DEADZONE_X:
                    self.kill(c.DeathType.FALL)
            else:
                self.animate(dt)
            if self.attack_cooldown < c.ATTACK_RATE:
                self.attack_cooldown += dt
        self.particle_group.update(dt)
        if self.dead and len(self.particle_group) == 0:
            self.done_dying = True
        if self.is_airborn:
            self.coyote_timer += dt
        else:
            self.coyote_timer = 0

    def attack(self, dt: float):
        if not self.attacking and self.attack_cooldown >= c.ATTACK_RATE * dt:
            self.attack_cooldown = 0
            self.current_sprite = 0
            self.image = self.sprites["attack"][0]
            self.attacking = True

    def change_color(self, new_color: str):
        """Change player color"""
        if new_color == self.color:
            return True

        # Check if color is available
        available_colors = GlobalSpriteManager.get_available_colors(self.player_num)
        if new_color not in available_colors:
            print(f"Color '{new_color}' not available for player {self.player_num}")
            return False

        # Load new sprites (will use cache if already loaded)
        old_color = self.color
        self.color = new_color

        if self.load_sprites():
            print(f"Player {self.player_num} changed from {old_color} to {new_color}")
            return True
        else:
            # Revert on failure
            self.color = old_color
            self.load_sprites()
            return False

    @classmethod
    def get_available_colors(self):
        """Get available colors for this player"""
        return GlobalSpriteManager.get_available_colors()

    def load_sprites(self, color="default"):
        """Load sprites using the global manager"""
        self.sprites = GlobalSpriteManager.load_player_sprites(color)
        if not self.sprites:
            print(
                f"Failed to load sprites for player {self.player_num} with color {self.color}"
            )
            return False
        return True

    def handle_gravity(self, dt):
        if self.is_airborn:
            if self.y_vel < c.MAX_GRAVITY:
                self.y_vel += c.GRAVITY * dt

    def handle_move(self, dt):
        if not self.is_airborn:
            self.x_vel = 0
            self.y_vel = 0

        intent_dict = self.input_handler.get_inputs()
        dx = intent_dict[c.Actions.MOVE_X]
        dy = intent_dict[c.Actions.MOVE_Y]
        Speed_addition = (
            c.MAX_LEFT_SPEED if dx < 0 else c.MAX_RIGHT_SPEED if dx > 0 else 0
        )
        if self.is_airborn and not self.double_jumped_frame:
            self.x_vel = numpy.clip(
                self.x_vel + (c.AIRBORN_SHIFT * dx * dt),
                -c.MAX_LEFT_SPEED * dt,
                c.MAX_RIGHT_SPEED * dt,
            )
        else:
            self.x_vel = numpy.clip(
                self.x_vel + (Speed_addition * dx * dt),
                -c.MAX_LEFT_SPEED * dt,
                c.MAX_RIGHT_SPEED * dt,
            )

        if dy > 0:
            if self.is_airborn:
                self.y_vel += c.VERTICLE_SHIFT * abs(dy) * dt
            if (
                dy > c.FALL_THRU_TOLERENCE
            ):  # some tolerance, so player must really press on joystick
                self.fall_thru = True
                self.is_airborn = True  # drop from platform
        else:
            self.fall_thru = False
        self.double_jumped_frame = False
        if intent_dict[c.Actions.ATTACK]:
            self.attack(dt)
        if intent_dict[c.Actions.JUMP_PRESS]:
            self.jump_press(dt)
        if intent_dict[c.Actions.JUMP_HOLD]:
            self.jump_hold(dt)
        # if intent_dict[c.Actions.ABILITY_1]: self.abilty_1(self.ability,dt)
        if (
            not intent_dict[c.Actions.JUMP_HOLD]
            and not intent_dict[c.Actions.JUMP_PRESS]
            and self.y_vel < 0
        ):
            self.is_jumping = False
            self.y_vel *= c.JUMP_CUT_MULT  # * dt
        self.handle_gravity(dt)
        self.pos_x += self.x_vel
        self.pos_y += self.y_vel
        self.rect.bottom = self.pos_y
        self.rect.x = self.pos_x

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.bottom = y
        self.rect.x = x

    def jump_press(self, dt):
        self.jump(dt)

    def jump_hold(self, dt):
        if self.is_airborn and self.is_jumping and self.jump_timer < c.JUMP_TIME:
            self.y_vel = c.JUMP * dt
            self.jump_timer += dt

    def jump(self, dt):
        if not self.is_jumping and (
            not self.is_airborn or self.coyote_timer < c.COYOTE_TIME
        ):
            self.jump_timer = 0
            self.is_jumping = True
            self.y_vel = c.JUMP * dt
            self.is_airborn = True
            # reset current sprite and make it the fist jump
            self.coyote_timer = c.COYOTE_TIME
            self.current_sprite = 0
            self.image = self.sprites["jump"][self.current_sprite]
        elif self.can_doubleJump and self.is_airborn:
            self.jump_timer = c.JUMP_TIME / 2
            self.is_jumping = True
            self.y_vel = c.JUMP * dt
            self.current_sprite = 0
            self.image = self.sprites["jump"][self.current_sprite]
            self.can_doubleJump = False
            self.double_jumped_frame = True

    def animate(self, dt):
        animation_speed = 60  # Adjust this value to change animation speed
        if self.attacking:
            self.current_sprite += dt * animation_speed
            current_sprite_int = int(self.current_sprite)
            if current_sprite_int >= ATTACK_SPRITE_FRAMES - 1:
                self.attacking = False
                self.image = self.sprites["run"][current_sprite_int]
            else:
                self.image = self.sprites["attack"][current_sprite_int]
        elif self.is_airborn:
            if self.current_sprite >= 7:
                self.current_sprite = 5
            else:
                self.current_sprite += dt * animation_speed
            current_sprite_int = int(self.current_sprite)
            self.image = self.sprites["jump"][current_sprite_int]
        else:  # Then we are running, if not airborn
            self.current_sprite += dt * animation_speed
            if self.current_sprite >= len(self.sprites["run"]):
                self.current_sprite = 0
            current_sprite_int = int(self.current_sprite)    
            self.image = self.sprites["run"][current_sprite_int]

    def drag(self, dt):
        if not self.is_airborn:
            self.pos_x += -c.DRAG_SPEED * dt

    def draw_particles(self, screen):
        self.particle_group.draw(screen)

    def get_dy(self):
        return self.y_vel

    def freeze(self):
        self.freeze = True

    def unfreeze(self):
        self.freeze = False

    def land(self):
        self.is_airborn = False
        self.is_jumping = False
        self.can_doubleJump = True
        self.y_vel = 0

    def fall(self):
        self.is_airborn = True

    def get_fall_thru(self):
        return self.fall_thru

    def is_dead(self):
        return self.dead

    def is_attacking(self):
        return self.attacking

    def is_done_dying(self):
        return self.done_dying

    def kill(self, death_type: c.DeathType):
        if self.dead:
            return
        match death_type:
            case c.DeathType.FALL:
                print("Fell off a cliff.")
                for _ in range(50):
                    pos = self.get_random_position_within()
                    pixel = self.get_random_pixel()
                    color = self.image.get_at(pixel)
                    direction = pygame.math.Vector2(
                        random.uniform(-0.2, 0.2), random.uniform(-1, 0)
                    )
                    direction = direction.normalize()
                    speed = random.randint(120, 300)
                    particles.Particle(
                        self.particle_group, pos, color, direction, speed
                    )
                if self.joystick:
                    self.joystick.rumble(0.5, 0.5, 500)  # Rumble for 1 second
            case c.DeathType.ENEMY:
                print("Explode.")
                for _ in range(50):
                    pos = self.get_random_position_within()
                    pixel = self.get_random_pixel()
                    color = self.image.get_at(pixel)
                    direction = pygame.math.Vector2(
                        random.uniform(-0.2, 0.2), random.uniform(-1, 0)
                    )
                    direction = direction.normalize()
                    speed = random.randint(120, 300)
                    particles.Particle(
                        self.particle_group, pos, color, direction, speed
                    )
            case _:
                print("Unknown death.")
        self.dead = True
        self.image.set_alpha(0)

    # Get a random position within the player rect
    def get_random_position_within(self):
        random_x = random.randint(self.rect.left, self.rect.right)
        random_y = random.randint(self.rect.top, self.rect.bottom)
        return random_x, random_y

    def get_random_pixel(self):
        size = self.image.get_size()
        random_x = random.randint(0, size[0] - 1)
        random_y = random.randint(0, size[1] - 1)
        return random_x, random_y

    def get_controller_id(self):
        return self.joystick.get_guid() if self.joystick else None


class ISkill:
    def use(self, target=None):
        pass


class Ninja_Time(ISkill):
    def __init__(self, player):
        self.player = player
        self.cooldown = 0
        self.active = False
        self.duration = 5
        self.start_time = 0

    def use(self, target=None):
        if self.cooldown <= 0:
            self.active = True
            self.start_time = pygame.time.get_ticks()
            self.cooldown = 10  # Set cooldown time in seconds


class GlobalSpriteManager:
    """Global sprite manager for multiple players with multiple colors"""

    _sprite_cache = {}
    _available_colors = []
    _initialized = False

    @classmethod
    def initialize(cls):
        """Initialize the sprite manager and scan for available sprites"""
        if cls._initialized:
            return

        print("Initializing Global Sprite Manager...")
        cls._scan_available_sprites()
        cls._initialized = True
        print(f"Found sprites for {len(cls._available_colors)} players")

    @classmethod
    def _scan_available_sprites(cls):
        """Scan the assets directory for available player sprites"""
        base_path = c.ASSETS_PATH
        available_colors = ["default"]
        common_colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "orange",
            "pink",
            "cyan",
            "black",
            "white",
        ]

        # Check for colored variants
        common_colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "orange",
            "pink",
            "cyan",
            "black",
            "white",
        ]
        for color in common_colors:
            color_path = os.path.join(base_path, "players", f"player_{color}")
            if os.path.exists(color_path):
                available_colors.append(color)

        if available_colors:
            cls._available_colors = available_colors

    @classmethod
    def load_player_sprites(cls, color="default"):
        """Load and cache sprites for a specific player and color"""
        if not cls._initialized:
            cls.initialize()

        cache_key = f"player_{color}"

        # Return cached sprites if already loaded
        if cache_key in cls._sprite_cache:
            return cls._sprite_cache[cache_key]

        # Build sprite path
        if color == "default":
            sprite_path = os.path.join(c.ASSETS_PATH, "players", f"player")
        else:
            sprite_path = os.path.join(c.ASSETS_PATH, "players", f"player_{color}")

        # Check if path exists
        if not os.path.exists(sprite_path):
            print(f"Sprite path not found: {sprite_path}")
            return None

        # Load sprites
        try:
            sprites = {
                "run": sprite_loader.load_sprites(
                    sprite_path,
                    "Run",
                    RUN_SPRITE_FRAMES,
                    c.SPRITE_WIDTH,
                    c.SPRITE_HEIGHT,
                ),
                "jump": sprite_loader.load_sprites(
                    sprite_path,
                    "Jump",
                    JUMP_SPRITE_FRAMES,
                    c.SPRITE_WIDTH,
                    c.SPRITE_HEIGHT,
                ),
                "attack": sprite_loader.load_sprites(
                    sprite_path,
                    "Attack",
                    ATTACK_SPRITE_FRAMES,
                    c.SPRITE_WIDTH,
                    c.SPRITE_HEIGHT,
                ),
            }

            # Cache the loaded sprites
            cls._sprite_cache[cache_key] = sprites
            print(f"Loaded sprites for player {color})")
            return sprites

        except Exception as e:
            print(f"Error loading sprites for player {color}: {e}")
            return None

    @classmethod
    def preload_all_sprites(cls):
        """Preload all available sprite combinations"""
        if not cls._initialized:
            cls.initialize()

        total_loaded = 0
        for color in cls._available_colors:
            if cls.load_player_sprites(color):
                total_loaded += 1

        print(f"Preloaded {total_loaded} sprite sets")

    @classmethod
    def get_available_colors(cls):
        """Get list of available colors for a player"""
        if not cls._initialized:
            cls.initialize()

        return cls._available_colors

    @classmethod
    def clear_cache(cls):
        """Clear the sprite cache to free memory"""
        cls._sprite_cache.clear()
        print("Sprite cache cleared")

    @classmethod
    def get_cache_info(cls):
        """Get information about cached sprites"""
        return {
            "cached_combinations": len(cls._sprite_cache),
            "available_players": len(cls._available_colors),
        }
