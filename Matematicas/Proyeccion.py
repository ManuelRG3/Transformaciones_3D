#se encarga de proyectar los vertices 3D en 2D, 
#aplicando la matriz de perspectiva o la proyeccion ortogonal, segun el modo activo.

def proyeccion_ortogonal(Vertices):
    return Vertices[:, :2]