#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:50:38 2023

@author: frank
"""

def lijst_even_getallen(begin,einde):
    lijst=[]
    for i in range(begin,einde+1):
        if i%2==0:
            lijst.append(i)
    return lijst

print(lijst_even_getallen(10,125))