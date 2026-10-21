import flet as ft
from Controlador.Escena import calcular_escena
from Interfaz.Lienzo import crear_lienzo, dibujar

def main(page: ft.Page):
    page.title = "Transformacion 3D"
    page.scroll = ft.ScrollMode.AUTO
    parametros = {"ry": 30}

    def calcular_lado():
        ancho = page.width or 500
        return int (max(250, min(500, ancho - 40)))

    lienzo = crear_lienzo(calcular_lado())

    def actualizar():
        puntos, aristas, matriza = calcular_escena(parametros)
        dibujar(lienzo, puntos, aristas)

    def cambiar_ry(e):
        parametros["ry"] = e.control.value
        actualizar()

    def redimensionar(e):
        lado = calcular_lado()
        lienzo.width = lado
        lienzo.height = lado
        actualizar()

    page.on_resize = redimensionar

    page.add(
        ft.Row(
            wrap=True, spacing=20, controls=[
                lienzo, ft.Container(width=300, content=ft.Column([
                    ft.Text("Rotacion en Y (grados)"), ft.Slider(min=0, max=360, value=30, on_change=cambiar_ry),]),
                                    ),
            ],
        )
    )
    actualizar()
    
ft.run(main)