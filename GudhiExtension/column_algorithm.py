import numpy as np
import itertools as it


def column_algorithm(filtered_boundary_matrix):
    algorithm_step_count = 0

    n = filtered_boundary_matrix.shape[1]
    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)

    for i in range(n):
        column_reduction = True

        while column_reduction:
            column_reduction = False

            for k in range(i):
                low = lowest_index(reduced_mat[:, i])
                if low != -1 and lowest_index(reduced_mat[:, k]) == low:
                    #print("We add: ", reduced_mat[:,k] )
                    #print("to: ", reduced_mat[:,i] )
                    reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:,k]) % 2
                    upper_tri[:, i] -= upper_tri[:, k]
                    column_reduction = True
                    algorithm_step_count += 1

    return algorithm_step_count


# Returns the index of the lowest 1 in a given column. If there is no "1" in the column. "-1" is returned.
def lowest_index(arr):
    farr = np.flip(arr)
    idx = np.where(farr == 1)
    if (len(idx[0]) == 0):
        return -1
    else:
        return len(arr) - idx[0][0] - 1


def build_boundary_matrix_from_filtration(filtration):
    mat = np.zeros(shape=(len(filtration), len(filtration)), dtype=int)
    index_set = {(): -1}
    counter = 0
    for simplex in filtration:
        dim = len(simplex)-1
        index_set[tuple(simplex)] = counter
        counter += 1
        if (dim > 0):
            for combi in it.combinations(simplex, dim):
                mat[index_set[combi], index_set[tuple(simplex)]] = 1

    mat = mat[~np.all(mat == 0, axis=1)]
    idx = np.argwhere(np.all(mat[..., :] == 0, axis=0))
    mat = np.delete(mat, idx, axis=1)
    return mat