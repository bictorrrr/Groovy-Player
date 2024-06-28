import flet as ft
import os
import json

reproducir = r"\\192.168.1.250\users\MUSICA\Albumes"
album = ""
cancion = ""

def reproducir_cancion(eleccion, page: ft.Page):
    global album
    global cancion
    global url
    print(f"LA CANCION SERAAAA: {eleccion}")
    with open('assets/ruta.json', 'r') as f:
        data = json.load(f)
    data['Cancion'] = eleccion
    with open('assets/ruta.json', 'w') as f:
        json.dump(data, f)

    album = data['Album']
    cancion = eleccion + ".flac"
    url = os.path.join(reproducir, album, cancion)

    # Buscar y eliminar el componente de audio existente si existe
    for component in page.overlay:
        if isinstance(component, ft.Audio):
            page.overlay.remove(component)
            break

    # Crear y añadir el nuevo componente de audio
    audio1 = ft.Audio(
        src=url,
        autoplay=True,
        volume=1,
        balance=0,
        on_loaded=lambda _: print(f"Loaded: {url}"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
    page.overlay.append(audio1)
    page.update()
