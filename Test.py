# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:00:30 2019

@author: lij19
"""

import BossDragon

boss = BossDragon.BossDragon(100)
print(boss.health)
boss.lossHealth(10)
print(boss.health)

print(boss.dealDamage())
