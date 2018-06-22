from ICA import *
from cec2014 import cec2014
import statistics
import numpy as np

# Función objetivo
def objetivo(i):
  def f(x):
    if "ncall" not in f.__dict__:
      f.ncall = 0
    else:
      f.ncall += 1
    return cec2014.cec14(x,i)
  f.n = i
  return f

# Parámetros modificables
PARAMS = {
  "nimperialists": 8,
  "assimilation_coef": 2,
  "zeta": 0.02,
  "initial_revolution_rate": 0.3,
  "damp_ratio": 0.99,
}


###
# Ejecución del algoritmo y opciones
###


DIM = 0
while DIM not in {10,30}:
  DIM = int(input("Dimensión (10/30): "))

print("Algoritmos disponibles: ", list(algoritmos.keys()))
nombre = ""
while nombre not in algoritmos.keys():
  nombre = input("nombre: ")

DOMAIN = {
  "dim": DIM,"lower_bound": -100, "upper_bound": 100, "max_evals": 10000*DIM
}

algoritmo = algoritmos[nombre]

print("Dimensión: {dim}".format(dim = DIM))
print("Algoritmo: {nombre}".format(nombre = algoritmo.nombre))
print("F","Media","Desviación estándar", sep=", ")

numpy.random.seed(73)

for i in range(1,21):
  a = []
  for _ in range(25):
    best = algoritmo(objetivo(i), PARAMS, DOMAIN)
    a.append(objetivo(i)(best) - 100*i)
  m = statistics.mean(a)
  s = statistics.stdev(a)
  print(i,m,s,sep = ", ")
