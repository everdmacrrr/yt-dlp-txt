import os
import subprocess
from datetime import datetime, timedelta



def parse_time(time_str, total_duration=None):
    """
    Convierte una cadena de tiempo (formato HH:MM:SS o segundos) a segundos totales.
    Si es un número, se interpreta como segundos.
    """
    try:
        if ":" in time_str:  # Formato HH:MM:SS o MM:SS
            parts = list(map(int, time_str.split(":")))
            if len(parts) == 3:  # HH:MM:SS
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:  # MM:SS
                return parts[0] * 60 + parts[1]
            elif len(parts) == 1:  # SS
                return parts[0]
        else:  # Segundos directos
            return int(time_str)
    except:
        return None  # Formato inválido

def seconds_to_time(seconds):
    """Convierte segundos a formato HH:MM:SS."""
    return str(timedelta(seconds=seconds))

def process_time_range(time_range, total_duration=None):
    """
    Procesa un rango de tiempo con wildcards (*) y segundos.
    Devuelve el rango formateado para yt-dlp o None si es inválido.
    """
    if "-" not in time_range:
        return None
    
    start, end = time_range.split("-", 1)
    start_is_relative = start.isdigit()
    end_is_relative = end.isdigit()

    # Procesar inicio
    if start == "*":
        start_clean = ""
    else:
        start_seconds = parse_time(start)
        if start_seconds is None:
            return None  # Formato inválido
        start_clean = seconds_to_time(start_seconds)

    # Procesar fin
    if end == "*":
        end_clean = ""
    else:
        end_seconds = parse_time(end)
        if end_seconds is None:
            return None  # Formato inválido
        end_clean = seconds_to_time(end_seconds)
    

    # Nueva lógica para segundos relativos al final (ej: *-25)
    if start == "*" and end.isdigit() and total_duration:
        end_clean = seconds_to_time(total_duration)
        start_clean = seconds_to_time(total_duration - int(end))
    
    # Validación final
    start_sec = parse_time(start_clean) if start_clean else 0
    end_sec = parse_time(end_clean) if end_clean else None
    
    if start_sec < 0 or (end_sec and end_sec < 0):
        return None
    if end_sec and start_sec >= end_sec:
        return None

    return f"{start_clean}-{end_clean}" if end_clean else f"{start_clean}"



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
    
    try:
        get_duration_cmd = ["yt-dlp", "--get-duration", url]
        duration_str = subprocess.check_output(get_duration_cmd, text=True).strip()
        total_duration = parse_time(duration_str)
    except:
        total_duration = None
        print("⚠️ No se pudo obtener la duración del video")

    # Analizar elementos adicionales (sección actualizada)
    for part in parts[1:]:
        part_lower = part.lower()
        if part_lower == "mp3":
            format_option = "mp3"
        elif ":" in part or "-" in part or "*" in part or part.isdigit():
            processed_range = process_time_range(part, total_duration)
            if processed_range:
                time_ranges.append(processed_range)
            else:
                print(f"⚠️ Rango inválido: {part}")
    
    # Validar rangos contra la duración (si está disponible)
    valid_ranges = []
    for tr in time_ranges:
        start, end = tr.split("-", 1)
        start_sec = parse_time(start) if start else 0
        end_sec = parse_time(end) if end else total_duration

        if total_duration:
            end_sec = min(end_sec, total_duration) if end_sec else total_duration
            if start_sec >= total_duration:
                print(f"⚠️ Rango ignorado (inicio después del final): {tr}")
                continue

        valid_ranges.append(f"{start}-{end}")

    # Determinar plantilla de nombre de archivo
    if valid_ranges:
        output_template = f"{output_dir}/%(title)s-%(id)s-%(section_title)s.%(ext)s"
    else:
        output_template = f"{output_dir}/%(title)s-%(id)s.%(ext)s"



    # Construcción del comando yt-dlp
    command = [
        "yt-dlp",
        "--no-playlist",
        "--flat-playlist",
        "-o", output_template
    ]

    # Agregar múltiples rangos de tiempo si existen
    if valid_ranges:
        command.append("--split-chapters")
        for time in valid_ranges:
            command += ["--download-sections", f"*{time}"]

    # Configurar formato de salida
    if format_option == "mp3":
        command += ["-x", "--audio-format", "mp3", "--embed-thumbnail"]
    else:
        command += ["-f", "mp4"]

    # Agregar la URL al final del comando
    command.append(url)

    # Ejecutar el comando
    subprocess.run(command, shell=False)

print("Descargas completadas.")