import flet as ft
import flet.canvas as cv

def crear_lienzo(lado):
    return cv.Canvas(shapes=[], width=lado, height=lado)

def dibujar(lienzo, puntos, aristas):
    lado = lienzo.width
    escala = lado/5
    centro = lado/2 
    trazo = ft.Paint(color=ft.Colors.BLUE, stroke_width=2, 
                     style=ft.PaintingStyle.STROKE)
    lienzo.shapes = []
    for i, j in aristas:
        x1 = centro + puntos[i][0] * escala
        y1 = centro - puntos[i][1] * escala
        x2 = centro + puntos[j][0] * escala
        y2 = centro - puntos[j][1] * escala
        lienzo.shapes.append(cv.Line(x1, y1, x2, y2, paint=trazo))
    lienzo.update()