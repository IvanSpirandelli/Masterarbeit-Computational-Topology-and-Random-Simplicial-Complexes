import numpy as np
import tikzplotlib

import Algorithms.column_algo.column_algorithm as ca
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import ListedColormap
from matplotlib import cm
from collections import OrderedDict


def mat_visualization(mat,xticklabels = None, yticklabels = None, xrange = None, yrange = None, name = "tmp", index = 0):

    if(xrange == None):
        xrange = (0,len(mat[0]))
    if(yrange == None):
        yrange = (0,len(mat))


    cropmat = mat[yrange[0]:yrange[-1], xrange[0]:xrange[-1]]
    cmap = ListedColormap(['xkcd:lightblue','xkcd:maroon'])
    im = plt.matshow(cropmat, origin="upper",cmap = cmap)

    ax = plt.gca()

    # Major ticks
    ax.set_xticks(np.arange(0, len(xticklabels), 1))
    ax.set_yticks(np.arange(0, len(yticklabels), 1))

    # Labels for major ticks
    ax.set_xticklabels(xticklabels)
    ax.set_yticklabels(yticklabels)

    # Minor ticks
    ax.set_xticks(np.arange(-.5, len(xticklabels), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(yticklabels), 1), minor=True)

    fontsize = 12

    for tick in ax.get_xticklabels():
        tick.set_fontsize(fontsize)
        tick.set_rotation(90)

    for tick in ax.get_yticklabels():
        tick.set_fontsize(fontsize)
    plt.subplots_adjust(left=-0.25)

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    #tikzplotlib.save("reduction_step_" + str(index) + ".tex")

    plt.savefig(name + str(index) + ".png", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches="tight", pad_inches=0.1, metadata=None)

    plt.show()
    plt.close()


def extract_and_print_pairs(filtration, lowest_ones):
    print_pairings_to_console(get_pairings(filtration, lowest_ones))

def get_pairings(filtration, lowest_ones):
    pairs = []
    for i,elem in enumerate(lowest_ones):
        if (elem != -1):
            pairs.append([filtration[elem], filtration[i]])
    return pairs

def print_pairings_to_console(pairings):
    for pair in pairings:
        print(pair[0], "->", pair[1])
