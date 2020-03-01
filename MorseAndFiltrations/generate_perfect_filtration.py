import itertools as it

def check_format(triangles):
    for t1 in triangles:
        edge = [t1[1],t1[2]]
        for t2 in triangles:
            if(t1 == t2):
                continue
            elif (edge in it.combinations(t2, 2)):
                raise ValueError('The format of input trianlges is faulty. Make sure, that the free face is at the end.')

def perfect_filtration_from_triangles(triangles):

    check_format(triangles)

    V = []
    E = []
    T = []

    for t in triangles:
        for v in (t[0],t[1],t[2]):
            if [v] not in V:
                V.append([v])

        for e in ([t[0],t[1]], [t[0],t[2]], [t[1],t[2]]):
            e.sort()
            if e not in E:
                E.append(e)

        t.sort()
        if t not in T:
            T.append(t)

    return V+E+T