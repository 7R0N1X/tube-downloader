import os
from pytube import Playlist
import subprocess
import shlex
import sys

sys.stdout.reconfigure(encoding='utf-8')

def descargar_y_convertir_lista_de_reproduccion(url_lista, ruta_destino, calidad_deseada=320):
    try:
        # Crear objeto Playlist
        playlist = Playlist(url_lista)

        # Crear la carpeta de destino si no existe
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        # Iterar sobre cada video en la lista de reproducción
        for video in playlist.videos:
            try:
                # Obtener la mejor stream de audio disponible en formato mp4
                stream = video.streams.filter(only_audio=True, file_extension='mp4').first()

                # Si no hay streams en formato mp4, obtener cualquier stream de audio
                if not stream:
                    stream = video.streams.filter(only_audio=True).first()

                # Nombre del archivo
                filename = ''.join(['_' if ord(char) > 127 else char for char in video.title])

                # Descargar el audio
                ruta_temporal_audio = os.path.join(ruta_destino, f"{filename}.{stream.subtype}")

                # Verificar si el archivo ya existe.
                if os.path.exists(ruta_temporal_audio):
                    print(f"El archivo '{filename}.{stream.subtype}' ya existe. Sobrescribiendo.")

                stream.download(output_path=ruta_destino, filename=f"{filename}.{stream.subtype}")

                # Convertir de formato a mp3 usando ffmpeg
                ruta_salida_mp3 = os.path.join(ruta_destino, f"{filename}.mp3")
                comando = f'ffmpeg -y -i "{ruta_temporal_audio}" -b:a {calidad_deseada}k "{ruta_salida_mp3}"'
                
                # Redirigir la salida de FFmpeg a un objeto subprocess.PIPE
                proceso_ffmpeg = subprocess.Popen(shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Capturar y mostrar solo el resultado final
                salida_ffmpeg, _ = proceso_ffmpeg.communicate()
                print(salida_ffmpeg.decode('utf-8'))

                print(f"Descarga y conversión exitosa: {video.title}")

                # Eliminar el archivo temporal de audio
                os.remove(ruta_temporal_audio)

            except Exception as e:
                print(f"Error con el video '{video.title}': {e}")

        print("Descarga y conversión de la lista de reproducción completa.")

    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    # URL de la lista de reproducción de YouTube
    url_lista_reproduccion = ""

    # Ruta donde se guardarán los archivos descargados
    ruta_destino = "Downloads"

    # Calidad deseada en kbps
    calidad_deseada = 320

    descargar_y_convertir_lista_de_reproduccion(url_lista_reproduccion, ruta_destino, calidad_deseada)
