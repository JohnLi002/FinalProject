# -*- coding: utf-8 -*-

import random

class BossDragon:
    
    # Class Variables
    actions = ["Tail Swipe", "Dragon Breath", "Glare"]
    health = 0
    
    # Constructor
    def __init__(self,hp):
       self.health = hp
    
    # Accessor Methods
    def getHealth(self):
        return self.health 
    
    # Mutator Methods
    def lossHealth(self, num):
        self.health -= num

    def dealDamage(self):
        num = int(random.random()*len(self.actions))
        action = self.actions[num]
        if(action == 'Tail Swipe'):
            return action, 10
        elif(action == 'Dragon Breath'):
            return action, 15
        else:
            return action, 5
    