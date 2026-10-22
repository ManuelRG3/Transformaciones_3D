import flet as ft
from Controlador.Escena import calcular_escena
from Interfaz.Lienzo import crear_lienzo, dibujar

sensibilidad = 0.5
inicial = {"rx" : 25, "ry" : 30}

def main(page: ft.Page):
    page.title = "Transformacion 3D"
    page.scroll = ft.ScrollMode.AUTO
    parametros = dict(inicial)
    ultimo = {"x" : None, "y" : None}

    def calcular_lado():
        ancho = page.width or 500
        return int (max(250, min(500, ancho - 40)))

    lienzo = crear_lienzo(calcular_lado())

    def actualizar():
        puntos, aristas, matriza = calcular_escena(parametros)
        dibujar(lienzo, puntos, aristas)

    def arrastrar(e):
        x, y = e.local_position.x, e.local_position.y
        if ultimo["x"] is not None:
            parametros["ry"] += (x - ultimo["x"]) * sensibilidad
            parametros["rx"] += (y - ultimo["y"]) * sensibilidad
            actualizar()
        ultimo["x"], ultimo["y"] = x, y

    def soltar(e):
        ultimo["x"] = None
        ultimo["y"] = None

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
        mouse_cursor= ft.MouseCursor.MOVE, 
        on_pan_update= arrastrar, 
        on_pan_end= soltar,
    )

    page.add(
        ft.Row(
            wrap=True, 
            spacing=20, 
            controls=[
                figura, 
                ft.Container(width=300,
                             content=ft.Column([
                                 ft.Text("Arrastrar la figura para rotarla"),
                                 ft.TextButton("Reiniciar", on_click=reiniciar)
                             ]))
            ]
        )
    )
    actualizar()
    
ft.run(main)