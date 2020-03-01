
def get_pawels_example():
    simplices = [[i] for i in range(15)] + [[i, i + 1] for i in (0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13)] + [[i, i + 5]
                                                                                                             for i in (
                                                                                                                 0, 1,
                                                                                                                 2, 3,
                                                                                                                 4, 5,
                                                                                                                 6, 7,
                                                                                                                 8,
                                                                                                                 9)] + [
                    [i, i + 6] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    simplices += [[i, i + 5, i + 6] for i in (0, 1, 2, 3, 5, 6, 7, 8)] + [[i, i + 1, i + 6] for i in
                                                                          (0, 1, 2, 3, 5, 6, 7, 8)]
    return simplices
def get_pawels_pairings_short():
    pairings_pawel_short = [[[i], [i, i + 5]] for i in range(5)] + [[[i], [i - 5, i]] for i in range(10, 15)] + [
        [[5], [5, 6]], [[6], [6, 7]], [[9], [8, 9]], [[8], [7, 8]]]
    # 14
    pairings_pawel_short += [[[i, i + 1], [i, i + 1, i + 6]] for i in range(4)] + [[[i, i + 6], [i, i + 5, i + 6]] for i
                                                                                   in range(4)]
    # 22
    pairings_pawel_short += [[[i, i + 1], [i - 5, i, i + 1]] for i in range(10, 14)] + [[[i, i + 6], [i, i + 1, i + 6]]
                                                                                        for i in range(5, 9)]
    # 30
    return pairings_pawel_short
def get_pawels_pairings_long():
    pairings_pawel_long = [[[i], [i, i + 1]] for i in range(4)] + [[[i], [i - 1, i]] for i in (14, 13, 12, 11)] + [
        [[4], [4, 9]]] + [[[9], [9, 14]]] + [[[10], [5, 10]]]
    pairings_pawel_long += [[[i, i + 5], [i, i + 5, i + 6]] for i in range(4)] + [[[i, i + 6], [i, i + 1, i + 6]] for i
                                                                                  in range(4)]  # 11 + 8
    pairings_pawel_long += [[[8, 9], [8, 9, 14]]]
    pairings_pawel_long += [[[i, i + 6], [i, i + 5, i + 6]] for i in (8, 7, 6, 5)] + [[[i, i + 5], [i, i + 5, i + 6]]
                                                                                      for i in (8, 7, 6)]
    return pairings_pawel_long
def get_long_edge_path_example():
    pairings = [[[i], [i, i + 1]] for i in (0,1,2,3,10,11,12,13)] + [[[i],[i-1,i]] for i in (9,8,7,6)] + [[[4],[4,9]],[[5],[5,10]]]
    pairings += [[[i,i+5],[i,i+5,i+6]] for i in (0,1,2,3,6,7,8)] + [[[i,i+6],[i,i+1,i+6]] for i in (0,1,2,3,5,6,7,8)]
    print(len(pairings))
    return pairings
def get_long_edge_path_example_more_critical():
    pairings = [[[i], [i, i + 1]] for i in (0,1,2,3,10,11,12,13)] + [[[i],[i-1,i]] for i in (9,8,7,6)] + [[[4],[4,9]],[[5],[5,10]]]
    pairings += [[[i,i+5],[i,i+5,i+6]] for i in (6,7,8)] + [[[i,i+6],[i,i+1,i+6]] for i in (5,6,7,8)]
    pairings += [[[i,i+6],[i,i+5,i+6]] for i in (0,1,2,3)] + [[[i,i+5],[i-1,i,i+5]] for i in (3,2,1)]
    print(len(pairings))
    return pairings
def get_long_edge_path_example_less_critical():
    pairings = [[[i], [i, i + 1]] for i in (0,1,2,3,10,11,12,13)] + [[[i],[i-1,i]] for i in (9,8,7,6)] + [[[4],[4,9]],[[5],[5,10]]]
    pairings += [[[i,i+5],[i,i+5,i+6]] for i in (0,1,2,3)] + [[[i,i+6],[i,i+1,i+6]] for i in (0,1,2,3)]
    pairings += [[[i,i+5],[i-1,i,i+5]] for i in (6,7,8,9)] + [[[i,i+6], [i, i + 5, i + 6]] for i in (8,7,6,5)]
    print(len(pairings))
    return pairings

def get_split_long_path_example():
    pairings = [[[i], [i, i + 1]] for i in (0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13)] + [[[14],[9,14]],[[4],[4,9]]]
    pairings += [[[i, i + 5], [i, i + 5, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    pairings += [[[i, i + 6], [i, i + 1, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    print(len(pairings))
    return  pairings
def get_split_long_path_inner_inverted_example():
    pairings = [[[i], [i, i + 1]] for i in (0, 1, 2, 3, 10, 11, 12, 13)]
    pairings += [[[i], [i-1, i]] for i in (9,8,7,6)]
    pairings += [[[i, i + 5], [i, i + 5, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    pairings += [[[i, i + 6], [i, i + 1, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    print(len(pairings))
    return  pairings
def get_split_long_path_outer_inverted_example():
    pairings = [[[i+1], [i, i + 1]] for i in (0, 1, 2, 3, 10, 11, 12, 13)]
    pairings += [[[i], [i, i+1]] for i in (8,7,6,5)]
    pairings += [[[i, i + 5], [i, i + 5, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    pairings += [[[i, i + 6], [i, i + 1, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    print(len(pairings))
    return  pairings
def get_split_long_path_all_inverted_example():
    pairings = [[[i+1], [i, i + 1]] for i in (0, 1, 2, 3, 10, 11, 12, 13)]
    pairings += [[[i], [i-1, i]] for i in (9,8,7,6)]
    pairings += [[[i, i + 5], [i, i + 5, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    pairings += [[[i, i + 6], [i, i + 1, i + 6]] for i in (0, 1, 2, 3, 5, 6, 7, 8)]
    print(len(pairings))
    return  pairings