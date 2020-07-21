import random

def get_random_2_complex(n,p):
    vertices = [[i] for i in range(n)]
    edges = [[i,j] for i in range(n) for j in range(n) if i<j]
    triangle = [[x,y,z] for x in range(n) for y in range(n) for z in range(n) if x<y<z if random.random()<p]

    return vertices + edges + triangle

def get_random_3_complex(n,p):
    vertices = [[i] for i in range(n)]
    edges = [[i,j] for i in range(n) for j in range(n) if i<j]
    triangle = [[x,y,z] for x in range(n) for y in range(n) for z in range(n) if x<y<z]
    tetrahedrons = [[q,r,u,v] for q in range(n) for r in range(n) for u in range(n) for v in range(n) if q<r<u<v if random.random()<p]

    return vertices + edges + triangle + tetrahedrons