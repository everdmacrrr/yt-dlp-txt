


Descargar de forma separada partes de cualquier vídeo de la forma más rápida posible.

### Requisitos

Instalar [`yt-dlp`](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file)

### Instalación

Con CMD en tu computadora. (Windows)

1. Presiona el botón de Windows.
2. Busca “CMD”
3. Das enter.
4. Pega esto:

`git clone https://github.com/everdmacrrr/yt-dlp-txt`

5. Ya esta instalado.
Nota:
Desde antes escoge donde quieres aguardar el proyecto.

### Formato dentro del txt

```bash
enlace_yt [OPTIONS]
```

Ejemplo general:

```bash
https://youtu.be/_UmdeHIY6DM 1:45-1:59
```

### Uso

1. Pegas en `input_links.txt` los enlaces a descargar por cada renglón.
2. Agregas los minutos de descarga que buscas: ej.

```bash
https://youtu.be/_UmdeHIY6DM 1:45-1:59
```

1. Guardas el documento.
2. Ejecutas / “Doble Click” al archivo: `descargar.bat`
3. Los archivos / vídeos descargados aparecerán en la carpeta de `output_mp4`

### Lista de opciones

Todo esto es dentro del txt de `input_links.txt`

Timestamps: 1:45-1:59 [OPCIONAL]

Formato mp3: [OPCIONAL]

Por predeterminado se guarda en mp4 y completo el vídeo. (Si solo pones el link eso pasa).

Solo descargar una sección:

```bash
https://youtu.be/_UmdeHIY6DM 1:45-1:59
```

Si quieres descargar varias partes de un solo vídeo:

```bash
https://youtu.be/_UmdeHIY6DM 1:45-1:59 1:52-2:30 7:58-9:35
```

Descargar parte de un vídeo pero en MP3

```bash
https://youtu.be/_UmdeHIY6DM 1:45-1:59 mp3
```

### Atajos en opciones de tiempo

Aqui esta lo divertido.

Volver a escribir el minuto completo puede ser tedioso, por lo que se agregan atajos rápidos para una descarga más rápida:

#### Función 1 - El resto del vídeo

Si se escribe:
`01:45-*`
Entonces se decargará desde el minuto 01:45 hasta el final del video.
Si se escribe
`*-2:15`
Se descargará desde el inicio del vídeo hasta ese minuto.

#### Función 2 - De números a segundos.
Aplica el mismo orden anterior, pero en vez de escribir el minuto, se escribe la cantidad de segundos.
Ejemplo:
`01:45-25`
Se descargan los siguientes 25 segundos despues del minuto 1:45

Si se escribe
`15-02:30`
Se descargan los 15 segundos antes del minuto 2:30

### Notas:

Puede que tenga errores, es el primer git que subo para compartir.

Además lo género más deepseek que yo…

No me la complique con el nombre.

Solo windows.

Quiero agregar más cosas a futuro, pero por ahora asi esta bien.

Posibles bugs / cosas que no cheque.

Por determinado se descargarán en mp4.
