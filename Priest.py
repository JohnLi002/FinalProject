# -*- coding: utf-8 -*-
"""
@author: John Li, John Khuc, Tony Lei
"""

from Player import Player
import random

class Priest(Player): 
    def __init__(self, health, name):
        super().__init__(health, name)
        self.skills = ["Heal","Holy Glader","Stat Boost"]
        
    def getSkillList(self): #return skills
        result = "Skills: \n"
        i = 1
        for x in self.skills:
            result += "- " + str(i) + " = " + x + "\n"
            i += 1
        
        return result
    
    def getSkills(self): #return array of skills
        return self.skills
    
    def getClass(self): #return class
        return "Priest"
    
    def heal(self, target): #increase health of another player
        target.setHealth(target.getHealth() + int(random.random()*11 + 10))
        return target
        
    def holyGlader(self): #deal damage and heal self
        damage = (super().attack() + self.buff)*1.3
        self.setHealth(self.getHealth() + int(random.random()*5+1))
        super().resetBuff()
        return damage
    
    def statBoost(self, target): #buff another player
        return target.setBuff(15)
