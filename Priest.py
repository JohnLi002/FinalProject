# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:21:17 2019

@author: leix
"""

from Player import Player

class Priest(Player): 
    def __init__(self, health, name):
        super().__init__(health, name)
        self.skills = ["Heal","Holy Glader","Stat Boost"]
        
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
        return "Priest"
