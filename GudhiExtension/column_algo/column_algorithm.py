import numpy as np
import itertools as it

#The column algorithm for matrix reduction
def column_algorithm(filtered_boundary_matrix):
    #variable counting the additions in the algorithm
    algorithm_step_count = 0

    #number of columns
    n = filtered_boundary_matrix.shape[1]
    reduced_mat = np.copy(filtered_boundary_matrix)
    upper_tri = np.identity(n, dtype=int)

    for i in range(n):
        #boolean to check if we have to do another search among the smaler indexed columns
        column_reduction = True

        while column_reduction:
            #assume nothing changes
            column_reduction = False

            for k in range(i):
                low = lowest_index(reduced_mat[:, i])
                #Check if we find a smaller column with same lowest 1 rowindex
                if low != -1 and lowest_index(reduced_mat[:, k]) == low:
                    #Additions
                    reduced_mat[:, i] = (reduced_mat[:, i] + reduced_mat[:,k]) % 2
                    upper_tri[:, i] -= upper_tri[:, k]
                    #Do another step
                    column_reduction = True
                    algorithm_step_count += 1

    return algorithm_step_count

#same as above, only that this also returns the reduced matrix.
def column_algorithm_with_reduced_return(filtered_boundary_matrix):
    max_dim = sum(filtered_boundary_matrix[:,-1])-1

    algorithm_step_count = [0 for _ in range(max_dim+1)]
    print(algorithm_step_count)

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
                    upper_tri[:, i] -= upper_tri[:, k]
                    column_reduction = True
                    algorithm_step_count[dim] = algorithm_step_count[dim]+1

    return algorithm_step_count, reduced_mat


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
                dim = sum(reduced_mat[:,i])-1
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


def build_boundary_matrix_from_filtration(filtration):
    mat = np.zeros(shape=(len(filtration), len(filtration)), dtype=int)
    #maintaining which simplex is at which position
    index_set = {(): -1}

    for idx,simplex in enumerate(filtration):
        dim = len(simplex)-1
        index_set[tuple(simplex)] = idx
        if (dim > 0):
            for combi in it.combinations(simplex, dim):
                mat[index_set[combi], index_set[tuple(simplex)]] = 1

    #removing 0 rows/columns
    mat = mat[~np.all(mat == 0, axis=1)]
    idx = np.argwhere(np.all(mat[..., :] == 0, axis=0))
    mat = np.delete(mat, idx, axis=1)
    return mat