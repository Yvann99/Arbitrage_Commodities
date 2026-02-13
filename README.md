Deux séries temporelles (disons le prix du Brent et celui du WTI) sont dites co-intégrées si, bien qu'elles ne soient pas stationnaires individuellement (elles dérivent avec le temps), une combinaison linéaire de ces deux séries est, elle, stationnaire.


1. Acquisition et Nettoyage des Données

Extraction des données historiques sur 3 ans via l'API yfinance.


Traitement des valeurs manquantes et synchronisation des séries temporelles.

2. Analyse de Stationnarité

Calcul du Spread (Brent−WTI).

Utilisation du test statistique Augmented Dickey-Fuller (ADF) pour vérifier la stationnarité de l'écart. Un spread stationnaire garantit que les déviations par rapport à la moyenne sont temporaires.

'Le test adfuller renvoie un tuple contenant : la statistique du test, la p-value et les valeurs critiques

'la stats du test: C'est un nombre (souvent négatif). Plus ce nombre est petit (très négatif), plus la probabilité que ton spread soit stationnaire est forte.

'si p<0,05 le spread est stationnaire et alors on va lancer la stratégie d'arbitrage
'sinon on considère que le spread est une marche aléatoire

'les valeurs critiques : C'est un dictionnaire qui donne les seuils de la statistique de test pour différents niveaux de confiance (1%, 5%, 10%).


3. Modélisation du Signal (Z-Score)

Calcul d'une moyenne et d'un écart-type mobiles (fenêtre glissante de 20 jours).

Normalisation du spread via le Z-Score pour identifier les seuils critiques :

Entrée (Short Spread) : Z>2 (Le Brent est surévalué).

Entrée (Long Spread) : Z<−2 (Le WTI est surévalué).

Sortie : Z revient vers 0.

4. Backtesting et Performance

Simulation des prises de position quotidiennes.

Calcul du PNL (Profit and Loss) cumulé pour évaluer la rentabilité de la stratégie.

