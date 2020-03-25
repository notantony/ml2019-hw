import numpy as np
import pandas as pd
import kernels

class KNN:
    def __init__(self, x, y, k=1, d=None, dist_f=kernels.euclidean, kernel_f=kernels.epanechnikov):
        self.x = x
        self.y = y
        self.dist_f = dist_f
        self.kernel_f = kernel_f
        
        if d:
            self.d = d
        elif k:
            self.k = k


    def run(self, item, answer):
        dists = []
        for i, sample in enumerate(self.x.iterrows()):
            dists.append((self.dist_f(item, sample[1]), self.y.iloc[i]))
        dists = sorted(dists)
        top = {}
        if hasattr(self, "d"):
            dist_base = self.d
        else:
            dist_base = dists[self.k][0] 
        for dist, y in dists:
            if y not in top:
                top[y] = 0
            top[y] += self.kernel_f(dist / dist_base)
        
        challenger = max(top.keys(), key=lambda key: -np.inf if key == answer else top[key])
        result = max(top.keys(), key=lambda key: top[key])
        return result, top.get(answer, 0) - top[challenger]
