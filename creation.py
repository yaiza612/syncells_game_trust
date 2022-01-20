import numpy as np


def create_savings(size):
    """
    :param size: determine the size of the matrix for savings.
    :return: return initial matrix with the savings of the cell (at the beginning is 0).
    """
    return np.zeros((size, size))


def create_medium(size, initial_density):
    """
    :param size: size of the grid
    :param initial_density: the initial density of cells
    :return: the grid populated by the cell (biologist term)
    """
    a = np.random.randint(low=0, high=5, size=(size, size))
    initial_medium = np.zeros((5, size, size))  # medium is the grid with our cells
    for _ in range(5):
        density_matrix = np.random.binomial(n=1, p=initial_density * 5, size=(size, size))
        initial_medium[_] = (a == _).astype(int) * density_matrix
    empty_cells = np.sum(initial_medium, axis=0)  # additional layer with the position taken 1 or free 0
    culture_medium = np.vstack((initial_medium, np.expand_dims(empty_cells, axis=0)))
    return culture_medium   # now is populated of cells and have an additional layer of positions taken and free


def create_selfish_and_cooperative(culture_medium, p_cooperative):
    """
    :param culture_medium: our grid with our 5 different types of cells
    :param p_cooperative: percentage of cell that are cooperative, rest will be selfish
    :return: matrix with the cooperative and selfish cells
    """
    # if the cell is cooperative the value is 1 and if the cell is selfish the value is 0
    list_cells = []
    for cell in range(0, 5):
        selfish_and_cooperative = np.logical_and(culture_medium[cell],
                                                 np.random.binomial(n=1, p=p_cooperative,
                                                                    size=culture_medium[cell].shape)).astype(int)
        list_cells.append(selfish_and_cooperative)
    selfish_and_cooperative = np.stack(list_cells)  # matrix defining which cells are selfish or cooperative
    return selfish_and_cooperative


def quorum_signals(quorum_signals_in_medium, selfish_and_cooperative, production, savings):
    """
    :param quorum_signals_in_medium: grid with the quorum signals of the medium
    :param selfish_and_cooperative: grid with the cells that are selfish and cooperative
    :param production: amount of quorum signals produced
    :param savings: amount of quorum signals saved
    :return: updated amount of quorum signal produced and updated savings
    """
    quorum_signals_in_medium += production * selfish_and_cooperative
    savings += 0.2 + (1 - np.sum(selfish_and_cooperative, axis=0)) * 0.8
    return quorum_signals_in_medium, savings
