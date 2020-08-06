import itertools as it
import random

#Constructs a random discrete Morse function as specified by Bruno Benedetti and Frank Lutz in
#"Random Discrete Morse Theory and a New Library of Triangulations".
#Note that the passed complex is altered during the algorithm! Unlike in the paper the algorithm
#expects all faces of the complex to be passed.
def random_discrete_morse(complex):

    critical_cells = []
    pairings = []

    #Create dictionary to maintain cofacets of each simplex in each dimension.
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

    #Cleanup
    del cofacets_by_dim[-1]
    for i in range(1,max_dim):
        del cofacets_by_dim[i][()]


    critical_cell_vector = [0 for i in range(0,max_dim)]

    max_dim_faces = []
    for elem in complex:
        if(len(elem) == max_dim):
            max_dim_faces.append(tuple(elem))

    codimone = max_dim-1

    #Find free faces and pick one to collapse.
    while(codimone > 0):
        free_faces = []
        for face in cofacets_by_dim[codimone]:
            if(len(cofacets_by_dim[codimone][face]) == 1):
                free_faces.append(face)

        if(len(free_faces) == 0):
            critical_face = random.choice(max_dim_faces)
            critical_cells.append(list(critical_face))
            critical_cell_vector[max_dim-1] += 1
            complex.remove(list(critical_face))

            remove_cofacet_from_faces_of_dim(cofacets_by_dim, critical_face, codimone, max_dim_faces)
        else:
            to_be_paired = random.choice(free_faces)
            free_faces.remove(to_be_paired)
            cofacet = cofacets_by_dim[codimone][to_be_paired].pop()
            del cofacets_by_dim[codimone][to_be_paired]
            pairings.append([list(to_be_paired), list(cofacet)])

            remove_cofacet_from_faces_of_dim(cofacets_by_dim, cofacet, codimone, max_dim_faces)
            if(codimone > 1): remove_cofacet_from_faces_of_dim(cofacets_by_dim, to_be_paired, codimone-1, max_dim_faces)

            complex.remove(list(cofacet))
            complex.remove(list(to_be_paired))

        if(len(max_dim_faces) == 0):
            for elem in complex:
                if (len(elem) == codimone):
                    max_dim_faces.append(tuple(elem))
            codimone-=1

    #Handle remaining elements in complex
    for simplex in complex:
        critical_cells.append(simplex)
        critical_cell_vector[len(simplex)-1] += 1
    return critical_cells, pairings, critical_cell_vector

#Adjust cofacet dictionary after removing free face
def remove_cofacet_from_faces_of_dim(cofacets_by_dim, cofacet, codimone, max_dim_faces):
    entries_to_be_removed = []
    if cofacet in max_dim_faces: max_dim_faces.remove(cofacet)
    for face in cofacets_by_dim[codimone]:
        if cofacet in cofacets_by_dim[codimone][face]:
            cofacets_by_dim[codimone][face].remove(cofacet)
            if(len(cofacets_by_dim[codimone][face]) is 0): entries_to_be_removed.append(face)

    for face in entries_to_be_removed:
        del cofacets_by_dim[codimone][face]
