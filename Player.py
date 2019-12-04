# -*- coding: utf-8 -*-
"""
@author: John Li, John Khuc, Tony Lei
"""
import random

class Player: 
    
    def __init__(self, health, name):
        self.__health = health
        self.name = name
        self.buff = 0
    
    def getHealth(self):
        return self.__health
    
    def setHealth(self, health): #set health
        self.__health = health
    
    def takeDamage(self, damage): #decrease health based on parameters given
        self.setHealth(self.getHealth() - damage)
    
    def attack(self): #randomly decide how much damage dealt
         roll = random.randint(1, 7)
         if roll > 2:
             return 10
         return 0
     
    def getName(self): #return name
        return self.name
    
    def setBuff(self, num): #returns buff int to inc attack
        self.buff += num
    
    def resetBuff(self): #reset buff
        self.buff = 0