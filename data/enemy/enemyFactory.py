import random 
from .samurai import *
class EnemyFactory():

    enemyTypes = {
        "samurai": Samurai
    }

    

    def __init__(self):
        self.enemy_widths = {}
        for name, cls in self.enemyTypes.items():
            temp_enemy = cls(0, 0)
            self.enemy_widths[name] = temp_enemy.rect.width
        pass


    def spawn_enemy(self, x, y, enemy = None) -> Enemy:
        if enemy: 
            return self.enemyTypes[enemy](x,y)
        else:
            return random.choice(list(self.enemyTypes.values()))(x,y)
        

    def get_enemy_width(self, enemy=None) -> tuple[int, str]:
        if enemy:
            return self.enemy_widths[enemy]
        else:
            # If choosing randomly, pick a random key first
            enemy = random.choice(list(self.enemy_widths.keys()))
            return (self.enemy_widths[enemy], enemy)

        
