# Imperialist Competitive Algorithm: A Socio Politically Inspired Optimization Strategy
# Developed By: Esmaeil Atashpaz Gargari
# Translated to Python By: Juanjo Sierra

from CreateInitialEmpires import *
from AssimilateColonies import *
from RevolveColonies import *
from PosessEmpire import *
from UniteSimilarEmpires import *
from ImperialisticCompetition import *
from Empire import Empire

def ICA(CostFunction, params, domain):
  # Initial empires are defined
  empires = CreateInitialEmpires(CostFunction, params["ncountries"], params["nimperialists"], params["zeta"], domain)

  # Main loop
  revolution_rate = params["initial_revolution_rate"]
  for decade in range(params["decades"]):
    revolution_rate = params["damp_ratio"]*revolution_rate

    for i,emp in enumerate(empires):
      emp = AssimilateColonies(emp, domain, params["assimilation_coef"], CostFunction)
      emp = RevolveColonies(emp, domain, revolution_rate, CostFunction)
      emp = PosessEmpire(emp)
      emp.empire_total_cost = emp.imperialist_fitness + params["zeta"] * np.mean(emp.colonies_fitness)
      empires[i] = emp

    # The imperialistic competition takes place
    empires = ImperialisticCompetition(empires, domain)

    if len(empires) == 1 and params["stop_if_just_one_empire"]:
      break

    best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)
    print("Decade {:4}, best solution: {:e}".format(decade, emp.imperialist_fitness))
