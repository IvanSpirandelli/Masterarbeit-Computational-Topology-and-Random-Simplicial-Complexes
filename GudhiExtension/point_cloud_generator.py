import random
import numpy as np
import itertools as it

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper


def generate_n_gridpoints_of_dim_with_dilation(n, dim, dilation):
    points = set()
    while (len(points) < n):
        point = (random.randrange(0, dilation+1, 1) for i in range(dim))
        points.add(point)
    return [list(elem) for elem in points]

def generate_one_point(dim):
    return list(random.random() for _ in range(dim))

def generate_n_points(n, dim):
    points = set()
    while (len(points) < n):
        point = (random.random() for _ in range(dim))
        points.add(point)

    return [list(elem) for elem in points]

def generate_n_points_poisson(n,lam,dim):
    print(np.random.poisson(lam,[dim,dim]*n))

def generate_n_points_normal(n,dim,mean,sigma):
    points = set()
    while (len(points) < n):
        point = (np.random.normal(mean,sigma) for _ in range(dim))
        points.add(point)
    return [list(elem) for elem in points]

def multivariate_gaussian(n, mean, cov):
    points = set()
    while(len(points) < n):
        point = np.random.multivariate_normal(mean, cov)
        points.add(tuple(point))
    return [list(elem) for elem in points]

def gaussian_mixture_model(n, means, covs):
    points = set()
    while (len(points) < n):
        i = random.choice(range(len(means)))
        point = np.random.multivariate_normal(means[i], covs[i])
        points.add(tuple(point))
    return [list(elem) for elem in points]