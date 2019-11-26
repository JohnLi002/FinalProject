# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:21:44 2019

@author: leix
"""

from Player import Player

class Thief(Player):
    def __init__(self, health, name):
        super().__init__(health - 20, name)
        self.skills = ["Poison Coating","Swift Strike","Smoke Bomb"]
        
    def getSkillList(self):
        result = "Thief Skills: \n"
        
        for x in self.skills:
            result += "-" + x + "\n"
        
        return result