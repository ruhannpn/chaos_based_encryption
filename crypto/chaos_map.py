# crypto/chaos_map.py

import numpy as np

def logistic_map(x0, r, size):
    x = x0
    seq = np.zeros(size)
    for i in range(size):
        x = r * x * (1 - x)
        seq[i] = x
    return seq
