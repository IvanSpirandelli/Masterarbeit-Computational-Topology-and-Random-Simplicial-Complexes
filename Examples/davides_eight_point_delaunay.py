import itertools as it

def get_simplices():
    tetrahedrons = [
        [0,1,2,4],[0,1,3,4],[0,1,3,7],[0,1,2,6],[0,1,6,7],
        [0,2,4,7],[0,2,5,6],[0,2,5,7],[0,3,4,7],[0,5,6,7],
        [1,2,3,4],[1,2,3,5],[1,2,5,6],[1,3,5,6],[2,3,4,5],
        [2,4,5,7],[1,3,6,7]]

    vertices = set()
    edges = set()
    triangles = set()

    for tetra in tetrahedrons:
        for i in range(4):
            for combi in it.combinations(tetra, i):
                if i == 1:
                    if combi not in vertices:
                        vertices.add(combi)
                elif i == 2:
                    if combi not in edges:
                        edges.add(combi)
                elif i == 3:
                    if combi not in triangles:
                        triangles.add(combi)
    tetrahedrons.sort()
    vertices = [list(vertex) for vertex in vertices]
    vertices.sort()
    edges = [list(edge) for edge in edges]
    edges.sort()
    triangles = [list(triangle) for triangle in triangles]
    triangles.sort()

    return vertices + edges + triangles + tetrahedrons

def get_pairings_for_collapse_to_dunce_hat():
    pairs = [
        [[3, 5, 6],[1, 3, 5, 6]] , [[1, 5, 6],[1, 2, 5, 6]], [[3, 6, 7],[1, 3, 6, 7]], [[3, 4, 7],[0, 3, 4, 7]],
         [[2, 5, 6],[0, 2, 5, 6]], [[0, 3, 7],[0, 1, 3, 7]], [[0, 4, 7],[0, 2, 4, 7]], [[0, 2, 4],[0, 1, 2, 4]],
        [[0, 1, 2],[0, 1, 2, 6]] , [[0, 1, 6],[0, 1, 6, 7]], [[0, 6, 7],[0, 5, 6, 7]], [[0, 5, 7],[0, 2, 5, 7]],
        [[2, 5, 7],[2, 4, 5, 7]],  [[2, 4, 5], [2, 3, 4, 5]], [[2, 3, 5],[1, 2, 3, 5]], [[1, 2, 3],[1, 2, 3, 4]],
        [[1, 3, 4], [0, 1, 3, 4]], [[2, 3],[2, 3, 4]],  [[3, 6],[1, 3, 6]], [[3, 7],[1, 3, 7]]
    ]
    return pairs