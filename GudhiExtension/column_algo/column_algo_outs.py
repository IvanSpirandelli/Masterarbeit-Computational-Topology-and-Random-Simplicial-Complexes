import GudhiExtension.column_algo.column_algorithm as ca
import matplotlib.pyplot as plt


def computation_with_console_outs(filtration):
    mat = ca.build_boundary_matrix_from_filtration(filtration)
    print("Cropped boundary Matrix: ")
    print(mat)
    print("______________________________________________________________________")
    steps, red = ca.column_algorithm_with_reduced_return(mat)
    print("Reduced Matrix: ")
    print(red)
    print("______________________________________________________________________")
    print("Steps: ", steps)


def mat_visualization(mat,xticklabels = None, yticklabels = None, xrange = None, yrange = None):
    if(xrange == None):
        xrange = (0,len(mat[0]))
        print(xrange)
    if(yrange == None):
        yrange = (0,len(mat))
        print(yrange)

    fig, axs = plt.subplots(1)

    axs.matshow(mat[yrange[0]:yrange[-1], xrange[0]:xrange[-1]])
    #axs.set_xlim(-3, 365)
    #axs.set_xlim(-3, 365)
    if(xticklabels != None):
        axs.set_xticklabels(xticklabels[xrange[0]:xrange[-1]+1])
        for tick in axs.get_xticklabels():
            tick.set_rotation(45)

    if(yticklabels != None):
        axs.set_yticklabels(yticklabels[yrange[0]:yrange[-1]+1])

    plt.show()
