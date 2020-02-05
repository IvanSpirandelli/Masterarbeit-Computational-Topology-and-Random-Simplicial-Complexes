import GudhiExtension.filtration_manipulation as fm
import GudhiExtension.column_algo.column_algo_outs as cao
import GudhiExtension.column_algo.column_algorithm as ca

from MorseAndFiltrations.gradient_field import gradient_field
from MorseAndFiltrations.toposort import toposort_flatten


def examples():
    pass
    simplices = [[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]
    pairings_a = [[[1,2],[0,1,2]],[[1],[0,1]],[[2],[0,2]]]
    pairings_b = [[[1,2],[0,1,2]],[[1],[0,1]],[[0],[0,2]]]

    simplices = [[i] for i in range(15)] + [[i,i+1] for i in (0,1,2,3,5,6,7,8,10,11,12,13)] + [[i,i+5] for i in (0,1,2,3,4,5,6,7,8,9)] + [[i,i+6] for i in (0,1,2,3,5,6,7,8)]
    simplices += [[i,i+5,i+6] for i in (0,1,2,3,5,6,7,8)] + [[i,i+1,i+6] for i in (0,1,2,3,5,6,7,8)]
    print(simplices)
    pairings_a = [[[i],[i,i+1]] for i in range(4)] + [[[i],[i-1,i]] for i in (14,13,12,11)] + [[[4],[4,9]]] + [[[9],[9,14]]] + [[[10],[5,10]]]
    pairings_a += [[[i,i+5], [i,i+5,i+6]] for i in range(4)] + [[[i,i+6], [i,i+1,i+6]] for i in range(4)] # 11 + 8
    pairings_a += [[[8,9],[8,9,14]]]
    pairings_a += [[[i,i+6], [i,i+5,i+6]] for i in (8,7,6,5)] + [[[i,i+5], [i,i+5,i+6]] for i in (8,7,6)]

    pairings_b = [[[i],[i,i+5]] for i in range(5)] + [[[i],[i-5,i]] for i in range(10,15)] + [[[5],[5,6]], [[6],[6,7]], [[9],[8,9]], [[8], [7,8]]]
    #14
    pairings_b += [[[i,i+1],[i,i+1,i+6]] for i in range(4)] + [[[i,i+6],[i,i+5,i+6]] for i in range(4)]
    #22
    pairings_b += [[[i,i+1],[i-5,i,i+1]] for i in range(10,14)] + [[[i,i+6],[i,i+1,i+6]] for i in range(5,9)]
    #30

simplices = [[0],[1],[2],[3],[0,1],[0,3],[1,2],[1,3],[2,3],[0,1,3],[1,2,3]]
pairings_ = []


gf = gradient_field(simplices, pairings_)
topsort = toposort_flatten(gf.hasse)
dim = len(max(topsort, key = len))
filtration = []
for i in range(1, dim+1):
    for elem in topsort:
        if len(elem) == i:
            filtration.append(list(elem))


mat = ca.build_boundary_matrix_from_filtration(filtration)
steps, red = ca.column_algorithm_with_reduced_return(mat)

print("Steps: " , steps)

max_len = max([len(i) for i in filtration])

xticklabels = [elem for elem in filtration if len(elem) > 1]
yticklabels = [elem for elem in filtration if len(elem) < max_len]

cao.mat_visualization(mat,xticklabels,yticklabels)
cao.mat_visualization(red,xticklabels,yticklabels)
