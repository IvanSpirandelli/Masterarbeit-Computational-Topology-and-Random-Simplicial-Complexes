import GudhiExtension.point_cloud_generator as pcg
import GudhiExtension.alpha_complex_wrapper as acw
import GudhiExtension.column_algo.column_algorithm as ca
import GudhiExtension.column_algo.column_algo_outs as cao
import Examples.rand_k_n_p as rnp

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib

def percentage_of_apparent_pairs_in_alpha_complexes(n, dim):
    points = pcg.gaussian_mixture_model(n,[[0,0],[1,1],[0,3]],[[[1,0],[0,1]],[[1,0],[0,1]],[[1,0],[0,1]]])
    alpha = acw.alpha_complex_wrapper(points, False)
    filtration = [elem[0] for elem in alpha.filtration]
    crit, pairs, clear = filtration_to_DMF(filtration)

    return (100 * len(pairs)*2)/len(filtration)

def distance_between_apparent_and_betti_in_random_k_complexes(p, n, k):
    filtration = []
    if(k == 2):
        filtration = rnp.get_random_2_complex(n,p)
    if(k == 3):
        filtration = rnp.get_random_3_complex(n,p)

    crit, pairs, clear = filtration_to_DMF(filtration)

    mat = ca.build_boundary_matrix_from_filtration(filtration,True)
    steps, lowest, red= ca.column_algorithm(mat)
    betti = ca.betti_numbers(filtration,lowest,k)

    # print([len([elem for elem in crit if len(elem) == 1]),
    #       len([elem for elem in crit if len(elem) == 2]),
    #       len([elem for elem in crit if len(elem) == 3])])
    # print(betti)

    return len(crit) - sum(betti), len(filtration)

def plots_of_percentage_of_apparent_pairs(dim):
    runs = 1000
    mus = {-1 : 0}
    stds = {-1 : 0}
    minmax = {0 : (0,0)}
    steps = []
    for step in range(50,1001,50):
        steps.append(step)
        mus[step] = []
        stds[step] = []
        minmax[step] = (100,0)
        data = []

        print("STEP: ", step)
        for _ in range(runs):
            print(_)
            res = percentage_of_apparent_pairs_in_alpha_complexes(step, dim)
            if(res > minmax[step][1] ):
                minmax[step] = (minmax[step][0],res)
            if(res < minmax[step][0]):
                minmax[step] = (res,minmax[step][1])
            data.append(res)

        # Fit a normal distribution to the data:
        mu, std = scs.norm.fit(data)

        mus[step].append(mu)
        stds[step].append(std)

        # Plot the histogram.
        plt.hist(data, bins=25, alpha = 0.6, histtype='bar', density = True)
        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 1000)
        p = scs.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
        plt.title(title)
        tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "at_steps_" + str(step) + "gaussian_mixture.tex")
        plt.show()

    print(steps)
    print(list(mus.items()))
    print(list(stds.items()))

    means = [elem[1][0] for elem in list(mus.items())[1:]]
    stads = [elem[1][0] for elem in list(stds.items())[1:]]

    print(steps)
    print(means)
    print(stads)

    plt.plot(steps, means)
    tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "mus_to_steps_gaussian_mixture.tex")
    plt.show()

    plt.plot(steps, stads)
    tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "stads_to_steps_gaussian_mixture.tex")
    plt.show()

def plots_of_distance_between_apparent_pairs_and_betti_numbers(n,k):
    runs = 2000
    mus = {-1 : 0}
    stds = {-1 : 0}
    minmax = {0 : (0,0)}
    steps = []
    perfects = []
    elements_in_filtration = []

    for step in range(0,101,1):

        print("STEP: ", step)

        step = step /100
        steps.append(step)
        mus[step] = []
        stds[step] = []
        minmax[step] = (100,0)
        data = []

        perfect = 0
        accumulated_len = 0
        for _ in range(runs):
            res, len_filt = distance_between_apparent_and_betti_in_random_k_complexes(step, n, k)

            if(res > minmax[step][1] ):
                minmax[step] = (minmax[step][0],res)
            if(res < minmax[step][0]):
                minmax[step] = (res,minmax[step][1])

            if(res == 0):
                perfect += 1
            accumulated_len += len_filt
            data.append(res)

        perfects.append([perfect])
        elements_in_filtration.append([accumulated_len/runs])

        # Fit a normal distribution to the data:
        mu, std = scs.norm.fit(data)

        mus[step].append(mu)
        stds[step].append(std)

        # Plot the histogram.
        plt.hist(data, bins=25, alpha = 0.6, histtype='bar', density = True)
        # Plot the PDF.
        xmin, xmax = plt.xlim()
        # x = np.linspace(xmin, xmax, 1000)
        # p = scs.norm.pdf(x, mu, std)
        # plt.plot(x, p, 'k', linewidth=2)
        title = "Betti to criticals: p = %.2f, n = %d, k=%d" % (step, n, k)
        plt.title(title)
        tikzplotlib.save("apparent_pairs_" + str(k) + "_complex_at_steps_" + str(step) + ".tex")
        plt.show()

    print(steps)
    print(list(mus.items()))
    print(list(stds.items()))

    means = [elem[1][0] for elem in list(mus.items())[1:]]
    stads = [elem[1][0] for elem in list(stds.items())[1:]]

    plt.plot(steps, means)
    plt.title("Mean distances")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "mus.tex")
    plt.show()

    plt.plot(steps, stads)
    plt.title("Std deviation")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "stads.tex")
    plt.show()

    plt.plot(steps, [perf[0]/runs for perf in perfects])
    plt.title("Percentage of perfect matchings")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "perfects.tex")
    plt.show()

    plt.plot(steps, elements_in_filtration)
    plt.title("Number of elements in filtration")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "total_elements.tex")
    plt.show()

plots_of_percentage_of_apparent_pairs(2)