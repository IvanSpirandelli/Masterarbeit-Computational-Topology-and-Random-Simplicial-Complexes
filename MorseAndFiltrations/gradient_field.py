import numpy as np

class gradient_field():
    def __init__(self,simplices, pairings):
        self.simplices = [tuple(simplex) for simplex in simplices]
        self.pairings = pairings

        self.dependencies = {():set()}
        self.compute_dependencies()
        self.adjust_hasse_with_pairings()

    def compute_dependencies(self):
        for simplex in self.simplices:
            self.dependencies[simplex] = set()
            for potential_face in self.simplices:
                if len(potential_face) == len(simplex) - 1:
                    if (all(elem in simplex for elem in potential_face)):
                        self.dependencies[simplex].add(potential_face)

    def adjust_hasse_with_pairings(self):
        for pair in self.pairings:
            greater = tuple(max(pair, key=len))
            smaller = tuple(min(pair, key=len))
            self.dependencies[greater].remove(smaller)
            self.dependencies[smaller].add(greater)



    def compute_hasse_old(self):
        for outer in self.simplices:
            self.hasse[outer] = set()
            for inner in self.simplices:
                if len(inner) == len(outer)-1:
                    if(all(elem in outer for elem in inner)):
                        self.hasse[inner].add(outer)

    
    def adjust_hasse_with_pairings_old(self):
        for pair in self.pairings:
            greater = tuple(max(pair, key=len))
            smaller = tuple(min(pair, key=len))
            self.hasse[smaller].remove(greater)
            self.hasse[greater].add(smaller)


