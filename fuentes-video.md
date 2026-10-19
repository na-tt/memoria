# Fuentes de video para la carga de trabajo

Documento de trabajo interno. **No forma parte de la memoria** y no debe
incluirse en el PDF.

Propósito: dejar registradas las opciones evaluadas para la secuencia de
entrada de la cadena de detección de objetos, con lo que está verificado y lo
que falta verificar. La decisión definitiva corresponde a P-03 (carga de
trabajo y modelo) y P-05 (matriz experimental y resoluciones); este documento
solo alimenta esas decisiones.

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

## 2. Recomendación: BDD100K

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

### Advertencias antes de fijarlo

- **Licencia sin verificar.** El sitio `bdd-data.berkeley.edu` no respondió
  durante esta revisión. La descarga exige aceptar un acuerdo; hay que leerlo
  y dejar la licencia escrita en la memoria. Si es de tipo no comercial, eso
  no impide su uso en una memoria de título, pero debe declararse.
- **Tamaño de la descarga sin verificar.** El conjunto completo es grande
  (decenas de GB); conviene descargar solo lo necesario en vez del conjunto
  íntegro.
- **Registro.** Puede requerir formulario o cuenta; eso afecta la
  reproducibilidad percibida, no la validez del resultado, pero conviene
  decirlo en el texto.

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
- [ ] Origen: nombre del conjunto, versión o partición, URL de descarga,
      fecha de descarga.
- [ ] **SHA-256** del archivo efectivamente usado.
- [ ] Resolución, tasa de cuadro, códec y perfil, y contenedor.
- [ ] Duración y número de fotogramas.
- [ ] Licencia y condiciones de uso, con la declaración correspondiente en la
      memoria.
- [ ] Procedimiento de obtención paso a paso, incluida la selección del clip
      si el conjunto es grande.
- [ ] Política de repetición: si la corrida excede la duración del clip, cómo
      se recicla el material (bucle o concatenación) y la garantía de que es
      idéntica en las nueve condiciones.
- [ ] Entrada bibliográfica del conjunto en `referencias.bib` (coordinar con
      P-19 y P-22).

---

## 5. Preguntas abiertas

1. ¿Se usa un clip completo de 40 s o un segmento de duración fija extraído de
   él? Un segmento fijo obliga a re-codificar o a recortar en tiempo de
   decodificación; conviene decidirlo junto con la duración de corrida de
   P-06.
2. ¿Una sola secuencia para todas las condiciones, o una secuencia por
   resolución? Debe ser la misma en A, B y C para cada resolución.
3. Si la licencia exige atribución en la publicación, ¿dónde se declara: en
   §3.3, en los agradecimientos o en ambos?
