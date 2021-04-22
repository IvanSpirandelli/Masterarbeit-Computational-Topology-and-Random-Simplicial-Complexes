import tikzplotlib

import Algorithms.filtration_manipulation as fm
import Algorithms.column_algo.column_algo_outs as cao
import Algorithms.column_algo.column_algorithm as ca
import Algorithms.point_cloud_generator as pcg
import Algorithms.alphacomplexwrapper as acw
import Algorithms.random_discrete_morse as rdm

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF


import Examples.n_gon_with_center_and_different_pairings as ngon
import Examples.davides_eight_point_delaunay as dav
import Examples.overlapping_wedge as overwedge
import Examples.simple_examples as se
import Examples.morozov_example as me
import Examples.rand_k_n_p as rnp
import Examples.wireframe_pyramid as wp
import Examples.dunce_hat as dh
import Examples.critically_connected_tube as cct
import Examples.worst_case_examples as wc


import scipy.stats as scs
import matplotlib.pyplot as plt
import numpy as np
import timeit

def show_matrices_for_filtration(filtration):
    mat = ca.build_boundary_matrix_from_filtration(filtration, False, False)
    max_len = max([len(i) for i in filtration])

    xticklabels = [elem for elem in filtration] # if len(elem) > 1
    yticklabels = [elem for elem in filtration] # if len(elem) < max_len
    cao.mat_visualization(mat, xticklabels, yticklabels)

    steps,_, red = ca.column_algorithm(mat)
    for i,it in enumerate(ca.column_algorithm_iterator(mat)):
        steps,_, red = it
        cao.mat_visualization(red, xticklabels, yticklabels, name="tetrahedron_with_fins", index=i+1)
    print("Steps: ", steps, sum(steps))
    return sum(steps)

def show_matrices_for_filtration_with_ranges(filtration, xrange, yrange):
    mat = ca.build_boundary_matrix_from_filtration(filtration, False, False)
    max_len = max([len(i) for i in filtration])

    xticklabels = [elem for id,elem in enumerate(filtration) if(id in range(xrange[0], xrange[1]))] # if len(elem) > 1
    yticklabels = [elem for id,elem in enumerate(filtration) if(id in range(yrange[0], yrange[1]))] # if len(elem) < max_len
    # yticklabels.reverse()
    cao.mat_visualization(mat, xticklabels, yticklabels, xrange, yrange, name="pizza_with_fins", index=0)

    steps,_, red = ca.column_algorithm(mat)
    for i,it in enumerate(ca.column_algorithm_iterator(mat)):
        steps,_, red = it
        cao.mat_visualization(red, xticklabels, yticklabels, xrange, yrange, name="pizza_with_fins", index=i+1)
    print("Steps: ", steps, sum(steps))
    return sum(steps)

x = []
y = []
z = []
for n in range(3,4):
    if n % 10 == 0: print(n)
    filtration = wc.get_n_gon_with_center_and_fins_filtration(n)
    filtration_two = wc.get_3d_extension_of_ngon(n)
    steps, _, _ = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration))
    steps_two, _, _ = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration_two))
    x.append(n)
    y.append(sum(steps))
    z.append(sum(steps_two))

plt.scatter(x,y)
plt.scatter(x,z)
plt.show()