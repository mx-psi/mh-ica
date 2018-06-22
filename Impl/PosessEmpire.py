import numpy as np

def PosessEmpire(emp):
  best = np.argmin(emp.colonies_fitness)
  if emp.colonies_fitness[best] < emp.imperialist_fitness:
    old_imperialist = emp.imperialist
    old_imperialist_fitness = emp.imperialist_fitness
    emp.imperialist = emp.colonies[best].copy()
    emp.imperialist_fitness = emp.colonies_fitness[best]
    emp.colonies[best] = old_imperialist
    emp.colonies_fitness[best] = old_imperialist_fitness
  return emp
