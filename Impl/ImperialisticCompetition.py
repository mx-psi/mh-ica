import numpy as np
from Empire import Empire

def ImperialisticCompetition(empires, domain):
    if np.random.rand() < 0.11 or len(empires) <= 1:
        return empires

    empires_total_cost = np.empty(len(empires))
    for i in range(len(empires)):
      empires_total_cost[i] = empires[i].empire_total_cost

    # Search for the weakest empire (the one with the higher cost)
    weakest_index = (-empires_total_cost).argsort()[0]
    weakest = empires[weakest_index]
    max_total_cost = empires_total_cost[weakest_index]
    total_powers = max_total_cost - empires_total_cost
    posession_probability = total_powers / np.sum(total_powers)

    # The empire that will conquer the colony is chosen
    winner = empires[SelectAnEmpire(posession_probability)]
    selected_colony = np.random.randint(0, len(weakest.colonies))

    # Conquest
    winner.colonies = np.append(winner.colonies, weakest.colonies[selected_colony].reshape(1,domain["dim"]), axis=0)
    winner.colonies_fitness = np.append(winner.colonies_fitness, weakest.colonies_fitness[selected_colony])
    weakest.colonies = np.delete(weakest.colonies, selected_colony, 0)
    weakest.colonies_fitness = np.delete(weakest.colonies_fitness, selected_colony)

    # If the weakest_index empire remains with one or less colonies (apart from the imperialist), it is also absorbed
    if len(weakest.colonies) <= 1:
        colonies_addition = np.append(weakest.colonies, weakest.imperialist.reshape(1,domain["dim"]), axis=0)
        fitness_addition = np.append(weakest.colonies_fitness, weakest.imperialist_fitness)
        winner.colonies = np.append(winner.colonies, colonies_addition, axis=0)
        winner.colonies_fitness = np.append(winner.colonies_fitness, fitness_addition)
        del empires[weakest_index]

    return empires

# A function for selecting a random empire with given probabilities
def SelectAnEmpire(possesion_probability):
    r = np.random.rand(len(possesion_probability))
    d = possesion_probability - r

    # The empire with higher value will be selected
    selected = (-d).argsort()[0]
    return selected
