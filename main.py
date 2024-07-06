import flet as ft
from assets.custom import Album, Barra_Inferior, Progreso
from assets.vista_canciones import vista_canciones
import os
import json
from math import pi

with open("assets/ruta.json", "r") as f:
    data = json.load(f)
ruta = os.getcwd()
print(ruta)
reproducir = r"C:\Users\victo\Music\MUSICA\Albumes"
album = data["Album"]
cancion = data["Cancion"]
artista = data["Artista"]
imagen =data["Imagen"]
url = reproducir + "\\" + album + "\\" + cancion

audio1 = ft.Audio(
        src=url,
        autoplay=True,
        volume=1,
        balance=0,
        on_loaded=lambda _: print(f"Loaded: {url}"),
        on_duration_changed=lambda _: print("Ha cambiado la duracion"),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )


def obtener_cancion():
    global url
    final = url
    print(f"ESTE ES LA RUTA: {final}")
    return final

eleccion = obtener_cancion()


def main(page: ft.Page):
    page.title = "Groovy Player 🎵"
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.DEEP_PURPLE,
    )
    page.fonts = {
        "Archivo Black": "https://raw.githubusercontent.com/google/fonts/master/ofl/archivoblack/ArchivoBlack-Regular.ttf"
    }
    page.window.maximized = True
    progreso = Progreso(audio1, page)
    page.overlay.append(Barra_Inferior(imagen, cancion, artista, progreso, page))
    grilla = ft.GridView(
        [],
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )
    try:
        for album in os.listdir(reproducir):
            ruta_completa = os.path.join(reproducir, album)
            if "_" in album:
                nombredelalbum, nombredelartista = album.split("_", 1)
            else:
                nombredelalbum = album
                nombredelartista = "Desconocido"
            grilla.controls.append(Album(nombredelalbum, nombredelartista, album, imagen, page))
            if os.path.isdir(ruta_completa):
                print(album)
    except FileNotFoundError:
        print(f"El directorio '{reproducir}' no existe.")
    except PermissionError:
        print(f"No tienes permisos para acceder al directorio '{reproducir}'.")

    inicio = ft.Container(
        ft.Column(
            [
                grilla,
            ]
        )
    )

    def route_change(route, valor=None):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(ft.Row([ft.Text("Empty")], height=60)),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "Groovy Music",
                                    size=30,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.WHITE,
                                    font_family="Archivo Black",
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            height=60
                        ),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.top_right,
                            colors=["#6e20cf", "#1d0b72"],
                        ),
                        border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=20, bottom_right=20),
                    ),
                    inicio,
                ],
            )
        )
        if page.route == "/canciones":
            page.views.append(
                ft.View(
                    "/canciones",
                    [ft.Container(ft.Row([ft.Text("Empty")], height=60)),
                    vista_canciones(page)],
                )
            )
        
        page.update()

    def view_pop(view):
        try:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        except:
            print("ERROR INESPERADO")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")
    
    page.update()

ft.app(target=main)
