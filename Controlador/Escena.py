import numpy as np

from Modelos.Cubo import FIGURAS

from Matematicas.Traslacion import traslacion
from Matematicas.Escalamiento import escalamiento
from Matematicas.Sesgado import sesgado
from Matematicas.Rotacion import (
    rotacion_y,
    rotacion_x,
    rotacion_z
)


Neutros = {
    "tx": 0,
    "ty": 0,
    "tz": 0,

    "sx": 1,
    "sy": 1,
    "sz": 1,

    "rx": 0,
    "ry": 0,
    "rz": 0,

    "shxy": 0,
    "shxz": 0,
    "shyx": 0,
    "shyz": 0,
    "shzx": 0,
    "shzy": 0,

    "d": 10.0,
}


def calcular_escena(Parametros, figura="Cubo"):

    Vertices, Aristas = FIGURAS[figura]

    p = {
        **Neutros,
        **Parametros
    }

    # TRASLACION

    t = traslacion(
        p["tx"],
        p["ty"],
        p["tz"]
    )

    # ROTACION

    r = (
        rotacion_x(p["rx"])
        @ rotacion_y(p["ry"])
        @ rotacion_z(p["rz"])
    )

    # SESGADO

    h = sesgado(
        p["shxy"],
        p["shxz"],
        p["shyx"],
        p["shyz"],
        p["shzx"],
        p["shzy"]
    )

    # ESCALAMIENTO

    s = escalamiento(
        p["sx"],
        p["sy"],
        p["sz"]
    )

    # MATRIZ DE TRANSFORMACION

    Matriz = t @ r @ h @ s

    Transformados = (
        Matriz @ Vertices.T
    ).T

    # PERSPECTIVA 3D

    d = max(float(p["d"]), 3.0)

    x = Transformados[:, 0]
    y = Transformados[:, 1]
    z = Transformados[:, 2]

    denominador = np.maximum(d - z, 0.5)

    factor = d / denominador

    Puntos_2d = np.column_stack((
        x * factor,
        y * factor
    ))

    # DEVOLVER RESULTADOS

    return Puntos_2d, Aristas, Matriz
