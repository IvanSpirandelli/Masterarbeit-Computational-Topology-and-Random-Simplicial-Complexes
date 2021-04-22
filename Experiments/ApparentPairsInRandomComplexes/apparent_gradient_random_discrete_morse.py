from copy import copy

import Algorithms.column_algo.column_algorithm as ca
import Algorithms.random_discrete_morse as rdm
import Examples.rand_k_n_p as rnp

from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

import matplotlib.pyplot as plt
import tikzplotlib

def distance_between_averaged_rdm_apparent_and_betti_in_random_k_complexes(p, n, k,runs_to_average_over = 1):
    filtration = []
    if (k == 2):
        filtration = rnp.get_random_2_complex(n, p)
    if (k == 3):
        filtration = rnp.get_random_3_complex(n, p)

    mat = ca.build_boundary_matrix_from_filtration(filtration, True)
    steps, lowest, red = ca.column_algorithm_with_a_twist(mat)
    betti = ca.betti_numbers(filtration, lowest, k)
    rdm_res = []
    betti_sum = sum(betti)
    rdm_perfects = 0
    for i in range(runs_to_average_over):
        _,_,critvec = rdm.random_discrete_morse(copy(filtration))
        rdm_res.append(sum(critvec) - betti_sum)
        if(sum(critvec) - betti_sum == 0):
            rdm_perfects += 1

    crits, pairs, clear = filtration_to_DMF(filtration)

    return sum(rdm_res)/runs_to_average_over, rdm_perfects/runs_to_average_over, len(crits)-betti_sum

def plots_for_varying_p_rdm_vs_apparent_and_betti_numbers(n,k,runs_per_step):
    mus_rdm = []
    mus_app = []
    steps = []
    perfect_percentage_rdm = []
    perfect_percentage_app = []

    for step in range(0,101,1):
        print("STEP: ", step)

        step = step /100
        steps.append(step)

        rdm_distance_per_step = 0
        rdm_perfect_per_step = 0

        apparent_dist_per_step = 0
        app_perfect_per_step = 0

        for _ in range(runs_per_step):
            rdm_dist,perfect_per_complex, apparent_dist = distance_between_averaged_rdm_apparent_and_betti_in_random_k_complexes(step, n, k)

            rdm_distance_per_step += rdm_dist
            rdm_perfect_per_step += perfect_per_complex

            apparent_dist_per_step += apparent_dist
            if(apparent_dist == 0):
                app_perfect_per_step += 1

        perfect_percentage_rdm.append(rdm_perfect_per_step/runs_per_step)
        perfect_percentage_app.append(app_perfect_per_step/runs_per_step)

        mus_rdm.append(rdm_distance_per_step/runs_per_step)
        mus_app.append(apparent_dist_per_step/runs_per_step)

    plt.plot(steps, mus_rdm)
    plt.title("Mean distances for RDM")
    tikzplotlib.save("random_morse_in_" + str(k) + "_complex_" + str(n) + "vertices_mus.tex")
    plt.show()

    plt.plot(steps, perfect_percentage_rdm)
    plt.title("Percentage of perfect matchings for RDM")
    tikzplotlib.save("random_morse_in_" + str(k) + "_complex_" + str(n) + "vertices_perfects.tex")
    plt.show()

    plt.plot(steps, mus_app)
    plt.title("Mean distances for AG")
    tikzplotlib.save("apparent_gradient_in_" + str(k) + "_complex_" + str(n) + "vertices_mus.tex")
    plt.show()

    plt.plot(steps, perfect_percentage_app)
    plt.title("Percentage of perfect matchings for AG")
    tikzplotlib.save("apparent_gradient_in_" + str(k) + "_complex_" + str(n) + "vertices_perfects.tex")
    plt.show()

plots_for_varying_p_rdm_vs_apparent_and_betti_numbers(15,2,100)