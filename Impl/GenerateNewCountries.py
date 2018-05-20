import numpy as np

def GenerateNewCountries(ncountries, problem_domain):
  lower_bound = problem_domain["lower_bound"]
  upper_bound = problem_domain["upper_bound"]
  dim = problem_domain["dim"]

  new_countries = np.random.uniform(lower_bound, upper_bound, ncountries*dim).reshape(ncountries,dim)
  return new_countries
