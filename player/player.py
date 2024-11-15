import pygame, sys, os



class Player(pygame.sprite.Sprite): #maybe make an object class that player inherits that inherits sprites
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # Find our path
        self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        # Get the sprites
        self.__spritify()
        self.is_airborn = False
        self.is_jumping = False
        self.is_doubleJump = False
        self.current_sprite = 0
        self.image = self.runSprites[self.current_sprite] #init as running
        self.rect = self.image.get_rect()
        #set position and keep track
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = [pos_x, pos_y]

    def handle_keys(self):
        key = pygame.key.get_pressed()
        playerMoveX = 0
        playerMoveY = 0
        if key[pygame.K_RIGHT]:
            playerMoveX += 0.5
        if key[pygame.K_LEFT]:
            playerMoveX += -0.5
        if key[pygame.K_UP]:
            playerMoveY += -0.5
        if key[pygame.K_DOWN]:
            playerMoveY += 0.5
        if key[pygame.K_SPACE]:
            self.jump()

        self.pos_x += playerMoveX
        self.pos_y += playerMoveY
        self.rect.topleft = [self.pos_x, self.pos_y]

    # Update sprite animation
    def update(self):
        # probably make a move function and within it handle keys
        self.handle_keys()
        if(self.is_airborn):
            if(self.jumping and self.current_sprite >= 5):
                self.jumping = False
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
            
        self.image = pygame.transform.scale(self.image, (90, 80)) 

    def jump(self):
        if(self.is_doubleJump):
            self.is_doubleJump = False #fake code, TODO: Implement double jump and call it
        else:
            self.jumping = True
        self.is_airborn = True
        #reset current sprite and make it the fist jump
        self.current_sprite = 0
        self.image = self.jumpSprites[self.current_sprite]


    def move_ip(self, x, y):
        self.pos

    #def land(self):


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
            self.pos_x += 0.2

