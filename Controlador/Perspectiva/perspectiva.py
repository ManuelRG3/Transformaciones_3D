#aplicacion de la matriz de perspectiva a los vertices 3D, para proyectarlos en 2D.

import numpy as np


def perspectiva(d):
    """Matriz de perspectiva del profesor: x' = x / (z/d + 1), y' = y / (z/d + 1)."""
    return np.array([
        [1, 0, 0,     0],
        [0, 1, 0,     0],
        [0, 0, 1,     0],
        [0, 0, 1 / d, 1],
    ], dtype=float)