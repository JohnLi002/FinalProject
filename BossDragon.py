# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:31:31 2019

@author: lij19
"""
import random


class BossDragon:
    actions = ["Tail Swipe", "Dragon Breath", "Glare"]
    health = 0
    
    def __init__(self,hp):
       self.health = hp
        
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
    def getHealth(self):
        return self.health
        