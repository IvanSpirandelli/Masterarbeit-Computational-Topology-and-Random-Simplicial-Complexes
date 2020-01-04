import matplotlib.pyplot as plt
import time
from datetime import datetime
from copy import deepcopy
import itertools as it

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper
from GudhiExtension.column_algorithm import column_algorithm
from GudhiExtension.point_cloud_generator import point_cloud_generator

dunce_hat = [
    [0],[1],[2],[3],[4],[5],[6],[7],
    [0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],
    [1,2],[1,3],[1,4],[1,5],[1,6],[1,7],
    [2,4],[2,5],[2,6],[2,7],
    [3,4],[3,5],
    [4,5],[4,7],
    [5,6],[5,7],
    [6,7],
    [0,1,4],[0,3,4],[0,1,3],[0,1,7],[0,2,7],[0,2,6],[0,5,6],[0,2,5],
    [1,2,4],[1,2,5],[1,2,6],[1,3,5],[1,6,7],
    [2,4,7],[3,4,5],[5,6,7],
    [4,5,7],
    [5,6,7]
]

dunce_collapsible_delaunay = [
    [0,1,2,4],[0,1,3,4],[0,1,3,7],[0,1,2,6],[0,1,6,7],[0,2,4,7],[0,2,5,6],[0,2,5,7],[0,3,4,7],[0,5,6,7],
    [1,2,3,4],[1,2,3,5],[1,2,5,6],[1,3,5,6],[2,3,4,5],[2,4,5,7],[1,3,6,7]
]

def build_complex_from_triangulation(tria):
    dim = len(tria[0])
    for i in range(dim - 1, 0, -1):
        for simplex in tria:
            for combi in it.combinations(simplex, i):
                print(combi)

def connect_shift_and_append_filtration(filtration, connection, shift, steps):
    out_fil = deepcopy(filtration)
    n = len(filtration)
    for k in range(n):
        simplex = out_fil[k]
        for i in range(steps):
            to_append = deepcopy(simplex)
            for j in range(len(to_append)):
                if(to_append[j] == connection):
                    continue
                else:
                    to_append[j] = to_append[j] + (i+1)*shift
            if(simplex != to_append):
                out_fil.append(to_append)

    return out_fil

def analize_dunce_wedge():
    ca = column_algorithm()
    fig, axs = plt.subplots(2)
    x = []
    sim = []
    y = []

    for i in range(20):
        dunce_wedge = connect_shift_and_append_filtration(dunce_hat, 0, 7,i)
        pre_algo = time.time()
        steps = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(dunce_wedge))
        y.append(steps)
        post_algo = time.time()

        print("Vertices: ", 8 + (i * 7))
        print("Simplices: ", len(dunce_wedge))
        print("Steps: ", steps)
        print(post_algo-pre_algo)

        x.append(8 + (i * 7))
        sim.append(len(dunce_wedge))

    axs[0].scatter(x, y)
    axs[1].scatter(sim, y)

    plt.show()

def analize_random_points(max_count):
    pcg = point_cloud_generator()

    fig, axs = plt.subplots(2)
    x = []
    sim = []
    y = []


    with open("../Experiments/Results/greedy_analysis_" + str(datetime.now()) + ".txt", "w+") as file:
        for i in range(3,max_count):
            ###
            stepline = "---"+ str(i) +"/125---"
            file.write(stepline)
            print(stepline)
            curr_t = time.time()
            ###

            points = pcg.generate_n_points(i,3)

            ###
            point_t = time.time()
            pointline = str(i) + " points generated in " + str(point_t-curr_t) + " seconds: "
            file.write(pointline)
            file.write(str(points))
            print(pointline)
            print(points)
            ###

            alpha = alpha_complex_wrapper(pcg.points)

            pre_algo = time.time()
            steps = column_algorithm(alpha.get_boundary_matrix())
            y.append(steps)
            post_algo = time.time()

            res_line = "Computed persistence in: " + str(steps) + " Steps.\n" + "Steps/Vertices = " + str(steps/i) + "\n" + "Took " + str(post_algo - pre_algo) + "seconds"
            file.write(res_line)
            print(res_line)

            x.append(i)
            sim.append(len(alpha.filtration))

    axs[0].scatter(x,y)
    axs[1].scatter(sim,y)

    plt.show()

analize_random_points(10)