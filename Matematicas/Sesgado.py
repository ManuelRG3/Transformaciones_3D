#se encarga de crear la matriz de sesgado a partir de los factores de sesgado en cada eje y tambien de los factores de sesgado cruzado,
#para luego multiplicarla con la matriz de transformacion acumulada.

import numpy as np

def sesgado(shxy, shxz, shyx, shyz, shzx, shzy):
    return np.array([
        [1, shxy, shxz, 0], 
        [shxy, 1, shyz, 0], 
        [shzx, shzy, 1, 0],
        [ 0,   0,  0,   1],

    ], dtype=float)