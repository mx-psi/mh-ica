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
