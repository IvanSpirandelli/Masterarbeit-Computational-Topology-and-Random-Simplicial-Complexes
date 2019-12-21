import random

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper


class computation_handler:

    def __init__(self, compute_persistance = False):
        self.points = [[0,0],[0,1],[1,1]]
        self.alpha = alpha_complex_wrapper(self.points, compute_persistance)

    def generate_n_gridpoints_of_dim_with_dilation(self, n, dim, dilation):
        points = set()
        while (len(points) < n):
            point = (random.randrange(0, dilation+1, 1) for i in range(dim))
            points.add(point)

        self.points=[list(elem) for elem in points]
        print("Genereated points: ")
        print(self.points)
        print('__________________________________________________________')

    def generate_n_points(self, n, dim):
        points = set()
        while (len(points) < n):
            point = (random.random() for i in range(dim))
            points.add(point)

        self.points = [list(elem) for elem in points]
        print("Genereated points: ")
        print(self.points)
        print('__________________________________________________________')

    def set_points(self, points):
        self.points = points
        self.compute_alpha()

    def compute_alpha(self):
        self.alpha = alpha_complex_wrapper(self.points)
        print("Generated alpha complex")
