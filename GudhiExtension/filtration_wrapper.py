import random
from copy import deepcopy
import itertools


class filtration_wrapper:
    def __init__(self, filtration):
        self.filtration = filtration

    def perturb_index_with_random_possible_of_same_dimension(self, index):
        current = self.filtration[index]
        possible_indices = []
        for num, simplex in enumerate(self.filtration, start=0):
            if(simplex != current and len(simplex) == len(current)):
                possible_indices.append(num)

        switchdex = possible_indices[random.randrange(len(possible_indices))+1]
        self.switch_simplices(index,switchdex)


    def switch_simplices(self, index1, index2):
        tmp = self.filtration[index1]
        self.filtration[index1] = self.filtration[index2]
        self.filtration[index2] = tmp

    def all_vertex_permutations(self, num_of_vertices = -1):
        if(num_of_vertices == -1):
            num_of_vertices = 0
            for simplex in self.filtration:
                if(len(simplex) == 1):
                    num_of_vertices += 1

        base = [i for i in range(num_of_vertices)]
        perms = itertools.permutations(base)

        for perm in perms:
            counter = 0

            for simplex in self.filtration:
                if(len(simplex) == 0):
                    simplex = perm[counter]
                    counter += 1
                    if(counter == len(perm)):
                        continue