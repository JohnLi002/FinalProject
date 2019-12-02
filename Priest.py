# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:21:17 2019

@author: leix
"""

from Player import Player
import random

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
    
    def heal(self, target):
        target.setHealth(target.getHealth() + int(random.random()*11 + 10))
        return target
        
    def holyGlader(self):
        damage = (super.attack() + self.buff)*1.3
        self.setHealth(self.getHealth() + int(random.random()*5+1))
        super().resetBuff()
        return damage
    
    def statBoost(self, target):
        return target.setBuff(15)
