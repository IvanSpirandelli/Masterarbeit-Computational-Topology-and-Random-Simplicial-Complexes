import GudhiExtension.filtration_manipulation as fm
import GudhiExtension.column_algo.column_algo_outs as cao
import GudhiExtension.column_algo.column_algorithm as ca
from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from Examples.n_gon_with_center_and_different_pairings import get_n_gon_with_center_and_pairings, get_cheap_pairings, get_expensive_pairings
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

x = []
y = []
for i in range(3,15):
    print(i,"/100")
    simplices = get_n_gon_with_center_and_pairings(i)
    pairings = get_expensive_pairings(i)

    filtration = DMF_to_filtration(simplices, pairings)
    print(len(filtration))
    x.append(len(filtration))
    steps = show_matrices_for_filtration(filtration)
    y.append(steps)

plt.scatter(x,y)
plt.savefig("n_gon_plot_many_additions" + ".png", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)
plt.show()



quit()