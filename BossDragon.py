# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:31:31 2019

@author: lij19
"""
import random


class BossDragon:
<<<<<<< Updated upstream
    actions = ["Tail Swipe", "Dragon Breath", "Glare"]
=======
    actions = ["Tail Swipe", "Dragon Breath", "Bite"]
    health = 0
>>>>>>> Stashed changes
    
    def __init__(self, health):
        self.health = health
        
        
    def lossHealth(self, num):
        self.health -= num

    def dealDamage(attack):
        num = int(random()*len(attack))
        action = attack[num]
        if(action == 'Tail Swipe'):
            return 10
        elif(action == 'Dragon Breath'):
            return 15
        else:
            return 5
        