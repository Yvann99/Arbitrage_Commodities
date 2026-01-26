'Le test adfuller renvoie un tuple contenant : la statistique du test, la p-value et les valeurs critiques


'la stats du test: C'est un nombre (souvent négatif). Plus ce nombre est petit (très négatif), plus la probabilité que ton spread soit stationnaire est forte.


'si p<0,05 le spread est stationnaire et alors on va lancer la stratégie d'arbitrage


'sinon on considère que le spread est une marche aléatoire


'les valeurs critiques : C'est un dictionnaire qui donne les seuils de la statistique de test pour différents niveaux de confiance (1%, 5%, 10%).