import numpy as np
from GenerateNewCountries import *

def RevolveColonies(emp, domain, revolution_rate, CostFunction):
    # How many countries revolve depends on the revolution rate
    num_revolving_colonies = np.round(revolution_rate * len(emp.colonies)).astype(int)
    dim = domain["dim"]

    # We only have to make new positions and recalculate if there is at least one colony to revolve
    if (num_revolving_colonies > 0):
        # Revolved colonies' positions are generated as new countries
        revolved_positions = GenerateNewCountries(num_revolving_colonies, domain)

        randperm = np.random.permutation(len(emp.colonies))
        emp.colonies = emp.colonies[randperm]
        emp.colonies_fitness = emp.colonies_fitness[randperm]

        # First 'num_revolving_colonies' are exchanged for their new positions
        emp.colonies[0:num_revolving_colonies] = revolved_positions
        emp.colonies_fitness[0:num_revolving_colonies] = np.apply_along_axis(CostFunction, 1, emp.colonies[0:num_revolving_colonies])
    return emp
