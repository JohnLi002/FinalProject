# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:00:30 2019

@author: lij19
"""
import Thief

t = Thief.Thief(100, "hi")

t.poisonCoat()
poison, damage = t.swiftStrike()

print(poison)
print(damage)

poison, damage = t.swiftStrike()
print(poison)
print(damage)

i = 5
i -= 1.2
print(i)

