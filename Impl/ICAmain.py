from ICA import *
from cec2014 import cec2014

params = {
  "ncountries": 80,
  "nimperialists": 8,
  "decades": 2000,
  "initial_revolution_rate": 0.3,
  "assimilation_coef": 2,
  "assimilation_angle_coef": 0.5,
  "zeta": 0.02,
  "damp_ratio": 0.99,
  "stop_if_just_one_empire": True,
  "uniting_threshold": 0.02,
  "zarib":1.05, # Zarib is used to prevent the weakest empire to have a probability of zero
  "alpha": 0.1  # importance of the mean minimun compared to the global minimum. Must be << 1
}

problem_domain = {
  "dim": 30,
  "lower_bound": -100,
  "upper_bound": 100  # tuple including lower and upper bounds
}

if __name__ == "__main__":
  objetivo = lambda x: cec2014.cec14(x,19)
  ICA(objetivo, params, problem_domain)
