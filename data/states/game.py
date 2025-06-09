import pygame as pg

from .states import States
from ..player import *
from ..enemy import *
import data.tools as tools
from ..mapBuilder import *
from pygame.locals import *
import data.constants as c  # Import constants


class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.map_spawn_counter = 0
        self.unit_size = c.SCREEN_WIDTH / c.GRID_UNITS_X
        self.enemies = pg.sprite.Group()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.stacked_dt = 0  # for debugging

    def cleanup(self):
        print("cleaning Game state")
        States.player_set.clear()
        States.players.empty()
        self.enemies.empty()
        self.map_spawn_counter = 0
        self.score = 0

    def startup(self):
        print("starting Game state")
        # look for joysticks
        self.joysticks = [
            pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())
        ]

        # get map
        self.stage = MapBuilder(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GRID_UNITS_X)
        self.stage.generate(c.GENERATIONALGO)
        # self.stage.generate() #USe this for random stage select... at some point, make a stage select screen and build there
        self.end_wait = 0
        # make enemy stuff
        self.enemy_factory = EnemyFactory()

        # Spawm Players
        num_player_divisor = len(States.players) + 1
        cur_player_num = 0
        for player in States.players:
            cur_player_num += 1
            starty = c.SCREEN_HEIGHT * (cur_player_num / num_player_divisor)
            spawn_tree = self.stage.get_tree(c.SPAWN_TREE)
            spawn_branch = Branch(
                c.SPAWN_PLATFORM_WIDTH,
                c.PLATFORM_HEIGHT,
                spawn_tree.get_rect().centerx,
                starty,
            )
            spawn_tree.add_branch(spawn_branch)
            x, y = spawn_branch.get_top_center()
            player.unfreeze()
            player.move(x, y)

        # Text list
        self.floating_texts = []

        # Timing
        self.last_map_update = pygame.time.get_ticks()
        self.map_update_timer = 0
        self.time_slow_multiplier = 1
        self.time_slow_timer = 0

    def get_event(self, events):
        return

    def update(self, screen, dt):
        self.draw(screen)
        dt_scaled = dt * self.time_slow_multiplier
        if self.time_slow_multiplier < 1 and self.time_slow_timer < c.SLOW_DOWN_TIME:
            self.time_slow_timer += dt  # USE Real dt because we want real time seconds
        else:
            self.time_slow_multiplier = 1
            self.time_slow_timer = 0
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        self.stacked_dt += dt

        self.stage.update(dt_scaled)
        self.enemies.update(dt_scaled)
        States.players.update(dt_scaled)
        if self.map_spawn_counter >= c.TREE_GAP:  # self.unit_size:
            self.add_tree()
            self.map_spawn_counter = 0
        self.map_spawn_counter += -c.PLATFORM_SPEED * dt_scaled

        for player in States.players:
            print(f"dy before collision: {player.get_dy()} player bottom: {player.rect.bottom}")
            tools.collisionHandler.handle_verticle_collision(
                player, self.stage.get_map()
            )
            print(f"dy after collision: {player.get_dy()} player bottom: {player.rect.bottom}")

            for enemy in self.enemies:
                if tools.collisionHandler.check_collision(player, enemy):
                    # TODO ADD RICOCHET IF PLAYER AND ENEMY ATTACK COLLIDES
                    if player.is_attacking() and not enemy.is_dead():
                        enemy.die()
                        # self.time_slow_multiplier = 0.5
                        enemy_value = enemy.get_worth()
                        self.score += enemy_value
                        self.floating_texts.append(
                            FloatingText(f"+{enemy_value}", enemy.get_rect().center)
                        )
                    elif enemy.is_collidable():
                        player.kill(c.DeathType.ENEMY)
            if States.pvp_flag:
                for player2 in States.players:
                    if (player != player2) and tools.collisionHandler.check_collision(
                        player, player2
                    ):
                        if player.is_attacking() and not player2.is_attacking():
                            player2.kill(c.DeathType.ENEMY)

            player.drag(dt_scaled)
        for text in self.floating_texts:
            text.update(dt_scaled)
        # Check if all players are dead, if not, update score
        all_dead_and_done = all(
            player.is_dead() and player.is_done_dying() for player in States.players
        )
        any_in_progress_dying = any(
            player.is_dead() and not player.is_done_dying() for player in States.players
        )

        if all_dead_and_done:
            self.end_wait += dt
            if self.end_wait >= 1:
                self.done = True
        elif not any_in_progress_dying:
            # Only update score if no one is mid-death FIX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.score += 1

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.stage.draw(screen)
        #States.players.draw(screen)
        for player in States.players:
            player.draw(screen)
            player.draw_particles(screen)
            collision_left_bound = (player.rect.centerx + player.rect.left) / 2
            collision_right_bound = (player.rect.centerx + player.rect.right) / 2
            if c.DEBUG:
                pygame.draw.rect(
                    #screen, (255, 0, 0), player.rect, 2
                    screen, (255, 0, 0), pygame.Rect(collision_left_bound, player.rect.top, collision_right_bound - collision_left_bound, player.rect.bottom - player.rect.top), 2
                )  # Draw player rect for debugging
        self.enemies.draw(screen)
        for enemy in self.enemies:
            enemy.draw_particles(screen)
        for text in self.floating_texts:
            text.draw(screen)
            if text.is_dead():
                self.floating_texts.remove(text)

    def add_tree(self):
        tree = self.stage.create_tree()
        if random.random() > 0.50:  # Makes enemies
            branch_rect = tree.get_random_branch().get_rect()
            enemy_width, enemy_name = (
                self.enemy_factory.get_enemy_width()
            )  # (width, enemy_name) tuple
            spawn_x = random.uniform(
                branch_rect.left, branch_rect.right - (enemy_width / 2)
            )
            self.enemies.add(
                self.enemy_factory.spawn_enemy(spawn_x, branch_rect.y, enemy_name)
            )


class FloatingText:
    def __init__(self, text, pos):
        self.font = pygame.font.Font(None, int(20 * c.WIDTH_SCALE))
        self.text = text
        self.pos = pygame.Vector2(pos)
        self.alpha = 255
        self.image = self.font.render(self.text, True, (0, 255, 0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.pos.y -= 100 * dt  # Move up
        self.alpha -= 510 * dt  # Fade out
        if self.alpha < 0:
            self.alpha = 0

        self.image.set_alpha(self.alpha)
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_dead(self):
        return self.alpha == 0

class Score():
    def __init__(self, score=0, kills=0, time_alive=0):
        self.score = score
        self.kills = kills
        self.time_alive = time_alive
        self.killscore

    def add_score(self, points):
        self.score += points

    def add_kill(self, kill_value):
        self.killscore += kill_value
        self.kills += 1
        self.add_score(kill_value)

    def get_score(self):
        return self.score
    
    