import matplotlib.pyplot as plt
import time
from datetime import datetime
from copy import deepcopy
import itertools as it

from Algorithms.alphacomplexwrapper import AlphaComplexWrapper
from Algorithms.column_algo.column_algorithm import column_algorithm
import Algorithms.point_cloud_generator as pcg
from Utilities.csv_file_container import csv_file_container

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

dunce_collapsible_delaunay_tetraeder = [
    [0,1,2,4],[0,1,3,4],[0,1,3,7],[0,1,2,6],[0,1,6,7],[0,2,4,7],[0,2,5,6],[0,2,5,7],[0,3,4,7],[0,5,6,7],
    [1,2,3,4],[1,2,3,5],[1,2,5,6],[1,3,5,6],[2,3,4,5],[2,4,5,7],[1,3,6,7]
]

delaunay_to_dunce_filtration = [[0], [1], [2], [4], [3], [7], [6], [5],
                                [0, 1], [0, 2], [0, 4], [1, 2], [1, 4], [2, 4],
                                [0, 3], [1, 3], [3, 4], [0, 7], [1, 7], [3, 7],
                                [0, 6], [1, 6], [2, 6], [6, 7], [2, 7], [4, 7],
                                [0, 5], [2, 5], [5, 6], [5, 7], [2, 3], [1, 5],
                                [3, 5], [3, 6], [4, 5],
                                [0, 1, 2], [0, 1, 4], [0, 2, 4], [1, 2, 4], [0, 1, 3],
                                [0, 3, 4], [1, 3, 4], [0, 1, 7], [0, 3, 7],
                                [0, 1, 6], [0, 2, 6], [1, 2, 6], [0, 6, 7], [1, 6, 7],
                                [0, 2, 7], [0, 4, 7], [2, 4, 7], [0, 2, 5], [0, 5, 6],
                                [2, 5, 6], [0, 5, 7], [2, 5, 7], [3, 4, 7], [5, 6, 7],
                                [1, 2, 3],  [1, 2, 5], [1, 3, 5], [2, 3, 5],
                                [1, 5, 6],  [3, 5, 6], [2, 4, 5], [3, 4, 5],
                                [4, 5, 7], [3, 6, 7], [1, 3, 7], [1, 3, 6], [2, 3, 4],
                                [0, 1, 3, 4], [1, 2, 3, 4], [1, 2, 3, 5], [2, 3, 4, 5],
                                [2, 4, 5, 7], [0, 2, 5, 7], [0, 5, 6, 7], [0, 1, 6, 7],
                                [0, 1, 2, 6], [0, 1, 2, 4], [0, 2, 4, 7], [0, 1, 3, 7],
                                [0, 2, 5, 6], [0, 3, 4, 7], [1, 3, 6, 7], [1, 2, 5, 6], [1, 3, 5, 6]]




def build_complex_from_triangulation(tria):
    dim = len(tria[0])
    out = deepcopy(tria)
    for i in range(dim - 1, 0, -1):
        for simplex in tria:
            for combi in it.combinations(simplex, i):
                if(not combi in out):
                    out.append(combi)
    out = sorted(out, key = len)
    return [list(e) for e in out]

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

    fig, axs = plt.subplots(2)
    x = []
    sim = []
    y = []

    cfc = csv_file_container("num_of_points;persistence_computation_steps;steps_div_by_vertices;computation_time;points")

    for i in range(3,max_count):
        points = pcg.generate_n_points(i, 3)
        alpha = AlphaComplexWrapper(points)
        pre_algo = time.time()
        mat = alpha.get_boundary_matrix()

        print(mat)
        print("-----")
        print(alpha.filtration)

        steps = column_algorithm(mat)
        y.append(steps)
        post_algo = time.time()
        x.append(i)
        sim.append(len(alpha.filtration))

        print("RATE: " + str(steps/i))

        cfc.add_row(str(i) + ";" + str(steps) + ";" + str(steps/i) + ";" + str(post_algo-pre_algo) + ";" + str(points))

    cfc.write_to_file("../Experiments/_Results/greedy_analysis_" + str(datetime.now()))

    axs[0].scatter(x,y)
    axs[1].scatter(sim,y)

    plt.show()

print(build_complex_from_triangulation(dunce_collapsible_delaunay_tetraeder))