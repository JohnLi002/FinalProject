import random

class Boss: 
    

    def __init__(self, health):
        self.__health = health
    
    def getHealth(self):
        return self.__health
    
    def setHealth(self, health):
        self.__health = health
    
    def takeDamage(self, damage):
        self.setHealth(self.getHealth() - damage)
    
    def attack(self):
         roll = random.randint(1, 7)
         if roll > 5:
             return 50
    
    