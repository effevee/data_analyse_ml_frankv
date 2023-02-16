#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:27:42 2023

@author: frank
"""

zin='De rode duivels gaan naar Qatar'

print('Lengte zin:',len(zin))

print(zin[8:15])

print('Aantal woorden:',len(zin.split()))

print('*'*50)

rugzak = ['brood','kaas','mes','wijn','boter']
print(rugzak)

print(rugzak[3])

rugzak[3]='cider'  # wijn vervangen door cider
print(rugzak)

rugzak.append('dafalgan')
rugzak.append('water')
print(rugzak)

rugzak.insert(2,'vork')
print(rugzak)

laatste=rugzak.pop()
print(laatste)
print(rugzak)

rugzak.pop(4)
print(rugzak)

zin=zin.replace('rode','paarse')
print(zin)

leerling=['Jan', 'Jansens', 15, 1.78]
print(leerling)

leerling+=rugzak
print(leerling)

print(leerling.remove('brood'))
print(leerling)


def swap2(g1,g2):
    g1,g2=g2,g1
    return g1,g2

getal1=20
getal2=30
getal1,getal2=swap2(getal1,getal2)
print('eerste getal:',getal1,'tweede getal:',getal2)

for e in rugzak:
    if e[-1]=='s':
        print(e)