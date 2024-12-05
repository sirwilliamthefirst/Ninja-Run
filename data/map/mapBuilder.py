import pygame, sys, os, random
import math
import data.constants as c  # Import constants
from perlin_noise import PerlinNoise
from scipy.stats import skewnorm



class MapBuilder():
    def __init__(self, screen_width, screen_height, grid_x_units, num_of_paths):
        self.path_list = []
        self.tree_list = []
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
        self.tile_img = pygame.image.load((os.path.join(c.ASSETS_PATH, 'map/tile.png')))
        self.background_img = pygame.image.load((os.path.join(c.ASSETS_PATH, 'map/background.png')))
        self.tree_img = pygame.image.load((os.path.join(c.ASSETS_PATH, 'map/tree.png')))
        self.branch_img = pygame.image.load((os.path.join(c.ASSETS_PATH, 'map/branch.png')))
        #Calculate number of background tiles needed
        self.num_background_tiles = math.ceil(self.screen_width / c.BACKGROUND_IMAGE_DIMENSIONS[0]) + 1
        self.height_functions = []
        GENERATION[c.GENERATIONALGO](self)

    def update(self):
        #append to end of list using 
        for tree in self.tree_list:
            tree.move_ip(c.PLATFORM_SPEED, 0)
            if tree.get_rect().right < 0:
                self.tree_list.remove(tree)
        
        if self.update_count >= self.unit_size:
                centerx = c.SCREEN_WIDTH + c.TREE_WIDTH/2
                tree = Tree(centerx, self.tree_img, self.branch_img)
                self.tree_list.append(tree)
                self.update_count = 0

        self.update_count += abs(c.PLATFORM_SPEED)

        for tile_list in self.path_list:
            for tile in tile_list:
                tile[1].x += -1
                if tile[1].x < 0:
                    tile_list.remove(tile)
            #add new tiles        
            if self.update_count >= self.unit_size:
                if random.random() > c.PLATFORM_PROBABILITY:  # Adjust this threshold for more/less platforms
                    y_pos = random.randint(50, self.screen_height - 100)

                    img = pygame.transform.scale(self.tile_img, (c.PLATFORM_WIDTH, c.PLATFORM_HEIGHT))  # Flexible tile size
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
            screen.blit(self.background_img, [self.background_position + i * c.BACKGROUND_IMAGE_DIMENSIONS[0], 0]) 
            i += 1

        for tree in self.tree_list:
            tree.draw(screen)
        #for path in self.path_list:
        #    for tile in path:
         #       screen.blit(tile[0], tile[1])

        self.background_position -= c.BACKGROUND_SCROLL_SPEED

        #Reset background counter when tile reaches end of screen
        if abs(self.background_position) >= c.BACKGROUND_IMAGE_DIMENSIONS[0]:
            self.background_position = 0

    def get_map(self):
        tile_list_all = []
        if self.tree_list:
            for tree in self.tree_list:
                tile_list_all.extend(tree.get_branches())
        else:
            for tile_list in self.path_list:
                tile_list_all.extend(tile_list)
        return tile_list_all

    def get_tree(self, i : int):
        return self.tree_list[i]
    
    def get_last_tree(self):
        return self.tree_list[-1]


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
                    img = pygame.transform.scale(self.tile_img, (c.PLATFORM_WIDTH, c.PLATFORM_HEIGHT))  # Flexible tile size
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = y_pos
                    #print(f"Tile height at x={x}: {noise_val}, y={img_rect.y}")

                    # Add tile to the list
                    tile = [img, img_rect]
                    tile_list.append(tile)
             # Append the generated path to path_list
            self.path_list.append(tile_list)

    def generateRandom(self, player):

        player_tile_made = False
        for _ in range(self.num_of_paths):
            tile_list = []
            if not player_tile_made:
                img = pygame.transform.scale(self.tile_img, (c.PLATFORM_WIDTH, c.PLATFORM_HEIGHT))  # Flexible tile size
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

                    img = pygame.transform.scale(self.tile_img, (c.PLATFORM_WIDTH, c.PLATFORM_HEIGHT))  # Flexible tile size
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = y_pos

                    # Add tile to the list
                    tile = [img, img_rect]
                    tile_list.append(tile)
            self.path_list.append(tile_list)

    def generateForest(self):
        for i in range(self.grid_x_units + 1):
            centerx = self.unit_size * i
            tree = Tree(centerx, self.tree_img, self.branch_img)
            self.tree_list.append(tree)
            


class Tree():
    
    def __init__(self, centerX, Tree_image, branch_image, width = c.TREE_WIDTH, height = c.TREE_HEIGHT, num_branches = None):
        self.width = width
        self.height = height
        self.centerX = centerX
        self.branches = []
        self.num_branches = num_branches
        self.img = pygame.transform.scale(Tree_image, (width, height))  # Flexible tile size
        self.branch_img = branch_image
        self.img_rect = self.img.get_rect()
        self.img_rect.centerx = centerX
        self.img_rect.bottom = c.TREE_HEIGHT
        self.generate_branches(self.num_branches)


    def generate_branches(self, num_branches = None):
        #if none, generate random number branches
        if not num_branches:
            randomNum = random.gauss(c.BRANCH_AVRG_NUM, c.BRANCH_NUM_DEVIATION)
            num_branches = int(randomNum)

        skew = -4
        mean = random.randint(400, 600)
        scale = 200
        branch_heights = []
        for _ in range(num_branches):
            while True:
                # Generate a potential branch height
                randomHeight = skewnorm.rvs(a=skew, loc=mean, scale=scale)

                # Clamp the height to screen bounds
                randomHeight = max(0, min(c.SCREEN_HEIGHT, randomHeight))

                # Check if this height is sufficiently spaced from existing ones
                if all(abs(randomHeight - h) >= c.BRANCH_MIN_SPACING for h in branch_heights):
                    branch_heights.append(randomHeight)
                    break

        # Create and append a new branch
        for randomHeight in branch_heights:
            width = random.gauss(c.PLATFORM_AVRG_WIDTH, c.PLATFORM_WIDTH_DEVIATION) 
            width = width if width > 0 else c.PLATFORM_AVRG_WIDTH 
            leftBound = self.img_rect.centerx - (c.TREE_WIDTH + width)/2
            rightBound = self.img_rect.centerx + (c.TREE_WIDTH + width)/2
            centerx = random.uniform(leftBound, rightBound)
            branch = Branch(width, c.PLATFORM_HEIGHT, centerx, randomHeight, self.branch_img)
            self.branches.append(branch)

    def get_rect(self):
        return self.img_rect   
    def move_ip(self, x,y):
        self.img_rect.move_ip(x,y)
        for branch in self.branches:
            branch.move_ip(x, y)

    def get_random_branch(self, num_branches=1):
        random.choice(self.branches, k=num_branches)

    def get_middle_branch(self):
        sorted_branches = sorted(self.branches, key = lambda branch: branch.get_top_center()[1])
        print(sorted_branches)
        if sorted_branches:
            middle_index = len(sorted_branches) // 2
            return sorted_branches[middle_index]
        return None  # In case there are no branches
    
    def draw(self, screen):
        screen.blit(self.img, self.img_rect)
        for branch in self.branches:
            branch.draw(screen)

    def get_branches(self):
        return self.branches



class Branch():
    def __init__(self, width, height, centerx, topy, branch_image):
        self.centerx = centerx 
        self.img = pygame.transform.scale(branch_image, (width, height))  # Flexible tile size
        self.img_rect = self.img.get_rect()
        self.img_rect.centerx = centerx
        self.img_rect.y = topy

    def draw(self, screen):
         screen.blit(self.img, self.img_rect)
    
    def get_rect(self):
        return self.img_rect
    
    def get_top_center(self):
        return (self.img_rect.centerx, self.img_rect.top)

    def move_ip(self, x, y):
        self.img_rect.move_ip(x, y)

GENERATION = {
    "perlin": MapBuilder.generatePerlin,
    "random": MapBuilder.generateRandom,
    "forest": MapBuilder.generateForest
}
