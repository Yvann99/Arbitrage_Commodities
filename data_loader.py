#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 16:30:05 2026

@author: yvannlandure
"""

#Importation des bibliothèques de travail
import numpy as np
import yfinance as yf
import scipy.stats 
import pandas as pd

#importation des données
tickers = ["BZ=F", "CL=F"]
dataset = yf.download(tickers, period ="3Y")["Close"]

#nettoyage des données et Gestion des lignes vides
dataset_clean = dataset.dropna()
print (dataset_clean.head())

#Création de la série temporelle de l'écart Brent-WTI
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller #pour le test
#Calcul du spread
dataset_clean['Spread'] = dataset_clean['BZ=F']-dataset_clean['CL=F'] #si la colonne n'existe pas, elle est créée

#test adfuller
result = adfuller(dataset_clean['Spread'].dropna())

#Affichage des résultats du test
adf_value = result[0]
p_value = result[1]
valeurs_critiques = result[2]
print("-"*15)
print(f"Statistique du test ADF: {adf_value:.4f}")
print("-"*15)
print(f"p_value du test ADF: {p_value:.4f}")
print("-"*15)

# Calcul de la moyenne et de l'écart-type mobiles (ex: fenêtre de 20 jours)
window = 20
dataset_clean['Mean'] = dataset_clean['Spread'].rolling(window=window).mean()
dataset_clean['Stdev'] = dataset_clean['Spread'].rolling(window=window).std()

# Calcul du Z-Score
dataset_clean['Z-Score'] = (dataset_clean['Spread'] - dataset_clean['Mean']) / dataset_clean['Stdev']

##Tracé du z-score
plt.figure(figsize=(12,6))
dataset_clean['Z-Score'].plot()
plt.axhline(0, color='black')
plt.axhline(2, color='red', linestyle='--')
plt.axhline(-2, color='green', linestyle='--')
plt.title("Z-Score du Spread Brent-WTI")
plt.show()