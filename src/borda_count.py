import numpy as np

class BordaCount:
    def __init__(self, weights: list, placements: list):
        super().__init__()
        self.weights = weights
        self.placements = placements

    def get_aggregate_value(self):
        ret = 0
        for placement in self.placements:
            if placement > 0:
                ret+=self.weights[placement-1]
        return ret