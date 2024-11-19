import pygame, sys, tools
from player import *
from map import *
from pygame.locals import *

pygame.init()

#Setup Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Define Tiles
TILE_SIZE = 20
GRID_UNITS_X = int(SCREEN_WIDTH / TILE_SIZE)
GRID_UNITS_Y = SCREEN_HEIGHT / TILE_SIZE #REPLACE Y WITH PERLIN NOISE VALUES

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ninja Run')
clock = pygame.time.Clock()

#look for joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

#create sprites and groups
moving_sprites = pygame.sprite.Group()
player1 = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2, joysticks[0] if joysticks and joysticks[0] else None)
moving_sprites.add(player1)


#get map
map = MapBuilder(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_UNITS_X, 3, player1) 

# Timing
map_update_interval = 10  # Update every 500ms (0.5 seconds)
last_map_update = pygame.time.get_ticks()

#def draw_grid():
#    for line in range(GRID_UNITS_X):
        #pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE), 1)
#        pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_WIDTH), 1)

run = True
while run:
    current_time = pygame.time.get_ticks()
    
    screen.fill((0,0,0))
    moving_sprites.draw(screen)
    if current_time - last_map_update > map_update_interval:
        map.update()
        tools.collisionHandler.handle_verticle_collision(player1, map.get_map())
        player1.handle_move()
        player1.drag()
        last_map_update = current_time
    
    map.draw(screen)
    #pygame.draw.rect(screen, (255, 255, 255), player1.rect)
    #draw_grid()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    moving_sprites.update()
    pygame.display.update()

pygame.quit()