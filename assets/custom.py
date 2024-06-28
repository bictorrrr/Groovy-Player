import flet as ft
import json

def guardar_album_y_navegar(album, page, audio1):
    # Cargar el archivo JSON
    with open('assets/ruta.json', 'r') as f:
        data = json.load(f)
    # Modificar el valor de la variable 'grupo'
    data['Album'] = album       
    # Guardar los cambios en el archivo JSON
    with open('assets/ruta.json', 'w') as f:
        json.dump(data, f)
    # Navegar a "/cartas_vista"
    page.go("/canciones")

class Album(ft.Container):
    def __init__(self, nombre,album, page, audio1):
        super().__init__()
        self.bgcolor = ft.colors.BLACK12
        self.content = ft.Column(
            [
                ft.Row([ft.Text(f"{nombre}")], alignment=ft.MainAxisAlignment.CENTER),
                ft.FloatingActionButton("Ver album", width=300, on_click= lambda _: guardar_album_y_navegar(album, page, audio1)),
            ]
        )
        self.border_radius = 20
