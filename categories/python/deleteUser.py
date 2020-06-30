# -*- coding: utf-8 -*-
"""
Created on Sat May 30 14:33:44 2020

@author: Admin
"""
import sys

idWantDelete = str(sys.argv[1])

with open('../fingerprintData/fingerpint_db.txt', 'r') as db:
    lines = db.readlines()

length = len(lines)
for i in range(0, length):
    if(lines[i].strip('\n') == idWantDelete):
        del(lines[i:i+2])
        break
    
with open('../fingerprintData/fingerpint_db.txt', 'w') as db:
    for line in lines:
        db.write(line)