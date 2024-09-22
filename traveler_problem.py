import random
from tqdm import tqdm

def calculate_distance(route, distances):
    """
    Calculates the total distance of a given route
    """

    distance = 0
    for i in range(len(route) - 1):
        distance += distances[route[i]][route[i + 1]]
    distance += distances[route[-1]][route[0]]
    return distance

def fitness(P, distances):
    """
    Calculates the fitness of each route in the population,
    the fitness is the total distance of the route
    """

    fit_values = []
    for route in P:
        fit_values.append(calculate_distance(route, distances))
    return fit_values

def selection(P, fit):
    """Selects the two best routes in the population"""
    sorted_population = []
    for i in range(len(P)):
        sorted_population.append((P[i], fit[i]))
    sorted_population.sort(key=lambda x: x[1])
    return sorted_population[0][0], sorted_population[1][0]

def crossover(P_1):
    """
    Performs the crossover between the two best routes, 
    selecting a random segment of the first parent and filling the child with the genes of the second parent
    """

    size = len(P_1[0])
    child = [None] * size

    a, b = sorted(random.sample(range(size), 2))

    child[a:b+1] = P_1[0][a:b+1]

    pos = (b+1) % size
    for gene in P_1[1]:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % size

    return child
    
def mutation(P, pm):
    """
    Performs the mutation of the population, swapping two random cities in a route
    """
    for i in P:
        r = random.random()
        if r < pm:
            a, b = sorted(random.sample(range(len(i)), 2))
            i[a], i[b] = i[b], i[a]

def evolutionAlgorithm(N, distances, pr, pm):
    """
    The evolution algorithm.
    """

    cities = list(range(len(distances)))
    P = []
    for _ in range(N):
        P.append(random.sample(cities, len(cities)))
    fit = fitness(P, distances)

    max_depth = 1000
    for _ in tqdm(range(max_depth), desc="Evolution"):
        P_1 = selection(P, fit)
        r = random.random()
        if r < pr:
            P.append(crossover(P_1))
        mutation(P, pm)
        fit = fitness(P, distances)
        
        # Select the N best routes, based on the fitness
        P_fit = list(zip(P, fit))
        P_fit = sorted(P_fit, key=lambda x: x[1])[:N]
        P = [x[0] for x in P_fit]
        fit = [x[1] for x in P_fit]
    
    best_route = selection(P, fit)[0]
    return best_route

distancias = [
    [0, 12, 23, 34, 45, 56, 67, 78, 89, 90],
    [12, 0, 25, 36, 47, 58, 69, 80, 91, 92],
    [23, 25, 0, 15, 26, 37, 48, 59, 70, 81],
    [34, 36, 15, 0, 17, 28, 39, 50, 61, 72],
    [45, 47, 26, 17, 0, 11, 22, 33, 44, 55],
    [56, 58, 37, 28, 11, 0, 13, 24, 35, 46],
    [67, 69, 48, 39, 22, 13, 0, 11, 22, 33],
    [78, 80, 59, 50, 33, 24, 11, 0, 13, 24],
    [89, 91, 70, 61, 44, 35, 22, 13, 0, 15],
    [90, 92, 81, 72, 55, 46, 33, 24, 15, 0]
]

best_route = evolutionAlgorithm(1000, distancias, 0.5, 0.1)
print(best_route)
print(calculate_distance(best_route, distancias))