import matplotlib.pyplot as plt

class sc_drawer():

    def __init__(self, points, simplex_tree):
        self.points = points
        self.simplex_tree = simplex_tree

    def draw_skeleton(self, dim =-1):

        if(dim == -1 or dim > self.simplex_tree.dimension()):
            dim = self.simplex_tree.dimension()

        for simplex in self.simplex_tree.get_skeleton(dim):
            if(len(simplex[0]) == 4):
                continue

            elif len(simplex[0]) == 3:
                zipped =  list(zip(self.points[simplex[0][0]], self.points[simplex[0][1]], self.points[simplex[0][2]]))
                plt.fill(list(zipped[0]),list(zipped[1]), color = 'beige', zorder = 1)

            elif(len(simplex[0]) == 2):
                zipped = list(zip(self.points[simplex[0][0]], self.points[simplex[0][1]]))
                plt.plot(list(zipped[0]),list(zipped[1]), color = 'coral', zorder = 2)

        x,y = zip(*self.points)
        plt.scatter(x,y, zorder = 3)

        plt.show()

    def draw_filtration_3D(self, plot, level=0):
        filtration = self.simplex_tree.get_filtration()

        step = 0
        index = 0
        dist_at_index = 0.0

        if (step == 0):
            # Moving forward in the list of simplices, until the layer of distance 0 is done
            while (step == 0):
                if (filtration[index][1] == dist_at_index):
                    index += 1
                else:
                    step += 1
                    dist_at_index = filtration[index][1]

            x, y = zip(*self.points)
            plot.scatter(x, y, zorder=3)

        latest_dist = 0.0

        while (step < level and index < len(filtration)):
            if (filtration[index][1] == dist_at_index):

                if (len(filtration[index][0]) == 2):
                    zipped = list(zip(self.points[filtration[index][0][0]], self.points[filtration[index][0][1]]))
                    plot.plot(list(zipped[0]), list(zipped[1]), lw=3, color='coral', zorder=2)

                elif (len(filtration[index][0]) == 3):
                    zipped = list(zip(self.points[filtration[index][0][0]],
                                      self.points[filtration[index][0][1]],
                                      self.points[filtration[index][0][2]]))
                    plot.fill(list(zipped[0]), list(zipped[1]), color='beige', zorder=1)

                elif (len(filtration[index][0]) == 3):
                    zipped = list(zip(self.points[filtration[index][0][0]],
                                      self.points[filtration[index][0][1]],
                                      self.points[filtration[index][0][2]],
                                      self.points[filtration[index][0][3]]))
                    plot.fill(list(zipped[0]), list(zipped[1]), list(zipped[2]), color='gray', zorder=0)
                index += 1
                latest_dist = dist_at_index
            else:
                dist_at_index = filtration[index][1]
                step += 1

        return latest_dist

    def draw_filtration_2D(self, plot, level = 0):
        filtration = self.simplex_tree.get_filtration()

        step = 0
        index = 0
        dist_at_index = 0.0
        #print("Index: ", index, ", DistAtIndex: ", dist_at_index, ", Step: ", step)
        if(step == 0):
            #Moving forward in the list of simplices, until the layer of distance 0 is done
            while(step == 0):
                if(filtration[index][1] == dist_at_index):
                    index += 1
                else:
                    step +=1
                    dist_at_index = filtration[index][1]

            x,y = zip(*self.points)
            plot.scatter(x,y, zorder = 3)


        latest_dist = 0.0
        #print("Index: ", index, ", DistAtIndex: ", dist_at_index, ", Step: ", step)
        while(step < level and index < len(filtration)):
            if(filtration[index][1] == dist_at_index):

                if(len(filtration[index][0]) == 2):
                    zipped = list(zip(self.points[filtration[index][0][0]], self.points[filtration[index][0][1]]))
                    plot.plot(list(zipped[0]), list(zipped[1]), lw = 3 ,color='coral', zorder=2)

                elif(len(filtration[index][0]) == 3):
                    zipped = list(zip(self.points[filtration[index][0][0]],
                                      self.points[filtration[index][0][1]],
                                      self.points[filtration[index][0][2]]))
                    plot.fill(list(zipped[0]), list(zipped[1]), color='beige', zorder=1)

                index+=1
                latest_dist = dist_at_index
            else:
                dist_at_index = filtration[index][1]
                step+=1
            #print("Index: ", index, ", DistAtIndex: ", dist_at_index, ", Step: ", step)
        return latest_dist