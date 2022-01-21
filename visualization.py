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
    cell = []
    quorum_signal = []
    saved = []
    selfish = []
    for _ in range(number_of_cells):
        number_cells = np.sum(culture_medium[_])
        number_qs = np.sum(current_qs[_])
        number_savings = np.sum(current_savings[_])
        number_selfish = np.sum((1 - selfish_and_cooperative[_]) * culture_medium[_])
        cell.append(number_cells)
        quorum_signal.append(number_qs)
        saved.append(number_savings)
        selfish.append(number_selfish)
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


def make_fig(number_of_cells, mediums, q_signals, savings, selfish_and_cooperatives, img_path, img_path_additional,
             video_name, time_as_string):
    size = mediums[0].shape[1]
    cell_amounts = defaultdict(list)
    q_signal_amounts = defaultdict(list)
    saving_amounts = defaultdict(list)
    percent_selfish_cells = defaultdict(list)
    names = ["A", "B", "C", "D", "E"]
    os.mkdir(time_as_string)
    os.mkdir(time_as_string + "/" + img_path)
    os.mkdir(time_as_string + "/" + img_path_additional)
    time_steps = range(len(mediums))
    num_digits_needed = int(np.ceil(np.log10(len(mediums))))
    # why not map the function?
    for _, (medium, q_signal, saving, selfish_per_time) in \
            enumerate(zip(mediums, q_signals, savings, selfish_and_cooperatives)):
        fig = plot_medium(number_of_cells, medium)
        plt.savefig(time_as_string + "/" + img_path + "/medium_" + "{:0{width}}".format(_, width=num_digits_needed))
        plt.close(fig)
        cells, qs, sv, selfish_cells = auxiliary_data(number_of_cells, medium, q_signal, saving,
                                                      selfish_per_time)
        for idx, (cell, q, s, selfish) in enumerate(zip(cells, qs, sv, selfish_cells)):
            cell_amounts[idx].append(cell / size ** 2)
            q_signal_amounts[idx].append(q / size ** 2)
            saving_amounts[idx].append(s / size ** 2)
            if cell == 0:
                percent_selfish_cells[idx].append(0)
            else:
                percent_selfish_cells[idx].append(100 * (selfish / cell))
    fig_cells, ax_cells = plt.subplots(figsize=(5, 2.7), layout='constrained')
    fig_q_signals, ax_q_signals = plt.subplots(figsize=(5, 2.7), layout='constrained')
    fig_savings, ax_savings = plt.subplots(figsize=(5, 2.7), layout='constrained')
    fig_selfish, ax_selfish = plt.subplots(figsize=(5, 2.7), layout='constrained')
    for idx, name in enumerate(names):
        ax_cells.plot(time_steps, cell_amounts[idx], label='Cell ' + name)
        ax_q_signals.plot(time_steps, q_signal_amounts[idx], label='Quorum signal ' + name)
        ax_savings.plot(time_steps, saving_amounts[idx], label='Savings ' + name)
        ax_selfish.plot(time_steps, percent_selfish_cells[idx], label='Percent selfish ' + name)
    ax_cells.set_xlabel('Time steps')  # Add an x-label to the axes.
    ax_cells.set_ylabel('Population of cells')  # Add a y-label to the axes.
    ax_cells.set_title("Trust game with cells")  # Add a title to the axes.
    ax_cells.legend()  # Add a legend.
    fig_cells.savefig(time_as_string + "/" + img_path_additional + '/cells')

    ax_q_signals.set_xlabel('Time steps')  # Add an x-label to the axes.
    ax_q_signals.set_ylabel('Quorum signals in the medium')  # Add a y-label to the axes.
    ax_q_signals.set_title('Trust game with cells')  # Add a title to the axes.
    ax_q_signals.legend()  # Add a legend.
    fig_q_signals.savefig(time_as_string + "/" + img_path_additional + '/quorum_signals')

    ax_savings.set_xlabel('Time steps')  # Add an x-label to the axes.
    ax_savings.set_ylabel('Savings of the cells')  # Add a y-label to the axes.
    ax_savings.set_title("Trust game with cells")  # Add a title to the axes.
    ax_savings.legend()  # Add a legend.
    fig_savings.savefig(time_as_string + "/" + img_path_additional + '/savings')

    ax_selfish.set_xlabel('Time steps')  # Add an x-label to the axes.
    ax_selfish.set_ylabel('Percent of selfish cells')  # Add a y-label to the axes.
    ax_selfish.set_title("Trust game with cells")  # Add a title to the axes.
    ax_selfish.legend()  # Add a legend.
    fig_selfish.savefig(time_as_string + "/" + img_path_additional + '/selfish')

    create_video(time_as_string + "/" + img_path, time_as_string, video_name)
