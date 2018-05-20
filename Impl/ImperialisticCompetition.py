import numpy as np
from Empire import Empire

def ImperialisticCompetition(empires, domain):
    if np.random.rand() > 0.11 or len(empires) <= 1:
        return empires

    imperialists, imperialists_fitness, colonies, colonies_fitness, empires_total_cost = [], [], [], [], np.empty(len(empires))
    for i in range(len(empires)):
      imperialists.append(empires[i].imperialist)
      imperialists_fitness.append(empires[i].imperialist_fitness)
      colonies.append(empires[i].colonies)
      colonies_fitness.append(empires[i].colonies_fitness)
      empires_total_cost[i] = empires[i].empire_total_cost

    # Search for the weakest empire (the one with the higher cost)
    weakest = (-empires_total_cost).argsort()[0]
    max_total_cost = empires_total_cost[weakest]
    total_powers = max_total_cost - empires_total_cost
    posession_probability = total_powers / np.sum(total_powers)

    # The empire that will conquer the colony is chosen
    selected_empire = SelectAnEmpire(posession_probability)
    selected_colony = np.random.randint(0, len(colonies[weakest]))

    # Conquest
    colonies[selected_empire] = np.append(colonies[selected_empire], colonies[weakest][selected_colony].reshape(1,domain["dim"]), axis=0)
    colonies_fitness[selected_empire] = np.append(colonies_fitness[selected_empire], colonies_fitness[weakest][selected_colony])

    # The colony is removed from its former empire
    colonies[weakest] = np.delete(colonies[weakest], selected_colony, 0)
    colonies_fitness[weakest] = np.delete(colonies_fitness[weakest], selected_colony)

    # If the weakest empire remains with one or less colonies (apart from the imperialist), it is also absorbed
    if len(colonies[weakest]) <= 1:
        colonies_addition = np.append(colonies[weakest], imperialists[weakest].reshape(1,domain["dim"]), axis=0)
        fitness_addition = np.append(colonies_fitness[weakest], imperialists_fitness[weakest])
        colonies[selected_empire] = np.append(colonies[selected_empire], colonies_addition, axis=0)
        colonies_fitness[selected_empire] = np.append(colonies_fitness[selected_empire], fitness_addition)

        del colonies[weakest]
        del colonies_fitness[weakest]
        imperialists = np.delete(imperialists, weakest, 0)
        imperialists_fitness = np.delete(imperialists_fitness, weakest)
        empires_total_cost = np.delete(empires_total_cost, weakest)

    empires = []
    for i in range(len(imperialists)):
      empires.append(Empire(imperialists[i], imperialists_fitness[i],
                         colonies[i], colonies_fitness[i], empires_total_cost[i]))

    return empires

# A function for selecting a random empire with given probabilities
def SelectAnEmpire(probability):
    r = np.random.rand(len(probability))
    d = probability - r

    # The empire with higher value will be selected
    selected = (-d).argsort()[0]
    return selected
