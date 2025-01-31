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
    time_ranges = []
    format_option = "mp4"

    # Analizar elementos adicionales
    for part in parts[1:]:
        part_lower = part.lower()
        if part_lower == "mp3":
            format_option = "mp3"
        elif ":" in part:
            time_ranges.append(part)

    # Determinar plantilla de nombre de archivo
    if time_ranges:
        output_template = f"{output_dir}/%(title)s-%(id)s-%(section_title)s-%(autonumber)s.%(ext)s"
    else:
        output_template = f"{output_dir}/%(title)s-%(id)s%-(autonumber)s.%(ext)s"

    # Construcción del comando yt-dlp
    command = [
        "yt-dlp",
        "--no-playlist",
        "--flat-playlist",
        "-o", output_template
    ]

    # Agregar múltiples rangos de tiempo si existen
    if time_ranges:
        command.append("--split-chapters")
        for time in time_ranges:
            command += ["--download-sections", f"*{time}"]

    # Configurar formato de salida
    if format_option == "mp3":
        command += ["-x", "--audio-format", "mp3", "--embed-thumbnail"]
    else:
        command += ["-f", "mp4"]

    # Agregar la URL al final del comando
    command.append(url)

    # Ejecutar el comando
    subprocess.run(command, shell=True)

print("Descargas completadas.")