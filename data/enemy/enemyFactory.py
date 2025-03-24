import random 
from .samurai import *
class EnemyFactory():

    enemyTypes = {
        "samurai": Samurai
    }

    def __init__(self):
        pass


    def spawn_enemy(self, x, y, enemy = None):
        if enemy: 
            return self.enemyTypes[enemy](x,y)
        else:
            return random.choice(list(self.enemyTypes.values()))(x,y)
        
