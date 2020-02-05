from MorseAndFiltrations.gradient_field import gradient_field
from MorseAndFiltrations.toposort import toposort_flatten

simplices = [[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]
pairings = [[[1,2],[0,1,2]],[[1],[0,1]],[[2],[0,2]]]

gf = gradient_field(simplices, pairings)
topsort = toposort_flatten(gf.hasse)
dim = len(max(topsort, key = len))
out = []
for i in range(1, dim+1):
    for elem in topsort:
        if len(elem) == i:
            out.append(list(elem))

print(out)
