from Boss import *
from Player import *

p1 = Player(100)
b = Boss(1000)

print("Player Health: ", p1.getHealth())
print("Boss Health: ", b.getHealth())

turn = 1
while(p1.getHealth() > 0):
    print("\nTurn: ", turn)
    p1.takeDamage(b.attack())
    b.takeDamage(p1.attack())
    print("Player Health: ", p1.getHealth())
    print("Boss Health: ", b.getHealth())
    turn += 1