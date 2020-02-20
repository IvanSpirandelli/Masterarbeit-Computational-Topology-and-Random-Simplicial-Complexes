from numpy.ma import arange

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

    axs.matshow(mat[yrange[0]:yrange[-1],xrange[0]:xrange[-1]], origin = "upper",
                extent=(-0.5,xrange[-1]-0.5, -0.5,yrange[-1]-0.5))

    #axs.set_ylim(-0.5, -yrange[-1]-1)
    #axs.set_xlim(-0.5, xrange[-1]-0.5)

    if(xticklabels != None):
        plt.xticks(arange(len(xticklabels)), xticklabels, fontsize = 5)
        #axs.set_xticklabels(xticklabels[xrange[0]:xrange[-1]+1])
        for tick in axs.get_xticklabels():
            tick.set_rotation(90)

    if(yticklabels != None):
        plt.yticks(arange(len(yticklabels)), yticklabels, fontsize=5)

    plt.savefig(name + str(index) + ".png", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)

    plt.show()