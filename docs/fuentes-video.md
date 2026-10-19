# Fuentes de video para la carga de trabajo

Documento de trabajo interno. **No forma parte de la memoria** y no debe
incluirse en el PDF.

Propósito: dejar registradas las opciones evaluadas para la secuencia de
entrada de la cadena de detección de objetos, con lo que está verificado y lo
que falta verificar. La decisión definitiva corresponde a P-03 (carga de
trabajo y modelo) y P-05 (matriz experimental y resoluciones); este documento
solo alimenta esas decisiones.

**Actualización (2026-10-19).** P-03 quedó cerrado y el conjunto de origen
decidido: **BDD100K**. La decisión está escrita en `sections/capitulo-3.tex`
§3.3.2 (`sec:input-sequence`), junto con la regla de selección del clip y la
política de repetición. P-05 quedó cerrado el mismo día: el clip está
registrado con nombre, SHA-256, contenedor, códec y número de fotogramas, y
las resoluciones experimentales están fijadas en §3.6 (ver §6 de este
documento).

Última revisión: 2026-10-19.

---

## 1. Requisitos que impone el diseño ya fijado

De `sections/capitulo-3.tex` §3.1 (P-01, completado) y de `docs/plan.md`:

- La entrada es un **archivo de video decodificado localmente**, no una
  cámara en vivo. La razón es que un archivo entrega la misma secuencia de
  fotogramas en cada corrida y en cada configuración, lo que permite comparar
  las salidas de A, B y C fotograma a fotograma.
- El archivo debe tener una **resolución al menos igual a la mayor de las
  resoluciones experimentales**. Con las resoluciones fijadas en P-05
  (320×180, 640×360, 1280×720), el archivo debe ser **≥ 1280×720**.
- La procedencia debe ser **documentable y verificable**: un lector tiene que
  poder obtener el mismo archivo, y hay que poder comprobar que es el mismo.
- La carga debe ser representativa de **detección de objetos de tráfico desde
  un punto de vista en primera persona** (video PoV de un vehículo en
  circulación).
- No se requieren anotaciones: el trabajo mide tiempos de procesamiento, no
  precisión de detección. Las anotaciones, si existen, sirven solo como
  control de cordura.

---

## 2. Decisión: BDD100K

**Yu, F., Chen, H., Wang, X., Xian, W., Chen, Y., Liu, F., Madhavan, V. y
Darrell, T. «BDD100K: A Diverse Driving Dataset for Heterogeneous Multitask
Learning». CVPR 2020.** arXiv:1805.04687.

### Características verificadas

Verificado el 2026-10-19 contra el texto del paper (arXiv:1805.04687v2) y el
repositorio oficial (`github.com/bdd100k/bdd100k`):

- **100 000 videos de conducción de 40 s cada uno**, recolectados de forma
  colaborativa a partir de grabaciones de *dashcam* (vía Nexar), con
  diversidad geográfica, ambiental y climática.
- **Resolución 720p y 30 fps**, es decir **1280×720 nativo**. Esto es lo
  decisivo: la condición de mayor resolución no requiere *upscaling*, y las
  otras dos solo submuestrean. Un archivo de menor resolución obligaría a
  ampliar en la condición superior, lo que introduce un costo artificial que
  no forma parte del fenómeno estudiado.
- Entre las tareas anotadas del conjunto está la **detección de objetos
  viales**.
- Incluye datos de GPS/IMU de las trayectorias (no necesarios aquí).

### Por qué conviene sobre el video actual

El video actual, descargado de YouTube, es técnicamente utilizable pero débil
para una memoria que declara un artefacto reproducible:

- La URL puede desaparecer, y una nueva descarga puede devolver otra
  codificación, otro recorte o directamente otro contenido.
- No hay forma de que un tercero verifique que procesó el mismo material.
- La licencia del material de origen es incierta.

Con un archivo de un conjunto de datos publicado, el procedimiento se reduce
a: descargar de un origen público, verificar un SHA-256 declarado y
documentar la licencia.

### Estado de la verificación (2026-10-19)

- **Licencia: verificada.** El portal `bdd-data.berkeley.edu` responde por
  HTTP (su certificado TLS no cubre el nombre del host, de modo que `https`
  falla con error de certificado). La pestaña *License* del portal contiene el
  texto del Berkeley DeepDrive: permiso de uso, copia, modificación y
  distribución con fines educativos, de investigación y sin fines de lucro,
  con la obligación de que el aviso de derechos de autor y sus párrafos de
  condiciones acompañen a toda copia o distribución. Es una licencia propia de
  la Universidad de California, no una licencia abierta de uso general; el uso
  en esta memoria queda cubierto y la licencia se declara en §3.3.2.
- **Descarga: bloqueada en esta sesión.** Exige registro y aceptación de la
  licencia en el portal. Los espejos citados por la documentación del conjunto
  (`https://dl.cv.ethz.ch/bdd100k/data/`) no resuelven por DNS desde la red
  usada, y `doc.bdd100k.com` tampoco. El archivo debe obtenerse desde el
  portal, con la cuenta del autor.
- **Tamaño.** Sin verificar. El paquete completo de videos se anuncia en
  1,8 TB; conviene descargar solo la parte que contiene el clip elegido.
- **Registro.** El portal requiere cuenta; eso afecta la reproducibilidad
  percibida, no la validez del resultado, y se declara en el texto.

---

## 3. Alternativas consideradas

| Conjunto | Ventaja | Limitación para este trabajo | Estado de verificación |
|---|---|---|---|
| **KITTI** (Geiger et al.) | El conjunto PoV de detección más citado; tráfico urbano y rural | Resolución de imagen bastante menor que 1280×720, lo que obligaría a reescalar hacia arriba en la condición superior | Resolución **no verificada** en esta revisión; confirmar antes de descartarlo |
| **nuScenes** | Alta calidad, múltiples cámaras, escenas urbanas densas | Exige registro y acuerdo de uso; descarga mucho mayor; 12 Hz y resolución no estándar respecto de la matriz | No verificada |
| **Waymo Open Dataset** | Muy alta resolución y gran volumen | Acuerdo de uso, descarga muy grande, sin ventaja para una cadena de 720p | No verificada |
| **Cityscapes** | Muy citado, escenas urbanas alemanas | Pensado para segmentación; fragmentos cortos de 30 fotogramas, inconveniente para corridas de duración fija | No verificada |
| **Video propio grabado** | Control total de la escena y de la licencia | No es reproducible por un tercero; requiere equipamiento y tiempo; difícil de justificar frente a un conjunto publicado | — |

Nota: la tabla no pretende ser una revisión de conjuntos de datos; solo
registra por qué se descartaron las alternativas obvias. Cualquier afirmación
marcada como no verificada debe comprobarse antes de escribirla en la memoria.

---

## 4. Qué hay que documentar cuando se fije el archivo

Lista de verificación para P-03/P-05, coherente con §3.10 de la memoria:

- [ ] Nombre exacto del archivo o del clip dentro del conjunto.
      **Hecho:** `bdd100k/videos/100k/train/0000f77c-6257be58.mov`.
- [x] Origen: nombre del conjunto y partición (BDD100K, partición de
      entrenamiento). Falta la fecha de descarga, que se registra al obtener
      el archivo. **Fecha: 2026-10-19.**
- [ ] **SHA-256** del archivo efectivamente usado.
      **Hecho:** `313eed7b8e46ae388c9d59f4e6068d5ab6fb98ce13e0d63b48b8cdd604d76767`
      (20 046 247 bytes).
- [x] Resolución y tasa de cuadro: 1280×720 a 30 fps, verificado en el texto
      del conjunto. Falta el códec, el perfil y el contenedor, que se leen del
      archivo descargado. **Leídos:** contenedor QuickTime, H.264 perfil High
      nivel 4.1, 1217 fotogramas en 40,37 s (~30,1 fps promedio). Ver §6 sobre
      la orientación codificada.
- [x] Licencia y condiciones de uso: Berkeley DeepDrive, verificada en el
      portal y declarada en §3.3.2 de la memoria.
- [x] Procedimiento de obtención, incluida la selección del clip: registro en
      el portal, descarga de la parte que contiene el clip y elección del
      primer archivo en orden lexicográfico de la partición de entrenamiento
      (§3.3.2).
- [x] Política de repetición: el clip se reinicia desde el primer fotograma si
      la corrida lo excede, igual en las nueve condiciones (§3.3.2).
- [x] Entrada bibliográfica del conjunto: `yu2020` en Zotero y en
      `referencias.bib`.

---

## 5. Preguntas abiertas

1. ~~¿Se usa un clip completo de 40 s o un segmento de duración fija?~~
   **Resuelto (P-03):** el clip completo; si la corrida excede su duración, se
   reinicia desde el primer fotograma. No se recorta ni se recodifica.
2. ~~¿Una sola secuencia para todas las condiciones, o una por resolución?~~
   **Resuelto (P-03):** una sola, la misma en A, B y C; las resoluciones se
   obtienen redimensionando el fotograma en la etapa de adquisición.
3. ~~¿Dónde se declara la licencia?~~ **Resuelto (P-03):** en §3.3.2, con la
   cita del conjunto.
4. ~~¿el SHA-256 del clip se imprime en la memoria o queda solo en el
   manifiesto del artefacto?~~ **Resuelto (P-05):** se imprime en §3.3.2,
   además del manifiesto, con `\seqsplit` para cortarlo.

---

## 6. Cierre de P-05 (2026-10-19)

**Resoluciones fijadas:** 320×180, 640×360 y 1280×720. Las tres son 16:9,
como el archivo de entrada, y submúltiplos exactos de 1280×720 (1/4, 1/2 y 1
lineal). Se descartaron 320×240 y 640×480 porque son 4:3 y obligarían a
recortar, deformar o rellenar la imagen en la adquisición.

**Clip registrado:**

| Campo | Valor |
|---|---|
| Nombre en el conjunto | `bdd100k/videos/100k/train/0000f77c-6257be58.mov` |
| Selección | primer archivo en orden lexicográfico de la partición de entrenamiento |
| Tamaño | 20 046 247 bytes |
| SHA-256 | `313eed7b8e46ae388c9d59f4e6068d5ab6fb98ce13e0d63b48b8cdd604d76767` |
| Contenedor | QuickTime (`.mov`, *major brand* `qt`, muxer Lavf57.71.100) |
| Códec | H.264/AVC, perfil High (100), nivel 4.1 (41) |
| Tamaño codificado | 720×1280, con matriz de rotación de 90° en la pista |
| Tamaño de presentación | 1280×720 |
| Fotogramas | 1217 |
| Duración | 40,37 s (≈30,1 fps promedio) |
| Fecha de descarga | 2026-10-19 |

**Procedencia.** Los portales oficiales no respondieron desde la red usada
(`bdd-data.berkeley.edu` sin respuesta; `dl.cv.ethz.ch` sin resolución DNS).
El archivo se extrajo desde una copia publicada en Hugging Face
(`linxxx3/bdd100k_videos`) de `bdd100k_videos.zip` (MD5 declarado
`253d9a2f9d89d2b09d8d93f397aecdd7`; 1 969 155 915 058 bytes en 19 partes de
100 GiB). La integridad se comprobó contra el CRC-32 que el directorio
central declara para ese miembro, y la identidad contra el SHA-256 de arriba.
La equivalencia byte a byte con la copia del portal oficial **no está
verificada**; si se repite la descarga desde el portal, basta comparar el
SHA-256.

**Extracción reproducible.** El procedimiento general está en
`docs/scripts/zipfetch.py`: lee el Zip64 EOCD por `Range`, descarga el
directorio central del `.zip` (12 857 856 bytes), localiza los miembros y
transfiere solo sus bytes, traduciendo el desplazamiento absoluto al trozo
correspondiente. Un clip cuesta ~33 MB de tráfico en lugar de ~1,97 TB.

```sh
./docs/scripts/zipfetch.py \
  --url "https://huggingface.co/datasets/linxxx3/bdd100k_videos/resolve/main/bdd100k_videos/bdd100k_videos.zip.part-{i:05d}" \
  --parts 19 --part-size 107374182400 --last-part-size 36420631858 \
  --member "bdd100k/videos/100k/train/0000f77c-6257be58.mov" -o clip.mov
```

Copia local de los diez primeros clips de la partición de entrenamiento (el
primero es el registrado; los otros nueve sirven para revisar propiedades del
conjunto) en `~/Downloads/BDD100K`, con `MANIFIESTO.md` y `sha256sums.txt`
(210 MB en total):

```sh
./docs/scripts/zipfetch.py \
  --url "https://huggingface.co/datasets/linxxx3/bdd100k_videos/resolve/main/bdd100k_videos/bdd100k_videos.zip.part-{i:05d}" \
  --parts 19 --part-size 107374182400 --last-part-size 36420631858 \
  --match "^bdd100k/videos/100k/train/.*\\.mov$" --limit 10 \
  -d ~/Downloads/BDD100K
```

**Hallazgo: los fotogramas están almacenados girados.** Los diez clips
revisados son 720×1280 codificados con una matriz de display de 90° en
`tkhd` y presentación de 1280×720; no es una rareza del clip elegido. Los
diez son `avc1` perfil High nivel 4.1, con 1202–1223 fotogramas en
40,09–40,72 s. Consecuencias:

- La etapa de adquisición debe aplicar la matriz de display; si no, el
  fotograma entra en retrato y las tres resoluciones dejan de tener sentido.
  OpenCV 4.8 (`cv2.VideoCapture`, backend FFMPEG) y la CLI de FFmpeg ya
  aplican la rotación por omisión; una lectura con `av`/PyAV o un `nvdec`
  crudo debe aplicarla explícitamente.
- La dirección de la rotación alterna entre clips: seis de los diez tienen un
  signo y cuatro el opuesto. Conviene comprobarla por archivo y no asumirla.
- El recuento de fotogramas y la duración varían de un clip a otro; cualquier
  cálculo de reinicio del clip debe leerlos del archivo, no suponerlos.
- `cv2.CAP_PROP_FPS` informa 59,94 en tres de los diez clips. Es un valor
  espurio derivado del `stts` del contenedor: la tasa media real es
  fotogramas/duración (29,98–30,20). No usar esa propiedad para conducir la
  fuente ni para verificar la duración.

**Verificación disponible en esta máquina (Jetson).** `ffprobe -of json` falla
con esta compilación de FFmpeg (`--disable-everything`, sin decodificador
H.264 por software), y el decodificador por omisión es `h264_cuvid`, que no
carga en Orin. Para leer metadatos se usan `ffmpeg -i` o `cv2`; para decodificar
con la CLI, `-c:v h264_nvv4l2dec`.
