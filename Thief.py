# -*- coding: utf-8 -*-
"""
@author: John Li, John Khuc, Tony Lei
"""

from Player import Player

class Thief(Player):
    def __init__(self, health, name):
        super().__init__(health - 20, name)
        self.skills = ["Poison Coat","Swift Strike","Smoke Bomb"]
        self.poison = False
        
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
        return "Thief"
    
    def poisonCoat(self): #poison coat makes it so that the next attack will cause status affect
        self.poison = True
    
    def swiftStrike(self):
        damage = (super().attack() + self.buff)*1
        if self.poison:
            damage *= 3
            self.poison = False
        super().resetBuff() #Buff can only be used for one attack
        return damage
    
    # the server can deal with the action smokebomb as it is solely a debuff