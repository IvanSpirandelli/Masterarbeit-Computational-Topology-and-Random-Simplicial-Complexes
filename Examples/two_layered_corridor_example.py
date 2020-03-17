def get_two_layered_corridor_example(n):
    if(n%2 == 1):
        n-=1
        raise Warning("Only even n allowed. n decreased by one!")
    if(n<4):
        n = 4
        raise Warning("Minimal n is 4. n increased to 4.")

    vertices = [[i] for i in range(n)]
    edges = [[0,1],[1,3],[0,2],[1,2]]
    for i in range(2,n-2,2):
        edges.append([i,i+1])
        edges.append([i,i+2])
        edges.append([i+1,i+3])
        edges.append([i+1,i+2])
    edges.append([n-2,n-1])

    return vertices+edges

