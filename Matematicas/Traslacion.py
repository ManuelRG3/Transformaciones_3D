#este codigo se encarga de crear la matriz de traslacion a partir de los valores de traslacion en cada eje,
#para luego multiplicarla con la matriz de transformacion acumulada.

import numpy as np

def traslacion(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],

    ], dtype=float)