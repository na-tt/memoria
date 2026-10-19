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
política de repetición. Queda en P-05 el registro del archivo concreto y su
SHA-256.

Última revisión: 2026-10-19.

---

## 1. Requisitos que impone el diseño ya fijado

De `sections/capitulo-3.tex` §3.1 (P-01, completado) y de `docs/plan.md`:

- La entrada es un **archivo de video decodificado localmente**, no una
  cámara en vivo. La razón es que un archivo entrega la misma secuencia de
  fotogramas en cada corrida y en cada configuración, lo que permite comparar
  las salidas de A, B y C fotograma a fotograma.
- El archivo debe tener una **resolución al menos igual a la mayor de las
  resoluciones experimentales**. Con las resoluciones candidatas
  (320×240, 640×480, 1280×720), el archivo debe ser **≥ 1280×720**.
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
- [x] Origen: nombre del conjunto y partición (BDD100K, partición de
      entrenamiento). Falta la fecha de descarga, que se registra al obtener
      el archivo.
- [ ] **SHA-256** del archivo efectivamente usado.
- [x] Resolución y tasa de cuadro: 1280×720 a 30 fps, verificado en el texto
      del conjunto. Falta el códec, el perfil y el contenedor, que se leen del
      archivo descargado.
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
4. **Abierta (P-05):** ¿el SHA-256 del clip se imprime en la memoria o queda
   solo en el manifiesto del artefacto?
