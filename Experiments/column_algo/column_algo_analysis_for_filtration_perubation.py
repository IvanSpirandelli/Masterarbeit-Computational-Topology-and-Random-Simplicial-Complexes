import itertools
from copy import deepcopy
import matplotlib.pyplot as plt
import math
import numpy as np

import Algorithms.column_algo.column_algorithm as ca
import Algorithms.point_cloud_generator as pcg
from Algorithms.alpha_complex_wrapper import alpha_complex_wrapper

def test_all_vertex_permutations(filtration):
    mat = ca.build_boundary_matrix_from_filtration(filtration)
    vertex_degrees = {}

    num_of_vertices = 0
    for simplex in filtration:
        if(len(simplex) == 1):
            vertex_degrees[num_of_vertices] = sum(mat[num_of_vertices])
            num_of_vertices += 1
        else:
            break

    base = [i for i in range(num_of_vertices)]
    perms = itertools.permutations(base)

    filtration_without_vertices = filtration[num_of_vertices:]
    print(filtration_without_vertices)

    out = []
    mats = []
    kept_perms = []
    for perm in perms:
        kept_perms.append(perm)
        permutation_weight = 0
        for i,p in enumerate(perm, start=1):
            permutation_weight += vertex_degrees[p] * i

        filtration = [[x] for x in perm] + filtration_without_vertices
        mats.append(ca.build_boundary_matrix_from_filtration(filtration))
        steps = ca.column_algorithm(mats[-1])

        out.append([steps, permutation_weight, filtration])

    min_steps = min(o[0] for o in out)
    min_weight = min(o[1] for o in out)

    print("Min steps: ", min_steps)
    print("Min weight: ", min_weight)

    double_check_out = deepcopy(out)
    double_check_out.sort()

    if(double_check_out[0][1] == min_weight):
        points = pcg.generate_n_points(5, 2)
        alpha = alpha_complex_wrapper(points)
        filtration =[elem[0] for elem in alpha.filtration]
        test_all_vertex_permutations(filtration)
    else:
        for dline in double_check_out:
            print(dline)
        #for num,line in enumerate(out,start=0):
        #    if(line[0] == min_steps and line[1] != min_weight):
        #        print('#############################')
        #        print("Permutation: ", kept_perms[num])
        #        print('#############################')
        #        print(line)
        #        print('#############################')
        #        print(mats[num])
        #        print('#############################')

def test_k_random_permutations_of_n_dim_simplices(filtration, n, k):
    simplices_to_permute = []
    start_index = 0;
    last_index = len(filtration)-1
    first_found = False
    for i, simplex in enumerate(filtration):
        if len(simplex)-1 == n:
            if(not first_found):
                first_found = True
                start_index = i
            simplices_to_permute.append(simplex)
        elif len(simplex)-1 > n:
            last_index = i-1
            break

    pre_simplices = filtration[:start_index]
    post_simplices = filtration[last_index+1:]

    x = [0]
    y = [ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration))]
    iterations = 0
    while iterations<k:
        print(iterations,"/",k)
        permuted_filtration = pre_simplices + [list(a) for a in np.random.permutation(simplices_to_permute)] + post_simplices
        steps = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(permuted_filtration))
        x.append(1)
        y.append(steps)
        iterations+=1

    fig, axs = plt.subplots(1)
    axs.scatter(x,y)
    plt.show()

def test_k_random_permutations_of_indexed_simplices(filtration, indices, k):
    print(filtration[indices[0]], filtration[indices[-1]])
    if(k>math.factorial(len(indices))):
        print("WARNING: You are testing for more permutations, than your index set has. Just iterate over all of them.")

    simplices_to_permute = []

    for index in indices:
        simplices_to_permute.append(filtration[index])

    pre_simplices = filtration[:indices[0]]
    post_simplices = filtration[indices[-1]+1:]

    x = [0]
    y = [ca.column_algorithm(ca.build_boundary_matrix_from_filtration(filtration))]
    #print(y)
    iterations = 0
    while iterations<k:
        print(iterations,"/",k)
        permuted_filtration = pre_simplices + [list(a) for a in np.random.permutation(simplices_to_permute)] + post_simplices
        steps = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(permuted_filtration))
        #print(steps)
        x.append(1)
        y.append(steps)
        iterations+=1

    fig, axs = plt.subplots(1)
    axs.scatter(x,y)
    plt.show()

def get_random_permutation_of_indexed_simplices(filtration, indices):
    simplices_to_permute = []

    for index in indices:
        simplices_to_permute.append(filtration[index])
    print(simplices_to_permute)
    pre_simplices = filtration[:indices[0]]
    post_simplices = filtration[indices[-1] + 1:]
    return pre_simplices + [list(a) for a in
                                           np.random.permutation(simplices_to_permute)] + post_simplices

#It is assumed, that the "indices" are at the end of what is shifted through. So indices[-1]-1 = end of range
def shift_indexed_simplices_through_range_of_filtration(filtration, indices, range_start):
    simplices_to_shift = []
    for index in indices:
        simplices_to_shift.append(filtration[index])
    pre_simplices = filtration[:range_start]
    post_simplices = filtration[indices[-1]+1:]
    print(simplices_to_shift)

    shift_pre = []
    shift_post = []
    y = []
    for i in range(range_start, indices[0]+1):
        shift_pre = filtration[range_start : i]
        shift_post = filtration[i: indices[0]]
        shifted_filtration = pre_simplices + shift_pre + simplices_to_shift + shift_post + post_simplices
        #print(pre_simplices)
        #print(shift_pre)
        #print(simplices_to_shift)
        #print(shift_post)
        #print(post_simplices)
        steps = ca.column_algorithm(ca.build_boundary_matrix_from_filtration(shifted_filtration))
        y.append(steps)

    x = [i for i in range(len(y))]
    fig, axs = plt.subplots(1)
    axs.scatter(x,y)
    plt.show()

def compare_filtrations(filtration_one, filtration_two):
    mat1 = ca.build_boundary_matrix_from_filtration(filtration_one)
    print(mat1)
    print("#######################")
    mat2 = ca.build_boundary_matrix_from_filtration(filtration_two)
    print(mat2)
    print("Filtration 1: ", ca.column_algorithm(mat1))
    print("Filtration 2: ", ca.column_algorithm(mat2))

delaunay_to_dunce_filtration = [[0], [1], [2], [4], [3], [7], [6], [5],
                                [0, 1], [0, 2], [0, 4], [1, 2], [1, 4], [2, 4],
                                [0, 3], [1, 3], [3, 4], [0, 7], [1, 7], [3, 7],
                                [0, 6], [1, 6], [2, 6], [6, 7], [2, 7], [4, 7],
                                [0, 5], [2, 5], [5, 6], [5, 7], [2, 3], [1, 5],
                                [3, 5], [3, 6], [4, 5], #35
                                [0, 1, 2], [0, 1, 4], [0, 2, 4], [1, 2, 4],
                                [0, 1, 3], [1, 3, 4], [0, 3, 4], [0, 1, 7],
                                [0, 3, 7], [0, 1, 6], [0, 2, 6], [1, 2, 6],
                                [0, 6, 7], [1, 6, 7], [0, 2, 7], [0, 2, 5],
                                [0, 4, 7], [2, 5, 6], [2, 4, 7], [0, 5, 6],
                                [1, 2, 3], [1, 2, 5], [1, 3, 5], [2, 3, 5],
                                [0, 5, 7], [2, 5, 7], [3, 4, 7], [5, 6, 7],
                                [1, 5, 6], [3, 5, 6], [2, 4, 5], [3, 4, 5],
                                [4, 5, 7], [3, 6, 7],
                                [1, 3, 7], [1, 3, 6], [2, 3, 4], #70-72
                                #73
                                [0, 1, 3, 4], [1, 2, 3, 4], [1, 2, 3, 5], [2, 3, 4, 5],
                                [2, 4, 5, 7], [0, 2, 5, 7], [0, 5, 6, 7], [0, 1, 6, 7],
                                [0, 1, 2, 6], [0, 1, 2, 4], [0, 2, 4, 7], [0, 1, 3, 7],
                                [0, 2, 5, 6], [0, 3, 4, 7], [1, 3, 6, 7], [1, 2, 5, 6], [1, 3, 5, 6]]

#shift_indexed_simplices_through_range_of_filtration(delaunay_to_dunce_filtration, [69,70,71], 35)
#test_k_random_permutations_of_n_dim_simplices(delaunay_to_dunce_filtration, 2, 100)
#test_k_random_permutations_of_indexed_simplices(delaunay_to_dunce_filtration, [35+ i for i in range(34)],10)

for _ in range(10):
    shift_indexed_simplices_through_range_of_filtration(get_random_permutation_of_indexed_simplices(delaunay_to_dunce_filtration, [35+ i for i in range(34)]), [69,70,71], 35)

def you_cant_run_but_you_can_hide_bitch():
    pass
    # filtration1 = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9]]
    # compare_filtrations(filtration1,filtration2)
    # points = pcg.generate_n_points(5, 2)
    # alpha = alpha_complex_wrapper(points)
    # filtration = [elem[0] for elem in alpha.filtration]

    # snap = [[0],[1],[2],[3],[0,1],[0,2],[1,2],[1,3],[2,3],[0,1,2],[1,2,3]]
    # filtration2 = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9]]
    # filtration1 = [[0], [1], [2], [3], [4], [0, 4], [0, 2], [2, 4],  [3, 4], [1, 2], [0, 1],  [0, 3], [2, 3], [1, 3], [2, 3, 4], [0, 2, 4], [0, 3, 4], [0, 1, 2],[0, 1, 3]]
    # filtration0 = [[0],[1],[2],[3],[4],[1,4],[0,1],[0,2],[0,3],[0,4],[1,2]]
    # test_all_vertex_permutations(filtration)



