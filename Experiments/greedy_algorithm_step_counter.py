import matplotlib.pyplot as plt
from GudhiExtension.computation_handler import computation_handler

ch = computation_handler()
outlines = []
fig, axs = plt.subplots(2)
x = []
sim = []
y = []
for i in range(3,125):
    print("---",i,"/50---")

    ch.generate_n_points(i,2)
    y.append(ch.column_algorithm(ch.alpha.build_boundary_matrix()))

    x.append(i)
    sim.append(len(ch.alpha.filtration))

axs[0].plot(x,y)
axs[1].plot(sim,y)

plt.show()