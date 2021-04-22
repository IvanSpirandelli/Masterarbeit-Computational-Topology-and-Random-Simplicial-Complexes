from operator import itemgetter

#This method constructs a filtration for which the standard persistent
#homology algorithm achieves its worst case bound. Pass @param n for vertices of base n-gon.
def get_n_gon_with_center_and_fins_filtration(n):
    if(n<3):
        raise Warning("Passed n too low. Setting n = 3.")
        n = 3
    base_vertices = [[i] for i in range(n + 1)]
    fin_vertices = [[i + n] for i in range(1, n + 1)]

    fin_edges = [[0, i + n] for i in range(1, n + 1)]
    fin_edges += [[i, i + n] for i in range(1, n + 1)]

    bounding_edges = [[i, i + 1] for i in range(1, n)]
    bounding_edges.append([1, n])

    base_edges = [[0, i] for i in range(1, n + 1)]

    base_triangles = [[0, i, i + 1] for i in range(1, n)]
    base_triangles.append([0, 1, n])
    fin_triangles = [[0, i, i + n] for i in range(1, n + 1)]

    return base_vertices + fin_vertices + bounding_edges + fin_edges + base_edges + base_triangles + fin_triangles

def get_3d_extension_of_ngon(n):
    if (n < 3):
        raise Warning("Passed n too low. Setting n = 3.")
        n = 3

    base_vertices = [[i] for i in range(n + 1)]
    fin_vertices = [[i + n] for i in range(1, n + 1)]

    fin_edges = [[0, i + n] for i in range(1, n + 1)]
    fin_edges += [[i, i + n] for i in range(1, n + 1)]

    bounding_edges = [[i, i + 1] for i in range(1, n)]
    bounding_edges.append([1, n])

    base_edges = [[0, i] for i in range(1, n + 1)]

    base_triangles = [[0, i, i + 1] for i in range(1, n)]
    base_triangles.append([0, 1, n])

    fin_triangles = [[0, i, i + n] for i in range(1, n + 1)]

    top_vertex = [[2*n+1]]
    rising_edge = [[0,2*n+1]]
    top_edges = [[i + n, 2*n+1] for i in range(1, n + 1)]
    top_bounding_edges = [[n + i, n + i + 1] for i in range(1, n)]
    top_bounding_edges += [[1+n, 2*n]]

    side_cover_edges = [[i, i+n+1] for i in range(1,n)]
    side_cover_edges += [[1,2*n]]

    upper_fin_triangles = [[0, i + n, 2*n+1] for i in range(1, n + 1)]
    top_triangles = [[i + n, i + n + 1, 2 * n+1] for i in range(1, n)]
    top_triangles += [[1+n, 2*n, 2*n+1]]


    side_covers_lower = [[i,i+1,i+n+1] for i in range(1,n)]
    side_covers_lower += [[1,n,2*n]]

    side_covers_upper = [[i,i+n,i+n+1] for i in range(1,n)]
    side_covers_upper += [[1, 1+n, 2*n]]

    base_tetrahedra = [[0, i, i + 1, i + n] for i in range(1, n)]
    base_tetrahedra.append([0, 1, n, n + 1])

    return base_vertices + fin_vertices + bounding_edges + fin_edges + base_edges + base_triangles + fin_triangles + \
           top_vertex + rising_edge + top_edges + top_bounding_edges + side_cover_edges + upper_fin_triangles + \
           top_triangles + side_covers_lower + side_covers_upper + base_tetrahedra




#This method constructs a filtration, specified by Dimitriy Morozov in the paper:
#"Persistence Algorithm Takes Cubic Time in the Worst Case",
#for which the standard persistent homology algorithm achieves its worst case bound.
#See paper for sepcification of @param n. Pass (n,True) to get construction printed to console.
def build_morozov_example(n, console_prints = False):
    if(n<3):
        raise Warning("Passed n too low. Setting n = 5.")
        n = 5

    vertices = [[0],[1],[2],[3]]
    base_vertices = []

    for i in range(n-4):
        base_vertices.append([i+4])

    for i in range(len(base_vertices)):
        vertices.append(base_vertices[i])


    triangles_with_two = []

    #add edges, that just kill components:
    fluff_edges = [[0,2], [1,2], [2,3]]
    for elem in base_vertices:
        fluff_edges.append([2,elem[0]])

    first_fin_left = vertices[-1][0]+1
    first_fin_right = vertices[-1][0]+2
    vertices.append([first_fin_left])
    vertices.append([first_fin_right])

    fin_edges = [[3,first_fin_right],[0,first_fin_left]]
    base_edges = [[1,3],[0,3]]
    fin_close_edges = [[3,first_fin_left],[1,first_fin_right]]
    #print("FFL: ", first_fin_left, "FFR: ", first_fin_right)
    base_triangles = [[0,1,3]]
    fin_triangles = [[0,3,first_fin_left],[1,3,first_fin_right]]

    to_split = [[0,3],[1,3]]

    for i in range(len(base_vertices)):
        add_base_triangle_and_implying(to_split, base_vertices[i][0], vertices, base_triangles, base_edges, fin_triangles, fin_edges, fin_close_edges, base_vertices[i][0]%2 == 0)

    for remaining in to_split:
        triangles_with_two.append([2,remaining[0],remaining[1]])

    base_edges.insert(0,[0,1])

    return output(vertices, fluff_edges, fin_close_edges, fin_edges, base_edges, base_triangles, triangles_with_two, fin_triangles, console_prints)


def add_fin_and_implying(a, b, top, fin_triangles, fin_edges, fin_close_edges, even_step):
    #fin edges are sorted properly in output!
    fin_triangles.append([a,b,top])
    fin_edges.insert(0,[b,top])
    fin_close_edges.append([a,top])

def add_base_triangle_and_implying(to_split,c, vertices, base_triangles, base_edges, fin_triangles, fin_edges, fin_close_edges, even_step):
        a = to_split[0][0]
        b = to_split[0][1]
        del to_split[0]

        base_triangles.append([a,b,c])

        if even_step:
            to_split.append([a, c])
            base_edges.insert(0,[a, c])
            newvert = vertices[-1][0] + 1
            vertices.append([newvert])
            add_fin_and_implying(a, c, newvert, fin_triangles, fin_edges, fin_close_edges, even_step)

            to_split.append([b, c])
            base_edges.insert(0,[b, c])
            newvert += 2
            vertices.append([newvert])
            add_fin_and_implying(b, c, newvert, fin_triangles, fin_edges, fin_close_edges, even_step)

        else:
            to_split.insert(len(to_split)-1,[a,c])
            base_edges.insert(1,[a, c])
            newvert = vertices[-2][0] + 1
            vertices.append([newvert])
            add_fin_and_implying(a, c, newvert, fin_triangles, fin_edges, fin_close_edges, even_step)

            to_split.append([b,c])
            base_edges.insert(0,[b, c])
            newvert += 2
            vertices.append([newvert])
            add_fin_and_implying(b, c, newvert, fin_triangles, fin_edges, fin_close_edges, even_step)


def output(vertices, fluff_edges, component_destroying_edges, fin_edges, base_edges, base_triangles, triangles_with_two, fin_triangles, prints):
    if prints:
        print("Vertices :")
        print(vertices)
        print("Other Edges: ")
    for edge in fluff_edges:
        edge.sort()
        if prints: print(edge)
    fluff_edges.sort()

    for edge in component_destroying_edges:
        edge.sort()
        if prints: print(edge)
    component_destroying_edges.sort()

    if prints: print("Fin Edges: ")
    for edge in fin_edges:
        edge.sort()
    fin_edges.sort(key=itemgetter(1))
    fin_edges.reverse()
    if prints:
        for edge in fin_edges:
            print(edge)

    if prints: print("Base Edges: ")
    for edge in base_edges:
        edge.sort()
        if prints: print(edge)

    if prints: print("Base Triangle: ")
    for tri in base_triangles:
        tri.sort()
        if prints: print(tri)

    if prints: print("Triangles with 2: ")
    for tri in triangles_with_two:
        tri.sort()
        if prints: print(tri)
    triangles_with_two.sort(key=itemgetter(2))
    triangles_with_two.sort(key=itemgetter(0))

    if prints: print("Fin Triangles: ")
    for tri in fin_triangles:
        tri.sort()
    fin_triangles.sort(key=itemgetter(2))
    if prints:
        for tri in fin_triangles:
            print(tri)

    return vertices + component_destroying_edges + fluff_edges + fin_edges + base_edges + base_triangles + triangles_with_two + fin_triangles


