import numpy as np
import numpy.matlib

def AssimilateColonies(emp, domain, assimilation_coef, CostFunction):
    # The imperialist position will have an impact in any colony movement
    vector = np.matlib.repmat(emp.imperialist, len(emp.colonies), 1) - emp.colonies

    # The multiplier helps searching different points around the imperialist
    multiplier = np.random.rand(len(vector)).reshape(len(vector), 1)

    # And finally we calculate each colony's new position, and clip the values according to the domain
    emp.colonies = emp.colonies + 2 * assimilation_coef * multiplier * vector
    emp.colonies = np.clip(emp.colonies, domain["lower_bound"],  domain["upper_bound"])
    emp.colonies_fitness = np.apply_along_axis(CostFunction, 1, emp.colonies)
    return emp


## Versión de asimilación con evolución diferencial
def AssimilateColoniesDE(emp, domain, CR, F, CostFunction):
  n = len(emp.colonies)

  if n < 4:
    return AssimilateColonies(emp, domain, 2, CostFunction)

  for j in range(n):
    b, c = emp.colonies[np.random.choice([idx for idx in range(n) if idx != j],
                                         2, replace = False)]

    mutant = np.clip(emp.colonies[j] + F*(emp.imperialist - emp.colonies[j]) + F*(b - c),
                     domain["lower_bound"], domain["upper_bound"])

    cross_points = np.random.rand(domain["dim"]) < CR

    if not np.any(cross_points):
      cross_points[np.random.randint(0, dimensions)] = True
    trial = np.where(cross_points, mutant, emp.colonies[j])
    trial_fitness =  CostFunction(trial)

    if trial_fitness < emp.colonies_fitness[j]:
      emp.colonies[j]         = trial
      emp.colonies_fitness[j] = trial_fitness
  return emp
