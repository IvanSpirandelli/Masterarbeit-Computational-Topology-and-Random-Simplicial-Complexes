def create_overlapping_wedge(n):
    if(n < 3):
        raise Exception("n is to small")
    if(n%2 == 0):
        raise Exception("n has to be odd")

    vertices = [[i] for i in range(n+1)]
    edges = [[0,i] for i in range(1,n+1)]
    edges += [[i,i+1] for i in range(1,n)]
    edges += [[i,i+2] for i in range(1,n-1,2)]

    triangles = [[i,i+1,i+2] for i in range(1,n-1,2)]
    triangles += [[0,i,i+1] for i in range(2,n,2)]

    return vertices + edges + triangles

def create_pairing_with_2_critical_cells_per_wedge(n):
    v_e = [[[i],[0,i]] for i in range(1,n+1)]
    e_t = [[[i,i+1],[i,i+1,i+2]] for i in range(1,n-1,2)]
    e_t = [[[i,i+1],[0,i,i+1]] for i in range(2,n,2)]

    return v_e + e_t
