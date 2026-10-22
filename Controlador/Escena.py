from Modelos.Cubo import Vertices, Aristas
from Matematicas.Rotacion import rotacion_y, rotacion_x, rotacion_z
from Matematicas.Proyeccion import proyeccion_ortogonal

def calcular_escena(Parametros):
    Matriz = rotacion_x(Parametros["rx"]) @ rotacion_y(Parametros["ry"]) @ rotacion_z(Parametros["rz"])
    Transformados = (Matriz @ Vertices.T).T
    Puntos_2d = proyeccion_ortogonal(Transformados)
    return Puntos_2d, Aristas, Matriz

