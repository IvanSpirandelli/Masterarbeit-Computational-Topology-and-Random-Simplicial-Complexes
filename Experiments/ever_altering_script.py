import GudhiExtension.filtration_manipulation as fm
import GudhiExtension.column_algo.column_algo_outs as cao
import GudhiExtension.column_algo.column_algorithm as ca
from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
import Examples.n_gon_with_center_and_different_pairings as ngon
from Examples.two_layered_corridor_example import get_two_layered_corridor_example

from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

from MorseAndFiltrations.gradient_field import gradient_field
from MorseAndFiltrations.toposort import toposort_flatten
from MorseAndFiltrations.generate_perfect_filtration import perfect_filtration_from_triangles
import matplotlib.pyplot as plt

def get_perfect_v_path_example():
    simplices = [[0],[1],[2],[3],[4],[5],[6],[7],[8],
                 [0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],
                 [1,8],[0,8],[0,7],[0,6],[0,5],[0,4],[0,3],[0,2],
                 [0,1,8],[0,7,8],[0,6,7],[0,5,6],[0,4,5],[0,3,4],[0,2,3],[0,1,2]
                 ]
    pairings = [[[0], [0, 1]], [[1], [1, 2]], [[2], [2, 3]], [[3], [3, 4]], [[4], [4, 5]], [[5], [5, 6]], [[6], [6, 7]], [[7], [7, 8]],
                [[1, 8], [0, 1, 8]], [[0, 8], [0, 7, 8]], [[0, 7], [0, 6, 7]], [[0, 6], [0, 5, 6]],
                [[0, 5], [0, 4, 5]], [[0, 4], [0, 3, 4]], [[0, 3], [0, 2, 3]], [[0, 2], [0, 1, 2]]]
    return simplices, pairings

def show_matrices_for_filtration(filtration):
    mat = ca.build_boundary_matrix_from_filtration(filtration)
    max_len = max([len(i) for i in filtration])

    xticklabels = [elem for elem in filtration if len(elem) > 1]
    yticklabels = [elem for elem in filtration if len(elem) < max_len]
    yticklabels.reverse()
    cao.mat_visualization(mat, xticklabels, yticklabels)

    steps, red = ca.column_algorithm_with_reduced_return(mat)
    for it in ca.column_algorithm_iterator(mat):
        steps, red = it
        cao.mat_visualization(red, xticklabels, yticklabels)
    print("Steps: ", steps, sum(steps))
    return sum(steps)

def compute_and_plot():
    x = []
    y = []
    for i in range(5,60):
        print(i,"/20")

        filtration = ngon.get_n_gon_with_center(i)
        pairings = ngon.get_expensive_pairings_same_directions(i)

        filtration = DMF_to_filtration(filtration,pairings)
        print(filtration)
        #print(pairings)

        x.append(len(filtration))
        steps = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration, False))
        y.append(steps)

    plt.scatter(x,y)
    plt.savefig("n_gon_plot_many_additions" + ".png", dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)
    plt.show()


#filtration = ngon.get_n_gon_with_center(5)
#pairings1 = ngon.get_expensive_pairings_same_directions(5)
#pairings2 = ngon.get_expensive_pairings_opposite_directions(5)

#filtration1 = DMF_to_filtration(filtration, pairings1)
#filtration2 = DMF_to_filtration(filtration, pairings2)

#mat1 = ca.build_boundary_matrix_from_filtration(filtration1)
#max_len1 = max([len(i) for i in filtration1])

#xticklabels1 = [elem for elem in filtration1 if len(elem) > 1]
#yticklabels1 = [elem for elem in filtration1 if len(elem) < max_len1]
#yticklabels1.reverse()
#cao.mat_visualization(mat1, xticklabels1, yticklabels1)

#mat2 = ca.build_boundary_matrix_from_filtration(filtration2)
#max_len2 = max([len(i) for i in filtration2])

#xticklabels2 = [elem for elem in filtration2 if len(elem) > 1]
#yticklabels2 = [elem for elem in filtration2 if len(elem) < max_len2]
#yticklabels2.reverse()
#cao.mat_visualization(mat2, xticklabels2, yticklabels2)

compute_and_plot()
quit()