import numpy as np
import itertools
import random

# count all the combinations
combinations = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # coordinates of the neighbours


def counting(coords, matrix):
    """
    :param: coords: coordinates x and y of the 8 neighbours surrounding.
    :param: matrix: grid.
    :return: all the neighbours.
    """
    return np.roll(np.roll(matrix, coords[0], axis=0), coords[1], axis=1)  # count in both axis


def diffusion(medium_populated_qs, diffusion_factor):
    """
    :param: medium_populated_qs: grid with the quorum signals.
    :param: diffusion_factor: amount of signal diffuse ( it is obviously a simplification).
    :return: the new grid with all the quorum signals diffused.
    """

    def spread(qs):
        """
        :param: qs: values of the amount of quorum signal in the grid.
        :return: the new values of amount of quorum signal.
        """
        return diffusion_factor * qs

    current_concentrations = list(map(counting, combinations, itertools.repeat(medium_populated_qs,
                                                                               len(combinations))))
    # list with the concentrations of quorum signal
    new_concentrations = np.array(list(map(spread, current_concentrations))).sum(axis=0) + \
                         (1 - diffusion_factor * len(combinations)) * medium_populated_qs
    return new_concentrations


def check_empty_neighbours(number_of_cells, medium):
    """
    :param number_of_cells: number of different type of cells
    :param medium: grid where all the different cells live
    :return: cells of the grid that are empty and number of neighbours of every cell (biologist term)
    """
    current_empty_cells = np.asarray(list(map(counting, combinations, itertools.repeat(medium[number_of_cells],
                                                                                       len(combinations)))))
    # list with the amount of neighbours
    number_of_neighbours = np.sum(current_empty_cells, axis=0)
    return current_empty_cells, number_of_neighbours


def survive_reproduce_or_die(number_of_cells, medium, savings, current_qs, threshold_surveillance,
                             threshold_reproduction, selfish_and_cooperative):
    """
    :param number_of_cells: number of different type of cells
    :param medium: grid where all the different cells live
    :param savings: every different type of cell produce a quorum signal that is partly saved
     if the cell is cooperative and completely saved if the cell is selfish.
    :param current_qs: actual concentration of quorum signal
    :param threshold_surveillance: amount of quorum signals the cells need to be able to produce their proteins needed
    for surveillance
    :param threshold_reproduction: amount of quorum signals the cells need to be able to produce their proteins needed
    for reproduction
    :param selfish_and_cooperative: matrix with the cells that are selfish or cooperative
    :return: the updated grid for cells (medium) and quorum signals
    """
    n = medium.shape[1]
    assert threshold_surveillance < threshold_reproduction  # threshold surveillance should be always smaller than
    # threshold of reproduction
    and_gate_with_savings = np.min(current_qs + medium[:number_of_cells] * savings, axis=0)
    # and gate, all the cells need
    # their own quorum signal and the quorum signals of the others to produce their proteins and survive
    survivors = (and_gate_with_savings >= threshold_surveillance).astype(int)  # 0 if dead, else 1 ; shape: n,n
    for layer in range(number_of_cells):
        medium[layer] = np.min((medium[layer], survivors), axis=0)
        current_qs[layer] += savings * (
                (1 - survivors) * medium[layer])  # the savings get release to the medium if the cell dies, since
        # the membrane suffer a lysis.
        for other_cell_type in range(number_of_cells):
            if other_cell_type != layer:
                current_qs[layer] -= survivors * threshold_surveillance * medium[other_cell_type]  # the cells consume
                # the quorum signals
    savings -= survivors * threshold_surveillance  # the cells consume the savings of their own quorum signal
    possible_reproducers = np.min((medium[number_of_cells],
                                   (and_gate_with_savings >= threshold_reproduction).astype(int)),
                                  axis=0)  # 1 if potential to reproduce, else 0
    empty_cell_grid, number_n = check_empty_neighbours(number_of_cells, medium)
    random_order_indices = list(itertools.product(range(medium.shape[2]), repeat=2))
    random.shuffle(random_order_indices)
    for idx in random_order_indices:
        if possible_reproducers[idx[0], idx[1]] == 1:  # first check if they are able to reproduce
            if number_n[idx[0], idx[1]] < 8:  # then check if there is space to reproduce and where
                direction_to_go = np.where(empty_cell_grid[:, idx[0], idx[1]] == 0)[0]
                if len(direction_to_go) == 1:
                    random_index_direction = direction_to_go[0]
                else:
                    random_index_direction = random.sample(list(direction_to_go), 1)[0]
                random_direction = combinations[random_index_direction]
                repro_layer = np.argmax(medium[:number_of_cells, idx[0], idx[1]])
                if medium[repro_layer, idx[0], idx[1]] == 1:
                    medium[repro_layer, (idx[0] - random_direction[0]) % n, (idx[1] - random_direction[1]) % n] = 1
                    medium[number_of_cells, (idx[0] - random_direction[0]) % n, (idx[1] - random_direction[1]) % n] = 1
                    selfish_and_cooperative[repro_layer, (idx[0] - random_direction[0]) % n,
                                            (idx[1] - random_direction[1]) % n] = \
                        selfish_and_cooperative[repro_layer, idx[0], idx[1]]  # child is same as parent, inherit
                    # the condition of be a cooperative cell or be a selfish cell
                    empty_cell_grid, number_n = check_empty_neighbours(number_of_cells, medium)
                    for layer in range(number_of_cells):
                        for other_cell_type in range(number_of_cells):
                            if other_cell_type != layer:
                                current_qs[layer, idx[0], idx[1]] -= \
                                    (threshold_reproduction - threshold_surveillance) * \
                                    medium[other_cell_type, idx[0], idx[1]]  # consume a bit more quorum signal
                                # if reproduce
                    savings[idx[0], idx[1]] -= (threshold_reproduction - threshold_surveillance)
                    # consume a bit more of savings if reproduce
    return medium, current_qs
