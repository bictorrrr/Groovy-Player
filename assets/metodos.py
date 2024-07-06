import flet as ft
import os
import json
from assets.custom import Barra_Inferior, Progreso

reproducir = r"C:\Users\victo\Music\MUSICA\Albumes"
album = ""
cancion = ""

def regresar(page: ft.Page,contenedor: ft.Container):
    page.go("/")
    


def reproducir_cancion(eleccion, page: ft.Page, contenedor: ft.Container):
    global album
    global cancion
    global url
    print(f"LA CANCION SERAAAA: {eleccion}")
    with open("assets/ruta.json", "r") as f:
        data = json.load(f)
    data["Cancion"] = eleccion
    with open("assets/ruta.json", "w") as f:
        json.dump(data, f)
    imagen = data['Imagen']
    cancion_act = data['Cancion']
    artista = data['Artista']
    album = data["Album"]

    cancion = eleccion + ".flac"
    url = os.path.join(reproducir, album, cancion)

    # Buscar y eliminar el componente de audio existente si existe
    for component in page.overlay:
        if isinstance(component, ft.Audio):
            page.overlay.remove(component)
            break
    for component in page.overlay:
        if isinstance(component, ft.Container):
            page.overlay.remove(component)
            break
    
    
    # Crear y añadir el nuevo componente de audio
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
    progreso = Progreso(audio1, page)
    barra = Barra_Inferior(imagen, cancion_act, artista, progreso, page)
    
    page.overlay.append(audio1)
    page.overlay.append(progreso)
    page.overlay.append(barra)
    page.update()