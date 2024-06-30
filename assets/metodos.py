import flet as ft
import os
import json

reproducir = r"C:\Users\victo\Music\MUSICA\Albumes"
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
    progreso = ft.ProgressBar(value=0.0, color=ft.colors.RED_800, bgcolor=ft.colors.GREEN_500)
    # Crear y añadir el nuevo componente de audio
    audio1 = ft.Audio(
        src=url,
        autoplay=True,
        volume=1,
        balance=0,
        on_loaded=lambda _: print(f"Loaded: {url}"),
        on_duration_changed=lambda _: print("Ha cambiado la duracion"),
        on_position_changed=lambda e: actualizar_progreso(e),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
    def actualizar_progreso(e):
        if audio1.get_duration() > 0:
            progreso.value = audio1.get_current_position() / audio1.get_duration()
        page.update()

    page.overlay.append(audio1)
    page.overlay.append(progreso)
    page.update()
