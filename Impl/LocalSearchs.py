# Local Search and CMA-ES for memetic version
# Developed by: Pablo Baeyens

import LSDani
from scipy.optimize import minimize

def ls(CostFunction, initial_sol, initial_fitness, nevals, domain):
  res = minimize(CostFunction, initial_sol,
           method = "L-BFGS-B",
           bounds = domain["dim"]*[(domain["lower_bound"], domain["upper_bound"])],
           options = dict(maxfun = nevals))
  return res["x"], res["fun"]


def ImproveEmpire(emp, domain, params, CostFunction):
  res = ls(CostFunction, emp.imperialist, emp.imperialist_fitness, params["nevals"], domain)

  if emp.imperialist_fitness < res[1]:
    emp.imperialist = res[0]
    emp.imperialist_fitness = res[1]

  return emp
