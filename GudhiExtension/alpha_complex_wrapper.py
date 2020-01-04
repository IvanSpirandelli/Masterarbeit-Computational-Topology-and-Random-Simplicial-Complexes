import gudhi
import numpy as np
import itertools as it

class alpha_complex_wrapper():
    def __init__(self, points = [[0,0],[0,1],[1,1]], compute_persistance_on_init = True):
        self.points = points
        self.complex = gudhi.AlphaComplex(self.points)
        self.simplex_tree = self.complex.create_simplex_tree()
        self.computed_persistence = compute_persistance_on_init;

        if(self.computed_persistence):
            self.persistence = self.simplex_tree.persistence()
        else:
            self.persistence = []

        self.filtration = self.simplex_tree.get_filtration()

    def get_boundary_matrix(self):
        mat = np.zeros(shape=(len(self.filtration),len(self.filtration)), dtype=int)
        index_set = {() : -1}
        counter = 0
        for elem in self.filtration:
            simplex = elem[0]
            dim = len(simplex)
            index_set[tuple(simplex)] = counter
            counter+=1
            if(dim > 0):
                for i in range(dim-1,0,-1):
                    for combi in it.combinations(simplex, i):
                        mat[index_set[combi], index_set[tuple(simplex)]] = 1


        return mat

    def get_all_filtration_steps(self):
        simplices = [[]]

        index = 0;
        dist_at_index = 0.0
        #filtration step 0 contains the set of points
        filtration_step = 0
        # Each next list in simplices contains the simplices added at distance 'dist_at_index'
        last_dist = dist_at_index
        while index != len(self.filtration):
            dist_at_index = self.filtration[index][1]
            simplices[filtration_step].append(self.filtration[index][0])
            if (dist_at_index == last_dist):
                index += 1
            else:
                index += 1
                last_dist = dist_at_index
                filtration_step += 1
                simplices.append([])

        # Cutting off last empty list and returning
        return simplices[:-1]

    def get_all_connected_filtration_steps(self):

        self.compute_persistence()

        #The first list of simplices yields the first connected step of the filtration.
        simplices = [[]]

        index = 0;
        dist_at_index = 0.0

        #filtration step 0 contains the first connected component of the alpha complex
        filtration_step = 0

        #Iterating until we got a connected component
        while(self.simplex_tree.persistent_betti_numbers(dist_at_index,dist_at_index)[0] != 1):
            dist_at_index = self.filtration[index][1]
            simplices[0].append(self.filtration[index][0])
            index += 1;

        simplices.append([])

        #Each next list in simplices contains the simplices added at distance 'dist_at_index'
        last_dist = dist_at_index
        while index != len(self.filtration):

            dist_at_index = self.filtration[index][1]

            if(dist_at_index != last_dist):
                last_dist = dist_at_index
                filtration_step +=1
                simplices.append([])

            simplices[filtration_step].append(self.filtration[index][0])
            index+=1
        #Cutting off last empty list and returning
        return simplices[:-1]

    def compute_persistence(self):
        if not self.computed_persistence:
            self.persistence = self.simplex_tree.persistence()
            self.computed_persistence = True

