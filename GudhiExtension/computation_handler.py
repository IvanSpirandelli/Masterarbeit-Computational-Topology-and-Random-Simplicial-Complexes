import random
import numpy as np
import itertools as it

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper


class computation_handler:

    def __init__(self, compute_persistance = False):
        self.points = [[0,0],[0,1],[1,1]]
        self.alpha = alpha_complex_wrapper(self.points, compute_persistance)

    def generate_n_gridpoints_of_dim_with_dilation(self, n, dim, dilation):
        points = set()
        while (len(points) < n):
            point = (random.randrange(0, dilation+1, 1) for i in range(dim))
            points.add(point)

        self.points=[list(elem) for elem in points]
        self.compute_alpha()
        #print("Genereated points: ")
        #print(self.points)
        #print('__________________________________________________________')

    def generate_n_points(self, n, dim):
        points = set()
        while (len(points) < n):
            point = (random.random() for i in range(dim))
            points.add(point)

        self.points = [list(elem) for elem in points]
        self.compute_alpha()
        #print("Genereated points: ")
        #print(self.points)
        #print('__________________________________________________________')

    def set_points(self, points):
        self.points = points
        self.compute_alpha()

    def compute_alpha(self):
        self.alpha = alpha_complex_wrapper(self.points)
        #print("Generated alpha complex")

    def column_algorithm(self, filtered_boundary_matrix):

        algorithm_step_count = 0

        n = filtered_boundary_matrix.shape[0]
        reduced_mat = np.copy(filtered_boundary_matrix)
        upper_tri = np.identity(n, dtype=int)

        for i in range(n):
            column_reduction = True
            while column_reduction:
                column_reduction = False

                for k in range(i):
                    low = self.lowest_index(reduced_mat[:, i])
                    if low != -1 and self.lowest_index(filtered_boundary_matrix[:,k]) == low:
                        reduced_mat[:,i] = (reduced_mat[:,k] - reduced_mat[:,i]) % 2
                        upper_tri[:,i] -= upper_tri[:,k]
                        column_reduction = True
                        algorithm_step_count += 1

        return algorithm_step_count

    #Returns the index of the lowest 1 in a given column. Returns the index of the LAST row
    def lowest_index(self, arr):
        farr = np.flip(arr)
        idx = np.where(farr == 1)
        if(len(idx[0]) == 0):
            return -1
        else:
            return len(arr) - idx[0][0] - 1

    def build_boundary_matrix_from_filtration(self, filtration):
        mat = np.zeros(shape=(len(filtration), len(filtration)), dtype=int)
        index_set = {(): -1}
        counter = 0
        for simplex in filtration:
            dim = len(simplex)
            index_set[tuple(simplex)] = counter
            counter += 1
            if (dim > 0):
                for i in range(dim - 1, 0, -1):
                    for combi in it.combinations(simplex, i):
                        mat[index_set[combi], index_set[tuple(simplex)]] = 1

        return mat