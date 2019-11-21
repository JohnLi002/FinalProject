# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:41:06 2019

@author: lij19
"""

import random

class Player: 
    
    
    def __init__(self, health, name):
        self.__health = health
        self.name = name
    
    def getHealth(self):
        return self.__health
    
    def setHealth(self, health):
        self.__health = health
    
    def takeDamage(self, damage):
        self.setHealth(self.getHealth() - damage)
    
    def attack(self):
         roll = random.randint(1, 7)
         if roll > 2:
             return 10
         return 0
     
    def getName(self):
        return "["+self.name +"]"
