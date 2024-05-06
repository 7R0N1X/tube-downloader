import os
from pytube import Playlist
from pytube.exceptions import AgeRestrictedError, RegexMatchError
from moviepy.editor import VideoFileClip


def banner():
    message = """
                    ::::::::::: :::::::::   :::::::  ::::    :::   :::   :::    ::: 
                    :+:     :+: :+:    :+: :+:   :+: :+:+:   :+: :+:+:   :+:    :+: 
                           +:+  +:+    +:+ +:+  :+:+ :+:+:+  +:+   +:+    +:+  +:+  
                          +#+   +#++:++#:  +#+ + +:+ +#+ +:+ +#+   +#+     +#++:+   
                         +#+    +#+    +#+ +#+#  +#+ +#+  +#+#+#   +#+    +#+  +#+  
                        #+#     #+#    #+# #+#   #+# #+#   #+#+#   #+#   #+#    #+# 
                        ###     ###    ###  #######  ###    #### ####### ###    ### 
    
    Puedes encontrar el código en nuestro repositorio de GitHub: https://github.com/7R0N1X/tube-downloader
    """
    print(message)


def clean_filename(filename):
    cleaned_filename = filename.replace("/", " ").replace("\\", " ").replace("|", " ").replace("?", " ")
    return cleaned_filename


def download_mp3(url):
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    pl = Playlist(url)
    for video in pl.videos:
        try:
            print(f'Descargando: {video.title}')
            # Filtrar los streams disponibles por resolución, ordenarlos por calidad descendente
            streams = video.streams.filter(
                progressive=True).order_by('resolution').desc()
            # Obtener el primer stream igual o inferior a 720
            target_stream = next(
                (s for s in streams if int(s.resolution[:-1]) <= 720), None)
            # Si se encuentra un stream compatible, descargarlo
            if target_stream:
                # Guardar el video en el directorio "downloads"
                video_path = target_stream.download(output_path='downloads/')
                # Limpiar el nombre del archivo
                cleaned_title = clean_filename(video.title)
                # Ruta completa al archivo de audio
                audio_path = os.path.join('downloads', f"{cleaned_title}.mp3")
                # Convertir el video a audio MP3 con una calidad de 320 kbps
                video_clip = VideoFileClip(video_path)
                try:
                    video_clip.audio.write_audiofile(audio_path, bitrate='320k')
                except Exception as e:
                    print(f"Error al convertir el video a MP3: {e}")
                finally:
                    # Cerrar el clip de video
                    video_clip.close()
                    # Eliminar el archivo de video descargado
                    os.remove(video_path)
        except AgeRestrictedError:
            print(f'El video "{video.title}" está restringido por edad y no puede ser descargado.')
        except RegexMatchError as e:
            print(f'Error al obtener la firma del video "{video.title}": {e}')
            continue


if __name__ == "__main__":
    banner()
    url = input('Ingrese una playlist: ')
    download_mp3(url)
