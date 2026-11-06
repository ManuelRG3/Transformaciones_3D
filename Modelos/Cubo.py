#Guarda la figura como datos: ocho vertices en coordenadas homogeneas 
#sy doce aristas para el cubo, cinco vertices y ocho aristas para la piramide, etc.

import math
import numpy as np


def _hom(puntos):

    p = np.array(puntos, dtype=float)

    return np.hstack([
        p,
        np.ones((len(p), 1))
    ])


def _anillo(inicio, n):

    return [
        (inicio + i, inicio + (i + 1) % n)
        for i in range(n)
    ]


# CUBO

def cubo():

    v = [
        (x, y, z)
        for x in (-1, 1)
        for y in (-1, 1)
        for z in (-1, 1)
    ]

    a = [
        (i, j)
        for i in range(8)
        for j in range(i + 1, 8)
        if bin(i ^ j).count("1") == 1
    ]

    return _hom(v), a


# PIRAMIDE

def piramide():

    v = [
        (-1, -1, -1),
        (1, -1, -1),
        (1, -1, 1),
        (-1, -1, 1),
        (0, 1, 0)
    ]

    a = _anillo(0, 4) + [
        (i, 4)
        for i in range(4)
    ]

    return _hom(v), a


# PRISMA TRIANGULAR

def prisma_triangular():

    tri = [
        (-1, -0.87),
        (1, -0.87),
        (0, 0.87)
    ]

    v = (
        [(x, y, -1) for x, y in tri]
        +
        [(x, y, 1) for x, y in tri]
    )

    a = (
        _anillo(0, 3)
        +
        _anillo(3, 3)
        +
        [(i, i + 3) for i in range(3)]
    )

    return _hom(v), a


# TRIANGULO

def triangulo():

    v = [
        (-1, -0.87, 0),
        (1, -0.87, 0),
        (0, 0.87, 0)
    ]

    return _hom(v), _anillo(0, 3)


# CONO

def cono(n=12):

    v = [
        (
            math.cos(2 * math.pi * i / n),
            -1,
            math.sin(2 * math.pi * i / n)
        )
        for i in range(n)
    ]

    v.append((0, 1, 0))

    a = (
        _anillo(0, n)
        +
        [(i, n) for i in range(0, n, 2)]
    )

    return _hom(v), a


# CILINDRO

def cilindro(n=12):

    v = []

    for y in (1, -1):

        v += [
            (
                math.cos(2 * math.pi * i / n),
                y,
                math.sin(2 * math.pi * i / n)
            )
            for i in range(n)
        ]

    a = (
        _anillo(0, n)
        +
        _anillo(n, n)
        +
        [(i, n + i) for i in range(0, n, 2)]
    )

    return _hom(v), a


# ESFERA REDUCIDA

def esfera(anillos=3, meridianos=8):

    v, a = [], []

    for k in range(1, anillos + 1):

        theta = math.pi * k / (anillos + 1)

        y = math.cos(theta)
        r = math.sin(theta)

        for j in range(meridianos):

            fi = 2 * math.pi * j / meridianos

            v.append((
                r * math.cos(fi),
                y,
                r * math.sin(fi)
            ))

    norte = len(v)
    v.append((0, 1, 0))

    sur = len(v)
    v.append((0, -1, 0))

    for k in range(anillos):

        a += _anillo(
            k * meridianos,
            meridianos
        )

        if k < anillos - 1:

            a += [
                (
                    k * meridianos + j,
                    (k + 1) * meridianos + j
                )
                for j in range(meridianos)
            ]

    a += [
        (norte, j)
        for j in range(meridianos)
    ]

    a += [
        (
            sur,
            (anillos - 1) * meridianos + j
        )
        for j in range(meridianos)
    ]

    return _hom(v), a


# SELECTOR DE FIGURAS

FIGURAS = {

    "Cubo": cubo(),

    "Pirámide": piramide(),

    "Prisma triangular": prisma_triangular(),

    "Triángulo": triangulo(),

    "Cono": cono(),

    "Cilindro": cilindro(),

    "Esfera": esfera(),

}
