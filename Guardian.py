# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:21:32 2019

@author: leix
"""

from Player import Player
import random

class Guardian(Player):
    def __init__(self, health, name):
        super().__init__(health + 100, name)
        self.skills = ["Taunt","Shield Bash","Protection"]
        
    def getSkillList(self):
        result = "Skills: \n"
        i = 1
        for x in self.skills:
            result += "- " + str(i) + " = " + x + "\n"
            i += 1
        
        return result
    
    def getSkills(self):
        return self.skills
    
    def getClass(self):
        return "Guardian"
    
    def taunt():
        return "Taunt"
    
    def protection():
        defUp = random.randint(0, 20)
        return defUp
    
    def shieldBash():
        return 5
    