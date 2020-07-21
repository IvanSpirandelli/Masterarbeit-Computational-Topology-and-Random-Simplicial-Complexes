import numpy as np

import GudhiExtension.column_algo.column_algorithm as ca
import matplotlib.pyplot as plt


def computation_with_console_outs(filtration):
    dim = max([len(i) for i in filtration])
    mat = ca.build_boundary_matrix_from_filtration(filtration)
    print("Cropped boundary Matrix: ")
    print(mat)
    print("______________________________________________________________________")
    steps, red = ca.column_algorithm_with_reduced_return(mat, dim)
    print("Reduced Matrix: ")
    print(red)
    print("______________________________________________________________________")
    print("Steps: ", steps)


def mat_visualization(mat,xticklabels = None, yticklabels = None, xrange = None, yrange = None, name = "tmp", index = 0):

    if(xrange == None):
        xrange = (0,len(mat[0]))
    if(yrange == None):
        yrange = (0,len(mat))

    fig, axs = plt.subplots(1)

    cropmat = mat[yrange[0]:yrange[-1],xrange[0]:xrange[-1]]
    axs.matshow(cropmat, origin = "upper", extent=(-0.5,xrange[-1]-xrange[0]-0.5, -0.5,yrange[-1]-yrange[0]-0.5))

    if(xticklabels != None):
        axs.set_xticks(np.arange(len(xticklabels)))

        for tick in axs.get_xticklabels():
            tick.set_fontsize(7)
            tick.set_rotation(90)
        axs.set_xticklabels(xticklabels)

    if(yticklabels != None):
        axs.set_yticks(np.arange(len(yticklabels)))

        for tick in axs.get_yticklabels():
            tick.set_fontsize(7)

        axs.set_yticklabels(yticklabels)

    plt.gcf().subplots_adjust(top=0.8)

    plt.savefig(name + str(index) + ".png", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)

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
