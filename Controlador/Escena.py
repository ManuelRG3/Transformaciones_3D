from Modelos.Cubo import Vertices, Aristas
from Matematicas.Rotacion import rotacion_y
from Matematicas.Proyeccion import proyeccion_ortogonal

def calcular_escena(Parametros):
    Matriz = rotacion_y(Parametros["ry"])
    Transformados = (Matriz @ Vertices.T).T
    Puntos_2d = proyeccion_ortogonal(Transformados)
    return Puntos_2d, Aristas, Matriz