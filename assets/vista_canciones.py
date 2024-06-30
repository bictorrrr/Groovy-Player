import flet as ft
import json
import os
from assets.metodos import reproducir_cancion

reproducir = r"C:\Users\victo\Music\MUSICA\Albumes"

def mostrar_canciones(page: ft.Page, canciones_listview: ft.ListView, audio1: ft.Audio):
    with open('assets/ruta.json', 'r') as f:
        data = json.load(f)
    
    album = data['Album']
    path = os.path.join(reproducir, album)
    
    if os.path.isdir(path):
        numero = 1
        for archivo in os.listdir(path):
            if archivo.endswith(".flac"):
                cancion_nombre = os.path.splitext(archivo)[0]
                canciones_listview.controls.append(ft.ListTile(leading=ft.Text(f"{numero}"),title=ft.Text(cancion_nombre), trailing=ft.IconButton(icon=ft.icons.PLAY_ARROW, bgcolor=ft.colors.DEEP_PURPLE, icon_color=ft.colors.WHITE, on_click= lambda _, cancion = cancion_nombre: reproducir_cancion(cancion, page))))
                numero += 1
    
    page.update()

def vista_canciones(page: ft.Page, audio1: ft.Audio):
    canciones_listview = ft.ListView([
        ft.Text("CANCIONNNN")
    ])
    
    mostrar_canciones(page, canciones_listview, audio1)
    
    canciones = ft.Column([
        ft.Row([
            ft.TextButton("Regresar", on_click=lambda _: page.go("/"))
        ]),
        canciones_listview
    ])
    return canciones