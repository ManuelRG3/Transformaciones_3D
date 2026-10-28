import flet as ft
import flet.canvas as cv


class C:
    GRID_MENOR = "#18213A"
    GRID_MAYOR = "#26335A"
    EJE_X = "#FF5C7A"
    EJE_Y = "#4ADE80"
    ARISTA = "#8B7CFF"
    VERTICE = "#00D1B2"


def _alfa(color, opacidad):
    return ft.Colors.with_opacity(opacidad, color)


def crear_lienzo(lado):
    return cv.Canvas(shapes=[], width=lado, height=lado)


def _linea(x1, y1, x2, y2, color, grosor):
    return cv.Line(
        x1, y1, x2, y2,
        paint=ft.Paint(
            color=color,
            stroke_width=grosor,
            style=ft.PaintingStyle.STROKE,
            stroke_cap=ft.StrokeCap.ROUND,
        ),
    )


def _cuadricula(lado, centro, escala):
    formas = []
    for k in range(-5, 6):
        pos = centro + k * escala / 2
        color = C.GRID_MAYOR if k % 2 == 0 else C.GRID_MENOR
        formas.append(_linea(pos, 0, pos, lado, color, 1))
        formas.append(_linea(0, pos, lado, pos, color, 1))
    formas.append(_linea(0, centro, lado, centro, _alfa(C.EJE_X, 0.7), 1.5))
    formas.append(_linea(centro, 0, centro, lado, _alfa(C.EJE_Y, 0.7), 1.5))
    return formas


def dibujar(lienzo, puntos, aristas):
    lado = lienzo.width
    escala = lado / 5
    centro = lado / 2

    def a_pantalla(p):
        return centro + p[0] * escala, centro - p[1] * escala

    formas = _cuadricula(lado, centro, escala)

    segmentos = []
    for i, j in aristas:
        x1, y1 = a_pantalla(puntos[i])
        x2, y2 = a_pantalla(puntos[j])
        segmentos.append((x1, y1, x2, y2))

    # Brillo (dos capas translúcidas debajo de la línea)
    for x1, y1, x2, y2 in segmentos:
        formas.append(_linea(x1, y1, x2, y2, _alfa(C.ARISTA, 0.12), 12))
    for x1, y1, x2, y2 in segmentos:
        formas.append(_linea(x1, y1, x2, y2, _alfa(C.ARISTA, 0.25), 6))
    # Línea principal
    for x1, y1, x2, y2 in segmentos:
        formas.append(_linea(x1, y1, x2, y2, C.ARISTA, 2.2))

    # Vértices con halo
    halo = ft.Paint(color=_alfa(C.VERTICE, 0.25), style=ft.PaintingStyle.FILL)
    nucleo = ft.Paint(color=C.VERTICE, style=ft.PaintingStyle.FILL)
    for p in puntos:
        x, y = a_pantalla(p)
        formas.append(cv.Circle(x, y, 8, paint=halo))
        formas.append(cv.Circle(x, y, 3.5, paint=nucleo))

    lienzo.shapes = formas
    lienzo.update()