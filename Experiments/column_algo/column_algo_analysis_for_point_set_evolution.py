import random
from copy import deepcopy
from datetime import datetime

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper
from GudhiExtension.column_algo.column_algorithm import column_algorithm
import GudhiExtension.point_cloud_generator as pcg
import matplotlib.pyplot as plt

def initial_points(top, num_points, dim, num_sets):
    print("init points")
    for i in range(num_sets):
        points = pcg.generate_n_points(num_points, dim)
        alpha = alpha_complex_wrapper(points)
        steps = column_algorithm(alpha.get_boundary_matrix())
        top.append([steps, points])

    top.sort(reverse = True)
    print("init points DONE")

def evolve(top, keep, fresh):
    top = top[:keep]
    out = []
    for elem in top:
        for i in range(fresh):
            evolved_elem = deepcopy(elem)
            change_n_points_in_set(evolved_elem[1],1)
            alpha = alpha_complex_wrapper(evolved_elem[1])
            steps = column_algorithm(alpha.get_boundary_matrix())
            evolved_elem[0] = steps
            out.append(evolved_elem)

    for elem in top:
        out.append(elem)

    out.sort(reverse = True)

    return out


def change_n_points_in_set(points, n):
    indices = [i for i in range(len(points))]
    sample = random.sample(indices, n)
    dim = len(points[0])

    for i in sample:
        points[i] = pcg.generate_one_point(dim)

def evol_analysis(num_points, dim, num_sets, keep, iterations):
    fig, axs = plt.subplots(2)
    x = [i for i in range(iterations)]
    y = []
    z = []

    top = []

    if(num_sets%keep != 0):
        num_sets += keep - num_sets%keep
        print("Set number of sets  to: " + str(num_sets))

    initial_points(top,num_points, dim, num_sets)

    for elem in top:
        print(elem)

    count = 0
    while count<iterations:
        top = evolve(top, keep, int(num_sets/keep) - 1)
        count += 1;
        print(count)
        y.append(sum(row[0] for row in top)/num_sets)
        z.append(top[0][0])

    print("###############################################################################################################")
    for elem in top:
        print(elem)

    axs[0].scatter(x, y)
    axs[1].scatter(x, z)
    plt.show()

    with open("../Experiments/_Results/evolutionary_greedy_analysis_" + str(num_points) + "points_" + str(datetime.now()) + ".csv", "w+") as file:
        file.write("n: " + str(num_points) + "; dim: " + str(dim) + "; sets per iteration: " + str(num_sets) + "; kept per iteration: " + str(keep) + "; number of iterations: " +str(iterations)+ "\n")
        file.write("Average algorithm steps: " + str(y)+ "\n")
        file.write("Top algorithm steps: " + str(z)+ "\n")
        file.write("---final_set---" + "\n")
        for row in top:
            print(row)
            file.write(str(row) + "\n")


for i in range(8,20):
    for _ in range(7):
        evol_analysis(i, 3, 12, 3, 50)