#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:02:32 2023

@author: frank
"""

import PySimpleGUI as sg
import joblib
import dataPipeLineWrapper as dPW
import pandas as pd
import numpy as np

# laden van model en dataPipeline
model = joblib.load('model.sav')
dataPipeline = joblib.load('data_pipeline.sav')

# tabel tab manual
tab_manual_layout =  [[sg.T('carat:'),sg.In(),
                       sg.T('depth:'),sg.In(),
                       sg.T('table:'),sg.In()],
                      [sg.T('    x:'),sg.In(),
                       sg.T('    y:'),sg.In(),
                       sg.T('    z:'),sg.In()],
                      [sg.T('sellersprice:'),sg.In()],
                      [sg.Button('Predict manual'),
                       sg.T(key='RES_MANUAL')]] 

# tabel hoofing
table_header = ['carat', 'depth', 'table', 'x', 'y', 'z', 'sellersprice', 'price', 'diff']

# tabel inhoud
table_content = []

# tabel tab auto
tab_auto_layout = [[sg.T('number of samples:'),
                    sg.Slider(range=(1,20), size=(300,10), 
                              default_value=5, 
                              orientation='h',
                              enable_events=True,
                              key='NUM_SL')],
                   [sg.T('max carat:'),
                    sg.Slider(range=(0.1,4.0), size=(300,10),
                              resolution=0.1,
                              orientation='h',
                              enable_events=True,
                              key='CARAT_TO_SL')],
                   [sg.Table(headings=table_header,
                             values=table_content,
                             display_row_numbers=True,
                             auto_size_columns=True,
                             justification='center',
                             key='RES_AUTO')],
                   [sg.Button('Get samples'), sg.Button('Calculate')]]

layout = [[sg.TabGroup([[sg.Tab('Manual', tab_manual_layout), 
                         sg.Tab('Automatic', tab_auto_layout)]],
           expand_x=True, expand_y=True)]]

# Create the Window
window = sg.Window('Diamond Price Control', layout, default_element_size=(12,1), size=(480,280))
# Event Loop to process "events"
while True:             
    event, values = window.read()
    # afsluiten
    if event == sg.WIN_CLOSED:
        break
    # klik op Predict manual knop 
    if event == 'Predict manual':
        try:
            carat = float(values[0])  # waarde uit 1ste veld
            depth = float(values[1])
            table = float(values[2])
            x = float(values[3])
            y = float(values[4])
            z = float(values[5])
            sellersprice = float(values[6])
            # dictionary maken van data
            ddata = {'carat':[carat], 'depth':[depth], 'table':[table],
                     'x':[x], 'y':[y], 'z':[z], 'price':[sellersprice]}
            # data in dataframe stoppen
            df_data = pd.DataFrame.from_dict(ddata)
            # door de dataPipeline sturen
            X,y,_ = dPW.preprocess_targetTf(df_data, ['carat', 'y'], 'price',
                                    learnedProcess=dataPipeline)
            # X transformeren naar X²
            X = dPW.polyTrans(X, 2)
            # voorspellen van de prijs
            predict_price = model.predict(X)
            # terug omzetten van de predict_price met 2**
            predict_price = np.round(2**predict_price, 2)
            # verschil tussen echte en voorspelde waarde
            diff = predict_price - sellersprice
            window['RES_MANUAL'].update('voorspelde prijs:'+str(predict_price[0])
                                        +' (verschil:'+str(diff[0])+')')
            if diff < 0:
                window['RES_MANUAL'].update(text_color='black')
            else:
                window['RES_MANUAL'].update(text_color='blue')                
        except Exception as E:
            window['RES_MANUAL'].update('ERR: '+str(E))
            window['RES_MANUAL'].update(text_color='red')
            
window.close()
