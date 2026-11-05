import math
import time
import flet as ft
import estilos as S

from Controlador.Escena import calcular_escena, Neutros
from Interfaz.Lienzo import crear_lienzo, dibujar
from Modelos.Cubo import FIGURAS


# CONFIGURACION
sensibilidad = 0.5
FPS_MAXIMO = 15
INTERVALO = 1 / FPS_MAXIMO

ultimo_dibujo = 0


inicial = {
    **Neutros,
    "rx": 25,
    "ry": 30,
    "d": 10
}


modos = {
    "traslacion": (
        "Traslación",
        "Traslación: arrastra para mover la figura; pellizca o usa la rueda para acercarla o alejarla en Z"
    ),

    "escalamiento": (
        "Escalamiento",
        "Escalamiento: arrastra para estirar en X e Y; pellizca o usa la rueda para escalar"
    ),

    "rotacion": (
        "Rotación",
        "Rotación: arrastra para girar en X e Y; gira dos dedos o usa la rueda para rotar en Z"
    ),

    "sesgado": (
        "Sesgado",
        "Sesgado: arrastra para inclinar la figura; pellizca o usa la rueda para inclinarla en profundidad"
    ),

    "perspectiva": (
        "Perspectiva",
        "Perspectiva: arrastra arriba o abajo para acercar o alejar al observador"
    ),
}


def limitar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def main(page: ft.Page):

    global ultimo_dibujo

    S.aplicar_tema(page, "Transformación 3D")

    parametros = dict(inicial)

    estado = {
        "modo": "rotacion",
        "figura": "Cubo"
    }

    previo = {
        "n": 0,
        "escala": 1.0,
        "rot": 0.0
    }

    lienzo = crear_lienzo(S.calcular_lado(page))

    # ACTUALIZACION OPTIMIZADA

    def actualizar(forzar=False):

        global ultimo_dibujo

        ahora = time.perf_counter()

        if not forzar and ahora - ultimo_dibujo < INTERVALO:
            return

        ultimo_dibujo = ahora

        puntos, aristas, matriz = calcular_escena(
            parametros,
            estado["figura"]
        )

        dibujar(lienzo, puntos, aristas)

    # ARRASTRE

    def arrastre(dx, dy):

        modo = estado["modo"]

        if modo == "traslacion":

            unidad = lienzo.width / 5

            parametros["tx"] = limitar(
                parametros["tx"] + dx / unidad,
                -1.5,
                1.5
            )

            parametros["ty"] = limitar(
                parametros["ty"] - dy / unidad,
                -1.5,
                1.5
            )

        elif modo == "escalamiento":

            parametros["sx"] = limitar(
                parametros["sx"] + dx * 0.005,
                0.3,
                3
            )

            parametros["sy"] = limitar(
                parametros["sy"] - dy * 0.005,
                0.3,
                3
            )

        elif modo == "rotacion":

            parametros["ry"] += dx * sensibilidad
            parametros["rx"] += dy * sensibilidad

        elif modo == "sesgado":

            parametros["shxy"] = limitar(
                parametros["shxy"] + dx * 0.004,
                -1,
                1
            )

            parametros["shyx"] = limitar(
                parametros["shyx"] - dy * 0.004,
                -1,
                1
            )

        elif modo == "perspectiva":

            parametros["d"] = limitar(
                parametros["d"] + dy * 0.12,
                3,
                20
            )

    # PELLIZCO Y ZOOM

    def pellizco(factor, giro):

        modo = estado["modo"]

        if modo == "traslacion":

            parametros["tz"] = limitar(
                parametros["tz"] - (factor - 1) * 3,
                -2,
                2
            )

        elif modo == "escalamiento":

            for clave in ("sx", "sy", "sz"):

                parametros[clave] = limitar(
                    parametros[clave] * factor,
                    0.3,
                    3
                )

        elif modo == "rotacion":

            parametros["rz"] -= giro

        elif modo == "sesgado":

            parametros["shxz"] = limitar(
                parametros["shxz"] + (factor - 1) * 2,
                -1,
                1
            )

            parametros["shyz"] = limitar(
                parametros["shyz"] + (factor - 1) * 2,
                -1,
                1
            )

        elif modo == "perspectiva":

            parametros["d"] = limitar(
                parametros["d"] / factor,
                3,
                20
            )

    # DETECCION DE MOVIMIENTO

    def gesto(e):

        n = e.pointer_count

        if n != previo["n"]:

            previo.update(
                n=n,
                escala=1.0,
                rot=0.0
            )

        if n >= 2:

            factor = e.scale / previo["escala"]

            giro = math.degrees(
                e.rotation - previo["rot"]
            )

            previo.update(
                escala=e.scale,
                rot=e.rotation
            )

            pellizco(factor, giro)

        else:

            arrastre(
                e.focal_point_delta.x,
                e.focal_point_delta.y
            )

        actualizar()

    def terminar(e):

        previo.update(
            n=0,
            escala=1.0,
            rot=0.0
        )

        actualizar(True)

    # RUEDA DEL MOUSE

    def rueda(e):

        factor = limitar(
            1 - e.scroll_delta.y / 1000,
            0.9,
            1.1
        )

        pellizco(
            factor,
            (1 - factor) * 100
        )

        actualizar(True)

    # DESCRIPCION DEL MODO

    texto_modo = S.texto_descripcion(
        modos["rotacion"][1]
    )

    # CAMBIAR TRANSFORMACION

    def cambiar_modo(clave):

        def manejador(e):

            estado["modo"] = clave

            texto_modo.value = modos[clave][1]
            texto_modo.update()

            S.resaltar(
                botones,
                clave
            )

        return manejador

    botones = S.crear_botones_modo(
        modos,
        estado["modo"],
        cambiar_modo
    )

    # CAMBIAR FIGURA

    def cambiar_figura(nombre):

        def manejador(e):

            estado["figura"] = nombre

            S.resaltar_figura(
                chips_figuras,
                nombre
            )

            actualizar(True)

        return manejador

    chips_figuras = S.crear_selector_figuras(
        list(FIGURAS),
        estado["figura"],
        cambiar_figura
    )

    # REINICIAR

    def reiniciar(e):

        parametros.update(inicial)

        actualizar(True)

    # REDIMENSIONAR

    def redimensionar(e):

        lado = S.calcular_lado(page)

        lienzo.width = lado
        lienzo.height = lado

        actualizar(True)

    page.on_resize = redimensionar

    # LIENZO INTERACTIVO

    figura = ft.GestureDetector(
        content=lienzo,
        mouse_cursor=ft.MouseCursor.MOVE,
        on_scale_update=gesto,
        on_scale_end=terminar,
        on_scroll=rueda,
    )

    # INTERFAZ PRINCIPAL

    page.add(
        S.pantalla(

            S.encabezado(
                "Transformaciones 3D",
                "Traslación · Escalamiento · Rotación · Sesgado · Perspectiva"
            ),

            S.marco_lienzo(figura),

            S.panel_controles(
                texto_modo,
                botones,
                S.boton_secundario(
                    "Reiniciar",
                    reiniciar
                ),
                chips_figuras
            ),
        )
    )

    actualizar(True)


ft.run(main)
