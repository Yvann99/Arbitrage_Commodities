def function(x):
    return x**2 + 10*x - 15

def dichotomie(f, y, epsilon=1e-4):
    low = 0
    high = 100
    compteur = 0
    
    if f(low) > f(high):
        order = "decroissant"
    else:
        order = "croissant"
    
    print(f"La fonction est {order} sur [{low};{high}]")

    while (high - low) > epsilon:
        compteur = compteur + 1
        mid = (low + high) / 2
        val_mid = f(mid)
        
        if abs(val_mid - y) < epsilon:
            # Correction ici : il faut renvoyer les deux valeurs
            return mid, compteur
            
        if order == "croissant":
            if val_mid > y:
                high = mid
            else:
                low = mid
        else:
            if val_mid > y:
                low = mid
            else:
                high = mid
                
    return (low + high) / 2, compteur
# Test
solution, iterations = dichotomie(function, 0)
print(f"La solution est environ : {solution:.4f}")
print(f"Nombre d'itérations : {iterations}")

def f(x):
    # Exemple : x^2 + 10x - 15
    return x**2 + 10*x - 15

def df(x):
    # Dérivée de f(x) : 2x + 10
    return 2*x + 10

def newton_raphson(func, dfunc, x0, epsilon=1e-6, max_iter=100):
    x = x0
    iterations = 0
    
    for i in range(max_iter):
        iterations += 1
        f_val = func(x)
        df_val = dfunc(x)
        
        # Sécurité : éviter la division par zéro si la dérivée est nulle
        if abs(df_val) < 1e-12:
            print("Erreur : Dérivée trop proche de zéro.")
            return None, iterations
        
        # Formule de Newton-Raphson : x_next = x - f(x)/f'(x)
        x_next = x - f_val / df_val
        
        # Condition d'arrêt : si l'écart entre deux étapes est inférieur à epsilon
        if abs(x_next - x) < epsilon:
            return x_next, iterations
            
        x = x_next
        
    print("Avertissement : Nombre maximum d'itérations atteint.")
    return x, iterations

# Test de l'algorithme
point_depart = 5.0 # x0
solution, nb_etapes = newton_raphson(f, df, point_depart)

if solution is not None:
    print(f"Solution trouvée : {solution:.6f}")
    print(f"Nombre d'itérations : {nb_etapes}")