import random
import pygame
import numpy
import os
import data.constants as c  # Import constants
import data.particles as particles
from data.player.input_handler import Input_handler
from data.tools import sprite_loader

RUN_SPRITE_FRAMES = 10  
JUMP_SPRITE_FRAMES = 10
ATTACK_SPRITE_FRAMES = 10

class Player(pygame.sprite.Sprite): #maybe make an object class that player inherits that inherits sprites
    def __init__(self, pos_x, pos_y, joystick = None, freeze = False):
        super().__init__()
        # Find our path
        #self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        self.joystick = joystick
        self.input_handler = Input_handler(joystick)
        # Get the sprites
        self.load_sprites()
        self.is_airborn = False
        self.is_jumping = False
        self.attacking = False
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
        self.freeze = freeze
        self.dead = False
        self.coyote_timer = 0
        self.done_dying = False
        self.particle_group = pygame.sprite.Group()
        

    def attack(self):
        if(not self.attacking and self.attack_cooldown >= c.ATTACK_RATE):
            self.attack_cooldown = 0
            self.current_sprite = 0
            self.image = self.attackSprites[0]
            self.attacking = True

    def handle_move(self):
        if not self.is_airborn:
            self.x_vel = 0
            self.y_vel = 0
        
        intent_dict = self.input_handler.get_inputs()
        delta_x = intent_dict[c.Actions.MOVE_X]
        delta_y = intent_dict[c.Actions.MOVE_Y]
        if self.is_airborn:
            self.x_vel = numpy.clip(self.x_vel + (c.AIRBORN_SHIFT * delta_x), -c.MAX_SPEED, c.MAX_SPEED)
        else:
             self.x_vel = numpy.clip(self.x_vel + (c.BASE_SPEED * delta_x), -c.MAX_SPEED, c.MAX_SPEED)
        
        if delta_y > 0:
            if self.is_airborn:
                self.y_vel += c.VERTICLE_SHIFT * abs(delta_y)
            if delta_y > c.FALL_THRU_TOLERENCE: #some tolerance, so player must really press on joystick
                    self.fall_thru = True
                    self.is_airborn = True #drop from platform
        else:
            self.fall_thru = False 
        
        if intent_dict[c.Actions.ATTACK]: self.attack()
        if intent_dict[c.Actions.JUMP_PRESS]: self.jump_press()
        if intent_dict[c.Actions.JUMP_HOLD]: self.jump_hold()
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

   
    def jump_press(self):
       self.jump()
    
    def jump_hold(self):
        if(self.is_airborn):
            self.y_vel += -c.VERTICLE_SHIFT
        else:
            self.jump()

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
        if(self.is_airborn):
            self.coyote_timer += 1
        else:
            self.coyote_timer = 0

        
    def jump(self):
        if(not self.is_jumping and (not self.is_airborn or self.coyote_timer < c.COYOTE_TIME)):
            self.is_jumping = True
            self.y_vel = c.JUMP
            self.is_airborn = True
            #reset current sprite and make it the fist jump
            self.coyote_timer = c.COYOTE_TIME
            self.current_sprite = 0
            self.image = self.jumpSprites[self.current_sprite]
        elif(self.can_doubleJump and self.is_airborn):
            self.y_vel = c.JUMP
            self.current_sprite = 0
            self.image = self.jumpSprites[self.current_sprite]
            self.can_doubleJump = False 

    def animate(self):
        if(self.attacking):
            self.current_sprite += 1
            self.image = self.attackSprites[self.current_sprite]
            if(self.current_sprite == ATTACK_SPRITE_FRAMES - 1):
                self.attacking = False
        elif(self.is_airborn):
            if(self.current_sprite >= 7):
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

    def load_sprites(self):
        # Set run Sprites
        self.runSprites = sprite_loader.load_sprites(os.path.join(c.ASSETS_PATH, "player"), "Run", RUN_SPRITE_FRAMES)
        self.jumpSprites = sprite_loader.load_sprites(os.path.join(c.ASSETS_PATH, "player"), "Jump", JUMP_SPRITE_FRAMES)
        self.attackSprites = sprite_loader.load_sprites(os.path.join(c.ASSETS_PATH, "player"), "Attack", ATTACK_SPRITE_FRAMES)



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
    
    def kill(self, death_type:c.DeathType):
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
            case _:
                print("Unknown death.")
        self.dead = True
        self.image.set_alpha(0)


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
    
    