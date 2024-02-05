import os
from pytube import Playlist, YouTube
import subprocess
import shlex
import sys

sys.stdout.reconfigure(encoding="utf-8")


def audio(url, ruta_destino, calidad_deseada=320):
    try:
        # Verificar si la URL es una lista de reproducción o un video individual
        if "playlist" in url.lower():
            playlist = Playlist(url)
            urls = playlist.video_urls
        else:
            urls = [url]

        # Crear la carpeta de destino si no existe
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        # Iterar sobre cada URL en la lista de reproducción o la URL individual
        for video_url in urls:
            try:
                video = YouTube(video_url)

                # Obtener la mejor stream de audio disponible en formato mp4
                stream = video.streams.filter(
                    only_audio=True, file_extension="mp4"
                ).first()

                # Si no hay streams en formato mp4, obtener cualquier stream de audio
                if not stream:
                    stream = video.streams.filter(only_audio=True).first()

                # Nombre del archivo
                filename = "".join(
                    ["_" if ord(char) > 127 else char for char in video.title]
                )

                # Descargar el audio
                ruta_temporal_audio = os.path.join(
                    ruta_destino, f"{filename}.{stream.subtype}"
                )

                # Verificar si el archivo ya existe.
                if os.path.exists(ruta_temporal_audio):
                    print(
                        f"El archivo '{filename}.{stream.subtype}' ya existe. Sobrescribiendo."
                    )

                stream.download(
                    output_path=ruta_destino, filename=f"{filename}.{stream.subtype}"
                )

                # Convertir de formato a mp3 usando ffmpeg
                ruta_salida_mp3 = os.path.join(ruta_destino, f"{filename}.mp3")
                comando = f'ffmpeg -y -i "{ruta_temporal_audio}" -b:a {calidad_deseada}k "{ruta_salida_mp3}"'

                # Redirigir la salida de FFmpeg a un objeto subprocess.PIPE
                proceso_ffmpeg = subprocess.Popen(
                    shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

                # Capturar y mostrar solo el resultado final
                salida_ffmpeg, _ = proceso_ffmpeg.communicate()
                print(salida_ffmpeg.decode("utf-8"))

                print(f"Descarga y conversión exitosa: {video.title}")

                # Eliminar el archivo temporal de audio
                os.remove(ruta_temporal_audio)

            except Exception as e:
                print(f"Error con la URL '{video_url}': {e}")

        print("Descarga y conversión completa.")

    except Exception as e:
        print(f"Error general: {e}")


def video(url, ruta_destino, calidad_deseada=1080):
    try:
        # Verificar si la URL es una lista de reproducción o un video individual
        if "playlist" in url.lower():
            playlist = Playlist(url)
            videos = playlist.videos
        else:
            videos = [YouTube(url)]

        # Crear la carpeta de destino si no existe
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        # Iterar sobre cada video en la lista de reproducción o el video individual
        for video in videos:
            try:
                # Obtener la mejor stream de video disponible en formato mp4
                stream = video.streams.filter(
                    file_extension="mp4", resolution=f"{calidad_deseada}p"
                ).first()

                # Si no hay streams en formato mp4 para la calidad deseada, obtener cualquier stream de video
                if not stream:
                    stream = video.streams.filter(file_extension="mp4").first()

                # Nombre del archivo
                filename = "".join(
                    ["_" if ord(char) > 127 else char for char in video.title]
                )

                # Descargar el video
                ruta_salida_video = os.path.join(
                    ruta_destino, f"{filename}.{stream.subtype}"
                )

                # Verificar si el archivo ya existe.
                if os.path.exists(ruta_salida_video):
                    print(
                        f"El archivo '{filename}.{stream.subtype}' ya existe. Sobrescribiendo."
                    )

                stream.download(
                    output_path=ruta_destino, filename=f"{filename}.{stream.subtype}"
                )

                print(f"Descarga exitosa: {video.title}")

            except Exception as e:
                if hasattr(video, 'watch_url'):
                    print(f"Error con la URL '{video.watch_url}': {e}")
                else:
                    print(f"Error con la URL '{url}': {e}")

        print("Descarga completa.")

    except Exception as e:
        print(f"Error general: {e}")


def banner():
    mensaje = """
                    ::::::::::: :::::::::   :::::::  ::::    :::   :::   :::    ::: 
                    :+:     :+: :+:    :+: :+:   :+: :+:+:   :+: :+:+:   :+:    :+: 
                           +:+  +:+    +:+ +:+  :+:+ :+:+:+  +:+   +:+    +:+  +:+  
                          +#+   +#++:++#:  +#+ + +:+ +#+ +:+ +#+   +#+     +#++:+   
                         +#+    +#+    +#+ +#+#  +#+ +#+  +#+#+#   +#+    +#+  +#+  
                        #+#     #+#    #+# #+#   #+# #+#   #+#+#   #+#   #+#    #+# 
                        ###     ###    ###  #######  ###    #### ####### ###    ### 
    
    Puedes encontrar el código en nuestro repositorio de GitHub: https://github.com/7R0N1X/Tube-Downloader
    """
    print(mensaje)


def menu(ruta_destino):
    opc = 0
    while opc != 3:
        banner()
        print(
            "1. Descargar MP3 \n2. Descargar MP4 \n3. Salir"
        )
        opc = int(input("Opción: "))
        if opc == 1:
            url_lista = str(
                input("URL: "))
            audio(
                url_lista, ruta_destino, 320)
        elif opc == 2:
            url_lista = str(
                input("URL: "))
            video(url_lista, ruta_destino, 1080)

        elif opc == 3:
            print()
        else:
            print("La opción ingresada no es correcta.")


if __name__ == "__main__":
    # Ruta donde se guardarán los archivos descargados
    ruta_destino = "Downloads"

    menu(ruta_destino)
