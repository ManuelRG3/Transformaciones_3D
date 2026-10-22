from Modelos.Cubo import Vertices, Aristas
from Matematicas.Traslacion import traslacion
from Matematicas.Escalamiento import escalamiento
from Matematicas.Sesgado import sesgado
from Matematicas.Rotacion import rotacion_y, rotacion_x, rotacion_z
from Matematicas.Proyeccion import proyeccion_ortogonal

Neutros = {
    "tx" : 0, "ty" : 0, "tz": 1,
    "sx" : 1, "sy" : 1, "sz": 1,
    "rx" : 0, "ry" : 0, "rz": 0,
    "shxy": 0, "shxz": 0, "shyx": 0, "shyz": 0, "shzx": 0, "shzy": 0,
}

def calcular_escena(Parametros):
    p = {**Neutros, **Parametros}
    t = traslacion(p["tx"], p["ty"], p["tz"])
    r = rotacion_x(p["rx"]) @ rotacion_y(p["ry"]) @ rotacion_z(p["rz"])
    h = sesgado(p["shxy"], p["shxz"], p["shyx"], p["shyz"], p["shzx"], p["shzy"])
    s = escalamiento(p["sx"], p["sy"], p["sz"])
    Matriz = t @ r @ h @ s 
    Transformados = (Matriz @ Vertices.T).T
    Puntos_2d = proyeccion_ortogonal(Transformados)
    return Puntos_2d, Aristas, Matriz

