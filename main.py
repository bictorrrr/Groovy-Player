import flet as ft
from assets.custom import Album
from assets.vista_canciones import vista_canciones
import os
import json


with open('assets/ruta.json', 'r') as f:
    data = json.load(f)
ruta = os.getcwd()
print(ruta)
reproducir = r"C:\Users\victo\Music\MUSICA\Albumes"
album = data['Album']
cancion = data['Cancion']
url = reproducir+"\\"+album+"\\"+cancion
def obtener_cancion():
    global url
    final = url
    print(f"ESTE ES LA RUTA: {final}")
    return final



eleccion = obtener_cancion()
audio1 = ft.Audio(
        src=eleccion,
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )

def main(page: ft.Page):
    page.title = "Groovy Player 🎵"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.DEEP_PURPLE,
    )

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
            if '_' in album:
                nombredelalbum, nombredelartista = album.split('_', 1)
            else:
                nombredelalbum = album
                nombredelartista = 'Desconocido'
            grilla.controls.append(Album(nombredelalbum, album, page, audio1))
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
    page.overlay.append(audio1)

    def route_change(route, valor=None):
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Container(ft.Row([
                            ft.Text("Inicio", 
                                    size=30,
                                    weight=ft.FontWeight.BOLD, 
                                    color=ft.colors.WHITE, 
                                    font_family="Consolas" )
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER), 
                        bgcolor=ft.colors.DEEP_PURPLE,
                        border_radius=20),
                        inicio,
                        
                    ],
                )
            )
            if page.route == "/canciones":
                page.views.append(
                    ft.View(
                        "/canciones",
                        [
                            vista_canciones(page, audio1)
                        ],
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



ft.app(target=main)
