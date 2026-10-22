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

def rotacion_x(angulo_grados):
    a = np.radians(angulo_grados)
    c, s = np.cos(a), np.sin(a)
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ])

def rotacion_z(angulo_grados):
    a = np.radians(angulo_grados)
    c, s =  np.cos(a), np.sin(a)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],

    ])