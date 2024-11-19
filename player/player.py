import pygame, sys, os


BASE_SPEED = 3
MAX_SPEED = 3
GRAVITY = 0.2
AIRBORN_SHIFT = 0.15
JUMP = -6
DRAG_SPEED = 0.5
VERTICLE_SHIFT = 0.1 #MAybe seperate into up direction and down direction
SPRITE_WIDTH = 50   # use a proportion calculator to change please ratio is 90/80
SPRITE_HEIGHT = 44

class Player(pygame.sprite.Sprite): #maybe make an object class that player inherits that inherits sprites
    def __init__(self, pos_x, pos_y, joystick = None):
        super().__init__()
        # Find our path
        self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        self.joystick = joystick
        # Get the sprites
        self.__spritify()
        self.is_airborn = False
        self.is_jumping = False
        self.is_doubleJump = False
        self.current_sprite = 0
        self.image = self.runSprites[self.current_sprite] #init as running
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT)) 
        self.rect = self.image.get_rect()
        self.fall_thru = False
        #set position and keep track
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.y_vel = 0
        self.x_vel = 0
        self.rect.topleft = [pos_x, pos_y]
        

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
        self.rect.topleft = [self.pos_x, self.pos_y]

    def handle_joystick(self):
        x_axis = self.joystick.get_axis(0) #left negative right pos
        y_axis = self.joystick.get_axis(1)

        if self.is_airborn and ((x_axis > 0 and self.x_vel < MAX_SPEED) or (x_axis < 0 and self.x_vel > -MAX_SPEED)):
            self.x_vel += AIRBORN_SHIFT * x_axis
        elif(not self.is_airborn):
                self.x_vel += BASE_SPEED * x_axis

        if self.joystick.get_button(0):
            self.jump()

        if y_axis < 0:
            if self.is_airborn:
                self.y_vel += VERTICLE_SHIFT * y_axis
        if y_axis > 0.4:
            self.fall_thru = True
            if self.is_airborn:
                self.y_vel += VERTICLE_SHIFT * abs(y_axis)
            else:
                self.is_airborn = True #drop from platform
        else:
            self.fall_thru = False    

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            if self.is_airborn and self.x_vel < MAX_SPEED:
                self.x_vel += AIRBORN_SHIFT
            elif(not self.is_airborn):
                self.x_vel += BASE_SPEED
        if key[pygame.K_LEFT]:
            if self.is_airborn and self.x_vel > -MAX_SPEED:
                self.x_vel += -AIRBORN_SHIFT
            elif(not self.is_airborn):
                self.x_vel += -BASE_SPEED
        if key[pygame.K_SPACE]:
            self.jump()
        if key[pygame.K_UP]:
            if self.is_airborn:
                self.y_vel += -VERTICLE_SHIFT
        if key[pygame.K_DOWN]:
            self.fall_thru = True
            if self.is_airborn:
                self.y_vel += VERTICLE_SHIFT
            else:
                self.is_airborn = True #drop from platform
        else:
            self.fall_thru = False    

    def handle_gravity(self):
        if self.is_airborn:
            if self.y_vel < 5:
                self.y_vel += GRAVITY

        
    # Update sprite animation
    def update(self):
        # probably make a move function and within it handle keys
        #self.handle_move()

        self.animate()

        #add gravity
            



    def jump(self):
        if(self.is_doubleJump):
            self.is_doubleJump = False #fake code, TODO: Implement double jump and call it
        elif(not self.is_jumping and not self.is_airborn):
            self.is_jumping = True
            self.y_vel = JUMP
            self.is_airborn = True
            #reset current sprite and make it the fist jump
            self.current_sprite = 0
            self.image = self.jumpSprites[self.current_sprite]


    def move_ip(self, x, y):
        self.pos

    def animate(self):
        if(self.is_airborn):
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
            
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT))  

    def __spritify(self):
        # Set run Sprites
        self.runSprites = []
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__000.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__001.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__002.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__003.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__004.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__005.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__006.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__007.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__008.png')))
        self.runSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Run__009.png')))

        # Set jump Sprites Note: I think set airborn and jump, jump last some amount of frames and overides airborn

        self.jumpSprites = []
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__002.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__003.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__004.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__005.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__006.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__007.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__008.png')))
        self.jumpSprites.append(pygame.image.load(os.path.join(self.mypath, 'img/ninja/Jump__009.png')))

    def drag(self):
        if(not self.is_airborn):
            self.pos_x += -DRAG_SPEED

    def get_dy(self):
        return self.y_vel
    
    def land(self):
        self.is_airborn = False

    def fall(self):
        self.is_airborn = True
    
    def get_fall_thru(self):
        return self.fall_thru