import numpy as np

def sesgado(shxy, shxz, shyx, shyz, shzx, shzy):
    return np.array([
        [1, shxy, shxz, 0], 
        [shxy, 1, shyz, 0], 
        [shzx, shzy, 1, 0],
        [ 0,   0,  0,   1],

    ], dtype=float)