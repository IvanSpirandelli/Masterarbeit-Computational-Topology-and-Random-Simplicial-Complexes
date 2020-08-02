import tikzplotlib

import Algorithms.filtration_manipulation as fm
import Algorithms.column_algo.column_algo_outs as cao
import Algorithms.column_algo.column_algorithm as ca
import Algorithms.point_cloud_generator as pcg
import Algorithms.alpha_complex_wrapper as acw
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


import scipy.stats as scs
import matplotlib.pyplot as plt
import numpy as np
import timeit


def draw_filtration_2D(plot, points, filtration, level=0):
    step = 0
    index = 0
    dist_at_index = 0.0
    # print("Index: ", index, ", DistAtIndex: ", dist_at_index, ", Step: ", step)
    if (step == 0):
        # Moving forward in the list of simplices, until the layer of distance 0 is done
        while (step == 0):
            if (filtration[index][1] == dist_at_index):
                index += 1
            else:
                step += 1
                dist_at_index = filtration[index][1]

        x, y = zip(*points)
        plot.scatter(x, y, zorder=3)

        for i,p in enumerate(points):
            label = "{:}".format(i)

            plt.annotate(label,  # this is the text
                         (p[0], p[1]),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5),  # distance from text to points (x,y)
                         ha='center')  # horizontal alignment can be left, right or center

    latest_dist = 0.0
    # print("Index: ", index, ", DistAtIndex: ", dist_at_index, ", Step: ", step)
    while (step < level and index < len(filtration)):
        if (filtration[index][1] == dist_at_index):

            if (len(filtration[index][0]) == 2):
                zipped = list(zip(points[filtration[index][0][0]], points[filtration[index][0][1]]))
                plot.plot(list(zipped[0]), list(zipped[1]), lw=3, color='coral', zorder=2)

            elif (len(filtration[index][0]) == 3):
                zipped = list(zip(points[filtration[index][0][0]],
                                  points[filtration[index][0][1]],
                                  points[filtration[index][0][2]]))
                plot.fill(list(zipped[0]), list(zipped[1]), color='beige', zorder=1)

            index += 1
            latest_dist = dist_at_index
        else:
            dist_at_index = filtration[index][1]
            step += 1
        # print("Index: ", index, ", DistAtIndex: ", dist_at_index, ", Step: ", step)
    return latest_dist



def stabelize(filtration, pairings):
    stableization_steps = 0
    print("FILTRATION: ", filtration)
    if(pairings == []):
        critical, pairings, _ = filtration_to_DMF(filtration)
        print("CRITICAL CELLS: ", critical)
        print("PAIRINGS: ", pairings)
        print("NUMBER: ", len(critical))
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    n_filtration = DMF_to_filtration(filtration, pairings)


    while n_filtration != filtration:
        print("FILTRATION: ", n_filtration)
        critical, pairings, _ = filtration_to_DMF(n_filtration)
        filtration = n_filtration
        print("CRITICAL CELLS: ", critical)
        print("PAIRINGS: ", pairings)
        print("NUMBER: ", len(critical))
        print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
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

def correlation_out(name, simplices, x, y ):
    with open(name + ".txt", "w+") as file:
        file.write(str(simplices) + ";\n")
        file.write("CRITICAL FACES: " + str(x) + "\n")
        file.write("CALCULATION STEPS: " + str(y) + "\n")
        spear, _ = scs.spearmanr(x, y)
        pear, _ = scs.pearsonr(x,y)
        cova = np.corrcoef(x,y)
        slope, intercept, r_value, p_value, std_err = scs.linregress(x,y)
        file.write("#######################"+ "\n")
        file.write("R-VALUE: " +  str(r_value)+ "\n")
        file.write("P-VALUE: " +  str(p_value) + "\n")
        file.write("COVARIANCE MATRIX: " +  str(cova) + "\n")
        file.write("PEARSON CORRELATION: " +  str(pear) + "\n")
        file.write("SPEARMAN CORRELATION: "+ str(spear) + "\n")
        file.write("#######################" + "\n")

        file.write("SLOPE:" + str(slope) + "\n")
        file.write("INTERCEPT:" +  str(intercept) + "\n")
        file.write("STANDARD ERROR:" +  str(std_err) + "\n")

        return pear, spear, p_value

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

    xticklabels = [elem for id,elem in enumerate(filtration) if(id in range(xrange[0],xrange[1]))] # if len(elem) > 1
    yticklabels = [elem for id,elem in enumerate(filtration) if(id in range(yrange[0],yrange[1]))] # if len(elem) < max_len
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
u = []
v = []


for i in range(8,80):
    print(i)
    if(i <= 48):
        filtration = me.build_morozov_example(i)
        steps,_,_ = ca.column_algorithm(ca.build_boundary_matrix_from_filtration_and_clear(filtration,[]))
        x.append(len(filtration))
        y.append(steps[0])

    filtration = ngon.get_fin_pizza_alternative(i)
    steps, _, _ = ca.column_algorithm(ca.build_boundary_matrix_from_filtration_and_clear(filtration, []))
    u.append(len(filtration))
    v.append(steps[0])


plt.scatter(x, y, color = 'xkcd:azure')
plt.scatter(u, v, color = 'xkcd:orange')

plt.savefig("morozov_ngon_comparison.png", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches="tight", pad_inches=0.1, metadata=None)

# tikzplotlib.save("compare_ngon_morozov.tex")
plt.show()
#


