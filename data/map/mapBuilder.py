import pygame, sys, os, random
import math
import data.constants as c  # Import constants
from scipy.stats import skewnorm



class MapBuilder():
    def __init__(self, screen_width, screen_height, grid_x_units):
        self.path_list = []
        self.tree_list = []
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
             
    def spawn_tree(self):
        centerx = c.SCREEN_WIDTH + c.TREE_WIDTH/2
        tree = Tree(centerx, self.tree_img, self.branch_img)
        self.tree_list.append(tree)
        self.update_count = 0
        return tree

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
            num_branches = num_branches if num_branches > 0 else 1

        #TODO: Make these constants
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
    "forest": MapBuilder.generateForest
}
