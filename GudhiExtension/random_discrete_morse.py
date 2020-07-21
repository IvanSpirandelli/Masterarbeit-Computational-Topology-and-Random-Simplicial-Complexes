import itertools as it
import numpy as np
import random

def random_discrete_morse(complex):

    critical_cells = []
    pairings = []

    cofacets_by_dim = {-1 : {(): set()}}
    max_dim = -1
    for elem in complex:
        elem = tuple(elem)
        if(len(elem) > 1):
            if(len(elem) > max_dim):
                max_dim = len(elem)
            if(not len(elem)-1 in cofacets_by_dim):
                cofacets_by_dim[len(elem)-1] = {(): set()}
            for comb in it.combinations(elem, len(elem)-1):
                try:
                    cofacets_by_dim[len(elem)-1][comb].add(elem)
                except:
                    cofacets_by_dim[len(elem)-1][comb] = {elem}

    del cofacets_by_dim[-1]
    for i in range(1,max_dim):
        del cofacets_by_dim[i][()]


    critical_cell_vector = [0 for i in range(0,max_dim)]

    max_dim_faces = []
    for elem in complex:
        if(len(elem) == max_dim):
            max_dim_faces.append(tuple(elem))

    codimone = max_dim-1

    while(codimone > 0):
        #print("CODIM", codimone)
        free_faces = []
        #print("CURRENT COFACETS:", cofacets_by_dim[codimone])
        for face in cofacets_by_dim[codimone]:

            if(len(cofacets_by_dim[codimone][face]) == 1):
                free_faces.append(face)

        #print("FREE FACES", free_faces)

        if(len(free_faces) == 0):
            critical_face = random.choice(max_dim_faces)
            critical_cells.append(list(critical_face))
            critical_cell_vector[max_dim-1] += 1
            #print("CRITICAL FACE", critical_face)
            complex.remove(list(critical_face))

            remove_cofacet_from_faces_of_dim(cofacets_by_dim, critical_face, codimone, max_dim_faces)
        else:
            to_be_paired = random.choice(free_faces)
            free_faces.remove(to_be_paired)
            cofacet = cofacets_by_dim[codimone][to_be_paired].pop()
            del cofacets_by_dim[codimone][to_be_paired]
            pairings.append([list(to_be_paired), list(cofacet)])

            #print("TO_BE_PAIRED", to_be_paired)
            #print("COFACET", cofacet)

            remove_cofacet_from_faces_of_dim(cofacets_by_dim, cofacet, codimone, max_dim_faces)
            if(codimone > 1): remove_cofacet_from_faces_of_dim(cofacets_by_dim, to_be_paired, codimone-1, max_dim_faces)

            complex.remove(list(cofacet))
            complex.remove(list(to_be_paired))

        if(len(max_dim_faces) == 0):
            for elem in complex:
                if (len(elem) == codimone):
                    max_dim_faces.append(tuple(elem))
            codimone-=1

        #print("MAXDIMFACES ", max_dim_faces)

    for simplex in complex:
        critical_cells.append(simplex)
        critical_cell_vector[len(simplex)-1] += 1
    return critical_cells, pairings, critical_cell_vector




def remove_cofacet_from_faces_of_dim(cofacets_by_dim, cofacet, codimone, max_dim_faces):
    entries_to_be_removed = []
    if cofacet in max_dim_faces: max_dim_faces.remove(cofacet)
    for face in cofacets_by_dim[codimone]:
        #print("FACE", face)
        if cofacet in cofacets_by_dim[codimone][face]:
            #print("HAS")
            cofacets_by_dim[codimone][face].remove(cofacet)
            if(len(cofacets_by_dim[codimone][face]) is 0): entries_to_be_removed.append(face)

    #print("COFACETS_BY_DIM_PRE_REMOVE: ", cofacets_by_dim)

    for face in entries_to_be_removed:
        del cofacets_by_dim[codimone][face]

    #print("COFACETS_BY_DIM_POST_REMOVE: ", cofacets_by_dim)
