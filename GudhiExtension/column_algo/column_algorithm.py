import numpy as np
import itertools as it

#same as above, only that this also returns the reduced matrix.
def column_algorithm(filtered_boundary_matrix, reduced_return = True):
    max_dim = sum(filtered_boundary_matrix[:,-1])-1

    algorithm_step_count = [0 for _ in range(max_dim+1)]

    n = filtered_boundary_matrix.shape[1]
    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)

    for i in range(n):
        column_reduction = True

        while column_reduction:
            column_reduction = False

            for k in range(i):
                low = lowest_index(reduced_mat[:, i])
                dim = sum(filtered_boundary_matrix[:,i])-1

                if low != -1 and lowest_index(reduced_mat[:, k]) == low:
                    reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:,k]) % 2
                    algorithm_step_count[0] = algorithm_step_count[0] + count_addition_of_ones(reduced_mat[:, i], reduced_mat[:,k])
                    upper_tri[:, i] -= upper_tri[:, k]
                    column_reduction = True
                    algorithm_step_count[dim] = algorithm_step_count[dim]+1

    if reduced_return:
        return algorithm_step_count, reduced_mat
    else:
        return algorithm_step_count

def count_addition_of_ones(a,b):
    count = 0;
    for i in range(len(a)):
        if a[i] == 1 or b[i] == 1:
            count +=1
    return count

def column_algorithm_iterator(filtered_boundary_matrix):
    max_dim = sum(filtered_boundary_matrix[:,-1])-1
    algorithm_step_count = [0 for _ in range(max_dim+1)]

    n = filtered_boundary_matrix.shape[1]
    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)

    for i in range(n):
        column_reduction = True

        while column_reduction:
            column_reduction = False

            for k in range(i):
                low = lowest_index(reduced_mat[:, i])
                dim = sum(filtered_boundary_matrix[:,i])-1
                if low != -1 and lowest_index(reduced_mat[:, k]) == low:
                    #print("We add: ", reduced_mat[:,k] )
                    #print("to: ", reduced_mat[:,i] )
                    reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:,k]) % 2
                    upper_tri[:, i] -= upper_tri[:, k]
                    column_reduction = True
                    algorithm_step_count[dim] = algorithm_step_count[dim]+1
                    yield algorithm_step_count, reduced_mat

# Returns the index of the lowest 1 in a given column. If there is no "1" in the column. "-1" is returned.
# TODO: Suboptimal implementation. Should be changed if we are to calculate massive amounts of data
def lowest_index(arr):
    #flipping the array, since we are looking for the last and not the first one.
    farr = np.flip(arr)
    #Now we can use where to locate the first entry in the flipped array.
    idx = np.where(farr == 1)
    if (len(idx[0]) == 0):
        return -1
    else:
        return len(arr) - idx[0][0] - 1


def build_boundary_matrix_from_filtration(filtration, clearing = True, crop_pre_clearing = True,  crop_post_clearing = False):
    mat = np.zeros(shape=(len(filtration), len(filtration)), dtype=int)
    #maintaining which simplex is at which position
    index_set = {(): -1}
    cleared_indices = set()

    for idx,simplex in enumerate(filtration):
        dim = len(simplex)-1
        index_set[tuple(simplex)] = idx
        if (dim > 0):
            max_index_of_facet = -1
            for combi in it.combinations(simplex, dim):
                mat[index_set[combi], index_set[tuple(simplex)]] = 1
                if(dim > 1 and clearing and index_set[combi] > max_index_of_facet):
                    max_index_of_facet = index_set[combi]
            if(clearing):
                mat[:,max_index_of_facet] = 0
                cleared_indices.add(max_index_of_facet)

    #removing 0-columns depending on specifications
    if(crop_pre_clearing):
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