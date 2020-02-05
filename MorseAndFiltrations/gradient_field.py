import numpy as np

class gradient_field():
    def __init__(self,simplices, pairings):
        self.simplices = [tuple(simplex) for simplex in simplices]
        self.pairings = pairings

        self.hasse = {():set()}
        self.compute_hasse()
        self.adjust_hasse_with_pairings()

    def compute_hasse(self):
        for outer in self.simplices:
            self.hasse[outer] = set()
            for inner in self.simplices:
                if len(inner) == len(outer)-1:
                    if(all(elem in outer for elem in inner)):
                        self.hasse[inner].add(outer)

    
    def adjust_hasse_with_pairings(self):
        for pair in self.pairings:
            greater = tuple(max(pair, key=len))
            smaller = tuple(min(pair, key=len))
            self.hasse[smaller].remove(greater)
            self.hasse[greater].add(smaller)


