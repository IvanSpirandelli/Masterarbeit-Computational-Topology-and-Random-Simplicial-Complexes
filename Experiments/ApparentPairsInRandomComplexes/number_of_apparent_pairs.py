import GudhiExtension.point_cloud_generator as pcg
import GudhiExtension.alpha_complex_wrapper as acw
import Examples.rand_k_n_p as rnp

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration
from MorseAndFiltrations.filtration_to_DMF import filtration_to_DMF

import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib

def percentage_of_apparent_pairs_in_alpha_complexes_on_uniform_point_clouds(n,dim):
    points = pcg.generate_n_points(n,dim)
    alpha = acw.alpha_complex_wrapper(points, False)
    filtration = [elem[0] for elem in alpha.filtration]
    crit, pairs, clear = filtration_to_DMF(filtration)
    return (100 * len(pairs)*2)/len(filtration)

def plots_of_percentage_of_apparent_pairs_uniform(dim):
    runs = 3
    mus = {0 : 0}
    stds = {0 : 0}
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
            res = percentage_of_apparent_pairs_in_alpha_complexes_on_uniform_point_clouds(step, dim)
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
        #plt.hist(data, bins=20, histtype='bar', weights=np.zeros_like(data) + 1. / len(data))
        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 1000)
        p = scs.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
        plt.title(title)
        tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "at_steps_" + str(step) + ".tex")
        plt.show()

    print(steps)
    print(list(mus.items()))
    print(list(stds.items()))

    means = [elem[1][0] for elem in list(mus.items())[1:]]
    stads = [elem[1][0] for elem in list(stds.items())[1:]]

    print(means)
    print(stads)

    plt.plot(steps, means)
    tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "mus_to_steps.tex")
    plt.show()

    plt.plot(steps, stads)
    tikzplotlib.save("apparent_pairs_in_dim" + str(dim) + "stads_to_steps.tex")
    plt.show()

plots_of_percentage_of_apparent_pairs_uniform(2)