# Local Search and CMA-ES for memetic version
# Developed by: Pablo Baeyens

import LSDani

def ls(CostFunction, initial_sol, initial_fitness, nevals, domain):
  sw = LSDani.SolisWets(CostFunction,
                        [domain["lower_bound"], domain["upper_bound"]],
                        domain["dim"])
  options = sw.getInitParameters(10)
  return sw.improve(initial_sol, initial_fitness, nevals, options)


def ImproveEmpire(emp, domain, CostFunction):
  res = ls(CostFunction, emp.imperialist, emp.imperialist_fitness, 500, domain)
  emp.imperialist = res[0]
  emp.imperialist_fitness = res[1]
  return emp
