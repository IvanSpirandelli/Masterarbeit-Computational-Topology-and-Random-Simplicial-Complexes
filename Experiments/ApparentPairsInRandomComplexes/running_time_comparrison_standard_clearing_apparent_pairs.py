import timeit
from copy import copy

import GudhiExtension.point_cloud_generator as pcg
import GudhiExtension.alpha_complex_wrapper as acw
import GudhiExtension.random_discrete_morse as rdm
import GudhiExtension.column_algo.column_algorithm as ca
import Examples.rand_k_n_p as rnp
import Examples.davides_eight_point_delaunay as dd

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib


def uniform_comparison(n,dim):
    points = pcg.generate_n_points(n,dim)
    alpha = acw.alpha_complex_wrapper(points, False)
    filtration = [elem[0] for elem in alpha.filtration]

    start = timeit.default_timer()
    mat1 = ca.build_boundary_matrix_from_filtration(filtration)
    steps,_,_ = ca.column_algorithm(mat1)
    stop = timeit.default_timer()
    without_clearing_time = stop-start
    print("WITHOUT CLEARING TIME: ", stop - start)
    print("WITHOUT CLEARING ADDITIONS: ", steps)
    #


    start = timeit.default_timer()

    mat12 = ca.build_boundary_matrix_from_filtration(filtration, True)
    steps,_,_ = ca.column_algorithm(mat12)
    stop = timeit.default_timer()
    with_clearing_time = stop-start
    print("WITH CLEARING TIME: ", stop - start)
    print("WITH CLEARING ADDITIONS: ", steps)

    print("--------------------")
    print("LENGTH OF FILTRATION: ", len(filtration))



    start = timeit.default_timer()
    crit, pairs, clear = filtration_to_DMF(filtration)
    print("ELEMENTS IN PAIRS: ", len(pairs) * 2)
    print("--------------------")

    mat2 = ca.build_boundary_matrix_from_filtration_and_clear(filtration,clear)
    steps,_,_ = ca.column_algorithm(mat2)
    stop = timeit.default_timer()
    apparent_clearing_time = stop-start
    print("APPARENT CLEARING TIME: ", stop - start)
    print("APPARENT CLEARING ADDITIONS: ", steps)

    print("Speedupfactor by clearing: ", without_clearing_time / with_clearing_time)
    print("Speedupfactor by apparents: ", without_clearing_time/ apparent_clearing_time)

    return without_clearing_time/apparent_clearing_time

def get_average_speedup_factor():
    speed2 = []
    speed3 = []
    speed4 = []
    runs = 50
    for i in range(runs):
        print(i)
        speed2.append(uniform_comparison(50,2))
        speed3.append(uniform_comparison(50,3))
        speed4.append(uniform_comparison(50,4))

    fit_data(speed2,2)
    fit_data(speed3,3)
    fit_data(speed4,4)

    return speed2,speed3,speed4

def fit_data(data,id):
    mu, std = scs.norm.fit(data)

    print("id", id)
    print("Mu", mu)
    print("Std", std)

    # Plot the histogram.
    plt.hist(data, bins=25, alpha=0.6, histtype='bar', density=True)
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 1000)
    #p = scs.norm.pdf(x, mu, std)
    #plt.plot(x, p, 'k', linewidth=2)
    #title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    #plt.title(title)
    tikzplotlib.save("speedup_in_dim" + str(id) + ".tex")
    plt.show()

uniform_comparison(30,4)

