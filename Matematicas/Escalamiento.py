import numpy as np

def escalamiento(SX, SY, SZ):
    return np.array([
        [SX, 0, 0, 0], 
        [0, SY, 0, 0], 
        [0, 0, SZ, 0], 
        [0, 0, 0, 1],

    ], dtype=float)