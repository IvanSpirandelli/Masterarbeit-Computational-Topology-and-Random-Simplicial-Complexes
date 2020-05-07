import GudhiExtension.filtration_manipulation as fm
import GudhiExtension.column_algo.column_algo_outs as cao
import GudhiExtension.column_algo.column_algorithm as ca
from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
import Examples.n_gon_with_center_and_different_pairings as ngon
import Examples.davides_eight_point_delaunay as dav
import Examples.overlapping_wedge as overwedge
import Examples.simple_examples as se
import Examples.mozorov_example as me

import GudhiExtension.point_cloud_generator as pcg
import GudhiExtension.alpha_complex_wrapper as acw

from Examples.two_layered_corridor_example import get_two_layered_corridor_example

from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF, filtration_to_DMF_with_all_emergent

from MorseAndFiltrations.gradient_field import gradient_field
from MorseAndFiltrations.toposort import toposort_flatten
from MorseAndFiltrations.generate_perfect_filtration import perfect_filtration_from_triangles
import matplotlib.pyplot as plt
import numpy as np
import timeit

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
    mat = ca.build_boundary_matrix_from_filtration(filtration, False, False)
    max_len = max([len(i) for i in filtration])

    xticklabels = [elem for elem in filtration] # if len(elem) > 1
    yticklabels = [elem for elem in filtration] # if len(elem) < max_len
    yticklabels.reverse()
    cao.mat_visualization(mat, xticklabels, yticklabels)

    steps,_, red = ca.column_algorithm(mat)
    for i,it in enumerate(ca.column_algorithm_iterator(mat)):
        steps,_, red = it
        cao.mat_visualization(red, xticklabels, yticklabels, name="1fishNfins", index=i)
    print("Steps: ", steps, sum(steps))
    return sum(steps)

def compute_plot_and_fit():
    x = []
    y = []
    oddx = []
    oddy = []

    v= []
    w= []
    oddv= []
    oddw= []
    for i in range(5,100):
        print(i,"/60")

        # simplices = ngon.get_n_gon_with_center_and_fins(i)
        # pairings = ngon.fin_pairings_many_critical_cells_v2(i)
        # filtration = DMF_to_filtration(simplices, pairings)

        filtration = me.build_morozov_example(i)

        steps,lows,red = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration, False, False))
        print(steps)
        if(i%2 == 0):
            x.append(len(filtration))
            y.append(steps[0])
        else:
            oddx.append(len(filtration))
            oddy.append(steps[0])

    p = np.polyfit(x, y, 3)
    f = np.poly1d(p)  # So we can call f(x)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.plot(x, y, 'bo', label="Data")
    ax.plot(x, f(x),'r', label="NGON")
    coeff1, res1, _, _, _ = np.polyfit(x, y, 1, full=True)
    coeff2, res2, _, _, _ = np.polyfit(x, y, 2, full=True)
    coeff3, res3, _, _, _ = np.polyfit(x, y, 3, full=True)

    print("ODD 1DIM ERROR: ", np.sum((np.polyval(coeff1, oddx) - oddy) **2))
    print("ODD 2DIM ERROR: ", np.sum((np.polyval(coeff2, oddx) - oddy) **2))
    print("ODD 3DIM ERROR: ", np.sum((np.polyval(coeff3, oddx) - oddy) **2))
    print(".............................")
    print("1DIM ERROR: ", np.sum((np.polyval(coeff1, x) - y) ** 2))
    print("2DIM ERROR: ", np.sum((np.polyval(coeff2, x) - y) ** 2))
    print("3DIM ERROR: ", np.sum((np.polyval(coeff3, x) - y) ** 2))
    print(".............................")
    print("1D-FIT NGON: ", res1)
    print("2D-FIT NGON: ", res2)
    print("3D-FIT NGON: ", res3)

    plt.show(legend = True)

def stabelize(filtration, pairings):
    stableization_steps = 0
    if(pairings == []):
        pairings = filtration_to_DMF_with_all_emergent(filtration, False)
        print(pairings)

    n_filtration = DMF_to_filtration(filtration, pairings)


    while n_filtration != filtration:
        print(n_filtration)
        pairings = filtration_to_DMF(n_filtration, True)
        filtration = n_filtration
        print(pairings)
        n_filtration = DMF_to_filtration(filtration, pairings)
        stableization_steps += 1

    return stableization_steps

def stabelize_and_check_for_same_pairings(filtration, pairings):
    mat = ca.build_boundary_matrix_from_filtration(filtration)
    _, initial_lows = ca.column_algorithm(mat,False)
    initial_pairs  = cao.get_pairings(filtration,initial_lows)
    cao.print_pairings_to_console(initial_pairs)

    print(filtration)


    stableization_steps = 0
    if(pairings == []):
        pairings = filtration_to_DMF(filtration, True)
        print(pairings)

    print("______________________")
    n_filtration = DMF_to_filtration(filtration, pairings)


    while n_filtration != filtration:
        print(n_filtration)
        pairings = filtration_to_DMF(n_filtration, True)
        filtration = n_filtration
        mat = ca.build_boundary_matrix_from_filtration(filtration)
        _, lows = ca.column_algorithm(mat, False)
        pairs = cao.get_pairings(filtration,lows)

        print("STARTING TO LIST DIFFERING PAIRINGS:")
        for pair in pairs:
            if pair not in initial_pairs:
                print(pair, "IS NOT IN INITIAL PAIRS!")
        print("___________DONE___________")

        n_filtration = DMF_to_filtration(filtration, pairings)
        stableization_steps += 1

    return stableization_steps

def comparing_running_times(n,dim):
    points = pcg.generate_n_points(n, dim)
    alpha = acw.alpha_complex_wrapper(points)
    filtration = [t[0] for t in alpha.filtration]
    # filtration = se.get_split_square()
    print(filtration)

    start = timeit.default_timer()
    mat = ca.build_boundary_matrix_from_filtration(filtration, False, False)
    stop = timeit.default_timer()
    mat_gen = stop - start
    print("MAT GEN WITHOUT DELETING: ", mat_gen)

    print("------------------------")
    start = timeit.default_timer()
    steps, red1 = ca.column_algorithm(mat)
    stop = timeit.default_timer()
    std_time = stop - start
    print("STANDARD STEPS: ", steps)
    print("STANDARD TIME: ", std_time)
    print("STANDARD SUMMED", std_time + mat_gen)

    print("------------------------")
    start = timeit.default_timer()
    steps, red2 = ca.column_algorithm_with_a_twist(mat)
    stop = timeit.default_timer()
    twist_time = stop - start
    print("TWIST STEPS: ", steps)
    print("TWIST TIME: ", twist_time)
    print("TWIST SUMMED", twist_time + mat_gen)

    print("###########################")
    start = timeit.default_timer()
    mat = ca.build_boundary_matrix_from_filtration(filtration, True, False)
    stop = timeit.default_timer()
    mat_gen_cleared = stop - start
    print("MAT GEN WITH DELETING: ", mat_gen_cleared)

    print("------------------------")
    start = timeit.default_timer()
    steps, red3 = ca.column_algorithm(mat)
    stop = timeit.default_timer()
    std_time = stop - start
    print("STANDARD STEPS: ", steps)
    print("STANDARD TIME: ", std_time)
    print("STANDARD CLEARED SUMMED", std_time + mat_gen_cleared)

    print("------------------------")
    start = timeit.default_timer()
    steps, red4 = ca.column_algorithm_with_a_twist(mat)
    stop = timeit.default_timer()
    twist_time = stop - start
    print("TWIST STEPS: ", steps)
    print("TWIST TIME: ", twist_time)
    print("TWIST CLEARED SUMMED", twist_time + mat_gen_cleared)

    print("ALL MATRICES ARE REDUCED TO SAME?", (red1 == red2).all() and (red1 == red3).all() and (red1 == red4).all())


# filtration = ngon.get_n_gon_with_center_and_fins(6)
# pairings = ngon.fin_pairings_many_critical_cells(6)
# filtration = DMF_to_filtration(filtration, pairings)
#
# steps, red, low = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration, False, False))
# print(steps)
#
# show_matrices_for_filtration(filtration)


compute_plot_and_fit()