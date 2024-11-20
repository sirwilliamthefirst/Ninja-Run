import pygame
import tools
from player import *
from map import *
from pygame.locals import *
import constants as c  # Import constants

pygame.init()


screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption('Ninja Run')
clock = pygame.time.Clock()

#look for joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

#create sprites and groups
moving_sprites = pygame.sprite.Group()
player1 = Player(c.SCREEN_WIDTH/2, c.SCREEN_HEIGHT/2, joysticks[0] if joysticks and joysticks[0] else None)
moving_sprites.add(player1)


#get map
map = MapBuilder(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GRID_UNITS_X, 3, player1) 

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
    map.draw(screen)
    moving_sprites.draw(screen)
    if current_time - last_map_update > map_update_interval:
        map.update()
        moving_sprites.update()
        tools.collisionHandler.handle_verticle_collision(player1, map.get_map())
       
        player1.drag()
        last_map_update = current_time
    
    
    #pygame.draw.rect(screen, (255, 255, 255), player1.rect)
    #draw_grid()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    pygame.display.update()

pygame.quit()