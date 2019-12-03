# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:00:30 2019

@author: lij19
"""
a = [0, 1, 2]

i = 0
while(i < len(a)):
    a[i] += 1
    i += 1

i = 0
while(True):
    if(a[i] == 3):
        del(a[i])
    else:
        i += 1
        
    if(i == len(a)):
        break

for x in a:
    print(x)