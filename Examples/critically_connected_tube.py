def get_c_c_t(n):
    vertices = [[i] for i in range((2 * n) + 1)]
    edges = [[i, i + 1] for i in range(n)]
    edges += [[0, n + 1]]
    edges += [[i, i + 1] for i in range(n + 1, 2 * n)]
    edges += [[i, i + n] for i in range(1,n+1)]
    return vertices + edges


def get_pairing(n):
    v_e = [[[i + 1], [i, i + 1]] for i in range(n)]
    v_e += [[[n + 1], [0, n + 1]]]
    v_e += [[[i + 1], [i, i + 1]] for i in range(n + 1, 2 * n)]

    return v_e

