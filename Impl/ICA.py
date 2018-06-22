# Imperialist Competitive Algorithm: A Socio Politically Inspired Optimization Strategy
# Developed By: Esmaeil Atashpaz Gargari
# Translated to Python By: Juanjo Sierra
# Improved by: Pablo Baeyens

from CreateInitialEmpires import *
from AssimilateColonies import *
from RevolveColonies import *
from PosessEmpire import *
from ImperialisticCompetition import *
from Empire import Empire
from LocalSearchs import *

# Versión ICA Original
def ICAOrig(CostFunction, params, domain):
  CostFunction.ncall = 0
  empires = CreateInitialEmpires(CostFunction, 80, params["nimperialists"], params["zeta"], domain)
  revolution_rate = params["initial_revolution_rate"]
  while CostFunction.ncall < domain["max_evals"]:
    revolution_rate = params["damp_ratio"]*revolution_rate

    for i,emp in enumerate(empires):
      emp = AssimilateColonies(emp, domain, params["assimilation_coef"], CostFunction)
      emp = RevolveColonies(emp, domain, revolution_rate, CostFunction)
      emp = PosessEmpire(emp)
      emp.empire_total_cost = emp.imperialist_fitness + params["zeta"] * np.mean(emp.colonies_fitness)
      empires[i] = emp

    empires = ImperialisticCompetition(empires, domain)

  best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)
  return best_empire.imperialist

ICAOrig.nombre = "ICA Original"

# Versión ICA memético
# Hace una búsqueda local para cada imperialista
def ICAAllLS(CostFunction, params, domain):
  CostFunction.ncall = 0
  empires = CreateInitialEmpires(CostFunction, 80, params["nimperialists"], params["zeta"], domain)

  revolution_rate = params["initial_revolution_rate"]
  while CostFunction.ncall < domain["max_evals"]:
    revolution_rate = params["damp_ratio"]*revolution_rate

    for i,emp in enumerate(empires):
      emp = ImproveEmpire(emp, domain, params, CostFunction)
      emp = AssimilateColonies(emp, domain, params["assimilation_coef"], CostFunction)
      emp = RevolveColonies(emp, domain, revolution_rate, CostFunction)
      emp = PosessEmpire(emp)
      emp.empire_total_cost = emp.imperialist_fitness + params["zeta"] * np.mean(emp.colonies_fitness)
      empires[i] = emp

    empires = ImperialisticCompetition(empires, domain)
    best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)

  best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)
  return best_empire.imperialist

ICAAllLS.nombre = "ICA BL todos"


def ICABestLS(CostFunction, params, domain):
  CostFunction.ncall = 0
  empires = CreateInitialEmpires(CostFunction, 80, params["nimperialists"], params["zeta"], domain)

  revolution_rate = params["initial_revolution_rate"]
  while CostFunction.ncall < domain["max_evals"]:
    revolution_rate = params["damp_ratio"]*revolution_rate

    for i,emp in enumerate(empires):
      emp = AssimilateColonies(emp, domain, params["assimilation_coef"], CostFunction)
      emp = RevolveColonies(emp, domain, revolution_rate, CostFunction)
      emp = PosessEmpire(emp)
      emp.empire_total_cost = emp.imperialist_fitness + params["zeta"] * np.mean(emp.colonies_fitness)
      empires[i] = emp

    empires = ImperialisticCompetition(empires, domain)
    best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)
    best_empire = ImproveEmpire(best_empire, domain, params, CostFunction)

  best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)
  return best_empire.imperialist

ICABestLS.nombre = "ICA BL mejor"

# Versión ICA DE
def ICADE(CostFunction, params, domain):
  CostFunction.ncall = 0
  empires = CreateInitialEmpires(CostFunction, 100, params["nimperialists"], params["zeta"], domain)
  revolution_rate = params["initial_revolution_rate"]
  while CostFunction.ncall < domain["max_evals"]:
    revolution_rate = params["damp_ratio"]*revolution_rate

    for i,emp in enumerate(empires):
      emp = AssimilateColoniesDE(emp, domain, 0.9, 0.5, CostFunction)
      emp = RevolveColonies(emp, domain, revolution_rate, CostFunction)
      emp = PosessEmpire(emp)
      emp.empire_total_cost = emp.imperialist_fitness + params["zeta"] * np.mean(emp.colonies_fitness)
      empires[i] = emp

    empires = ImperialisticCompetition(empires, domain)
    best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)

  best_empire = min(empires, key = lambda emp: emp.imperialist_fitness)
  return best_empire.imperialist

ICADE.nombre = "ICA DE"


algoritmos = {
  "original": ICAOrig,
  "BLtodos": ICAAllLS,
  "BLMejor": ICABestLS,
  "DE": ICADE
}
