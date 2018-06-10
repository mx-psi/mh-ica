from ICA import *
from cec2014 import cec2014
import statistics
import numpy as np

def objetivo(i):
  def f(x):
    if "ncall" not in f.__dict__:
      f.ncall = 0
    else:
      f.ncall += 1

    if not x.flags["C_CONTIGUOUS"]:
      x = np.ascontiguousarray(x)
    return cec2014.cec14(x,i)
  return f

params = {
  "ncountries": 80,
  "nimperialists": 8,
  "decades": 2000,
  "initial_revolution_rate": 0.3,
  "assimilation_coef": 2,
  "zeta": 0.02,
  "damp_ratio": 0.99,
  "stop_if_just_one_empire": False,
  "uniting_threshold": 0.02,
  "zarib":1.05, # Zarib is used to prevent the weakest empire to have a probability of zero
  "alpha": 0.1  # importance of the mean minimun compared to the global minimum. Must be << 1
}

DIM = 30
problem_domain = {
  "dim": DIM,
  "lower_bound": -100,
  "upper_bound": 100,  # tuple including lower and upper bounds
  "max_evals": 10000*DIM # 10000*dim
}

if __name__ == "__main__":
  print("F","Media","Desviación estándar", sep=", ")
  for i in range(1,21):
    a = []
    for _ in range(25):
      best = ICA(objetivo(i), params, problem_domain)
      a.append(objetivo(i)(best) - 100*i)
    m = statistics.mean(a)
    s = statistics.stdev(a)
    print(i,m,s, sep = ", ")
