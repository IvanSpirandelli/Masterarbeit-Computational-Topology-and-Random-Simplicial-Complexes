import itertools
from copy import deepcopy

import numpy as np

import GudhiExtension.column_algorithm as ca
import GudhiExtension.point_cloud_generator as pcg
from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper

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
        points = pcg.generate_n_points(5, 3)
        alpha = alpha_complex_wrapper(points)
        filtration =[elem[0] for elem in alpha.filtration]
        test_all_vertex_permutations(filtration)
    else:
        for num,line in enumerate(out,start=0):
            if(line[0] == min_steps and line[1] != min_weight):
                print('#############################')
                print("Permutation: ", kept_perms[num])
                print('#############################')
                print(line)
                print('#############################')
                print(mats[num])
                print('#############################')


#filtration = [[0],[1],[2],[3],[0,1],[0,2],[1,2],[1,3],[2,3],[0,1,2]]
points = pcg.generate_n_points(5, 2)
alpha = alpha_complex_wrapper(points)
filtration = [elem[0] for elem in alpha.filtration]
test_all_vertex_permutations(filtration)


#filtrations that does NOT fullfill what I hoped for!
#filtration = [[0],[1],[2],[3],[4],[5],[3, 5], [0, 1], [1, 3], [1, 5], [1, 3, 5], [2, 5], [1, 2], [1, 2, 5], [2, 4], [0, 3], [0, 1, 3], [4, 5], [2, 4, 5], [0, 2], [0, 1, 2], [3, 4], [3, 4, 5]]
