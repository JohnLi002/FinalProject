# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:20:32 2019

@author: leix
"""
from Player import Player

class Ranger(Player):

    def __init__(self, health, name):
        super().__init__(health + 50, name)
        self.skills = ["Sharp Shot","Crippling Shot","Collapsing Shot"]
        
    def getSkillList(self):
        skillList = "Ranger Skills: \n"
        
        for x in self.skills:
            skillList += "-" + x + "\n"
        
        return skillList
    
    def getSkills(self):
        return self.skills
    
    def getClass(self):
        return "Ranger"
    