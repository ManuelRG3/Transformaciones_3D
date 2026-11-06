#concentra el aspecto visual: colores, tamaños, bordes, gradientes, etc. 
#y provee funciones para crear los controles de la interfaz.

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
    "perspectiva": ft.Icons.CAMERA_ALT,
}


# ───────────── AUXILIARES ─────────────
def _alfa(color, opacidad):
    return ft.Colors.with_opacity(opacidad, color)


def _relleno(horizontal, vertical):
    return ft.Padding(
        left=horizontal,
        right=horizontal,
        top=vertical,
        bottom=vertical
    )


def _borde(color, grosor=1):
    lado = ft.BorderSide(grosor, color)

    return ft.Border(
        left=lado,
        right=lado,
        top=lado,
        bottom=lado
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
        bgcolor=Colores.PRIMARIO,
        border_radius=Radio.M,
        alignment=ft.Alignment(0, 0),
        content=ft.Icon(
            ft.Icons.VIEW_IN_AR,
            color="white",
            size=28
        ),
    )

    return ft.Row(
        spacing=Espacio.M,
        controls=[
            logo,

            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        titulo,
                        size=28,
                        weight=ft.FontWeight.W_800,
                        color=Colores.TEXTO
                    ),

                    ft.Text(
                        subtitulo,
                        size=13,
                        color=Colores.TEXTO_SUAVE
                    ),
                ],
            ),
        ],
    )


# ───────────── LIENZO ─────────────
def marco_lienzo(contenido):

    return ft.Container(
        content=contenido,
        padding=Espacio.S,
        bgcolor=Colores.FONDO_LIENZO,
        border=_borde(Colores.BORDE),
        border_radius=Radio.L,
    )


# ───────────── BOTONES DE MODO ─────────────
def _contenido_modo(clave, titulo, activo):

    color = "white" if activo else Colores.TEXTO_SUAVE

    return ft.Row(
        spacing=12,
        controls=[
            ft.Icon(
                ICONOS[clave],
                size=20,
                color=color
            ),

            ft.Text(
                titulo,
                size=14,
                weight=ft.FontWeight.W_600,
                color=color
            ),
        ],
    )


def _aspecto_modo(activo):

    if activo:
        return dict(
            gradient=None,
            bgcolor=Colores.PRIMARIO,
            border=_borde(Colores.BORDE),
            shadow=None,
        )

    return dict(
        gradient=None,
        bgcolor=Colores.SUPERFICIE_ALT,
        border=_borde(Colores.BORDE),
        shadow=None,
    )


def crear_botones_modo(modos, activo, al_elegir):

    """Devuelve {clave: boton}."""

    botones = {}

    for clave, datos in modos.items():

        botones[clave] = ft.Container(
            data=(clave, datos[0]),

            content=_contenido_modo(
                clave,
                datos[0],
                clave == activo
            ),

            padding=_relleno(18, 9),
            border_radius=Radio.M,
            ink=True,

            on_click=al_elegir(clave),

            **_aspecto_modo(clave == activo),
        )

    return botones


def resaltar(botones, activo):

    for clave, boton in botones.items():

        _, titulo = boton.data

        es_activo = clave == activo

        boton.content = _contenido_modo(
            clave,
            titulo,
            es_activo
        )

        for atributo, valor in _aspecto_modo(es_activo).items():
            setattr(boton, atributo, valor)

        boton.update()


# ───────────── BOTÓN SECUNDARIO ─────────────
def boton_secundario(texto, on_click=None):

    return ft.Container(
        padding=_relleno(18, 12),
        border_radius=Radio.M,
        border=_borde(Colores.ACENTO),
        bgcolor=Colores.SUPERFICIE_ALT,
        ink=True,
        on_click=on_click,
        alignment=ft.Alignment(0, 0),

        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,

            controls=[
                ft.Icon(
                    ft.Icons.REFRESH,
                    size=18,
                    color=Colores.ACENTO
                ),

                ft.Text(
                    texto,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=Colores.ACENTO
                ),
            ],
        ),
    )


# ───────────── SELECTOR DE FIGURAS ─────────────
def _aspecto_figura(activa):

    if activa:
        return dict(
            gradient=None,
            bgcolor=Colores.PRIMARIO,
            border=_borde(Colores.BORDE),
        )

    return dict(
        gradient=None,
        bgcolor=Colores.SUPERFICIE_ALT,
        border=_borde(Colores.BORDE),
    )


def crear_selector_figuras(nombres, activa, al_elegir):

    """Devuelve {nombre: chip}."""

    chips = {}

    for nombre in nombres:

        es_activa = nombre == activa

        chips[nombre] = ft.Container(

            content=ft.Text(
                nombre,
                size=12,
                weight=ft.FontWeight.W_600,
                color="white" if es_activa else Colores.TEXTO_SUAVE
            ),

            padding=_relleno(12, 7),
            border_radius=20,
            ink=True,

            on_click=al_elegir(nombre),

            **_aspecto_figura(es_activa),
        )

    return chips


def resaltar_figura(chips, activa):

    for nombre, chip in chips.items():

        es_activa = nombre == activa

        chip.content.color = (
            "white" if es_activa
            else Colores.TEXTO_SUAVE
        )

        for atributo, valor in _aspecto_figura(es_activa).items():
            setattr(chip, atributo, valor)

        chip.update()


# ───────────── TEXTOS ─────────────
def texto_descripcion(valor):

    return ft.Text(
        valor,
        size=13,
        color=Colores.TEXTO_SUAVE,
        expand=True
    )


def _etiqueta(texto):

    return ft.Text(
        texto.upper(),
        size=11,
        weight=ft.FontWeight.W_700,
        color=Colores.TEXTO_SUAVE
    )


# ───────────── PANEL Y PANTALLA ─────────────
def panel_controles(
    descripcion,
    botones,
    boton_reinicio,
    chips_figuras=None
):

    info = ft.Container(

        padding=12,
        border_radius=Radio.M,
        bgcolor=Colores.SUPERFICIE_ALT,
        border=_borde(Colores.BORDE),

        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=10,

            controls=[
                ft.Icon(
                    ft.Icons.INFO_OUTLINE,
                    size=18,
                    color=Colores.ACENTO
                ),

                descripcion,
            ],
        ),
    )

    bloque_figuras = []

    if chips_figuras:

        bloque_figuras = [

            _etiqueta("Figura"),

            ft.Row(
                list(chips_figuras.values()),
                wrap=True,
                spacing=Espacio.S,
                run_spacing=Espacio.S
            ),

            ft.Divider(
                color=Colores.BORDE,
                height=4
            ),
        ]

    return ft.Container(

        width=340,
        padding=20,
        border_radius=Radio.L,
        bgcolor=Colores.SUPERFICIE,
        border=_borde(Colores.BORDE),

        content=ft.Column(

            spacing=12,

            controls=[

                *bloque_figuras,

                _etiqueta("Modo de transformación"),

                ft.Column(
                    list(botones.values()),
                    spacing=6
                ),

                ft.Divider(
                    color=Colores.BORDE,
                    height=4
                ),

                info,

                boton_reinicio,
            ],
        ),
    )


# ───────────── PANTALLA PRINCIPAL ─────────────
def pantalla(encabezado_, figura, panel):

    return ft.Container(

        expand=True,
        padding=Espacio.L,
        bgcolor=Colores.FONDO,

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

                    controls=[
                        figura,
                        panel
                    ],
                ),
            ],
        ),
    )