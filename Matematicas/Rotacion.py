#se encarga de crear las matrices de rotacion a partir 
#del angulo en grados, para luego multiplicarlas con la matriz de transformacion acumulada.

import numpy as np

def rotacion_y(angulo_grados):
    a = np.radians(angulo_grados)
    c, s = np.cos(a), np.sin(a)
    return np.array([
        [ c, 0, s, 0], 
        [ 0, 1, 0, 0], 
        [-s, 0, c, 0], 
        [ 0, 0, 0, 1], 

    ], dtype=float)

def rotacion_x(angulo_grados):
    a = np.radians(angulo_grados)
    c, s = np.cos(a), np.sin(a)
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ], dtype=float)

def rotacion_z(angulo_grados):
    a = np.radians(angulo_grados)
    c, s =  np.cos(a), np.sin(a)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],

    ], dtype=float)