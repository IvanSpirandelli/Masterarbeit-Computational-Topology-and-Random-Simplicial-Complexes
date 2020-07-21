def get_3_layer_pyramid():
    vertices = [[i] for i in range(6)]
    edges = []
    edges.append([0,1])
    edges.append([0,3])
    edges.append([1,3])
    edges.append([1,2])
    edges.append([1,4])
    edges.append([2,4])
    edges.append([3,4])
    edges.append([3,5])
    edges.append([4,5])
    return vertices + edges

def get_perfect_paring():
    pairings = []
    pairings.append([[1],[0,1]])
    pairings.append([[3],[0,3]])
    pairings.append([[2],[1,2]])
    pairings.append([[4],[3,4]])
    pairings.append([[5],[3,5]])
    return pairings
