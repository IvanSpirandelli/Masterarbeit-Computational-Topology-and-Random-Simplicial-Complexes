import random
import numpy as np
import itertools as it

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper


class point_cloud_generator:

    def __init__(self):
        self.points = [[0,0],[0,1],[1,1]]

    def generate_n_gridpoints_of_dim_with_dilation(self, n, dim, dilation):
        points = set()
        while (len(points) < n):
            point = (random.randrange(0, dilation+1, 1) for i in range(dim))
            points.add(point)

        self.points=[list(elem) for elem in points]
        return self.points

    def generate_n_points(self, n, dim):
        points = set()
        while (len(points) < n):
            point = (random.random() for i in range(dim))
            points.add(point)

        self.points = [list(elem) for elem in points]
        return self.points


    def set_points(self, points):
        self.points = points



