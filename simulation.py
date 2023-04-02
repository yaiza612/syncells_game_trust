from creation import quorum_signals
from rules import survive_reproduce_or_die, diffusion
import numpy as np


def run_simulation(number_of_cells, cooperativeness, culture_medium, savings, current_quorum_signals,
                   selfish_and_cooperative_cells, qs_production, diffusion_factor, threshold_for_survive,
                   threshold_for_reproduce, iterations, generator):
    """
    :param number_of_cells: number of different types of cells
    :param cooperativeness: amount of cooperation, how much QS the cell shares
    :param culture_medium: grid with all the cells types
    :param savings: matrix with the savings of every cell
    :param current_quorum_signals: matrix of quorum signals in the medium
    :param selfish_and_cooperative_cells: matrix with selfish and cooperative cells
    :param qs_production: amount of quorum signal produced by every cell
    :param diffusion_factor: how much amount of a quorum signal diffuse in the medium
    :param threshold_for_survive: amount of quorum signals you need for survive
    :param threshold_for_reproduce: amount of quorum signals you need for reproduce yourself
    :param iterations: how many time steps for running the simulation
    :return: updated culture medium, current quorum signals and savings of the next time step
    """
    list_medium = [np.copy(culture_medium)]
    list_qs = [np.copy(current_quorum_signals)]
    list_savings = [np.copy(savings)]
    list_selfish_and_cooperative = [np.copy(selfish_and_cooperative_cells)]
    for _ in range(iterations):
        current_quorum_signals = diffusion(current_quorum_signals, diffusion_factor)
        current_quorum_signals, savings = quorum_signals(cooperativeness, current_quorum_signals,
                                                         selfish_and_cooperative_cells, qs_production, savings,
                                                         culture_medium)
        culture_medium, current_quorum_signals, selfish_and_cooperative_cells, savings = \
            survive_reproduce_or_die(number_of_cells, culture_medium, savings, current_quorum_signals,
                                     threshold_for_survive, threshold_for_reproduce, selfish_and_cooperative_cells, generator)
        list_medium.append(np.copy(culture_medium))
        list_qs.append(np.copy(current_quorum_signals))
        list_savings.append(np.copy(savings))
        list_selfish_and_cooperative.append(np.copy(selfish_and_cooperative_cells))
    return list_medium, list_qs, list_savings, list_selfish_and_cooperative

