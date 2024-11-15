import pygame, sys, os, random
from perlin_noise import PerlinNoise

class MapBuilder():
    def __init__(self, screen_width, screen_hieght, grid_x_units, num_of_paths):
        self.path_list = []
        self.num_of_paths = num_of_paths
        self.mypath = os.path.dirname(os.path.realpath( __file__ ))
        self.screen_width = screen_width
        self.screen_height = screen_hieght
        self.grid_x_units = grid_x_units
        self.unit_size = screen_width/grid_x_units
        self.offset = 0
        self.freq = 0.001
        #load images
        
        #initialize the world
        tile_img = pygame.image.load((os.path.join(self.mypath, 'img/tile.png')))

        #seedTile = random.randint(0, 2**32 - 1)
        self.height_functions = []
        for i in range(self.num_of_paths):
            seedHeight = random.randint(0, 2**32 - 1)
            heightNoise = PerlinNoise(octaves=10, seed=seedHeight)
            self.height_functions.append(heightNoise)

        #tileNoise = PerlinNoise(octaves=3, seed=seedTile)
        

        

        for p in range(len(self.height_functions)):
            tile_list = []
            for i in range(self.grid_x_units):
                # is there a tile?
                x = i * self.unit_size
                is_tile = random.randint(0, 100) > 75
                #print("tile noise on", x, ":", tileNoise(x * 0.001))
                if(is_tile):
                    img = pygame.transform.scale(tile_img, (32, 4)) #change later!
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = ((self.height_functions[p](x * (1/self.screen_height)) + 1) * (self.screen_height/self.num_of_paths) * (p+1)) #ensure its positive
                    print("tile height on", x, ":", ((self.height_functions[p](x/self.screen_width) + 1) * (self.screen_height/self.num_of_paths) * (p+1)), "we passed:", x/self.screen_width )
                    #img_rect.y = ((self.height_functions[p](x) + 1)/2) * self.screen_height #ensure its positive
                    #print("tile height on", x, ":", self.height_functions[p](x/self.screen_height))
                    tile = [img, img_rect]
                    tile_list.append(tile)
            self.path_list.append(tile_list)

    def update(self):
        #append to end of list using 
        for tile_list in self.path_list:
            for tile in tile_list:
                tile[1].x += -1
        # TODO: Update world data using perlin

      

    def draw(self, screen):
        for path in self.path_list:
            for tile in path:
                screen.blit(tile[0], tile[1])

    