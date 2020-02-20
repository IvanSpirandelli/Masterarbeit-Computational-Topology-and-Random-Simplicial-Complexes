import itertools as it

from MorseAndFiltrations.DMF_to_filtration import DMF_to_filtration


def filtration_to_DMF(filtration):
    critical = [0]*len(filtration)
    pairings = []
    for ind,simplex in enumerate(filtration):
        if(len(simplex) == 1):
            critical[ind] = 1
        elif not simplex_in_pairings(simplex, pairings):
            pair = find_max_face(simplex,filtration, pairings)
            if(pair == None):
                critical[ind] = 1
            else:
                pairings.append([list(pair),simplex])
    return pairings

def simplex_in_pairings(simplex, pairings):
    simplex = list(simplex)
    for pair in pairings:
        if(simplex in pair):
            return True
    return False

def find_max_face(simplex, filtration, pairings):
    combis = [comb for comb in it.combinations(simplex, len(simplex)-1)]
    combis.sort()
    curr_max_index = -1
    for combi in combis:
        tmp = filtration.index(list(combi))
        if tmp > curr_max_index:
            curr_max_index = tmp

    if(curr_max_index == -1 or simplex_in_pairings(filtration[curr_max_index], pairings)):
        return None

    return filtration[curr_max_index]
