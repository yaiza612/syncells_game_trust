import matplotlib.colors
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
import matplotlib.patches as p
import cv2
import os


def plot_medium(number_of_cells, culture_medium):
    """
    Helper function to plot medium
    """
    fig, axis = plt.subplots()
    a = np.zeros_like(culture_medium[0])
    for _ in range(number_of_cells):
        a += (_ + 1) * culture_medium[_]
    if np.max(a) > number_of_cells:
        print("error")
    # define color map
    set_colors = ["white", "aquamarine", "lightcoral", "blueviolet", "gold", "deepskyblue"]
    matplotlib.colors.to_rgb("white")
    color_map = dict()
    for i, color in enumerate(set_colors):
        color_map[i] = np.asarray(matplotlib.colors.to_rgb(color))
    data_3d = np.zeros((culture_medium.shape[1], culture_medium.shape[1], 3))
    for layer in range(3):
        for x in range(culture_medium.shape[1]):
            for y in range(culture_medium.shape[2]):
                data_3d[x, y, layer] = color_map[a[x, y]][layer]
    # print(data_3d.shape)
    axis.imshow(data_3d)
    values = range(number_of_cells + 1)
    labels = {0: 'Empty'}
    for key in range(1, number_of_cells + 1):
        labels[key] = chr(64 + key)
    labels = {0: 'Empty', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    patches = [p.Patch(color=set_colors[i], label=labels[i]) for i in values]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    return fig


def auxiliary_data(number_of_cells, culture_medium, current_qs, current_savings, selfish_and_cooperative):
    """
    Helper function to plot other additional data
    """
    cell = [np.sum(culture_medium[_]) for _ in range(number_of_cells)]
    quorum_signal = [np.sum(current_qs[_]) for _ in range(number_of_cells)]
    saved = [np.sum(culture_medium[_] * current_savings) for _ in range(number_of_cells)]
    selfish = [np.sum((1 - selfish_and_cooperative[_]) * culture_medium[_]) for _ in range(number_of_cells)]
    return cell, quorum_signal, saved, selfish


def create_video(image_folder, video_path, video_name):
    """
    Helper function to create the video of the culture medium with the cells
    """
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(os.path.join(video_path, video_name) + ".avi", 0, 30, (width, height))

    for i, image in enumerate(images):
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def visualize(number_of_cells, all_mediums, all_q_signals, all_savings, all_selfish_and_cooperatives,
              img_path, img_path_additional, video_name, dir_name, prod_figs):
    os.mkdir(dir_name)
    for iter_idx, mediums, q_signals, savings, selfish_and_cooperatives in zip(range(prod_figs), all_mediums, all_q_signals, all_savings, all_selfish_and_cooperatives):
        iter_dir = f"{dir_name}/seed_{iter_idx}"
        make_figs_and_video(number_of_cells, mediums, q_signals, savings, selfish_and_cooperatives, img_path, img_path_additional,
             video_name, iter_dir)
    make_summary_fig(number_of_cells, all_mediums, all_q_signals, all_savings, all_selfish_and_cooperatives, dir_name)



def plot_trajectory(data_per_cell, cell_names, time_steps, legend_label, xlabel, ylabel, title, fig_path, multiple_seeds=False):
    fig, ax = plt.subplots(figsize=(12, 8), layout='constrained')
    for idx, name in enumerate(cell_names):
        if multiple_seeds:
            set_colors = ["aquamarine", "lightcoral", "blueviolet", "gold", "deepskyblue"]
            color_map = dict()
            for i, color in enumerate(set_colors):
                color_map[i] = np.asarray(matplotlib.colors.to_rgb(color))
            mean = np.asarray(data_per_cell[idx])[:, 0]
            std = np.asarray(data_per_cell[idx])[:, 1]
            ax.plot(time_steps, mean, label=legend_label + name, color=color_map[idx])
            ax.fill_between(time_steps, mean+0.2*std, mean-0.2*std, alpha=0.3, color=color_map[idx])
        else:
            try:
                idx_of_first_none = data_per_cell[idx].index(None)
                plot_time_steps = time_steps[0:idx_of_first_none]
                plot_data_per_cell = data_per_cell[idx][0:idx_of_first_none]
            except ValueError:
                plot_time_steps = time_steps
                plot_data_per_cell = data_per_cell[idx]
            ax.plot(plot_time_steps, plot_data_per_cell, label=legend_label + name)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.savefig(fig_path)

def make_summary_fig(number_of_cells, all_mediums, all_q_signals, all_savings, all_selfish_and_cooperatives, dir_name):
    num_seeds = len(all_mediums)
    size = all_mediums[0][0].shape[1]
    cell_amounts_t = defaultdict(list)
    q_signal_amounts_t = defaultdict(list)
    saving_amounts_t = defaultdict(list)
    percent_selfish_cells_t = defaultdict(list)
    names = ["A", "B", "C", "D", "E"]
    time_steps = range(len(all_mediums[0]))
    # shape of all_mediums, all_q_signals and all_selfish_and_cooperatives:
    # (num_seeds, num_timesteps+1, num_cells, x_dim of dish, y_dim of dish)
    # shape of all_savings: (num_seeds, num_timesteps + 1, x_dim of dish, y_dim of dish)
    # we want to change the shapes in the following way:
    # shape of all_mediums, all_q_signals and all_selfish_and_cooperatives:
    # (num_timesteps+1, num_seeds, num_cells, x_dim of dish, y_dim of dish)
    # shape of all_savings: (num_timesteps + 1, num_seeds, x_dim of dish, y_dim of dish)
    all_mediums = np.swapaxes(np.asarray(all_mediums), 0, 1)
    all_q_signals = np.swapaxes(np.asarray(all_q_signals), 0, 1)
    all_savings = np.swapaxes(np.asarray(all_savings), 0, 1)
    all_selfish_and_cooperatives = np.swapaxes(np.asarray(all_selfish_and_cooperatives), 0, 1)

    for _, (medium_t, q_signal_t, saving_t, selfish_per_time_t) in \
            enumerate(zip(all_mediums, all_q_signals, all_savings, all_selfish_and_cooperatives)):
        #  iterating over timesteps
        cell_amounts_s = defaultdict(list)
        q_signal_amounts_s = defaultdict(list)
        saving_amounts_s = defaultdict(list)
        percent_selfish_cells_s = defaultdict(list)
        for medium_s, q_signal_s, saving_s, selfish_per_time_s in zip(medium_t, q_signal_t, saving_t,
                                                                      selfish_per_time_t):
            cells, qs, sv, selfish_cells = auxiliary_data(number_of_cells, medium_s, q_signal_s, saving_s,
                                                          selfish_per_time_s)
            for idx, (cell, q, s, selfish) in enumerate(zip(cells, qs, sv, selfish_cells)):
                cell_amounts_s[idx].append((cell / size ** 2) / num_seeds)
                q_signal_amounts_s[idx].append((q / size ** 2) / num_seeds)
                saving_amounts_s[idx].append((s / size ** 2) / num_seeds)
                if cell == 0:
                    percent_selfish_cells_s[idx].append(None)
                else:
                    percent_selfish_cells_s[idx].append((100 * (selfish / cell)) / num_seeds)
        for idx in range(number_of_cells):
            for time_dict, seed_dict in zip([cell_amounts_t, q_signal_amounts_t, saving_amounts_t, percent_selfish_cells_t],
                                            [cell_amounts_s, q_signal_amounts_s, saving_amounts_s, percent_selfish_cells_s]):
                average = np.nanmean(np.array(seed_dict[idx], dtype=np.float64))
                std = np.nanstd(np.array(seed_dict[idx], dtype=np.float64))
                time_dict[idx].append([average, std])
    cells_data = [cell_amounts_t, q_signal_amounts_t, saving_amounts_t, percent_selfish_cells_t]
    legend_labels = ['Cell ', 'Quorum signal ', 'Savings ', 'Percent selfish ']
    xlabels = ['Time steps'] * 4
    ylabels = ['Population of cells', 'Quorum signals in the medium', 'Savings of the cells',
               'Percent of selfish cells']
    titles = ['Trust game with cells'] * 4
    fig_names = ['cells', 'quorum_signals', 'savings', 'selfish']
    for cell_data, legend_label, xlabel, ylabel, title, fig_name in \
            zip(cells_data, legend_labels, xlabels, ylabels, titles, fig_names):
        fig_path = dir_name + "/" + fig_name
        plot_trajectory(cell_data, names, time_steps, legend_label, xlabel, ylabel, title, fig_path, multiple_seeds=True)
def make_figs_and_video(number_of_cells, mediums, q_signals, savings, selfish_and_cooperatives, img_path, img_path_additional,
             video_name, dir_name, single_seed=True):
    size = mediums[0].shape[1]
    cell_amounts = defaultdict(list)
    q_signal_amounts = defaultdict(list)
    saving_amounts = defaultdict(list)
    percent_selfish_cells = defaultdict(list)
    names = ["A", "B", "C", "D", "E"]
    os.mkdir(dir_name)
    os.mkdir(dir_name + "/" + img_path)
    os.mkdir(dir_name + "/" + img_path_additional)
    time_steps = range(len(mediums))
    num_digits_needed = int(np.ceil(np.log10(len(mediums))))
    # why not map the function?
    for _, (medium, q_signal, saving, selfish_per_time) in \
            enumerate(zip(mediums, q_signals, savings, selfish_and_cooperatives)):
        fig = plot_medium(number_of_cells, medium)
        plt.savefig(dir_name + "/" + img_path + "/medium_" + "{:0{width}}".format(_, width=num_digits_needed))
        plt.close(fig)
        cells, qs, sv, selfish_cells = auxiliary_data(number_of_cells, medium, q_signal, saving,
                                                      selfish_per_time)
        for idx, (cell, q, s, selfish) in enumerate(zip(cells, qs, sv, selfish_cells)):
            cell_amounts[idx].append(cell / size ** 2)
            q_signal_amounts[idx].append(q / size ** 2)
            saving_amounts[idx].append(s / size ** 2)
            if cell == 0:
                percent_selfish_cells[idx].append(None)
            else:
                percent_selfish_cells[idx].append(100 * (selfish / cell))
    cells_data = [cell_amounts, q_signal_amounts, saving_amounts, percent_selfish_cells]
    legend_labels = ['Cell ', 'Quorum signal ', 'Savings ', 'Percent selfish ']
    xlabels = ['Time steps'] * 4
    ylabels = ['Population of cells', 'Quorum signals in the medium', 'Savings of the cells',
               'Percent of selfish cells']
    titles = ['Trust game with cells'] * 4
    fig_names = ['cells', 'quorum_signals', 'savings', 'selfish']
    for cell_data, legend_label, xlabel, ylabel, title, fig_name in \
            zip(cells_data, legend_labels, xlabels, ylabels, titles, fig_names):
        fig_path = dir_name + "/" + img_path_additional + "/" + fig_name
        plot_trajectory(cell_data, names, time_steps, legend_label, xlabel, ylabel, title, fig_path)
    create_video(dir_name + "/" + img_path, dir_name, video_name)
