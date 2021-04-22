import timeit
from copy import copy

import Algorithms.point_cloud_generator as pcg
import Algorithms.alphacomplexwrapper as acw
import Algorithms.random_discrete_morse as rdm
import Algorithms.column_algo.column_algorithm as ca
import Examples.rand_k_n_p as rnp
import Examples.davides_eight_point_delaunay as dd

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib


def uniform_comparison(n,dim, console_outs = False):
    # points = pcg.generate_n_points(n,dim)

    #
    # if(dim == 2):
    #     points = pcg.multivariate_gaussian(n,[0,0],
    #                                         [[1,0],[0,1]])
    # else:
    #     points = pcg.multivariate_gaussian(n, [0, 0, 0],
    #                                         [[1, 0, 0], [0, 1, 0], [0 ,0 ,1]])
    #

    if(dim == 2):
        points = pcg.gaussian_mixture_model(n,[[0,0],[1,1],[0,3]],
                                            [[[1,0],[0,1]],[[1,0],[0,1]],[[1,0],[0,1]]])
    else:
        points = pcg.gaussian_mixture_model(n, [[0, 0, 0], [1, 1, 1], [0, 3, 0.5]],
                                            [[[1, 0, 0], [0, 1, 0], [0 ,0 ,1]],
                                             [[1, 0, 0], [0, 1, 0], [0 ,0 ,1]],
                                             [[1, 0, 0], [0, 1, 0], [0 ,0 ,1]]])

    alpha = acw.AlphaComplexWrapper(points, False)
    filtration = [elem[0] for elem in alpha.filtration]

    start = timeit.default_timer()
    mat1 = ca.build_boundary_matrix_from_filtration(filtration)
    steps_without,_,_ = ca.column_algorithm(mat1)
    stop = timeit.default_timer()
    without_clearing_time = stop-start
    if(console_outs):
        print("WITHOUT CLEARING TIME: ", stop - start)
        print("WITHOUT CLEARING ADDITIONS: ", steps_without)

        print("--------------------")
        print("LENGTH OF FILTRATION: ", len(filtration))

    start = timeit.default_timer()
    crit, pairs, clear = filtration_to_DMF(filtration)
    if (console_outs):
        print("ELEMENTS IN PAIRS: ", len(pairs) * 2)
        print("--------------------")

    mat2 = ca.build_boundary_matrix_from_filtration_and_clear(filtration,clear)
    steps_apparent,_,_ = ca.column_algorithm(mat2)
    stop = timeit.default_timer()
    apparent_clearing_time = stop-start

    if (console_outs):
        print("APPARENT CLEARING TIME: ", stop - start)
        print("APPARENT CLEARING ADDITIONS: ", steps_apparent)

    s = without_clearing_time/ apparent_clearing_time
    a = 100-(100/steps_without[0] * steps_apparent[0])

    if (console_outs):
        print("Speedupfactor by apparents: ", s)
        print("Additions cleared via apparents : ", a)

    return s,a,len(pairs)*200/len(filtration)

def get_average_speedup_factor(n,runs):
    speed2 = []
    speed3 = []
    speed4 = []

    additions2 = []
    additions3 = []
    additions4 = []

    percentage2 = []
    percentage3 = []
    percentage4 = []

    estimated_time_till_finish = [0]

    for i in range(runs):
        if(i > 0):
            print("Step: ", i, "Estimated time till finish: ", (sum(estimated_time_till_finish)/i)*(runs-i))
        start = timeit.default_timer()
        s2,a2,p2 = uniform_comparison(n,2)
        speed2.append(s2)
        additions2.append(a2)
        percentage2.append(p2)

        s3,a3,p3 = uniform_comparison(n,3)
        speed3.append(s3)
        additions3.append(a3)
        percentage3.append(p3)
        stop = timeit.default_timer()

        estimated_time_till_finish.append(stop-start)

        # s4,a4 = uniform_comparison(n,4)
        # speed4.append(s4)
        # additions4.append(a4)

    fit_data(speed2,"s2")
    fit_data(speed3,"s3")
    # fit_data(speed4,4)

    fit_data(additions2, "a2")
    fit_data(additions3, "a3")

    fit_data(percentage2, "p2")
    fit_data(percentage3, "p3")

def fit_data(data,id):
    mu, std = scs.norm.fit(data)

    # Plot the histogram.
    plt.hist(data, bins=100, alpha=0.6, histtype='bar', density=True)
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 1000)
    #p = scs.norm.pdf(x, mu, std)
    #plt.plot(x, p, 'k', linewidth=2)
    title = id + "_mean = " + str(mu)
    plt.title(title)
    tikzplotlib.save("apparent_gains_gaussian_mixture_300_points_value_" + str(id) + "_runs_" + str(len(data)) + ".tex")
    plt.show()

def analyse_gap(n, iterations):
    big_elements = []
    big_percentage = []
    big_steps = []

    small_elements = []
    small_percentage = []
    small_steps = []

    saved_additions = []

    for i in range(iterations):
        print(i)
        points = pcg.multivariate_gaussian(n, [0, 0, 0], [[1, 0, 0], [0, 1, 0], [0 ,0 ,1]])

        alpha = acw.AlphaComplexWrapper(points, False)
        filtration = [elem[0] for elem in alpha.filtration]

        mat1 = ca.build_boundary_matrix_from_filtration(filtration)
        steps_without,_,_ = ca.column_algorithm(mat1)
        crit, pairs, clear = filtration_to_DMF(filtration)

        mat2 = ca.build_boundary_matrix_from_filtration_and_clear(filtration,clear)
        steps_apparent,_,_ = ca.column_algorithm(mat2)

        a = 100-(100/steps_without[0] * steps_apparent[0])
        saved_additions.append(a)

        if(a < 50):
            small_elements.append(len(filtration))
            small_percentage.append((100 * len(pairs)*2)/len(filtration))
            small_steps.append(steps_without[0])
        else:
            big_elements.append(len(filtration))
            big_percentage.append((100 * len(pairs)*2)/len(filtration))
            big_steps.append(steps_without[0])

    print("SMALL_ELEMENTS_MEAN", sum(small_elements)/len(small_elements))
    print("SMALL_PERCENTAGE_MEAN", sum(small_percentage)/len(small_percentage))
    print("SMALL_STEPS_MEAN", sum(small_steps)/len(small_steps))

    print("###############")

    print("BIG_ELEMENTS_MEAN", sum(big_elements) / len(big_elements))
    print("BIG_PERCENTAGE_MEAN", sum(big_percentage) / len(big_percentage))
    print("BIG_STEPS_MEAN", sum(big_steps) / len(big_steps))

    fit_data(saved_additions,"_")


get_average_speedup_factor(300,100)
# analyse_gap(30,100)
