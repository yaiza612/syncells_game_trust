import argparse
from datetime import datetime
from gym.utils import seeding
import numpy as np
from creation import create_medium, create_savings, create_selfish_and_cooperative
from simulation import run_simulation
from visualization import visualize


def main(number_of_cells, cooperativeness, production, step, size, initial_density, cooperation, threshold_survival,
         threshold_reproduction, initial_QS, diffusion_factor, determinism_cell_num, determinism_coop, num_iters, path_images_simulation, path_additional_figures,
         name_video, timestamp, prod_figs):
    if type(cooperation) is float:
        cooperation = [cooperation] * number_of_cells
    cooperation = [0.9, 0.75, 0.5, 0.25, 0.1]
    all_mediums = []
    all_q_signals = []
    all_savings = []
    all_selfish_and_cooperatives = []
    for iteration in range(num_iters):
        print(iteration)
        generator, seed = seeding.np_random(iteration)
        medium = create_medium(number_of_cells, size, initial_density, determinism_cell_num, generator)
        selfish_and_cooperative = create_selfish_and_cooperative(number_of_cells, medium, cooperation, determinism_coop, generator)
        quorum_signals_initial = np.ones((number_of_cells, size, size)) * initial_QS
        initial_savings = create_savings(size)
        q_signal = quorum_signals_initial
        mediums, q_signals, savings, selfish_and_cooperatives = \
            run_simulation(number_of_cells, cooperativeness, medium, initial_savings, q_signal, selfish_and_cooperative,
                           production, diffusion_factor, threshold_survival, threshold_reproduction, step, generator)
        all_mediums.append(mediums)
        all_q_signals.append(q_signals)
        all_savings.append(savings)
        all_selfish_and_cooperatives.append(selfish_and_cooperatives)
    print("simulation done")
    visualize(number_of_cells, all_mediums, all_q_signals, all_savings, all_selfish_and_cooperatives,
              path_images_simulation, path_additional_figures, name_video, timestamp, prod_figs)
    param_strings = ["number of cells", "cooperativeness", "production", "step", "size", "initial_density",
                     "cooperation", "threshold_survival",
                     "threshold_reproduction", "initial_QS", "diffusion_factor", "path_images_simulation",
                     "path_additional_figures", "name_video", "timestamp"]
    params = [number_of_cells, cooperativeness, production, step, size, initial_density, cooperation,
              threshold_survival, threshold_reproduction,
              initial_QS, diffusion_factor, path_images_simulation, path_additional_figures, name_video, timestamp]
    with open(timestamp + "/log.txt", "w") as f:
        for string, param in zip(param_strings, params):
            f.write(string + ": " + str(param) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Variables to specify simulation')
    parser.add_argument('-num', '--number_of_cells', default=5, help='Number of different populations of cells',
                        type=int, choices=range(2, 27))
    parser.add_argument('-co', '--cooperativeness', default=0.8, help='Amount of QS kept', type=float)
    parser.add_argument('-prod', '--production', default=0.4, help='amount of quorum signal that the cell produces',
                        type=float)
    parser.add_argument('-s', '--step', default=30, help='steps of simulation', type=int)
    parser.add_argument('-n', '--size', default=50, help='size for the grid (square)', type=int)
    parser.add_argument('-d', '--initial_density', default=0.05, help='initial density of cells', type=float)
    parser.add_argument('-c', '--cooperation', default=0.6, help='initial percentage of cooperative cells', type=float)
    parser.add_argument('-ts', '--threshold_survival', default=0.4, help='amount of quorum signal for surviving',
                        type=float)
    parser.add_argument('-tr', '--threshold_reproduction', default=0.5, help='amount of quorum signal for reproducing')
    parser.add_argument('-i', '--initial_QS', default=0.8, help='initial amount of quorum signal', type=int)
    parser.add_argument('-f', '--diffusion_factor', default=0.1,
                        help='amount of quorum signal that diffuse in the medium',
                        type=float)
    parser.add_argument('-pis', '--path_images_simulation', help='Path for saving the images required for the video',
                        default="medium", type=str)
    parser.add_argument('-pa', '--path_additional_figures', help='Path for saving the additional figures',
                        default="additional", type=str)
    parser.add_argument('-v', '--name_video', help='Name for save the video generated', default="video", type=str)
    parser.add_argument('-it', '--num_iters', help='Number of iterations to run the simulation', default=10, type=int)
    parser.add_argument('-nf', '--number_figs', help='Choose how many figures generate. \n '
                                                  'If you choose to produce a figure for each seed, this can take quite a while', default=1, type=int)
    parser.add_argument('-dtcn', '--determinism_cell_numbers', help='Force an equal amount of cells of each type at the beginning',
                        action='store_false')
    parser.add_argument('-dtcoop', '--determinism_cooperativeness',
                        help='Force an exact percentage of cells to be cooperative',
                        action='store_false')

    args = parser.parse_args()
    assert (0 <= args.initial_density * args.number_of_cells <= 1), "The initial density should be a number between 0" \
                                                                    " and 1 divided by the number of cell types "
    now = datetime.now()  # current date and time
    time_as_string = now.strftime("%m_%d_%Y__%H_%M_%S")
    main(number_of_cells=args.number_of_cells, cooperativeness=args.cooperativeness,
         production=args.production, step=args.step, size=args.size,
         initial_density=args.initial_density, cooperation=args.cooperation, threshold_survival=args.threshold_survival,
         threshold_reproduction=args.threshold_reproduction, initial_QS=args.initial_QS,
         diffusion_factor=args.diffusion_factor, determinism_cell_num=args.determinism_cell_numbers, determinism_coop=args.determinism_cooperativeness, num_iters=args.num_iters,
         path_images_simulation=args.path_images_simulation, path_additional_figures=args.path_additional_figures,
         name_video=args.name_video, timestamp=time_as_string, prod_figs=args.number_figs)
