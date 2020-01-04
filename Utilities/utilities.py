import itertools as it

def get_all_sublists(in_list):
    out = []
    for i in range(len(in_list)):
            for combi in it.combinations(in_list, i):
                out.append(combi)

    return out

def sort_list_by_element_list_length(in_list):
    return in_list.sort(key=len)