from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper
from GudhiExtension.computation_handler import computation_handler

ch = computation_handler()
outlines = []
ch.generate_n_points(3,2)
complex = alpha_complex_wrapper(ch.points)
print(complex.filtration)
complex.build_boundary_matrix()