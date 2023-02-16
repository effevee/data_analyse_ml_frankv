#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 19:00:16 2023

@author: frank
"""

import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Getal 1:'), sg.InputText()],
            [sg.Text('Getal 2:'), sg.InputText()],
            [sg.Button('x'), sg.Button('/'), sg.Button('+'), sg.Button('-'), sg.Button('rest')],
            [sg.Text(' '*50,key="RESULT")]]

# Create the Window
window = sg.Window('Rekenmachine', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'x':
        try:
            window['RESULT'](' '*50)
            g1=float(values[0])
            g2=float(values[1])
            window['RESULT'](str(g1*g2))
        except:
            window['RESULT'](' ')*50
            window['RESULT']('Probleem met de bewerking: ' + values[0] + 'x' + values[1])

    if event == '/':
        try:
            window['RESULT'](' '*50)
            g1=float(values[0])
            g2=float(values[1])
            window['RESULT'](str(g1/g2))
        except:
            window['RESULT'](' '*50)
            window['RESULT']('Probleem met de bewerking: ' + values[0] + '/' + values[1])
    
    if event == '+':
        try:
            window['RESULT'](' '*50)
            g1=float(values[0])
            g2=float(values[1])
            window['RESULT'](str(g1+g2))
        except:
            window['RESULT'](' '*50)
            window['RESULT']('Probleem met de bewerking: ' + values[0] + '+' + values[1])

    if event == '-':
        try:
            window['RESULT'](' '*50)
            g1=float(values[0])
            g2=float(values[1])
            window['RESULT'](str(g1-g2))
        except:
            window['RESULT'](' '*50)
            window['RESULT']('Probleem met de bewerking: ' + values[0] + '-' + values[1])

    if event == 'rest':
        try:
            window['RESULT'](' '*50)
            g1=float(values[0])
            g2=float(values[1])
            window['RESULT'](str(g1%g2))
        except:
            window['RESULT'](' '*50)
            window['RESULT']('Probleem met de bewerking: ' + values[0] + '%' + values[1])

window.close()
