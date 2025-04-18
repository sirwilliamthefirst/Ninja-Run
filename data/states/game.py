import pygame as pg

from .states import States
from ..player import *
from ..enemy import *
import data.tools as tools
from ..map import *
from pygame.locals import *
import data.constants as c  # Import constants

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.map_spawn_counter = 0
        self.unit_size = c.SCREEN_WIDTH/c.GRID_UNITS_X
        self.enemies = pg.sprite.Group()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
    def cleanup(self):
        print('cleaning Game state')
        States.player_set.clear()
        States.players.empty()
        self.enemies.empty()
        self.map_spawn_counter = 0
        self.score = 0
        
    def startup(self):
        print('starting Game state')
        #look for joysticks
        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
    
        #get map
        self.stage = MapBuilder(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GRID_UNITS_X) 
        self.stage.generate(c.GENERATIONALGO)
        #self.stage.generate() #USe this for random stage select... at some point, make a stage select screen and build there

        #make enemy stuff
        self.enemy_factory = EnemyFactory()
        for player in States.players:
            spawn_tree = self.stage.get_tree(c.SPAWN_TREE)
            spawn_branch = spawn_tree.get_middle_branch()
            x, y = spawn_branch.get_top_center()
            player.unfreeze()
            player.move(x, y)

        # Timing
        self.last_map_update = pygame.time.get_ticks()

    def get_event(self, events):
        return
          
    def update(self, screen, dt):
        self.draw(screen)
        current_time = pygame.time.get_ticks()

        if current_time - self.last_map_update > c.MAP_UPDATE_INTERVAL:
            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            self.stage.update()
            self.enemies.update()
            if self.map_spawn_counter >= self.unit_size:
                self.update_forest()
            self.map_spawn_counter += abs(c.PLATFORM_SPEED)


            States.players.update(dt)
            for player in States.players:
                tools.collisionHandler.handle_verticle_collision(player, self.stage.get_map())
                for enemy in self.enemies:
                    if tools.collisionHandler.check_collision(player, enemy):
                        #TODO ADD RICOCHET IF PLAYER AND ENEMY ATTACK COLLIDES
                        if player.is_attacking():
                            enemy.die()
                            self.score += 20
                        elif enemy.is_collidable():
                            player.kill(c.DeathType.ENEMY)
                player.drag()
            self.last_map_update = current_time
            #Check if all players are dead, if not, update score
            all_dead_and_done = all(player.is_dead() and player.is_done_dying() for player in States.players)
            any_in_progress_dying = any(player.is_dead() and not player.is_done_dying() for player in States.players)

            if all_dead_and_done:
                self.done = True
            elif not any_in_progress_dying:
                # Only update score if no one is mid-death
                self.score += 1
                
            
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.stage.draw(screen)
        States.players.draw(screen)
        for player in States.players:
            player.draw_particles(screen)
        self.enemies.draw(screen)
        for enemy in self.enemies:
            enemy.draw_particles(screen)

    def update_forest(self):
        tree = self.stage.create_tree()
        if(random.random() > .50): #Makes enemies
            branch_rect = tree.get_random_branch().get_rect()
            self.enemies.add(self.enemy_factory.spawn_enemy(branch_rect.x, branch_rect.y))
        self.map_spawn_counter = 0
  