import pygame, sys, os, random
import math
# from perlin_noise import PerlinNoise

PLATFORM_WIDTH = 75 #32
PLATFORM_HEIGHT = 12 #4
PLATFORM_PROBABILITY = 0.85 #Threshhold for random num generator to determine number of platforms

BACKGROUND_IMAGE_DIMENSIONS = [928, 600] #Width and Height of background image file, used for moving background
GENERATIONALGO = "random"


class MapBuilder():
    def __init__(self, screen_width, screen_height, grid_x_units, num_of_paths, player):
        self.path_list = []
        self.num_of_paths = num_of_paths
        self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_x_units = grid_x_units
        self.unit_size = screen_width/grid_x_units
        self.update_count = 0
        self.freq = 0.05
        self.background_position = 0
        #load images
        
        #initialize the world
        self.tile_img = pygame.image.load((os.path.join(self.mypath, 'img/tile.png')))
        self.background_img = pygame.image.load((os.path.join(self.mypath, 'img/background.png')))

        #Calculate number of background tiles needed
        self.num_background_tiles = math.ceil(self.screen_width / BACKGROUND_IMAGE_DIMENSIONS[0]) + 1

        #seedTile = random.randint(0, 2**32 - 1)
        self.height_functions = []
        GENERATION[GENERATIONALGO](self, player)
        #self.generateRandom(player)

    def update(self):
        #append to end of list using 
        for tile_list in self.path_list:
            for tile in tile_list:
                tile[1].x += -1
                if tile[1].x < 0:
                    tile_list.remove(tile)
            #add new tiles        
            if self.update_count >= self.unit_size:
                if random.random() > PLATFORM_PROBABILITY:  # Adjust this threshold for more/less platforms
                    y_pos = random.randint(50, self.screen_height - 100)

                    img = pygame.transform.scale(self.tile_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Flexible tile size
                    img_rect = img.get_rect()
                    img_rect.x = self.screen_width
                    img_rect.y = y_pos

                    # Add tile to the list
                    tile = [img, img_rect]
                    tile_list.append(tile)
                self.update_count = 0
            self.update_count += 1
      

    def draw(self, screen):
        #Render the background tiles
        i = 0
        while(i < self.num_background_tiles): 
            screen.blit(self.background_img, [self.background_position+i*BACKGROUND_IMAGE_DIMENSIONS[0], 0]) 
            i += 1

        for path in self.path_list:
            for tile in path:
                screen.blit(tile[0], tile[1])

        self.background_position -= 1

        #Reset background counter when tile reaches end of screen
        if abs(self.background_position) >= BACKGROUND_IMAGE_DIMENSIONS[0]:
            self.background_position = 0

    def get_map(self):
        tile_list_all = []
        for tile_list in self.path_list:
            for tile in tile_list:
                tile_list_all.append(tile)
        return tile_list_all
            

    #DON'T CALL
    def generatePerlin(self):
        for i in range(self.num_of_paths):
            seedHeight = random.randint(0, 2**32 - 1)
            heightNoise = PerlinNoise(octaves=1, seed=seedHeight)
            self.height_functions.append(heightNoise)

        #tileNoise = PerlinNoise(octaves=3, seed=seedTile)
        for p in range(len(self.height_functions)):
            tile_list = []
            for i in range(self.grid_x_units):
                # is there a tile?
                x = i * self.unit_size
                 # Use noise to determine if there's a platform at this x-coordinate
                noise_val = self.height_functions[p](x * self.freq)
                normalized_val = (noise_val + 0.5)  # Normalize to range [0, 1]
                 # Map the normalized noise value to screen height
                y_pos = int(normalized_val * (self.screen_height - 100)) + 50  # Adding padding
                y_pos += random.randint(-50,50) #add more randomness
                 # Decide whether to place a platform (using noise threshold)
                if normalized_val > random.uniform(0.2, 0.4):  # Adjust this threshold for more/less platforms
                    img = pygame.transform.scale(self.tile_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Flexible tile size
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = y_pos
                    print(f"Tile height at x={x}: {noise_val}, y={img_rect.y}")

                    # Add tile to the list
                    tile = [img, img_rect]
                    tile_list.append(tile)
             # Append the generated path to path_list
            self.path_list.append(tile_list)

    def generateRandom(self, player):

        #tileNoise = PerlinNoise(octaves=3, seed=seedTile)
        player_tile_made = False
        for p in range(self.num_of_paths):
            tile_list = []
            if not player_tile_made:
                img = pygame.transform.scale(self.tile_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Flexible tile size
                img_rect = img.get_rect()
                img_rect.x = player.rect.centerx
                img_rect.y = player.rect.bottom

                # Add tile to the list
                tile = [img, img_rect]
                tile_list.append(tile)
                player_tile_made = True
            for i in range(self.grid_x_units):
                x = i * self.unit_size
               
                if random.random() >  0.85:  # Adjust this threshold for more/less platforms
                    y_pos = random.randint(50, self.screen_height - 100)

                    img = pygame.transform.scale(self.tile_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Flexible tile size
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = y_pos
                    print(f"Tile height at x={x}: y={img_rect.y}")

                    # Add tile to the list
                    tile = [img, img_rect]
                    tile_list.append(tile)
             # Append the generated path to path_list
            self.path_list.append(tile_list)

GENERATION = {
    "perlin": MapBuilder.generatePerlin,
    "random": MapBuilder.generateRandom
}
