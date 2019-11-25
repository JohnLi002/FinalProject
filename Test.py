# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:00:30 2019

@author: lij19
"""
import Ranger, Priest, Guardian, Thief

r = Ranger.Ranger(100,"hi")
p = Priest.Priest(100, "hi2")
g = Guardian.Guardian(100, "hi3")
t = Thief.Thief(100, "hi4")

print(r.getSkillList())
print(p.getSkillList())
print(g.getSkillList())
print(t.getSkillList())

