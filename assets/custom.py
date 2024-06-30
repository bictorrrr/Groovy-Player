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
    def __init__(self, nombre, album, page, audio1):
        super().__init__()
        self.bgcolor = ft.colors.BLACK12
        self.content = ft.Column(
            [
                ft.Row([ft.Text(f"{nombre}")], alignment=ft.MainAxisAlignment.CENTER),
            ]
        )
        self.border_radius = 20
        self.data = "true"  # Asegúrate de inicializar self.data

        # Asigna las funciones de hover
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
            ft.FloatingActionButton("Ver álbum", width=300, on_click=lambda _: guardar_album_y_navegar(album, page, audio1))
        )
        page.update()

    def quitar_para_abrir(self, page):
        if len(self.content.controls) > 1:  # Verifica que haya controles para quitar
            self.content.controls.pop()
            page.update()
