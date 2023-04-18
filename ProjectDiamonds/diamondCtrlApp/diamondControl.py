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
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import codecs
import os


# om javascript popups te sluiten
def closePopUps(selDriver):
    # id van venster site
    parent = selDriver.current_window_handle
    # ids van javascript popups
    uselessWindows = selDriver.window_handles
    # door alle ids lopen
    for winID in uselessWindows:
        # indien niet gelijk aan venster site
        if winID != parent:
            # zet focus op popup
            selDriver.switch_to.window(winID)
            # sluit popup
            selDriver.close()
            
# om andere popups te sluiten
def closePopUpsDivs(selDriver):
    try:
        # sluit cookies popup
        elem = selDriver.find_element(By.CSS_SELECTOR,'#onetrust-close-btn-container > button')
        elem.click()
        # sluit reclame popup
        elem = selDriver.find_element(By.CSS_SELECTOR,'#body1 > div.ECModalstyle__Modal-sc-n33mnt-1' + 
                '.dpWiHq.InspirationTrafficPopupstyles__ECModalStyled-sc-8kybsb-0.fbtFrg > button')
        elem.click()
        return True
    except:
        return False
    
# waarde feature uit de broncode string filteren
def getElemByDiv(html_str,div_name):
    if div_name in html_str:
        ib = html_str.index(div_name)+len(div_name)   # begin index van data
        ie = html_str.index('</div>',ib)              # einde index van data
        return html_str[ib:ie]
    else:
        return None

# gegevens ophalen van een diamant
def getDiamondData(idx,selDriver):
    selDriver.implicitly_wait(4)
    if idx == 4: # prutsen
        idx+=1
    diamond = '/html/body/div[1]/div[3]/div/div/div[1]/div/div[2]/div[2]/div[3]/div/div[@@]/div/div[2]/a/div/div/div/div[5]'.replace('@@',str(idx))
    try:
        elem = selDriver.find_element(By.XPATH,diamond)
        elem.click()
    except:
        print('diamant niet gevonden (id:',idx,')')
        return 0,0,0,0,0,False
    selDriver.implicitly_wait(4)
    # broncode van webpagina opslaan
    with codecs.open('file_'+str(idx),'w','utf-8') as f:
        h = selDriver.page_source
        f.write(h)
    # initialiseren variabelen
    carat = 0
    xyz = '0x0x0'
    table = 0
    depth = 0
    price = '€0'
    num_found = 0
    # opgeslagen broncode bestand openen
    with codecs.open('file_'+str(idx),'r','utf-8') as f:
        # lijn per lijn overlopen
        for l in f:
            # price
            res = getElemByDiv(l,'<div class="price--EotcN" data-qa="price2-itemPage_Desktop">')
            if res is not None:
                price = res
                num_found+=1
            # carat
            res = getElemByDiv(l,'<div role="cell" class="propertyRow--yeaVt propertyValueRow" data-qa="stone_carat_value-diamond_information-productDetailsTab">')
            if res is not None:
                carat = float(res)
                num_found+=1
            # table
            res = getElemByDiv(l,'<div role="cell" class="propertyRow--yeaVt propertyValueRow" data-qa="tableSize_value-diamond_information-productDetailsTab">')
            if res is not None:
                table = float(res)
                num_found+=1
            # depth
            res = getElemByDiv(l,'<div role="cell" class="propertyRow--yeaVt propertyValueRow" data-qa="depth_value-productDetailsTab">')
            if res is not None:
                depth = float(res)
                num_found+=1
            # xyz
            res = getElemByDiv(l,'<div role="cell" class="propertyRow--yeaVt propertyValueRow" data-qa="stone_lw_value-productDetailsTab">')
            if res is not None:
                xyz= res
                num_found+=1
            # alles gevonden ?
            if num_found == 5:
                break
    # opgeslagen broncode bestand verwijderen
    os.remove('file_'+str(idx))
    # debug
    print(price,carat,table,depth,xyz)
    return price,carat,table,depth,xyz,True
          
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
table_header = ['carat', 'depth', 'table', '  x ', '  y ', '  z ', 'sellersprice', 'price', 'diff']

# tabel inhoud
table_content = []

# tabel tab auto
tab_auto_layout = [[sg.T('number of samples:'),
                    sg.Slider(range=(1,20), size=(480,10), 
                              default_value=5, 
                              orientation='h',
                              enable_events=True,
                              key='NUM_SL')],
                   [sg.T('max carat:'),
                    sg.Slider(range=(0.1,4.0), size=(480,10),
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
window = sg.Window('Diamond Price Control', layout, default_element_size=(12,1), size=(600,280))
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

    # klik op Get samples knop 
    if event == 'Get samples':
        # aantal samples van website
        val_num_samples = int(values['NUM_SL'])
        # willekeurige waarde nemen tussen 0.1 en val_max_carat
        val_max_carat = float(values['CARAT_TO_SL'])
        print(val_num_samples,val_max_carat)
        for i in range(val_num_samples):
            # willekeurige carat in float 
            carat = random.uniform(0.1,val_max_carat)
            # openen Chrome browser
            driver = webdriver.Chrome('./chromedriver')
            # website url
            driver.get('https://www.jamesallen.com/loose-diamonds/all-diamonds/'
                       +'page-1/?Shape=emerald-cut&CaratFrom='+str(carat))
            # sluiten popups
            closePopUps(driver)
            closePopUpsDivs(driver)
            # ophalen data diamanten
            price,carat,table,depth,xyz,status = getDiamondData(random.randint(1,5), driver)
            if status == True:
                # data toevoegen aan rij table_content
                row = []
                row.append(carat)
                row.append(depth)
                row.append(table)
                xyz = xyz.split('x')
                row+=xyz
                row.append(price)
                row.append('null') # placeholder voorspelde prijs
                row.append('null') # placeholder verschil met verkoopprijs
                table_content.append(row)
                # gui updaten
                window['RES_AUTO'].Update(table_content)
            # sluiten van de pagina
            driver.close()
    
    # klik op Calculate samples knop             
    if event == 'Calculate':
        table2 = table_content.copy()
        for i in range(len(table2)):
            table2[i][6]=float(table2[i][6].replace('€',''))
        table = np.array(table2)
        # door de rijen lopen
        # for row in range(len(table)):
        #     # strings omzetten naar float
        #     carat = float(table[row][0])  # waarde uit 1ste veld
        #     depth = float(table[row][1])
        #     table = float(table[row][2])
        #     x = float(table[row][3])
        #     y = float(table[row][4])
        #     z = float(table[row][5])
        #     sellersprice = float(table[row][6])
        #     # dictionary maken van data
        #     ddata = {'carat':[carat], 'depth':[depth], 'table':[table],
        #               'x':[x], 'y':[y], 'z':[z], 'price':[sellersprice]}
        #     # data in dataframe stoppen
        #     df_data = pd.DataFrame.from_dict(ddata)
        #     # door de dataPipeline sturen[]
        #     X,y,_ = dPW.preprocess_targetTf(df_data, ['carat', 'y'], 'price',
        #                             learnedProcess=dataPipeline)
        #     # X transformeren naar X²
        #     X = dPW.polyTrans(X, 2)
        #     # voorspellen van de prijs
        #     predict_price = model.predict(X)
        #     # terug omzetten van de predict_price met 2**
        #     predict_price = np.round(2**predict_price, 2)
        #     # verschil tussen echte en voorspelde waarde
        #     diff = predict_price - sellersprice
        #     # tabel rij updaten
        #     table[row][7] = str(predict_price)
        #     table[row][8] = str(diff)
        #     print(table[row])
    
window.close()
