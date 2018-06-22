import numpy as np
from GenerateNewCountries import *
from Empire import Empire

def CreateInitialEmpires(CostFunction, ncountries, nimperialists, zeta, problem_domain):

    # Generation of the initial countries
    countries = GenerateNewCountries(ncountries, problem_domain)
    fitness = np.apply_along_axis(CostFunction, 1, countries)

    # And now the countries get sorted by their fitness
    order = np.argsort(fitness)
    fitness = fitness[order]
    countries = countries[order]
    ######################

    num_colonies = np.shape(countries)[0] - nimperialists

    # Countries are divided into imperialists and colonies
    imperialists = countries[0:nimperialists]
    imperialists_fitness = fitness[0:nimperialists]
    colonies = countries[nimperialists:]
    colonies_fitness = fitness[nimperialists:]

    # Imperialist power is calculated
    if max(imperialists_fitness) > 0:
        imperialist_power = 1.3 * max(imperialists_fitness) - imperialists_fitness
    else:
        imperialist_power = 0.7 * max(imperialists_fitness) - imperialists_fitness

    # Number of colonies per imperialist are defined according to their power
    colonies_per_imperialist = np.round(imperialist_power/np.sum(imperialist_power) * num_colonies)

    # Given a random permutation of the colonies, they are splitted
    randperm = np.random.permutation(num_colonies)
    colonies = colonies[randperm]
    colonies_fitness = colonies_fitness[randperm]
    cumulative_colonies_per_imperialist = np.cumsum(colonies_per_imperialist).astype(int)
    new_colonies = np.split(colonies, cumulative_colonies_per_imperialist)[0:nimperialists]
    new_colonies_fitness = np.split(colonies_fitness, cumulative_colonies_per_imperialist)
    empires_total_cost = np.array([])

    for i in range(nimperialists):
        empires_total_cost = np.append(empires_total_cost, imperialists_fitness[i] + zeta * np.mean(new_colonies_fitness[i]))

    empires = []
    for i in range(nimperialists):
      empires.append(Empire(imperialists[i], imperialists_fitness[i], new_colonies[i], new_colonies_fitness[i], empires_total_cost[i]))

    return empires
