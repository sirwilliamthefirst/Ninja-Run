import random
import pygame
import sys
import os
import data.constants as c  # Import constants
import data.particles as particles
from enum import Enum

RUN_SPRITE_FRAMES = 10
JUMP_SPRITE_FRAMES = 10
ATTACK_SPRITE_FRAMES = 10


class DeathType(Enum):
    FALL = "fall"
    ENEMY = "enemy"

class Player(pygame.sprite.Sprite): #maybe make an object class that player inherits that inherits sprites
    def __init__(self, pos_x, pos_y, joystick = None, freeze = False):
        super().__init__()
        # Find our path
        self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        self.joystick = joystick
        # Get the sprites
        self.__spritify()
        self.is_airborn = False
        self.is_jumping = False
        self.is_attacking = False
        self.attack_cooldown = c.ATTACK_RATE
        self.can_doubleJump = True
        self.current_sprite = 0
        self.image = self.runSprites[self.current_sprite] #init as running
        self.image = pygame.transform.scale(self.image, (c.SPRITE_WIDTH, c.SPRITE_HEIGHT)) 
        self.rect = self.image.get_rect()
        self.fall_thru = False
        #set position and keep track
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.y_vel = 0
        self.x_vel = 0
        self.rect.topleft = [pos_x, pos_y]
        self.old_keys = pygame.key.get_pressed()
        self.old_joystick = dict()
        self.freeze = freeze
        self.dead = False
        self.done_dying = False
        self.particle_group = pygame.sprite.Group()
        

    def attack(self):
        if(not self.is_attacking and self.attack_cooldown >= c.ATTACK_RATE):
            self.attack_cooldown = 0
            self.current_sprite = 0
            self.image = self.attackSprites[0]
            self.is_attacking = True


    def handle_move(self):
        if not self.is_airborn:
            self.x_vel = 0
            self.y_vel = 0
        if(self.joystick):
            self.handle_joystick()
        else:
            self.handle_keys()

        self.handle_gravity()

        self.pos_x += self.x_vel
        self.pos_y += self.y_vel
        self.rect.bottom = self.pos_y
        self.rect.x = self.pos_x

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.bottom = x
        self.rect.x = y

    def handle_joystick(self):
        x_axis = self.joystick.get_axis(0) #left negative right pos
        y_axis = self.joystick.get_axis(1)
        if self.is_airborn and ((x_axis > 0 and self.x_vel < c.MAX_SPEED) or (x_axis < 0 and self.x_vel > -c.MAX_SPEED)):
            self.x_vel += c.AIRBORN_SHIFT * x_axis
        elif(not self.is_airborn):
                self.x_vel += c.BASE_SPEED * x_axis
        self.handle_joystick2()
        #if self.joystick.get_button(0):
         #   if(self.is_airborn):
          #      self.y_vel += -c.VERTICLE_SHIFT
           # else:
            #    self.jump()
        """
        if y_axis < 0:
            if self.is_airborn:
                self.y_vel += c.VERTICLE_SHIFT * y_axis
        """
        if y_axis > 0:
            if self.is_airborn:
                self.y_vel += c.VERTICLE_SHIFT * abs(y_axis)
            if y_axis > c.FALL_THRU_TOLERENCE: #some tolerance, so player must really press on joystick
                    self.fall_thru = True
                    self.is_airborn = True #drop from platform
            else:
                self.fall_thru = False  

    def handle_keys2(self, keys):
        mapping = {
            pygame.K_SPACE: "jump",
        }
        pressed_keys = [key for key in mapping.keys() if keys[key]]
        for pressed_key in pressed_keys:
            if not self.old_keys[pressed_key]:
                getattr(self, f"{mapping[pressed_key]}_press")()
            else:
                getattr(self, f"{mapping[pressed_key]}_hold")()
        self.old_keys = keys

    def handle_joystick2(self):
        mapping = {
            0: "jump",
            }
        joystick_state = {i: self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())}
        pressed_keys  = [key for key, value in joystick_state.items() if value and key in mapping]
        for pressed_key in pressed_keys:
            if not self.old_joystick.get(pressed_key, False):
                getattr(self, f"{mapping[pressed_key]}_press")()
            else:
                getattr(self, f"{mapping[pressed_key]}_hold")()
        self.old_joystick = joystick_state

    def jump_press(self):
       self.jump()
    
    def jump_hold(self):
        if(self.is_airborn):
            self.y_vel += -c.VERTICLE_SHIFT
        else:
            self.jump()

    def handle_keys(self):
        key = pygame.key.get_pressed()
        self.handle_keys2(key)
        event = pygame.event.get()
        if key[pygame.K_RIGHT]:
            if self.is_airborn and self.x_vel < c.MAX_SPEED:
                self.x_vel += c.AIRBORN_SHIFT
            elif(not self.is_airborn):
                self.x_vel += c.BASE_SPEED
        if key[pygame.K_LEFT]:
            if self.is_airborn and self.x_vel > -c.MAX_SPEED:
                self.x_vel += -c.AIRBORN_SHIFT
            elif(not self.is_airborn):
                self.x_vel += -c.BASE_SPEED
        #if key[pygame.K_SPACE]:
        #    if(self.is_airborn):
        #        self.y_vel += -c.VERTICLE_SHIFT
        #        if self.can_doubleJump:
        #            self.jump()
        #    else:
        #        self.jump()
        if key[pygame.K_UP] and self.is_airborn:
            self.y_vel += -c.VERTICLE_SHIFT
        if key[pygame.K_DOWN]:
            self.fall_thru = True
            if self.is_airborn:
                self.y_vel += c.VERTICLE_SHIFT
            else:
                self.is_airborn = True #drop from platform
        else:
            self.fall_thru = False  
        if key[pygame.K_a]:
            self.attack()  

    def handle_gravity(self):
        if self.is_airborn:
            if self.y_vel < c.MAX_GRAVITY:
                self.y_vel += c.GRAVITY

        
    # Update sprite animation
    def update(self, dt):
        if(not self.dead):
            if self.freeze == False:
                self.handle_move()
                if self.pos_y > c.SCREEN_HEIGHT or self.pos_x < c.DEADZONE:
                    self.kill(c.DeathType.FALL)
            if self.attack_cooldown < c.ATTACK_RATE:
                self.attack_cooldown += 1
            self.animate()
        self.particle_group.update(1)
        if(self.dead and len(self.particle_group) == 0):
            self.done_dying = True

        
    def jump(self):
        if(not self.is_jumping and not self.is_airborn):
            self.is_jumping = True
            self.y_vel = c.JUMP
            self.is_airborn = True
            #reset current sprite and make it the fist jump
            self.current_sprite = 0
            self.image = self.jumpSprites[self.current_sprite]
        elif(self.can_doubleJump and self.is_airborn):
            self.y_vel = c.JUMP
            self.current_sprite = 0
            self.image = self.jumpSprites[self.current_sprite]
            self.can_doubleJump = False 


    def animate(self):
        if(self.is_attacking):
            self.current_sprite += 1
            self.image = self.attackSprites[self.current_sprite]
            if(self.current_sprite == ATTACK_SPRITE_FRAMES - 1):
                self.is_attacking = False
        elif(self.is_airborn):
            if(self.is_jumping and self.current_sprite >= 5):
                self.is_jumping = False
                self.current_sprite = 5
            elif(self.current_sprite >= 7):
                self.current_sprite = 5
            else:
                self.current_sprite += 1
            self.image = self.jumpSprites[self.current_sprite]
        else: #Then we are running, if not airborn
            self.current_sprite += 1
            if(self.current_sprite >= len(self.runSprites)):
                self.current_sprite = 0
            self.image = self.runSprites[self.current_sprite]
            
        self.image = pygame.transform.scale(self.image, (c.SPRITE_WIDTH, c.SPRITE_HEIGHT))  

    def __spritify(self):
        # Set run Sprites
        self.runSprites = []
        #NOTE: This method will cause a problem if more than 10 frames exist
        for i in range(RUN_SPRITE_FRAMES):
            self.runSprites.append(pygame.image.load(os.path.join(c.ASSETS_PATH, f'player/Run__{i}.png')).convert_alpha())

        self.jumpSprites = []
        for i in range(JUMP_SPRITE_FRAMES):
            self.jumpSprites.append(pygame.image.load(os.path.join(c.ASSETS_PATH, f'player/Jump__{i}.png')).convert_alpha())

        self.attackSprites = []
        for i in range(ATTACK_SPRITE_FRAMES):
            self.attackSprites.append(pygame.image.load(os.path.join(c.ASSETS_PATH, f'player/Attack__{i}.png')).convert_alpha())


    def drag(self):
        if(not self.is_airborn):
            self.pos_x += -c.DRAG_SPEED

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
        self.can_doubleJump = True
        self.y_vel = 0

    def fall(self):
        self.is_airborn = True
    
    def get_fall_thru(self):
        return self.fall_thru
    
    def is_dead(self):
        return self.dead
    
    def is_done_dying(self):
        return self.done_dying
    
    def kill(self, death_type: DeathType):
        if(self.dead):
            return
        match death_type:
            case c.DeathType.FALL:
                print("Fell off a cliff.")
            case c.DeathType.ENEMY:
                print("Explode.")
                for _ in range(50):
                    pos = self.get_random_position_within()
                    pixel = self.get_random_pixel()
                    color = self.image.get_at(pixel)
                    direction = pygame.math.Vector2(random.uniform(-0.2, 0.2), random.uniform(-1, 0))
                    direction = direction.normalize()
                    speed = random.randint(2, 5)
                    particles.Particle(self.particle_group, pos, color, direction, speed)
                    print(len(self.particle_group))
                self.image.set_alpha(0)
            case _:
                print("Unknown death.")
        self.dead = True

    #Get a random position within the player rect
    def get_random_position_within(self):
        random_x = random.randint(self.rect.left, self.rect.right)
        random_y = random.randint(self.rect.top, self.rect.bottom)
        return random_x, random_y
    
    def get_random_pixel(self):
        size = self.image.get_size()
        random_x = random.randint(0, size[0]-1)
        random_y = random.randint(0, size[1]-1)
        return random_x, random_y
    

    def get_controller_id(self):
        return self.joystick.get_guid() if self.joystick else None
    
    