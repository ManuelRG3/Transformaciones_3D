import flet as ft


# ───────────── PALETA ─────────────
class Colores:
    FONDO = "#0B0F1A"
    FONDO_2 = "#111A38"
    SUPERFICIE = "#131A2A"
    SUPERFICIE_ALT = "#1B2438"
    FONDO_LIENZO = "#0E1424"
    BORDE = "#2A3550"

    PRIMARIO = "#6C5CE7"
    PRIMARIO_CLARO = "#A29BFE"
    ACENTO = "#00D1B2"

    TEXTO = "#E8ECF8"
    TEXTO_SUAVE = "#8B96B3"
    ERROR = "#FF5C7A"


class Espacio:
    XS, S, M, L, XL = 4, 8, 16, 24, 32


class Radio:
    S, M, L = 8, 12, 20


ICONOS = {
    "traslacion": ft.Icons.OPEN_WITH,
    "escalamiento": ft.Icons.ASPECT_RATIO,
    "rotacion": ft.Icons.THREED_ROTATION,
    "sesgado": ft.Icons.TRANSFORM,
}


# ───────────── AUXILIARES ─────────────
def _alfa(color, opacidad):
    return ft.Colors.with_opacity(opacidad, color)


def _relleno(horizontal, vertical):
    return ft.Padding(left=horizontal, right=horizontal, top=vertical, bottom=vertical)


def _borde(color, grosor=1):
    lado = ft.BorderSide(grosor, color)
    return ft.Border(left=lado, right=lado, top=lado, bottom=lado)


def _degradado_primario():
    return ft.LinearGradient(
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(1, 1),
        colors=[Colores.PRIMARIO, "#8E7CFF"],
    )


# ───────────── TEMA GLOBAL ─────────────
def aplicar_tema(page: ft.Page, titulo: str):
    page.title = titulo
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = Colores.FONDO
    page.padding = 0
    page.theme = ft.Theme(
        use_material3=True,
        color_scheme=ft.ColorScheme(
            primary=Colores.PRIMARIO,
            secondary=Colores.ACENTO,
            surface=Colores.SUPERFICIE,
            error=Colores.ERROR,
        ),
    )


def calcular_lado(page: ft.Page):
    ancho = page.width or 1000
    alto = page.height or 800
    return int(max(250, min(520, ancho - 90, alto - 190)))


# ───────────── ENCABEZADO ─────────────
def encabezado(titulo, subtitulo):
    logo = ft.Container(
        width=52,
        height=52,
        border_radius=Radio.M,
        gradient=_degradado_primario(),
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(blur_radius=20, color=_alfa(Colores.PRIMARIO, 0.5),
                            offset=ft.Offset(0, 6)),
        content=ft.Icon(ft.Icons.VIEW_IN_AR, color="white", size=28),
    )
    return ft.Row(
        spacing=Espacio.M,
        controls=[
            logo,
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(titulo, size=28, weight=ft.FontWeight.W_800, color=Colores.TEXTO),
                    ft.Text(subtitulo, size=13, color=Colores.TEXTO_SUAVE),
                ],
            ),
        ],
    )


# ───────────── LIENZO ─────────────
def marco_lienzo(contenido):
    return ft.Container(
        content=contenido,
        padding=Espacio.S,
        border=_borde(Colores.BORDE),
        border_radius=Radio.L,
        gradient=ft.RadialGradient(
            center=ft.Alignment(0, 0),
            radius=0.9,
            colors=["#16203D", Colores.FONDO_LIENZO],
        ),
        shadow=ft.BoxShadow(blur_radius=40, color=_alfa("#000000", 0.5),
                            offset=ft.Offset(0, 16)),
    )


# ───────────── BOTONES DE MODO ─────────────
def _contenido_modo(clave, titulo, activo):
    color = "white" if activo else Colores.TEXTO_SUAVE
    return ft.Row(
        spacing=12,
        controls=[
            ft.Icon(ICONOS[clave], size=20, color=color),
            ft.Text(titulo, size=14, weight=ft.FontWeight.W_600, color=color),
        ],
    )


def _aspecto_modo(activo):
    if activo:
        return dict(
            gradient=_degradado_primario(),
            bgcolor=None,
            border=_borde(_alfa("#FFFFFF", 0.15)),
            shadow=ft.BoxShadow(blur_radius=20, color=_alfa(Colores.PRIMARIO, 0.45),
                                offset=ft.Offset(0, 6)),
        )
    return dict(
        gradient=None,
        bgcolor=Colores.SUPERFICIE_ALT,
        border=_borde(Colores.BORDE),
        shadow=None,
    )


def crear_botones_modo(modos, activo, al_elegir):
    """Devuelve {clave: boton}. `al_elegir(clave)` debe regresar el manejador del click."""
    botones = {}
    for clave, datos in modos.items():
        botones[clave] = ft.Container(
            data=(clave, datos[0]),
            content=_contenido_modo(clave, datos[0], clave == activo),
            padding=_relleno(18, 9),
            border_radius=Radio.M,
            ink=True,
            animate=200,
            on_click=al_elegir(clave),
            **_aspecto_modo(clave == activo),
        )
    return botones


def resaltar(botones, activo):
    for clave, boton in botones.items():
        _, titulo = boton.data
        es_activo = clave == activo
        boton.content = _contenido_modo(clave, titulo, es_activo)
        for atributo, valor in _aspecto_modo(es_activo).items():
            setattr(boton, atributo, valor)
        boton.update()


def boton_secundario(texto, on_click=None):
    return ft.Container(
        padding=_relleno(18, 12),
        border_radius=Radio.M,
        border=_borde(Colores.ACENTO),
        bgcolor=_alfa(Colores.ACENTO, 0.08),
        ink=True,
        on_click=on_click,
        alignment=ft.Alignment(0, 0),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.REFRESH, size=18, color=Colores.ACENTO),
                ft.Text(texto, size=14, weight=ft.FontWeight.W_600, color=Colores.ACENTO),
            ],
        ),
    )


# ───────────── TEXTOS Y CHIPS ─────────────
def texto_descripcion(valor):
    return ft.Text(valor, size=13, color=Colores.TEXTO_SUAVE, expand=True)


def _chip(icono, texto):
    return ft.Container(
        padding=_relleno(10, 6),
        border_radius=20,
        bgcolor=Colores.SUPERFICIE_ALT,
        border=_borde(Colores.BORDE),
        content=ft.Row(
            spacing=6,
            tight=True,
            controls=[
                ft.Icon(icono, size=14, color=Colores.PRIMARIO_CLARO),
                ft.Text(texto, size=12, color=Colores.TEXTO_SUAVE),
            ],
        ),
    )


def _etiqueta(texto):
    return ft.Text(texto.upper(), size=11, weight=ft.FontWeight.W_700,
                   color=Colores.TEXTO_SUAVE)


# ───────────── PANEL Y PANTALLA ─────────────
def panel_controles(descripcion, botones, boton_reinicio):
    info = ft.Container(
        padding=12,
        border_radius=Radio.M,
        bgcolor=_alfa(Colores.ACENTO, 0.07),
        border=_borde(_alfa(Colores.ACENTO, 0.25)),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Icon(ft.Icons.INFO_OUTLINE, size=18, color=Colores.ACENTO),
                descripcion,
            ],
        ),
    )
    return ft.Container(
        width=340,
        padding=20,
        border_radius=Radio.L,
        bgcolor=_alfa(Colores.SUPERFICIE, 0.9),
        border=_borde(Colores.BORDE),
        shadow=ft.BoxShadow(blur_radius=40, color=_alfa("#000000", 0.4),
                            offset=ft.Offset(0, 16)),
        content=ft.Column(
            spacing=12,
            controls=[
                _etiqueta("Modo de transformación"),
                ft.Column(list(botones.values()), spacing=6),
                ft.Divider(color=Colores.BORDE, height=4),
                info,
                ft.Row(
                    wrap=True,
                    spacing=Espacio.S,
                    run_spacing=Espacio.S,
                    controls=[
                        _chip(ft.Icons.TOUCH_APP, "Arrastrar"),
                        _chip(ft.Icons.PINCH, "Pellizcar"),
                        _chip(ft.Icons.MOUSE, "Rueda"),
                    ],
                ),
                boton_reinicio,
            ],
        ),
    )


def pantalla(encabezado_, figura, panel):
    return ft.Container(
        expand=True,
        padding=Espacio.L,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[Colores.FONDO, Colores.FONDO_2, Colores.FONDO],
        ),
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=Espacio.L,
            controls=[
                encabezado_,
                ft.Row(
                    wrap=True,
                    spacing=Espacio.L,
                    run_spacing=Espacio.L,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[figura, panel],
                ),
            ],
        ),
    )