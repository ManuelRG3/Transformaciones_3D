#este codigo se encarga de proyectar los vertices 3D en 2D,
#aplicando la matriz de perspectiva o la proyeccion ortogonal, segun el modo activo.

import numpy as np


def proyeccion_perspectiva(puntos, d):
    """El observador está en z = d mirando hacia -z.
    Lo que está más cerca (z mayor) se ve más grande."""
    x = puntos[:, 0]
    y = puntos[:, 1]
    z = puntos[:, 2]

    denominador = np.maximum(d - z, 0.1)   # evita dividir entre 0
    factor = d / denominador

    return np.column_stack((x * factor, y * factor))