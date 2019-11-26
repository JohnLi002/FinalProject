# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:00:30 2019

@author: lij19
"""
import Ranger

r = Ranger.Ranger(100,"hi")
r.setBuff(10)
r.resetBuff()

print(r.buff)

