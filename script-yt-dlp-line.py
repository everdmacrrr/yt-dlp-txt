import os
import subprocess

# Crear la carpeta de salida si no existe
output_dir = "output_mp4"
os.makedirs(output_dir, exist_ok=True)

# Leer los links del archivo
with open("input_links.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Recorrer cada línea y procesar la descarga
for line in lines:
    parts = line.strip().split()  # Dividir por espacios
    if not parts:
        continue
    
    url = parts[0]  # Primer elemento es el link
    time_range = None
    format_option = "mp4"

    # Analizar si hay tiempos y formato mp3
    for part in parts[1:]:
        if ":" in part:  # Si tiene ":", probablemente es un rango de tiempo
            time_range = part
        elif part.lower() == "mp3":  # Si encuentra "mp3", cambia formato
            format_option = "mp3"

    # Construcción del comando yt-dlp
    command = [
        "yt-dlp",
        "--no-playlist",
        "--flat-playlist",
        "-o", f"{output_dir}/%(title)s.%(ext)s"
    ]

    # Si hay un rango de tiempo, agregarlo
    if time_range:
        command += ["--download-sections", f"*{time_range}"]

    # Seleccionar el formato de salida
    if format_option == "mp3":
        command += ["-x", "--audio-format", "--embed-thumbnail", "mp3"]
    else:
        command += ["-f", "mp4"]

    # Agregar la URL al comando
    command.append(url)

    # Ejecutar el comando
    subprocess.run(command, shell=True)

print("Descargas completadas.")
