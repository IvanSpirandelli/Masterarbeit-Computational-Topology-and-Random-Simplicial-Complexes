import math
import GudhiExtension.column_algo.column_algorithm as ca
import GudhiExtension.column_algo.column_algo_outs as cao
import matplotlib.pyplot as plt
from operator import itemgetter

def build_morozov_example(n):
    if(n<3):
        raise Warning("Increased n to 3, which is the minimal example to see the desired behaviour")
        n = 3

    v = math.ceil((n-1)/2)

    #print("n: ", n, "v: ", v)
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

    print(base_vertices)

    for i in range(len(base_vertices)):
        #print(to_split)
        add_base_triangle_and_implying(to_split, base_vertices[i][0], vertices, base_triangles, base_edges, fin_triangles, fin_edges, fin_close_edges, base_vertices[i][0]%2 == 0)

    for remaining in to_split:
        triangles_with_two.append([2,remaining[0],remaining[1]])

    base_edges.insert(0,[0,1])

    return output(vertices, fluff_edges, fin_close_edges, fin_edges, base_edges, base_triangles, triangles_with_two, fin_triangles)


def add_fin_and_implying(a, b, top, fin_triangles, fin_edges, fin_close_edges, even_step):
    #fin edges are sorted properly in output!
    fin_triangles.append([a,b,top])
    fin_edges.insert(0,[b,top])
    fin_close_edges.append([a,top])

def add_base_triangle_and_implying(to_split,c, vertices, base_triangles, base_edges, fin_triangles, fin_edges, fin_close_edges, even_step):
        #print("SPLITLIST: ", to_split)
        a = to_split[0][0]
        b = to_split[0][1]
        del to_split[0]
        #print("VERTEX: ", c)

        #print("TO_SPLIT:")
        #print(a,b)
        #print("__________")
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

def output(vertices, fluff_edges, component_destroying_edges, fin_edges, base_edges, base_triangles, triangles_with_two, fin_triangles):
    prints = False

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

    #print("NUMBER OF TRIANGLES: ", len(triangles_with_two)+len(fin_triangles)+len(base_triangles))

    return vertices + component_destroying_edges + fluff_edges + fin_edges + base_edges + base_triangles + triangles_with_two + fin_triangles

def show_matrices_for_filtration(filtration):
    mat = ca.build_boundary_matrix_from_filtration(filtration, clearing=True)
    max_len = max([len(i) for i in filtration])

    xticklabels = [elem for elem in filtration if len(elem) > 2]
    yticklabels = [elem for elem in filtration if len(elem) < max_len and len(elem)>1]
    yticklabels.reverse()

    xrange = (len(mat[0]) - len(xticklabels), len(mat[0]))
    yrange = (len(mat) - len(yticklabels), len(mat))

    cao.mat_visualization(mat, xticklabels, yticklabels, xrange, yrange, index=0)

    steps, red = ca.column_algorithm_with_reduced_return(mat)
    for idx,it in enumerate(ca.column_algorithm_iterator(mat)):
        steps, red = it
        cao.mat_visualization(red, xticklabels, yticklabels, xrange, yrange, index= idx)
    return steps


# x = []
# y = []
# for i in range(5,30):
#     print(i,"/10")
#     filtration = build_morozov_example(i)
#     x.append(i)
#     mat = ca.build_boundary_matrix_from_filtration(filtration, False)
#     steps, red = ca.column_algorithm(mat)
#     #steps = show_matrices_for_filtration(filtration)
#     print("STEPS: ",steps, "BY TYPE: ", sum(steps))
#
#     print("NUM OF SIMPLICES: ", len(filtration))
#     y.append(sum(steps))
#
# plt.scatter(x,y)
#plt.show()