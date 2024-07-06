import flet as ft
import json
import os

ruta = r"C:\Users\victo\Music\MUSICA\Album_covers"




def guardar_album_y_navegar(album, artista, imagen, page):
    # Cargar el archivo JSON
    with open("assets/ruta.json", "r") as f:
        data = json.load(f)
    # Modificar el valor de la variable 'grupo'
    data["Album"] = album
    data["Artista"] = artista
    data_album = data["Album"]
    if "_" in data_album:
        nombredelalbum, nombredelartista = data_album.split("_", 1)
    imagen = nombredelalbum
    data["Imagen"] = imagen
    # Guardar los cambios en el archivo JSON
    with open("assets/ruta.json", "w") as f:
        json.dump(data, f)
    # Navegar a "/cartas_vista"
    page.go("/canciones")

class Barra_Inferior(ft.BottomAppBar):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            cls._instance.clean_up()
        cls._instance = super(Barra_Inferior, cls).__new__(cls)
        return cls._instance

    def __init__(self, imagen: str, nombrecancion: str, artista: str, progreso: ft.Control, page: ft.Page):
        if hasattr(self, 'initialized') and self.initialized:
            return
        self.initialized = True

        super().__init__()
        ruta_imagen = os.path.join(ruta, imagen + ".jpg")
        print(f"Ruta de la imagen: {ruta_imagen}")
        
        # Verifica si la imagen existe
        if not os.path.exists(ruta_imagen):
            print(f"Error: La imagen '{ruta_imagen}' no existe.")
            ruta_imagen = "default.jpg"  # Usa una imagen por defecto si la imagen no se encuentra
        self.shape = ft.NotchShape.CIRCULAR
        self.padding = ft.Padding(left=10,right=10,top=0,bottom=0)
        self.bgcolor= ft.colors.BACKGROUND
        self.content = ft.Container(ft.Row(
            [
                ft.Row(
                    [
                        ft.Image(
                            src=ruta_imagen,
                            width=55,
                            height=55
                        ),
                        ft.Column(
                            [
                                ft.Text(nombrecancion, width=80, max_lines=2),
                                ft.Text(artista)
                            ]
                        ),
                    ]
                ),
                ft.Column(
                    [
                        progreso,
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.icons.SKIP_PREVIOUS),
                                ft.IconButton(icon=ft.icons.PLAY_ARROW),
                                ft.IconButton(icon=ft.icons.SKIP_NEXT)
                            ], alignment=ft.MainAxisAlignment.CENTER)
                    ], width=page.window.width - 325
                ),
                ft.Row([
                    ft.IconButton(icon=ft.icons.VOLUME_UP, width=125)
                ],
                width=125
                )
            ]
        ), gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.top_right,
                            colors=["#6e20cf", "#1d0b72"],
                        ),)

    def clean_up(self):
        self.content.clean()
        self.update()
        
class Progreso(ft.ProgressBar):
    def __init__(self, audio : ft.Audio, page: ft.Page):
        super().__init__()
        self.value = 0.0
        self.color = ft.colors.WHITE
        self.bgcolor = ft.colors.BLACK12
        self.border_radius = 5
        self.audio = audio
        def actualizar_progreso(e):
            if self.audio.get_duration() > 0:
                self.value = self.audio.get_current_position() / self.audio.get_duration()
            page.update()
        self.audio.on_position_changed = actualizar_progreso
        

class Album(ft.Container):
    def __init__(self, nombre,artista, album, imagen, page):
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
        self.on_hover = self.hover_handler(nombre, artista, album, imagen, page)

    def hover_handler(self, nombre, artista, album, imagen, page):
        def handler(event):
            if self.data == "true":
                self.mostrar_para_abrir(nombre, artista, album, imagen, page)
                self.data = "false"
            else:
                self.quitar_para_abrir(page)
                self.data = "true"

        return handler

    def mostrar_para_abrir(self, nombre,artista, album, imagen, page):
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
            ft.Container(
                ft.Container(
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(nombre, font_family="Archivo Black", size=10),
                                ft.Container(
                                    ft.Icon(ft.icons.PLAY_ARROW, color=ft.colors.WHITE),
                                    gradient=ft.RadialGradient(
                                        colors=["#6e20cf", "#1d0b72"],
                                    ),
                                    shape=ft.BoxShape.CIRCLE,
                                    width=40,
                                    height=40,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ),
                    bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                ),
                alignment=ft.alignment.bottom_center,
                on_click=lambda _: guardar_album_y_navegar(album, artista, imagen, page),
            )
        )
        page.update()

    def quitar_para_abrir(self, page):
        if len(self.content.controls) > 1:  # Verifica que haya controles para quitar
            self.content.controls.pop()
            page.update()
