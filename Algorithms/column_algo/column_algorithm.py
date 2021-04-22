import numpy as np
import itertools as it


# Standard reduction scheme to compute persistent homology. Expects a filtered_boundary_matrix.
# Returns a list of counted steps [total_count, columns_corresponding_to_edges, columns_corresponding_to_triangles, ...]
# Returns the lowest 1s in each column. Returns the reduced boundary matrix.
def column_algorithm(filtered_boundary_matrix):
    n = filtered_boundary_matrix.shape[1]

    max_dim = max([sum(filtered_boundary_matrix[:, i]) - 1for i in range(n)])
    algorithm_step_count = [0 for _ in range(max_dim + 1)]


    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)

    lows_reduced = [-1 for _ in range(n)]
    lowest_ones = [-1 for _ in range(n)]

    dims = [sum(filtered_boundary_matrix[:, i]) - 1 for i in range(n)]

    for i in range(n):
        lowest_ones[i] = lowest_index(reduced_mat[:, i])

    for i in range(n):
        low = lowest_ones[i]
        while low != -1 and lows_reduced[low] != -1:
            k = lows_reduced[low]
            reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:, k]) % 2
            algorithm_step_count[0] = algorithm_step_count[0] + count_addition_of_ones(reduced_mat[:, i],
                                                                                       reduced_mat[:, k])
            # algorithm_step_count[0] = algorithm_step_count[0] + sum(reduced_mat[:, k])
            upper_tri[:, i] -= upper_tri[:, k]

            algorithm_step_count[dims[i]] = algorithm_step_count[dims[i]] + 1

            low = lowest_ones[i] = lowest_index(reduced_mat[:, i])

        if lowest_ones[i] != -1:
            lows_reduced[lowest_ones[i]] = i

    return algorithm_step_count, lowest_ones, reduced_mat


# Twisted reduction scheme to compute persistent homology. Introduced by Michael Kerber and Chao Chen in
# "Persistent homology computation with a twist"
# Expects a filtered_boundary_matrix.
# Returns a list of counted steps [total_count, columns_corresponding_to_edges, columns_corresponding_to_triangles, ...]
# Returns the lowest 1s in each column. Returns the reduced boundary matrix.
def column_algorithm_with_a_twist(filtered_boundary_matrix):
    max_dim = sum(filtered_boundary_matrix[:, -1]) - 1

    algorithm_step_count = [0 for _ in range(max_dim + 1)]

    n = filtered_boundary_matrix.shape[1]
    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)
    lows_reduced = [-1 for _ in range(n)]

    lowest_ones = [-1 for _ in range(n)]

    dims = [sum(filtered_boundary_matrix[:, i]) - 1 for i in range(n)]

    for i in range(n):
        lowest_ones[i] = lowest_index(reduced_mat[:, i])

    for d in range(max_dim, 0, -1):
        for i in range(n):
            if dims[i] == d:
                low = lowest_ones[i]
                while low != -1 and lows_reduced[low] != -1:
                    k = lows_reduced[low]
                    reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:, k]) % 2
                    algorithm_step_count[0] = algorithm_step_count[0] + count_addition_of_ones(reduced_mat[:, i],
                                                                                               reduced_mat[:, k])
                    # algorithm_step_count[0] = algorithm_step_count[0] + sum(reduced_mat[:, k])
                    upper_tri[:, i] -= upper_tri[:, k]
                    algorithm_step_count[d] = algorithm_step_count[d] + 1
                    low = lowest_ones[i] = lowest_index(reduced_mat[:, i])

                if lowest_ones[i] != -1:
                    lows_reduced[lowest_ones[i]] = i
                    reduced_mat[:, lowest_ones[i]] = 0

    return algorithm_step_count, lowest_ones, reduced_mat


def count_addition_of_ones(a, b):
    count = 0
    for i in range(len(a)):
        if a[i] == 1 or b[i] == 1:
            count += 1
    return count

#The standard reduction scheme as an iterator. Each step represents one column addition.
#Algorithmic logic as above.
def column_algorithm_iterator(filtered_boundary_matrix):
    max_dim = sum(filtered_boundary_matrix[:, -1]) - 1

    algorithm_step_count = [0 for _ in range(max_dim + 1)]

    n = filtered_boundary_matrix.shape[1]
    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)

    lows_reduced = [-1 for _ in range(n)]
    lowest_ones = [-1 for _ in range(n)]

    dims = [sum(filtered_boundary_matrix[:, i]) - 1 for i in range(n)]
    for i in range(n):
        lowest_ones[i] = lowest_index(reduced_mat[:, i])

    for i in range(n):
        low = lowest_ones[i]
        while low != -1 and lows_reduced[low] != -1:
            k = lows_reduced[low]
            reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:, k]) % 2
            algorithm_step_count[0] = algorithm_step_count[0] + count_addition_of_ones(reduced_mat[:, i],
                                                                                       reduced_mat[:, k])
            # algorithm_step_count[0] = algorithm_step_count[0] + sum(reduced_mat[:, k])
            upper_tri[:, i] -= upper_tri[:, k]
            algorithm_step_count[dims[i]] = algorithm_step_count[dims[i]] + 1
            low = lowest_ones[i] = lowest_index(reduced_mat[:, i])
            yield algorithm_step_count, lowest_ones, reduced_mat



# Returns the index of the lowest 1 in a given column. If there is no "1" in the column. "-1" is returned.
def lowest_index(arr):
    # flipping the array, since we want the use where and are looking for the last and not the first one.
    farr = np.flip(arr)
    # Now we can use where to locate the first entry in the flipped array.
    idx = np.where(farr == 1)
    if (len(idx[0]) == 0):
        return -1
    else:
        return len(arr) - idx[0][0] - 1


# Constructs boundary matrix out of filtration. Can be cropped as desired.
def build_boundary_matrix_from_filtration(filtration, clearing=False, crop_pre_clearing=False,
                                          crop_post_clearing=False):
    mat = np.zeros(shape=(len(filtration), len(filtration)), dtype=int)
    # maintaining which simplex is at which position
    index_set = {(): -1}
    cleared_indices = set()

    for idx, simplex in enumerate(filtration):
        dim = len(simplex) - 1
        index_set[tuple(simplex)] = idx
        if (dim > 0):
            max_index_of_facet = -1
            for combi in it.combinations(simplex, dim):
                mat[index_set[combi], index_set[tuple(simplex)]] = 1
                if (dim > 1 and clearing and index_set[combi] > max_index_of_facet):
                    max_index_of_facet = index_set[combi]
            if (clearing and max_index_of_facet != -1):
                mat[:, max_index_of_facet] = 0
                cleared_indices.add(max_index_of_facet)

    # removing 0-columns depending on specifications
    if (crop_pre_clearing):
        mat = mat[~np.all(mat == 0, axis=1)]
        indices = np.argwhere(np.all(mat[..., :] == 0, axis=0))
        updated_indices = []
        if crop_post_clearing:
            updated_indices = indices
        else:
            for idx in indices:
                if not (idx[0] in cleared_indices):
                    updated_indices.append(idx)

        mat = np.delete(mat, updated_indices, axis=1)

    return mat


# Constructs uncropped boundary matrix out of filtrations. Passing a list of columns to clear sets
# the specified columns to zero.
def build_boundary_matrix_from_filtration_and_clear(filtration, cols_to_clear=None):
    if cols_to_clear is None:
        cols_to_clear = []
    mat = np.zeros(shape=(len(filtration), len(filtration)), dtype=int)
    # maintaining which simplex is at which position
    index_set = {(): -1}
    for idx, simplex in enumerate(filtration):
        dim = len(simplex) - 1
        index_set[tuple(simplex)] = idx
        if (dim > 0):
            if (len(cols_to_clear) > 0 and idx == cols_to_clear[0]):
                del cols_to_clear[0]
                continue
            for combi in it.combinations(simplex, dim):
                mat[index_set[combi], index_set[tuple(simplex)]] = 1

    return mat


# Computes the Betti numbers from a filtration of dimension dim and its lowest 1s
def betti_numbers(filtration, lowest_ones, dim):
    zk = [0] * (dim + 1)
    bk = [0] * (dim + 1)
    for i in range(len(filtration)):
        if (len(filtration[i]) == 1):
            zk[0] += 1
        else:
            if (lowest_ones[i] == -1):
                zk[len(filtration[i]) - 1] += 1
            else:
                bk[len(filtration[i]) - 1] += 1

    return [zk[i] - bk[i + 1] for i in range(0, dim)] + [zk[dim]]
