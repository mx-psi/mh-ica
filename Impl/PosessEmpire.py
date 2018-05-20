import numpy as np

def PosessEmpire(emp):

    best_colony = np.argmin(emp.colonies_fitness)

    if emp.colonies_fitness[best_colony] < emp.imperialist_fitness:
        old_imperialist = emp.imperialist
        old_imperialist_fitness = emp.imperialist_fitness
        emp.imperialist = emp.colonies[best_colony]
        emp.imperialist_fitness = emp.colonies_fitness[best_colony]
        emp.colonies[best_colony] = old_imperialist
        emp.colonies_fitness[best_colony] = old_imperialist_fitness

    return emp
