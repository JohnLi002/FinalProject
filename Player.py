# -*- coding: utf-8 -*-

import random

class Player: 
    
    # Constructor
    def __init__(self, health, name):
        self.__health = health
        self.name = name
    
    # Accessor Methods
    def getHealth(self):
        return self.__health
    
    def getName(self):
        return self.name

    # Mutator Methods    
    def setHealth(self, health):
        self.__health = health
    
    def takeDamage(self, damage):
        self.setHealth(self.getHealth() - damage)
    
    def attack(self):
         roll = random.randint(1, 7)
         if roll > 2:
             return 10
         return 0
     
   