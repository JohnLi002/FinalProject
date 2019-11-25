# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:21:17 2019

@author: leix
"""

from Player import Player

class Priest(Player): 
    def __init__(self, health, name):
        super().__init__(health, name)
        self.Skills = ["Heal","Holy Glader","Stat Boost"]
        
    def getSkillList(self):
        result = "Skills: \n"
        for x in self.Skills:
            result += "-" + x + "\n"
        return result