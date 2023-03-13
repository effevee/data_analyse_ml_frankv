#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 21:02:12 2023

@author: frank
"""

from sklearn.pipeline import Pipeline                 # klasse voor de data pipeline lib
from sklearn.preprocessing import StandardScaler      # klasse voor het standaardiseren van de data
from sklearn.compose import ColumnTransformer         # klasse om kolommen te transformeren en/of te verwijderen
from sklearn.preprocessing import PolynomialFeatures  # klasse om hogere machten toe te voegen aan de datapunten
import numpy as np


def preprocess_targetTf(dataset,features,target,learnedProcess=None):
    # uit de dataset de features halen
    X = dataset[features]
    # uit de dataset de target halen
    y = dataset[target]
    # object voor het transformeren van numerieke kolommen.
    # in steps komt een rij daarin tuples. Iedere tuple bevat een transformatie functie.
    # het eerste elem van de tuple is een naam (zelf te kiezen), het tweede elem is de transformatie functie
    X_res = None
    if learnedProcess == None: # indien learnedProcess niet ingevuld is moet er geleerd worden met leer of trainset
        num_transform = Pipeline(steps=[('scaler',StandardScaler())])
        # object voor kolommen te transformeren
        # in tranformers zit een lijst van tuples met de transformers.
        # het eerste elem van de tuple is een naam (zelf te kiezen), het tweede elem is de transformatie (num_transform)
        # het derde elem zijn de kolommen waarop de transformatie moet gebeuren 
        coltransform = ColumnTransformer(transformers=[('num',num_transform,features)])
        # proces pipeline maken met daarin de transofrmaties
        process = Pipeline(steps=[('coltrans',coltransform)])
        # is geleerd, learnedProcess wordt ingevuld
        learnedProcess = process
        # voer de transformatie uit
        # hier wordt de dataset getransformeerd naa de kolommen die we willen behouden
        # en het standaardiseren van de data (x-gem)/stdev
        X_res = process.fit_transform(X)
    else:
        # de geleerde transfrormaties worden uitgevoerd op test, validatie en nieuwe waarden
        X_res = learnedProcess.transform(X)
    # dataframe omzetten naar lijst
    y=list(y)
    y=np.log2(y)
    # retourneren van de getransformeerde data en proces
    return X_res,y,learnedProcess


def polyTrans(X,degree=2):
    poly_feats = PolynomialFeatures(degree=degree,include_bias=False)
    X_poly = poly_feats.fit_transform(X)
    return X_poly
