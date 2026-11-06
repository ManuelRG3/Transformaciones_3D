#Convierte los puntos 2D a pixeles y los dibuja en el lienzo, junto con la cuadricula y los ejes.
#tambien se encarga de crear el lienzo y las pinturas reutilizables para dibujar los elementos de la escena.

import flet as ft
import flet.canvas as cv


class C:
    GRID_MENOR = "#18213A"
    GRID_MAYOR = "#26335A"
    EJE_X = "#FF5C7A"
    EJE_Y = "#4ADE80"
    ARISTA = "#8B7CFF"
    VERTICE = "#00D1B2"


# PINTURAS REUTILIZABLES

PAINT_GRID_MENOR = ft.Paint(
    color=C.GRID_MENOR,
    stroke_width=1
)

PAINT_GRID_MAYOR = ft.Paint(
    color=C.GRID_MAYOR,
    stroke_width=1
)

PAINT_EJE_X = ft.Paint(
    color=C.EJE_X,
    stroke_width=1.5
)

PAINT_EJE_Y = ft.Paint(
    color=C.EJE_Y,
    stroke_width=1.5
)

PAINT_ARISTA = ft.Paint(
    color=C.ARISTA,
    stroke_width=2.2,
    stroke_cap=ft.StrokeCap.ROUND
)

PAINT_VERTICE = ft.Paint(
    color=C.VERTICE,
    style=ft.PaintingStyle.FILL
)


def crear_lienzo(lado):

    return cv.Canvas(
        shapes=[],
        width=lado,
        height=lado
    )


def _linea(x1, y1, x2, y2, paint):

    return cv.Line(
        x1, y1, x2, y2,
        paint=paint
    )


def _cuadricula(lado, centro, escala):

    formas = []

    for k in range(-5, 6):

        pos = centro + k * escala / 2

        paint = (
            PAINT_GRID_MAYOR
            if k % 2 == 0
            else PAINT_GRID_MENOR
        )

        formas.append(
            _linea(
                pos, 0, pos, lado,
                paint
            )
        )

        formas.append(
            _linea(
                0, pos, lado, pos,
                paint
            )
        )

    formas.append(
        _linea(
            0, centro, lado, centro,
            PAINT_EJE_X
        )
    )

    formas.append(
        _linea(
            centro, 0, centro, lado,
            PAINT_EJE_Y
        )
    )

    return formas


def dibujar(lienzo, puntos, aristas):

    lado = lienzo.width

    escala = lado / 5
    centro = lado / 2

    def a_pantalla(p):

        return (
            centro + p[0] * escala,
            centro - p[1] * escala
        )

    formas = _cuadricula(
        lado,
        centro,
        escala
    )

    # ARISTAS: UNA SOLA LINEA POR ARISTA

    for i, j in aristas:

        x1, y1 = a_pantalla(puntos[i])
        x2, y2 = a_pantalla(puntos[j])

        formas.append(
            _linea(
                x1, y1, x2, y2,
                PAINT_ARISTA
            )
        )

    # VERTICES SIN HALOS

    for p in puntos:

        x, y = a_pantalla(p)

        formas.append(
            cv.Circle(
                x, y, 3.5,
                paint=PAINT_VERTICE
            )
        )

    lienzo.shapes = formas
    lienzo.update()
