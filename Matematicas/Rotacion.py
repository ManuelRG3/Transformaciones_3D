import numpy as np

def rotacion_y(angulo_grados):
    a = np.radians(angulo_grados)
    c, s = np.cos(a), np.sin(a)
    return np.array([
        [ c, 0, s, 0], 
        [ 0, 1, 0, 0], 
        [-s, 0, c, 0], 
        [ 0, 0, 0, 1], 

    ])