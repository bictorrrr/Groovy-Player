import flet as ft
import json

ruta = r"C:\Users\victo\Music\MUSICA\Album_covers"


def guardar_album_y_navegar(album, page, audio1):
    # Cargar el archivo JSON
    with open("assets/ruta.json", "r") as f:
        data = json.load(f)
    # Modificar el valor de la variable 'grupo'
    data["Album"] = album
    # Guardar los cambios en el archivo JSON
    with open("assets/ruta.json", "w") as f:
        json.dump(data, f)
    # Navegar a "/cartas_vista"
    page.go("/canciones")


class Album(ft.Container):
    def __init__(self, nombre, album, page, audio1):
        super().__init__()
        self.bgcolor = ft.colors.BLACK12
        self.content = ft.Stack(
            [
                ft.Image(
                    src=ruta + "/" + nombre + ".jpg",
                )
            ]
        )
        self.border_radius = 20
        self.data = "true"  # Inicializar self.data

        # funciones de hover
        self.on_hover = self.hover_handler(nombre, album, page, audio1)

    def hover_handler(self, nombre, album, page, audio1):
        def handler(event):
            if self.data == "true":
                self.mostrar_para_abrir(nombre, album, page, audio1)
                self.data = "false"
            else:
                self.quitar_para_abrir(page)
                self.data = "true"

        return handler

    def mostrar_para_abrir(self, nombre, album, page, audio1):
        # Buscar y eliminar cualquier FloatingActionButton existente
        existing_button = None
        for control in self.content.controls:
            if isinstance(control, ft.FloatingActionButton):
                existing_button = control
                break

        if existing_button:
            self.content.controls.remove(existing_button)
        
        # Agregar el nuevo FloatingActionButton
        self.content.controls.append(
            ft.Container( ft.Container(
                ft.Container(ft.Row([
                    ft.Text(nombre, font_family="Archivo Black", size=10),
                    ft.Container(
                        ft.Icon(ft.icons.PLAY_ARROW, color=ft.colors.WHITE),
                        gradient=ft.RadialGradient(
                                    colors=["#6e20cf", "#1d0b72"],
                                ),
                        shape=ft.BoxShape.CIRCLE,
                        width=40,
                        height=40
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)), bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK)
            ),alignment=ft.alignment.bottom_center,
            on_click=lambda _: guardar_album_y_navegar(album, page, audio1),)
        )
        page.update()

    def quitar_para_abrir(self, page):
        if len(self.content.controls) > 1:  # Verifica que haya controles para quitar
            self.content.controls.pop()
            page.update()
