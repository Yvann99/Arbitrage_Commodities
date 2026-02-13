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

# Paramètres de la stratégie
window = 20
entry_threshold = 2.0
exit_threshold = 0

# Calcul de la moyenne et écart-type mobiles
dataset_clean['Mean'] = dataset_clean['Spread'].rolling(window=window).mean()
dataset_clean['Stdev'] = dataset_clean['Spread'].rolling(window=window).std()

# Calcul du Z-Score
dataset_clean['Z-Score'] = (dataset_clean['Spread'] - dataset_clean['Mean']) / dataset_clean['Stdev']

# Initialisation de la colonne Position (0 = neutre, 1 = Long Spread, -1 = Short Spread)
dataset_clean['Position'] = 0

# Génération des signaux (logique simplifiée)
for i in range(1, len(dataset_clean)):
    z = dataset_clean['Z-Score'].iloc[i]
    prev_pos = dataset_clean['Position'].iloc[i-1]
    
    if prev_pos == 0:
        if z > entry_threshold:
            dataset_clean.iloc[i, dataset_clean.columns.get_loc('Position')] = -1 # Short Spread
        elif z < -entry_threshold:
            dataset_clean.iloc[i, dataset_clean.columns.get_loc('Position')] = 1  # Long Spread
    elif prev_pos == 1:
        if z >= exit_threshold:
            dataset_clean.iloc[i, dataset_clean.columns.get_loc('Position')] = 0  # Sortie Long
        else:
            dataset_clean.iloc[i, dataset_clean.columns.get_loc('Position')] = 1  # Garder Long
    elif prev_pos == -1:
        if z <= exit_threshold:
            dataset_clean.iloc[i, dataset_clean.columns.get_loc('Position')] = 0  # Sortie Short
        else:
            dataset_clean.iloc[i, dataset_clean.columns.get_loc('Position')] = -1 # Garder Short

# Calcul des rendements du spread (différence de prix jour J - jour J-1)
dataset_clean['Spread_Change'] = dataset_clean['Spread'].diff()

# Calcul du PNL quotidien (on utilise la position de la veille pour le mouvement d'aujourd'hui)
dataset_clean['Daily_PNL'] = dataset_clean['Position'].shift(1) * dataset_clean['Spread_Change']

# Calcul du PNL cumulé
dataset_clean['Cum_PNL'] = dataset_clean['Daily_PNL'].fillna(0).cumsum()

# Affichage des statistiques de performance
total_pnl = dataset_clean['Cum_PNL'].iloc[-1]
print(f"PNL Total de la stratégie : {total_pnl:.2f} $")

# Visualisation
plt.figure(figsize=(12,6))
dataset_clean['Cum_PNL'].plot(color='blue', lw=2)
plt.title("Évolution du PNL Cumulé - Arbitrage Brent/WTI")
plt.xlabel("Date")
plt.ylabel("Profit ($)")
plt.grid(True)
plt.show()