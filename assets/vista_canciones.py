import flet as ft
import json
import os
from assets.metodos import reproducir_cancion, regresar
from assets.custom import Barra_Inferior, Progreso

reproducir = r"C:\Users\victo\Music\MUSICA\Albumes"
ruta = r"C:\Users\victo\Music\MUSICA\Album_covers"

contenedor_barra = ft.Container()

def bg_color(e):
    e.control.gradient = (
        ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#6e20cf", "#1d0b72"],
        )
        if e.data == "true"
        else ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#151218", "#151218"],
        )
    )
    e.control.update()

def mostrar_canciones(page: ft.Page, canciones_listview: ft.ListView):
    with open("assets/ruta.json", "r") as f:
        data = json.load(f)

    album = data["Album"]
    path = os.path.join(reproducir, album)

    if os.path.isdir(path):
        numero = 1
        for archivo in os.listdir(path):
            if archivo.endswith(".flac"):
                cancion_nombre = os.path.splitext(archivo)[0]
                id_cancion, cancion = cancion_nombre.split('_')
                canciones_listview.controls.append(
                    ft.Row(
                        [
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.icons.MUSIC_NOTE),
                                                ft.Text(cancion),
                                            ]
                                        ),
                                        ft.Container(
                                            ft.Icon(ft.icons.PLAY_ARROW, color=ft.colors.WHITE),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    width=page.window.width-30,
                                    height=50,
                                ),
                                on_click=lambda _, cancion=cancion_nombre: reproducir_cancion(
                                    cancion, page, contenedor_barra
                                ),
                                border_radius=10,
                                on_hover=bg_color,
                            ),
                        ],
                        width=page.window.width-30,
                        height=30,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
                numero += 1

    page.update()

def vista_canciones(page: ft.Page):
    canciones_listview = ft.ListView([])
    mostrar_canciones(page, canciones_listview)
    with open("assets/ruta.json", "r") as f:
        data = json.load(f)
    data_album = data["Album"]
    if "_" in data_album:
        nombredelalbum, nombredelartista = data_album.split("_", 1)
    canciones = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Image(
                                src=ruta + "/" + nombredelalbum + ".jpg",
                                width=150,
                                height=150,
                            )
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Text(
                                            nombredelalbum,
                                            size=30,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.WHITE,
                                            font_family="Archivo Black",
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    width=page.window.width - 197,
                                    height=120
                                ),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.top_right,
                                    colors=["#641ec4", "#1d0b72"],
                                ),
                                border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=20, bottom_right=20),
                                
                            ),
                            ft.Container(ft.Row(
                                [
                                    ft.Stack(
                                        [
                                            ft.Text(
                                                spans=[
                                                    ft.TextSpan(
                                                        f"De: {nombredelartista}",
                                                        ft.TextStyle(
                                                            size=20,
                                                            weight=ft.FontWeight.BOLD,
                                                            foreground=ft.Paint(
                                                                color=ft.colors.DEEP_PURPLE,
                                                                stroke_width=6,
                                                                stroke_join=ft.StrokeJoin.ROUND,
                                                                style=ft.PaintingStyle.STROKE,
                                                            ),
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            ft.Text(
                                                spans=[
                                                    ft.TextSpan(
                                                        f"De: {nombredelartista}",
                                                        ft.TextStyle(
                                                            size=20,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=ft.colors.WHITE,
                                                        ),
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        
                    )
                ]
            ),
            ft.Text(
                "Canciones",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                font_family="Archivo Black",
            ),
            canciones_listview,
            ft.FilledButton(
                "Regresar",
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: regresar(page, contenedor_barra)
            ),
            contenedor_barra
        ]
    )

    return ft.Container(
        canciones,
        expand=True,
    )
