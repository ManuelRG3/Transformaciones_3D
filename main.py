import math
import flet as ft
from Controlador.Escena import calcular_escena, Neutros
from Interfaz.Lienzo import crear_lienzo, dibujar

sensibilidad = 0.5
inicial = {**Neutros, "rx": 25, "ry": 30}

modos = {
    "traslacion": ("Traslación",
                   "Traslación: arrastra para mover la figura"),
    "escalamiento": ("Escalamiento",
                     "Escalamiento: arrastra para estirar en X e Y; pellizca (o usa la rueda) para escalar todo por igual"),
    "rotacion": ("Rotación",
                 "Rotación: arrastra para girar en X e Y; gira dos dedos (o usa la rueda) para rotar en Z"),
    "sesgado" : ("Sesgado",
                 "Sesgado: Arrastra para inclinar la figura (a los lados, arriba o abajo); pellizca o usa la rueda del raton para inclinarla segun la profundidad"),
}


def limitar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def main(page: ft.Page):
    page.title = "Transformacion 3D"
    parametros = dict(inicial)
    estado = {"modo": "rotacion"}
    previo = {"n": 0, "escala": 1.0, "rot": 0.0}

    def calcular_lado():
        ancho = page.width or 500
        return int(max(250, min(500, ancho - 40)))

    lienzo = crear_lienzo(calcular_lado())

    def actualizar():
        puntos, aristas, matriz = calcular_escena(parametros)
        dibujar(lienzo, puntos, aristas)

    def arrastre(dx, dy):
        modo = estado["modo"]
        if modo == "traslacion":
            unidad = lienzo.width / 5
            parametros["tx"] = limitar(parametros["tx"] + dx / unidad, -1.5, 1.5)
            parametros["ty"] = limitar(parametros["ty"] - dy / unidad, -1.5, 1.5)
        elif modo == "escalamiento":
            parametros["sx"] = limitar(parametros["sx"] + dx * 0.005, 0.3, 3)
            parametros["sy"] = limitar(parametros["sy"] - dy * 0.005, 0.3, 3)
        elif modo == "rotacion":
            parametros["ry"] += dx * sensibilidad
            parametros["rx"] += dy * sensibilidad
        elif modo == "sesgado" :
            parametros["shxy"] = limitar(parametros["shxy"] + dx * 0.004, -1, 1)
            parametros["shyx"] = limitar(parametros["shyx"] - dy * 0.004, -1, 1)

    def pellizco(factor, giro):
        modo = estado["modo"]
        if modo == "traslacion":
            # Separar los dedos acerca la figura (z menor), juntarlos la aleja
            parametros["tz"] = limitar(parametros["tz"] - (factor - 1) * 3, -2, 2)
        elif modo == "escalamiento":
            for clave in ("sx", "sy", "sz"):
                parametros[clave] = limitar(parametros[clave] * factor, 0.3, 3)
        elif modo == "rotacion":
            parametros["rz"] -= giro
        elif modo == "sesgado":
            parametros["shxz"] = limitar(parametros["shxz"] * (factor - 1) * 2, -1, 1)
            parametros["shyz"] = limitar(parametros["shyz"] * (factor - 1) * 2, -1, 1)

    def gesto(e):
        n = e.pointer_count
        if n != previo["n"]:
            previo.update(n=n, escala=1.0, rot=0.0)
        if n >= 2:
            factor = e.scale / previo["escala"]
            giro = math.degrees(e.rotation - previo["rot"])
            previo.update(escala=e.scale, rot=e.rotation)
            pellizco(factor, giro)
        else:
            arrastre(e.focal_point_delta.x, e.focal_point_delta.y)
        actualizar()

    def terminar(e):
        previo.update(n=0, escala=1.0, rot=0.0)

    def rueda(e):
        factor = limitar(1 - e.scroll_delta.y / 1000, 0.9, 1.1)
        pellizco(factor, (1 - factor) * 100)
        actualizar()

    texto_modo = ft.Text(modos["rotacion"][1])

    def cambiar_modo(clave):
        def manejador(e):
            estado["modo"] = clave
            texto_modo.value = modos[clave][1]
            texto_modo.update()
        return manejador

    botones = [ft.TextButton(modos[c][0], on_click=cambiar_modo(c)) for c in modos]

    def reiniciar(e):
        parametros.update(inicial)
        actualizar()

    def redimensionar(e):
        lado = calcular_lado()
        lienzo.width = lado
        lienzo.height = lado
        actualizar()

    page.on_resize = redimensionar

    figura = ft.GestureDetector(
        content=lienzo,
        mouse_cursor=ft.MouseCursor.MOVE,
        on_scale_update=gesto,
        on_scale_end=terminar,
        on_scroll=rueda,
    )

    page.add(
        ft.Row(
            wrap=True,
            spacing=20,
            controls=[
                figura,
                ft.Container(
                    width=300,
                    content=ft.Column([
                        texto_modo,
                        ft.Row(botones, wrap=True, spacing=0),
                        ft.TextButton("Reiniciar", on_click=reiniciar),
                    ]),
                ),
            ],
        )
    )
    actualizar()


ft.run(main)