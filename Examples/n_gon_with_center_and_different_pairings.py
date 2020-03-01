def get_expensive_pairings(n):
    v_e = [[[i],[i-1,i]] for i in range(n,0,-1)]
    e_t = [[[0,i],[0,i,i+1]] for i in range(2,n)]
    e_t.append([[0,n],[0,1,n]])
    return v_e + e_t

def get_cheap_pairings(n):
    v_e = [[[i],[i,i+1]] for i in range(n)]
    e_t = [[[1,n],[0,1,n]]]
    e_t += [[[0,i],[0,i-1,i]] for i in range(n,1,-1)]
    return  v_e + e_t

def get_n_gon_with_center_and_pairings(n):
    vertices = [[i] for i in range(n+1)]
    edges = [[0,i] for i in range(1,n+1)]
    edges += [[i,i+1] for i in range(1,n)]
    edges.append([1,n])

    triangles = [[0,i,i+1] for i in range(1,n)]
    triangles.append([0,1,n])

    simplices = vertices + edges + triangles
    expensive_pairings = get_expensive_pairings(n)

    return simplices

