# -*- coding: utf-8 -*-
"""
@author: John Li, John Khuc, Tony Lei
"""

from Player import Player
import random

class Guardian(Player):
    def __init__(self, health, name):
        super().__init__(health + 100, name)
        self.skills = ["Taunt","Shield Bash","Protection"]
        self.defense = 0
        
    def getSkillList(self):
        result = "Skills: \n"
        i = 1
        for x in self.skills:
            result += "- " + str(i) + " = " + x + "\n"
            i += 1
        
        return result
    
    def getSkills(self): #return list of skills
        return self.skills
    
    def getClass(self): #identify class
        return "Guardian"
    
    
    def protection(self): #increase def
        defUp = random.randint(0, 20)
        self.defense += defUp
    
    #return attack based on player attack method and buffs
    def shieldBash(self): 
        damage = (super().attack() + self.buff)*1.5
        self.resetBuff()
        
        return damage
    
    def defending(self): #return def
        block = self.defense
        self.defense = 0
        return block
    