from copy import copy

import Algorithms.point_cloud_generator as pcg
import Algorithms.alphacomplexwrapper as acw
import Algorithms.column_algo.column_algorithm as ca
import Algorithms.random_discrete_morse as rdm
import Examples.rand_k_n_p as rnp

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib

def filtration_len_in_alpha_complexes(n,dim):
    filt1 = []
    filt2 = []
    runs = 50
    for i in range(runs):
        print(i)
        points1 = pcg.gaussian_mixture_model(n,[[0,0],[1,1],[0,3]],[[[1,0],[0,1]],[[1,0],[0,1]],[[1,0],[0,1]]])
        alpha1 = acw.AlphaComplexWrapper(points1, False)
        filtration1 = [elem[0] for elem in alpha1.filtration]
        filt1.append(len(filtration1))

        points2 = pcg.generate_n_points(n,dim)
        alpha2 = acw.AlphaComplexWrapper(points2, False)
        filtration2 = [elem[0] for elem in alpha2.filtration]
        filt2.append(len(filtration2))

    print("Mixture: ", sum(filt1)/runs)
    print("Uniform: ", sum(filt2)/runs)

def percentage_of_apparent_pairs_in_alpha_complexes(n, dim):

    points = pcg.generate_n_points(n, dim)
    alpha = acw.AlphaComplexWrapper(points, False)
    filtration = [elem[0] for elem in alpha.filtration]
    crit, pairs, clear = filtration_to_DMF(filtration)

    return (100 * len(pairs)*2)/len(filtration)

def percentage_of_apparent_pairs_in_random_k_complexes(p,n,k):
    filtration = rnp.get_random_2_complex(n,p)
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
    steps, lowest, red= ca.column_algorithm_with_a_twist(mat)

    betti = ca.betti_numbers(filtration,lowest,k)

    return len(crit) - sum(betti), len(filtration)

def sum_of_betti_in_random_k_complexes(p, n, k):
    filtration = []
    if (k == 2):
        filtration = rnp.get_random_2_complex(n, p)
    if (k == 3):
        filtration = rnp.get_random_3_complex(n, p)

    mat = ca.build_boundary_matrix_from_filtration(filtration, True)
    steps, lowest, red = ca.column_algorithm_with_a_twist(mat)
    betti = ca.betti_numbers(filtration, lowest, k)
    betti_sum = sum(betti)
    return betti_sum

def distance_between_averaged_rdm_and_betti_in_random_k_complexes(p, n, k,runs_to_average_over = 250):
    filtration = []
    if (k == 2):
        filtration = rnp.get_random_2_complex(n, p)
    if (k == 3):
        filtration = rnp.get_random_3_complex(n, p)

    mat = ca.build_boundary_matrix_from_filtration(filtration, True)
    steps, lowest, red = ca.column_algorithm_with_a_twist(mat)
    betti = ca.betti_numbers(filtration, lowest, k)
    res = []
    betti_sum = sum(betti)
    perfects = 0
    for i in range(runs_to_average_over):
        _,_,critvec = rdm.random_discrete_morse(copy(filtration))
        res.append(sum(critvec) - betti_sum)
        if(sum(critvec) - betti_sum == 0):
            perfects += 1

    return sum(res)/runs_to_average_over, perfects/runs_to_average_over

def plots_of_percentage_of_apparent_pairs(dim):
    runs = 5
    mus = {-1 : 0}
    stds = {-1 : 0}
    minmax = {0 : (0,0)}
    steps = []
    for step in range(650,1001,50):
        steps.append(step)
        mus[step] = []
        stds[step] = []
        minmax[step] = (100,0)
        data = []

        print("STEP: ", step)
        for _ in range(runs):
            if(step >= 500):
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

        # # Plot the histogram.
        # plt.hist(data, bins=25, alpha = 0.6, histtype='bar', density = True)
        # # Plot the PDF.
        # xmin, xmax = plt.xlim()
        # x = np.linspace(xmin, xmax, 1000)
        # p = scs.norm.pdf(x, mu, std)
        # plt.plot(x, p, 'k', linewidth=2)
        # title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
        # plt.title(title)
        # tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "at_steps_" + str(step) + "random_2_10_points.tex")
        # plt.show()
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
    tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "uniform_mus.tex")
    plt.show()

    plt.plot(steps, stads)
    tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "uniform_stds.tex")
    plt.show()

def plots_of_percentage_of_apparent_pairs_by_dim(n, runs):
    mus = {-1 : 0}
    stds = {-1 : 0}
    minmax = {0 : (0,0)}
    steps = []
    for step in range(2,7):
        steps.append(step)
        mus[step] = []
        stds[step] = []
        minmax[step] = (100,0)
        data = []

        print("STEP: ", step)
        for _ in range(runs):
            print(_)
            res = percentage_of_apparent_pairs_in_alpha_complexes(n, step)
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
        tikzplotlib.save("apparent_pairs_in_dim" + str(step) + "_on_pointscloud_of_size_" + str(n) + "_gaussian_mixture.tex")
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
    tikzplotlib.save("apparent_pairs_on_" + str(n) + "_points_uniform.tex")
    plt.show()

    plt.plot(steps, stads)
    tikzplotlib.save("apparent_pairs_on_" + str(n) + "_points_uniform.tex")
    plt.show()

def plots_of_distance_between_apparent_pairs_and_betti_numbers(n,k,runs_per_step):
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
        for _ in range(runs_per_step):
            print(_)
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
        elements_in_filtration.append([accumulated_len/runs_per_step])

        # Fit a normal distribution to the data:
        mu, std = scs.norm.fit(data)

        mus[step].append(mu)
        stds[step].append(std)

        # plt.hist(data, bins=25, alpha = 0.6, histtype='bar', density = True)
        # title = "Betti to criticals: p = %.2f, n = %d, k=%d" % (step, n, k)
        # plt.title(title)
        # tikzplotlib.save("apparent_pairs_" + str(k) + "_complex_at_steps_" + str(step) + ".tex")
        # plt.show()

    print(steps)
    print(list(mus.items()))
    print(list(stds.items()))

    means = [elem[1][0] for elem in list(mus.items())[1:]]
    stads = [elem[1][0] for elem in list(stds.items())[1:]]

    plt.show()
    plt.plot(steps, means)
    plt.title("Mean distances")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "mus.tex")
    plt.show()

    plt.plot(steps, stads)
    plt.title("Std deviation")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "stads.tex")
    plt.show()

    plt.plot(steps, [perf[0]/runs_per_step for perf in perfects])
    plt.title("Percentage of perfect matchings")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "perfects.tex")
    plt.show()

    plt.plot(steps, elements_in_filtration)
    plt.title("Number of elements in filtration")
    tikzplotlib.save("apparent_pairs_in_k_complex" + str(k) + "total_elements.tex")
    plt.show()

def plots_of_distance_between_random_discrete_morse_and_betti_numbers(n,k,runs_per_step):
    mus = []
    steps = []
    perfect_percentage = []

    for step in range(0,101,1):
        print("STEP: ", step)

        step = step /100
        steps.append(step)

        distance_per_step = 0
        perfect_per_step = 0
        for _ in range(runs_per_step):
            res,perfect_per_complex = distance_between_averaged_rdm_and_betti_in_random_k_complexes(step, n, k)

            distance_per_step += res
            perfect_per_step += perfect_per_complex

        perfect_percentage.append(perfect_per_step/runs_per_step)
        mus.append(distance_per_step/runs_per_step)

    plt.plot(steps, mus)
    plt.title("Mean distances")
    tikzplotlib.save("random_morse_in_" + str(k) + "_complex_" + str(n) + "vertices_mus.tex")
    plt.show()

    plt.plot(steps, perfect_percentage)
    plt.title("Percentage of perfect matchings")
    tikzplotlib.save("random_morse_in_" + str(k) + "_complex_" + str(n) + "vertices_perfects.tex")
    plt.show()

def plots_of_sum_of_betti_numbers(n,k,runs_per_step):
    data = []
    steps = []
    perfect_percentage = []

    for step in range(0,101, 1):
        print("STEP: ", step)

        step = step /100
        steps.append(step)
        aggregated_res = 0
        for _ in range(runs_per_step):
            aggregated_res += sum_of_betti_in_random_k_complexes(step, n, k)

        data.append(aggregated_res/runs_per_step)


    plt.plot(steps, data)
    plt.title("Mean sum of Betti numbers")
    tikzplotlib.save("summed_bettis" + str(k) + "_complex_" + str(n)+".tex")
    plt.show()

plots_of_distance_between_random_discrete_morse_and_betti_numbers(20,2,200)