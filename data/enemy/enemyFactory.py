import random 
from .samurai import *
class EnemyFactory():

    enemy_types = {
        "samurai": Samurai
    }

    enemy_worths = {
        "samurai": 25
    }

    def __init__(self):
        self.enemy_widths = {}
        for name, cls in self.enemy_types.items():
            temp_enemy = cls(0, 0)
            self.enemy_widths[name] = temp_enemy.rect.width
        pass


    def spawn_enemy(self, x, y, enemy = None) -> Enemy:
        if enemy: 
            return self.enemy_types[enemy](x,y, self.enemy_worths[enemy])
        else:
            enemy_type = random.choice(list(self.enemy_types.keys()))
            return random.choice(list(self.enemy_types[enemy_type]))(x,y, self.enemy_worths[enemy_type]) 
        

    def get_enemy_width(self, enemy=None) -> tuple[int, str]:
        if enemy:
            return self.enemy_widths[enemy]
        else:
            # If choosing randomly, pick a random key first
            enemy = random.choice(list(self.enemy_widths.keys()))
            return (self.enemy_widths[enemy], enemy)

        
