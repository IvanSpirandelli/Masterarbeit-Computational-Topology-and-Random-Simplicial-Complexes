import math
import random

import numpy as np


def switch_indexed_simplex_with_random_possible_of_same_dimension(filtration, index):
    current = filtration[index]
    possible_indices = []
    for num, simplex in enumerate(filtration, start=0):
        if (simplex != current and len(simplex) == len(current)):
            possible_indices.append(num)

    switchdex = possible_indices[random.randrange(len(possible_indices)) + 1]
    switch_simplices(index, switchdex)


def switch_simplices(filtration, index1, index2):
    tmp = filtration[index1]
    filtration[index1] = filtration[index2]
    filtration[index2] = tmp

def get_random_permutation_of_indexed_simplices(filtration, indices):
    permuted_simplices = np.random.permutation([filtration[index] for index in indices])
    for i,index in enumerate(indices):
        filtration[index] = list(permuted_simplices[i])

def get_random_permutation_of_simplices_of_dimension_d(filtration, d):
    indices = []
    for i,elem in enumerate(filtration):
        if len(elem) == d+1:
            indices.append(i)
    get_random_permutation_of_indexed_simplices(filtration,indices)