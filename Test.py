# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:00:30 2019

@author: lij19
"""

import Priest

p = Priest.Priest(1,"1")
p2 = Priest.Priest(1,"2")
p2 = p.heal(p2)
print(p2.getHealth())