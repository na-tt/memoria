# Pendientes de la memoria

Documento de trabajo interno. **No forma parte de la memoria** y no debe
incluirse en el PDF.

Su propósito es servir de contexto a sesiones agénticas dedicadas a completar
un pendiente a la vez. Cada entrada está pensada como una unidad de trabajo
autocontenida: incluye el estado actual, las decisiones que faltan, el
contexto normativo del proyecto, el entregable esperado y los criterios de
aceptación.

Para una sesión concreta no es necesario leer el archivo completo: basta con
la tabla de la sección 3, la entrada del pendiente asignado y las entradas de
las que depende. La sección 2 sirve para orientarse en el estado del
documento.

---

## 1. Cómo usar este archivo

Antes de trabajar en cualquier pendiente:

1. Leer `docs/scope.md`, `docs/plan.md` y `docs/future.md`. El primero fija el
   alcance y las exclusiones; el segundo es el plan vigente; el tercero evita
   proponer como nuevo algo que ya fue postergado deliberadamente.
2. Leer `AGENTS.md`, en particular las reglas de disciplina de alcance,
   investigación académica, escritura, experimentos, git y build.
3. Para texto en español, leer `.agents/skills/academic-spanish/SKILL.md`.
   Para fuentes, usar la biblioteca Zotero con `zotero-cli`
   (`.agents/skills/zotero-cli/SKILL.md`).
4. Verificar las referencias a archivos y líneas: corresponden al estado del
   repositorio al **2026-10-19** y pueden haberse desplazado. Usar
   `grep -n` antes de editar.
5. No inventar fuentes, resultados, mediciones ni decisiones. Si una decisión
   depende del autor o del profesor guía, dejarla explícitamente planteada en
   vez de resolverla por cuenta propia.
6. No ampliar el alcance. Si aparece una idea atractiva fuera de alcance,
   registrarla en `docs/future.md` solo si el autor lo pide; no incorporarla a
   la memoria.

Convenciones del documento:

- `\todo{...}` es un marcador **visible en el PDF** (definido en
  `commands.tex`). `% TODO` es un comentario de brecha de cita, invisible en el
  PDF.
- Los estados son: **AHORA** (se puede empezar ya), **PARCIAL** (parte se puede
  avanzar) y **BLOQUEADO** (requiere otro pendiente).
- Las líneas se citan como `archivo:línea` o `archivo:línea-línea`.
- Al completar un pendiente: actualizar la tabla de la sección 3, dejar el
  registro de la decisión en el capítulo correspondiente y, si la decisión
  modifica el plan, proponer el cambio a `docs/plan.md` por separado.

---

## 2. Mapa del estado actual del documento

| Archivo | Estado | Observación |
|---|---|---|
| `main.tex` | Preliminar | Front matter, capítulos 1–3, `conclusiones` vacío, bibliografía y anexo de relleno. `\toggletrue{revisarbib}` activo en la línea 35. |
| `sections/portada.tex` | Casi final | Fecha de compilación con `\DTMnow`; título y datos institucionales presentes. |
| `sections/resumen.tex` | Incompleto | Dos `\todo` (resultados y conclusión); el del modelo quedó cerrado en P-03. |
| `sections/abstract.tex` | Incompleto | Los mismos dos `\todo`, en inglés. |
| `sections/capitulo-1.tex` | Borrador avanzado | Dos `% TODO` de cita (privacidad; adopción de rclpy). |
| `sections/capitulo-2.tex` | Borrador avanzado | Tres `% TODO` de cita/atribución (el de potencia se cerró en P-07); sin `\todo` visibles desde P-03. Ocho figuras. |
| `sections/capitulo-3.tex` | Borrador avanzado | 1 `\todo` visible, de P-08 (§3.9); §3.1–§3.8 cerradas desde P-07; sin resultados. |
| `sections/conclusiones.tex` | Vacío | Solo `\chapter*{Conclusiones}`; no está numerado ni tiene secciones. |
| Capítulos 4, 5 y 6 | **No existen** | `docs/plan.md` los exige y el capítulo 1 los anuncia. |
| `sections/anexos.tex` | Relleno | `\appendix` + `\chapter{Apendice A}`. |
| `glosario.tex` | Prueba de concepto | 31 entradas; ninguna se invoca con `\gls`. |
| `referencias.bib` | Operativo | 43 entradas; 39 citadas; 4 sin citar; 2 `@standard` sin driver en biblatex. |
| Código de la cadena y del benchmark | **No existe en este repositorio** | El capítulo 3 ya afirma que está bajo control de versiones. |

El PDF compilado tiene 52 páginas. El índice general llega hasta el capítulo 3
y el apéndice; la bibliografía **no aparece en el índice**. No hay referencias
cruzadas indefinidas, pero varias figuras y la tabla experimental no se
referencian desde el texto.

---

## 3. Tabla de pendientes

| ID | Pendiente | Inicio | Depende de | Prioridad |
|---|---|---|---|---|
| P-01 | Fijar la plataforma experimental | **HECHO** | — | Alta |
| P-02 | Fijar el entorno de software, DDS, QoS y ejecutor | **HECHO** | P-01 | Alta |
| P-03 | Seleccionar la carga de trabajo y el modelo | **HECHO** | P-01, P-02 | Alta |
| P-04 | Definir las configuraciones de particionamiento | **HECHO** | P-03 | Alta |
| P-05 | Fijar la matriz experimental y las resoluciones | **HECHO** | P-03, P-04 | Alta |
| P-06 | Diseñar el procedimiento de benchmark | **HECHO** | P-03, P-05 | Alta |
| P-07 | Definir la instrumentación y la medición de métricas | **HECHO** | P-02 | Alta |
| P-08 | Preespecificar el análisis estadístico | AHORA | P-05 (para detalles) | Alta |
| P-09 | Implementar la cadena monolítica | AHORA | P-03, P-05 | Alta |
| P-10 | Implementar la cadena ROS 2 | BLOQUEADO | P-04, P-09 | Alta |
| P-11 | Construir el arnés de benchmark y versionar el artefacto | BLOQUEADO | P-06, P-07, P-09, P-10 | Alta |
| P-12 | Ejecutar experimentos piloto | BLOQUEADO | P-09–P-11 | Alta |
| P-13 | Ejecutar la campaña experimental final | BLOQUEADO | P-12 | Alta |
| P-14 | Analizar datos y generar tablas y figuras | BLOQUEADO | P-13, P-08 | Alta |
| P-15 | Redactar el capítulo 4 (Resultados) | BLOQUEADO | P-14 | Alta |
| P-16 | Redactar el capítulo 5 (Discusión) | BLOQUEADO | P-15 | Alta |
| P-17 | Redactar el capítulo 6 y cerrar la estructura | BLOQUEADO | P-16 | Alta |
| P-18 | Completar resumen y abstract | BLOQUEADO | P-17, P-03 | Media |
| P-19 | Cerrar las brechas de citas de los capítulos 1–2 | AHORA | — | Media |
| P-20 | Auditar afirmaciones cuantitativas y de novedad | AHORA | — | Media |
| P-21 | Corregir figuras, procedencia y referencias cruzadas | PARCIAL | — | Media |
| P-22 | Depurar la bibliografía y el modo de revisión | AHORA | P-19, P-20 | Media |
| P-23 | Decidir el uso del glosario y unificar la terminología | AHORA | — | Media |
| P-24 | Cerrar el front matter, los anexos y la limpieza del repositorio | AHORA | — | Media |
| P-25 | Revisión final de consistencia y compilación | BLOQUEADO | Todos | Alta |

Ruta crítica: **P-01 → P-02 → P-03 → P-04 → P-05 → P-06/P-07 → P-09 → P-10
→ P-11 → P-12 → P-13 → P-14 → P-15 → P-16 → P-17 → P-18 → P-25**.

Trabajo que puede avanzar en paralelo desde ya: P-07, P-08, P-19, P-20,
P-22, P-23 y la parte de P-24 que no dependa de decisiones experimentales.

---

## 4. Bloque A — Decisiones experimentales

### P-01 · Fijar la plataforma experimental

**Estado: completado.** La plataforma quedó fijada en
`sections/capitulo-3.tex` §3.1 (tabla `tab:platform-configuration`, sin
`\todo`) y la designación se corrigió en `sections/capitulo-2.tex` §2.2.
Valores fijados: kit NVIDIA Jetson Orin Nano Super (P3766) con el módulo de
8 GB; RAM 8 GB LPDDR5 128 bits a 102 GB/s; SSD NVMe FORESEE XP1000F256G de
256 GB (sin tarjeta SD); modo de energía 25 W, verificado con
`nvpmodel -q`; enfriamiento original del kit sin modificaciones (curva de
ventilador por defecto); entrada por archivo de video decodificado
localmente, sin cámara; temperatura del SoC registrada en todas las
corridas. La herramienta térmica se fijó en `tegrastats`, pero se escribe
en §3.8 dentro de P-07. No hubo cambios en `docs/plan.md` ni en el título.

**Nota (2026-10-19).** `nvpmodel -q` en el equipo informa `NV Power Mode:
MAXN_SUPER` (identificador 2), no un modo de 25 W; los topes efectivos son
1,728 GHz de CPU, 1,02 GHz de GPU y 3,199 GHz de memoria. Este pendiente no se
reabre sin decisión del autor, pero la discrepancia debe resolverse antes de
la campaña: o se fija el modo de 25 W con `nvpmodel -m <id>` y se documenta el
identificador, o `tab:platform-configuration` y §3.1 pasan a declarar MAXN
SUPER. §3.2 remite al «modo de energía fijado en la Sección 3.1» para no verse
afectada por esa decisión.

**Estado previo (contexto histórico).** El capítulo 3 dejaba todos los datos del equipo como
`\todo{SPECIFY}` (`sections/capitulo-3.tex:18-38`): módulo exacto, RAM,
almacenamiento, modo de energía, enfriamiento, cámara o dispositivo de entrada
y monitoreo de temperatura. El capítulo 2, en cambio, ya afirma que se usa la
**Jetson Orin Nano Super**, kit de desarrollo basado en el módulo de 8 GB
(`sections/capitulo-2.tex:99-101`), y describe CPU, GPU, memoria unificada y
rendimiento de hasta 67 TOPS (`sections/capitulo-2.tex:133-157`). El título y
`docs/scope.md` dicen solo “NVIDIA Jetson Orin Nano”.

**Objetivo.** Fijar una única configuración de hardware, documentarla y
eliminar la inconsistencia entre capítulos.

**Decisiones que hay que tomar.**

- Módulo y kit exactos (Orin Nano 8 GB, Orin Nano Super Developer Kit u otra
  variante). Verificar en el datasheet `nvidiacorporation2024` a qué variante
  corresponden las cifras de 67 TOPS y 102 GB/s antes de mantenerlas.
- RAM y almacenamiento (tipo y capacidad; por ejemplo, NVMe o tarjeta SD).
- Modo de energía fijo (7 W, 15 W o 25 W). La literatura de la familia Orin
  distingue modos al informar tasas de fotogramas (`scalcon2024`), de modo que
  el modo forma parte de la condición experimental.
- Configuración de enfriamiento (ventilador del kit, curva fija, etc.) y cómo
  se monitorea la temperatura (`tang2026` justifica fijarla y documentarla).
- Fuente de entrada: cámara CSI, archivo de video o secuencia de imágenes.
  Debe ser reproducible y compatible con P-05. Si es cámara, documentar
  exposición, resolución y tasa; si es archivo, fijar el archivo y su
  resolución.
- Procedimiento de monitoreo térmico y ambiental.

**Contexto y restricciones.** `docs/plan.md` §6.1 exige registrar módulo, RAM,
almacenamiento, modo de energía, enfriamiento, dispositivo de entrada y
temperatura. El alcance fija una sola plataforma; no se comparan módulos. La
designación del título no debe cambiarse sin consultar al autor. Sugerencia
del agente: si el equipo real es el kit Super, probablemente convenga mantener
“Orin Nano” en el título y explicar la variante exacta en §2.2 y §3.1.

**Entregable.** §3.1 con una lista o tabla de valores exactos, sin `\todo`.
Actualizar §2.2 si la variante o las cifras cambian. Mantener coherencia con la
portada, el resumen y el abstract.

**Criterios de aceptación.** Ningún `\todo` en §3.1; los valores son
verificables contra el datasheet, la etiqueta del equipo o una fotografía;
modo de energía, enfriamiento y fuente de entrada quedan fijados; capítulo 2,
capítulo 3 y portada usan la misma designación.

**Dependencias.** Ninguna. Desbloquea P-02, P-03 y P-09.

**Notas.** No convertir la descripción en una comparación de modos de energía
ni de módulos Jetson: eso está fuera de alcance (`docs/scope.md` §8).

---

### P-02 · Fijar el entorno de software, DDS, QoS y ejecutor

**Estado: completado (2026-10-19).** §3.2 se reescribió como tabla
verificable (`tab:software-environment`) con valores fijados y el comando que
los verifica en el equipo: JetPack 7.2.1 (`nvidia-jetpack` 7.2.1-b49, Jetson
Linux 39.2.1, kernel 6.8), Ubuntu 24.04 LTS, ROS 2 Jazzy Jalisco con paquetes
binarios `arm64`, `rmw_fastrtps_cpp` sobre Fast DDS 2.14.7, CPython 3.12.3,
depliegue sin contenedores y `tegrastats` como herramienta de monitoreo. Se
agregó la subsección §3.2.1 (Calidad de servicio, `sec:qos`) con el perfil
fijo —`RELIABLE`, `VOLATILE`, `KEEP_LAST` con profundidad 1 y
plazo/vigencia/vivacidad por omisión—, el código `QoSProfile` que lo declara y
la justificación de cada política y de la alternativa descartada. §3.5 declara
el ejecutor: `SingleThreadedExecutor` de `rclpy`, grupo de callbacks mutuamente
exclusivo, una suscripción por nodo, con la razón de descartar el ejecutor
multihilo. §3.10 incorporó «implementación de DDS y versión», «configuración de
transporte de DDS», «tipo de ejecutor y grupos de callbacks» y «gobernador de
frecuencia y frecuencias efectivas». En `main.tex` se agregó `array` y el tipo
de columna `L` (ancho fijo, alineado a la izquierda, sin sangría ni
espaciado estirado) para las tablas nuevas. La correspondencia JetPack 7.2.1 /
Ubuntu 24.04 / Jazzy quedó respaldada con `nvidiacorporation2026jetpack`,
`rep2000` y `rosjazzydocs`.

**Verificación diferida (trasladada a P-11).**

- `ros-jazzy-*` 7.1.x, `ros-jazzy-fastrtps` 2.14.7 y las versiones instaladas de
  `python3-numpy` (1.26.4) y `python3-opencv` (4.6.0) son los valores de
  rosdistro jazzy y del archivo de Ubuntu 24.04 al cierre de esta sesión, no
  observados todavía en la Jetson. Los comandos de la tabla `tab:software-environment`
  los confirman al instalar; si difieren, se corrige la tabla. La comprobación
  se ejecuta en el arranque de P-11, junto con el registro del manifiesto.
- Runtime de inferencia: delegado a P-03 (§3.3), idéntico en A, B y C. No
  bloquea el cierre de P-02.

**Política de relojes (decidida 2026-10-19).** Se fija el gobernador
`performance` en los seis núcleos de la CPU y en el dominio de `devfreq` de la
GPU; el dominio de memoria conserva su escalado y se registra su frecuencia. Se
rechaza dejar el escalado por omisión (el escalado responde a la carga, que
difiere entre A y B/C, lo que sesgaría la comparación en la dirección de H1 y
H3) y se rechaza `jetson_clocks` (fija también la memoria al máximo y saca al
equipo del presupuesto de potencia de §3.1). Gobernadores disponibles
verificados en el equipo: `ondemand userspace performance schedutil`; dominios
de `devfreq`: `17000000.gpu` y `bwmgr`.

**Bibliografía (cerrado 2026-10-19).** Tres entradas en Zotero, con clave
fijada desde la interfaz y fecha de acceso: `rep2000`, `rosjazzyrclpy` y
`nvidiacorporation2026jetpack`. BBT exporta `referencias.bib` automáticamente,
de modo que el `.bib` no se edita a mano: el flujo es Zotero → BBT → archivo, y
la clave se fija en el campo *Citation Key* del ítem, no en *Extra* (en esta
biblioteca BBT no lee ni escribe claves por *Extra*: `rosjazzydocs`, correctamente
fijada, tiene *Extra* vacío). Se corrigieron dos defectos de metadata de la
entrada importada de REP 2000 —autor invertido «Dirk, Thomas» y «Geofrey» por
«Geoffrey»— y el título de la de `rclpy`, que arrastraba el banner «rclpy 3.2.1»
inconsistente con la versión 7.1.12 de Jazzy. Queda por decidir si la fecha de
`rep2000` es la de publicación (2018-04-18) o la de actualización (2026-07-08).

**Estado previo (contexto histórico).** §3.2 tenía siete `\todo{SPECIFY}`
(sistema operativo, JetPack, distribución de ROS 2, implementación de DDS,
configuración de QoS, versión de Python y versiones de paquetes) y §3.5 dejaba
el tipo de ejecutor dentro de un `\todo`. El capítulo 2 explica por qué estas
decisiones importan: la QoS afecta la latencia (`fernandez2020`,
`kronauer2021`), la implementación de DDS afecta el rendimiento
(`maruyama2016`, `kronauer2021`, `zhang2024`) y el ejecutor es inseparable del
rendimiento del nodo (`macenski2023`, `casini2026`).

**Objetivo.** Fijar todas las condiciones de software y middleware que se
mantienen constantes, y expresarlas de forma que puedan reproducirse.

**Decisiones que hay que tomar.**

- Distribución de Linux y versión; versión de JetPack.
- Una distribución de ROS 2 (por ejemplo, la versión LTS compatible con
  JetPack) y su versión exacta.
- Una implementación de DDS y su versión, seleccionada a través de `rmw`.
- Configuración de QoS exacta: confiabilidad, durabilidad, política de
  historial y profundidad, y políticas adicionales solo si se usan. Debe
  quedar expresada como valores concretos (código o archivo de configuración),
  no como prosa.
- Versión de Python y del intérprete; versiones del runtime de inferencia, de
  las bibliotecas de imagen y de las herramientas de monitoreo.
- Procedimiento de instalación y configuración del entorno (flasheo de
  JetPack, instalación de ROS 2, selección de `rmw`, variables de entorno),
  con comandos y versiones, para que la reproducibilidad no dependa de la
  memoria del autor.
- Tipo de ejecutor y grupos de callbacks, idénticos en todos los nodos y
  configuraciones. Justificar la elección con `macenski2023` y `casini2026`.
- Configuración de CPU/GPU, gobernador, afinidad si se usa, y variables de
  entorno relevantes.

**Contexto y restricciones.** El alcance fija una sola distribución, una sola
implementación de DDS, una sola QoS y un despliegue sin contenedores; estas
decisiones son condiciones controladas, no variables. No se comparan DDS ni
políticas de QoS. La configuración de QoS y la profundidad de historial
interactúan con la política de descarte de fotogramas que se defina en P-06.

**Entregable.** Tabla de §3.2 con valores exactos; declaración del ejecutor en
§3.5; lista de reproducibilidad de §3.10 completada de forma consistente con
§3.2. Si se agregan fuentes para métodos de medición o documentación oficial,
coordinarlo con P-19 y P-22.

**Criterios de aceptación.** Todos los valores están fijados y son idénticos
entre configuraciones; se registra el comando o archivo que permite
verificarlos; la QoS y el ejecutor no cambian entre A, B y C; no queda
ninguna referencia a “principal” o “a determinar”.

**Dependencias.** Requiere P-01 para las versiones compatibles de JetPack y
ROS 2. Desbloquea P-03, P-07, P-09 y P-10.

**Notas.** No introducir comparaciones de DDS, QoS, distribuciones ni
contenedores, aunque aparezcan durante la instalación. Registrarlas, si acaso,
en `docs/future.md`.

---

### P-03 · Seleccionar la carga de trabajo y el modelo

**Estado: completado (2026-10-19).** La decisión quedó escrita en
`sections/capitulo-2.tex` §2.5 (justificación frente a los cinco criterios del
plan) y en `sections/capitulo-3.tex` §3.3, que se dividió en dos subsecciones
nuevas: §3.3.1 «Modelo y configuración de inferencia» (`sec:model-configuration`,
con la tabla `tab:model-configuration`) y §3.3.2 «Secuencia de entrada»
(`sec:input-sequence`). Valores fijados:

- **Modelo:** YOLOv8n, de la familia YOLO, en su implementación y pesos
  publicados por Ultralytics.
- **Pesos:** `yolov8n.pt`, 6 549 796 bytes, SHA-256
  `f59b3d83e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`. El mismo
  archivo se sirve en las versiones 8.3.0 y 8.4.0 de `ultralytics/assets`, de
  modo que la identidad se fija por hash y no por etiqueta de versión.
- **Licencia:** AGPL-3.0, declarada en los metadatos internos del archivo de
  pesos; el artefacto experimental se distribuye bajo esa misma licencia.
- **Runtime:** TensorRT 10.16.2, el que incluye JetPack 7.2.1, invocado con
  `bindings` explícitos (`execute_async_v3` sobre flujo de CUDA) y no con la
  interfaz de alto nivel de Ultralytics, porque esa interfaz ejecuta
  preprocesamiento, inferencia y postprocesamiento en una sola llamada e
  impediría asignar las tres etapas a nodos distintos.
- **Formato y motor:** ONNX exportado una vez con Ultralytics 8.3.0, `opset` 17
  y entrada fija de 640×640; motor construido en el dispositivo con
  `trtexec --fp16`. Se versionan el ONNX y su hash, no el motor.
- **Precisión:** FP16. Se descartan INT8 (exigiría calibración y validación de
  exactitud, fuera de alcance) y FP32 (desaprovecha los núcleos tensor).
- **Entrada del modelo:** 640×640 con `letterbox` en todas las condiciones, de
  modo que la etapa de inferencia no varía con la resolución experimental.
- **Postprocesamiento:** confianza 0,25; solapamiento 0,70 en la supresión de
  no máximos; máximo 300 detecciones; supresión codiciosa por clase (valores
  por omisión de la implementación de referencia).
- **Secuencia de entrada:** BDD100K (Yu *et al.*, CVPR 2020), clips de 40 s a
  1280×720 y 30 fps; un solo clip, el primero en orden lexicográfico de la
  partición de entrenamiento; reciclado por reinicio del clip si la corrida lo
  excede; el archivo de origen no se recodifica.

También se corrigió el argumento de §3.6, que justificaba la dimensión de
resolución afirmando que el costo de inferencia crecía con ella
(`szegedi2026`): con la entrada del modelo fija en 640×640, la resolución
actúa sobre decodificación, preprocesamiento y tamaño de los mensajes, y no
sobre el cómputo de la red. Es la segunda salida que preveía P-05 («o bien una
corrección de la afirmación»). La fila «Runtime de inferencia» de
`tab:software-environment` pasó a declarar TensorRT 10.16.2 con su comando de
verificación. En `main.tex` se agregó `seqsplit` para poder cortar el hash.
Las entradas nuevas (`yu2020`, `redmon2016`, `ultralytics2023`) se agregaron a
Zotero y Better BibTeX las exportó a `referencias.bib`.

**Pendiente heredado por P-05.** El clip concreto y su SHA-256 no se pudieron
registrar en esta sesión: la descarga de BDD100K exige registro y aceptación de
la licencia en el portal del conjunto, y los espejos documentados
(`dl.cv.ethz.ch`, `doc.bdd100k.com`) no resuelven. La regla de selección ya
está fijada en §3.3.2, de modo que P-05 solo debe registrar el nombre del
archivo, su SHA-256, contenedor, códec, número de fotogramas y fecha de
descarga, y decidir si el hash se imprime también en la memoria o queda solo
en el manifiesto del artefacto.

**Dependencias.** Requiere P-01 y P-02 para verificar viabilidad. Desbloquea
P-04, P-05, P-09 y P-18.

---

### P-04 · Definir las configuraciones de particionamiento

**Estado: completado (2026-10-19).** La decisión quedó escrita en
`sections/capitulo-3.tex`: la segmentación en operaciones en §3.5.1
(`sec:operations`, tabla `tab:operations`), la verificación de equivalencia en
§3.5.3 (`sec:equivalence`), el mapeo operación→nodo en §3.6
(`tab:configurations`, figura `fig:partitioning`) y el modelo de concurrencia
en §3.6.1 (`sec:concurrency`). Valores fijados:

- **Flujo:** siete operaciones. (1) adquisición: decodifica el clip y
  redimensiona al tamaño experimental; (2) acondicionamiento: `letterbox` a
  640×640 y BGR→RGB; (3) detección: tensor, TensorRT y decodificación de las
  8400 candidatas con umbral 0,25; (4) supresión de no máximos; (5)
  adaptación de coordenadas al marco del fotograma y descarte de cajas
  centradas en el relleno; (6) filtro de dominio; (7) registro del resultado.
- **Configuraciones:** A monolítica (1 proceso), B de 2 nodos
  (`[1] | [2–7]`), C de 4 nodos (`[1] | [2] | [3–4] | [5–7]`) y **D de 7
  nodos**, uno por operación. Son anidadas: cada una es una fusión de
  operaciones contiguas de la siguiente, de modo que la única diferencia es
  dónde cruza la información un límite de proceso. C es la división que
  corresponde a una pila de percepción habitual (captura,
  acondicionamiento, detector, consumidor).
- **Por qué D.** Escalamiento deliberado del grado de particionamiento, no un
  despliegue recomendado: sus tres fronteras adicionales separan operaciones
  de cómputo trivial y transportan decenas de KB, de modo que C→D estima el
  costo fijo de una frontera mientras B→C (mensaje de 1,23 MB) estima el
  costo asociado al tamaño del mensaje. Con eso se rompe la colinealidad
  entre «número de fronteras» y «bytes» que preocupaba a este pendiente.
  Volumen calculado por fotograma: A 0; B 0,23/0,92/2,76 MB; C
  1,50/2,19/4,03 MB; D 1,62/2,31/4,15 MB (resoluciones 1–3, tope de 300
  detecciones). C y D difieren en menos de 0,2 MB: D agrega fronteras, no
  tráfico.
- **Tópicos y tipos:** `/imagen_entrada` (`sensor_msgs/Image`, `bgr8`,
  fotograma a la resolución experimental), `/imagen_modelo` (`Image`,
  `rgb8`, 640×640), `/candidatas`, `/detecciones`, `/detecciones_marco` y
  `/detecciones_relevantes` (`vision_msgs/Detection2DArray`); la operación 7
  no publica. La cadena es estrictamente lineal: un tópico de entrada y otro
  de salida por nodo, que es lo que permite mantener una suscripción por
  nodo con el ejecutor de P-02.
- **Cargas útiles descartadas.** No se publica la salida cruda del motor
  (84×8400 fp32, 2,82 MB) porque exigiría un tipo de mensaje que ninguna pila
  de visión despliega y sería mayor que cualquier imagen; ni el tensor de
  entrada (4,92 MB) porque su construcción es la operación de menor cómputo
  de la cadena. Ambas quedarían dentro de la operación de detección.
- **Etapa «salida».** Resuelta: es la operación 7 (registro). No es una etapa
  de cómputo aparte y en C comparte nodo con el filtro de dominio, de modo
  que la discrepancia entre cinco etapas lógicas y cuatro nodos desaparece.
- **Filtro de dominio.** Decisión de aplicación, no parámetro del modelo:
  retiene las categorías anotadas en BDD100K que existen en COCO (persona,
  bicicleta, automóvil, motocicleta, autobús, camión, tren, semáforo). Se
  aplica después del tope de 300 e idéntico en todo, así que no interviene en
  la comparación.
- **Equivalencia funcional.** La línea base produce una salida de referencia
  sobre un tramo fijo, versionada con el artefacto. Cada configuración
  procesa el mismo tramo con la fuente a una tasa inferior a la de la etapa
  más lenta (sin muestras descartadas, comprobado contra el conteo de
  fotogramas por nodo) y las detecciones se comparan por índice de fotograma.
  Se exige coincidencia total en cantidad y etiquetas, y tolerancia de 1 píxel
  en coordenadas y 10⁻³ en puntajes; la igualdad exacta es lo esperado porque
  motor, pesos y preprocesamiento son los mismos y la serialización de punto
  flotante es sin pérdida. Se ejecuta una vez por configuración y resolución
  antes de la campaña; durante la campaña la misma igualdad se usa como
  criterio de validez de la corrida (§3.3.1, §3.7).
- **Concurrencia.** A procesa estrictamente en secuencia; en ROS 2 cada nodo
  procesa un fotograma por vez, pero distintos nodos pueden tener fotogramas
  distintos en vuelo (hasta $k$ fotogramas con $k$ nodos). Se declara como
  propiedad emergente y se registra su cuantía; se descarta imponer una
  barrera o confirmación por fotograma (agregaría un camino de retorno) y se
  descarta dar a la línea base un pipeline solapado (sería una segunda
  variable). Consecuencia declarada: la comparación mide el costo de adoptar
  el particionamiento tal como ROS 2 lo produce por omisión, solapamiento
  incluido.
- **Figura.** `assets/figures/chapter-3/ros2-particionamiento.dot` →
  `.png`, incluida como `fig:partitioning` en §3.6. Se redibujó con Graphviz y
  no con D2: con D2 el texto quedaba a 1,2 mm de altura al ancho de caja de
  texto, y Graphviz, cuyas unidades son físicas, permite verificar el tamaño
  final. Se eliminaron `assets/figures/chapter-2/ros2-cadena-video.d2` y su
  PNG, que representaban un mapeo ya descartado.

**Cambios fuera del capítulo.** `docs/plan.md` §9 se reescribió con las cuatro
configuraciones, sus criterios y una **nota de experimentación abierta**: el
número de configuraciones y la ubicación exacta de las fronteras quedan
abiertos a ajuste durante la etapa de pilotos, porque es posible que fronteras
que separan operaciones triviales no produzcan diferencias medibles; cualquier
ajuste se decide en los pilotos, se registra en `docs/plan.md` y en este
archivo, y se informa como desviación. §10 pasó a 4×3 = 12 condiciones.
`docs/future.md` §10 quedó anotado como parcialmente cubierto.

**Pendiente heredado.** El mecanismo de marcas de tiempo lo cerró P-07: el
índice viaja en `header.frame_id` y las marcas se consolidan por índice
(§3.8.1, `docs/instrumentacion.md` §2). §3.5.3 fija el criterio de
comparación, no el mecanismo, de modo que ambos son compatibles.

**Estado previo (contexto histórico).** §3.5 y §3.6 dejaban como `\todo` el
mapeo exacto de etapas a nodos, el tipo de ejecutor y la verificación de
equivalencia funcional. La figura editable
`assets/figures/chapter-2/ros2-cadena-video.d2` proponía cuatro nodos
(adquisición, preprocesamiento, inferencia, postprocesamiento) con tópicos
`/imagen_cruda`, `/imagen_procesada` y `/detecciones`, y **no estaba incluida
en el documento**. El capítulo 3 describía una cadena lógica de cinco etapas
(adquisición, preprocesamiento, inferencia, postprocesamiento, salida) y una
cadena ROS 2 de cuatro nodos.

**Objetivo.** Definir qué etapas se agrupan en cada nodo para las
configuraciones B (dos nodos) y C (cuatro nodos), los tópicos y tipos de
mensaje, y un criterio operacional de equivalencia funcional.

**Decisiones que hay que tomar.**

- **Etapa “salida”.** Aclarar si es un nodo, una publicación final, un
  consumidor de resultados o simplemente el final del postprocesamiento. Hoy
  la cadena lógica tiene cinco etapas y la de ROS 2 cuatro nodos; la
  discrepancia debe resolverse antes de escribir §3.4–§3.6.
- **Fronteras de B.** Definir qué dos etapas se agrupan y por qué la división
  es arquitectónicamente significativa. Si B es un subconjunto anidado de C
  (es decir, C conserva la frontera de B y agrega otras), la atribución del
  sobrecosto por frontera es más limpia; si no, explicar el compromiso.
- **Fronteras de C.** Mapear las cuatro etapas a cuatro nodos y justificar que
  la división no es arbitraria.
- **Tópicos y tipos.** Nombres, tipos (`sensor_msgs/Image`,
  `vision_msgs/Detection2DArray`, etc.), codificación de imagen y resolución
  que transporta cada mensaje.
- **Tamaño de las cargas útiles.** Decidir si la imagen que cruza la primera
  frontera es la imagen de entrada a resolución completa o la imagen ya
  redimensionada al tamaño del modelo. Esto determina si el costo de
  comunicación realmente escala con la resolución (ver P-05).
- **Concurrencia.** Definir si la implementación monolítica procesa los
  fotogramas estrictamente en secuencia o si se permite procesamiento solapado
  entre fotogramas. La arquitectura de ROS 2 puede procesar fotogramas
  distintos en nodos distintos; comparar una cadena ROS 2 con solapamiento
  contra un monolito estrictamente secuencial mezcla el efecto de la
  comunicación con el del paralelismo. Hay que elegir y declarar el modelo de
  concurrencia de la línea base.
- **Equivalencia funcional.** Definir una prueba operacional: misma secuencia
  de entrada, mismas detecciones dentro de una tolerancia declarada (número,
  etiquetas, coordenadas, puntajes), y cómo se registra. No basta con afirmar
  que “producen salidas equivalentes”.

**Contexto y restricciones.** `docs/plan.md` §9 fija A monolítica, B de dos
nodos y C de cuatro nodos; no se agregan más configuraciones. La composición
de nodos, la comunicación intraproceso y el transporte por memoria compartida
están excluidos (`docs/scope.md` §8): los nodos deben ser procesos separados
con comunicación interproceso ordinaria. La QoS y el ejecutor provienen de
P-02. Cualquier figura que se use debe coincidir exactamente con el mapeo
elegido.

**Entregable.** §3.5 y §3.6 con el mapeo etapa→nodo, una tabla o diagrama por
configuración, los tópicos y tipos, y el procedimiento de verificación de
equivalencia. Actualizar o descartar `ros2-cadena-video.d2` según el mapeo
final.

**Criterios de aceptación.** B y C quedan definidas sin ambigüedad; cada
frontera tiene una justificación; la etapa “salida” está resuelta; la prueba
de equivalencia es reproducible; la figura y el texto coinciden; no se usan
mecanismos excluidos.

**Dependencias.** Requiere P-03 (modelo y runtime) y P-02 (QoS y ejecutor).
Desbloquea P-05, P-10 y P-21.

**Notas.** Este pendiente es el lugar natural para detectar el factor de
confusión entre “número de fronteras” y “tamaño de la carga útil que cruza cada
frontera”. Si
las fronteras se agregan en puntos con cargas útiles de distinto tamaño, el
efecto del grado de particionamiento no es separable del efecto del tamaño de
mensaje. Documentar esa limitación para el capítulo 5.

---

### P-05 · Fijar la matriz experimental y las resoluciones

**Estado: completado (2026-10-19).** La decisión quedó escrita en
`sections/capitulo-3.tex`: las resoluciones experimentales en §3.6
(`sec:configurations`, tabla `tab:experimental-matrix`) y la identidad del
clip en §3.3.2 (`sec:input-sequence`). Valores fijados:

- **Resoluciones:** 320×180, 640×360 y 1280×720. Las tres conservan la
  relación de aspecto 16:9 del archivo de entrada y son submúltiplos exactos
  de su resolución de presentación: 1/4, 1/2 y 1 en escala lineal, 1/16, 1/4
  y 1 en área. Se descartaron las candidatas 320×240 y 640×480 porque son
  4:3: la fuente es 16:9 y una reducción a 4:3 exigiría recortar, deformar o
  rellenar la imagen, es decir, una operación geométrica que el diseño no
  contempla y que haría que el detector viera contenido distinto en cada
  condición. La resolución mayor coincide con la del archivo, de modo que
  ninguna condición amplía la imagen.
- **Punto de aplicación:** la resolución es un parámetro de la operación 1
  (adquisición), que decodifica, aplica la matriz de rotación de la pista y
  redimensiona el fotograma antes de publicarlo en `/imagen_entrada`. El
  archivo de origen no se recodifica y el modelo recibe siempre 640×640
  (P-03). El valor se registra en el manifiesto de cada corrida, junto con
  los demás parámetros.
- **Matriz:** 4 configuraciones × 3 resoluciones = 12 condiciones, sin
  dimensiones adicionales. `tab:experimental-matrix` y `docs/plan.md` §10
  quedaron con los valores finales; la tabla de pendientes pasa P-06 y P-09 a
  AHORA.
- **Cargas útiles recalculadas.** Con las resoluciones nuevas, el volumen por
  fotograma de `tab:partitioning-payloads` es A 0; B 0,17/0,69/2,76 MB; C
  1,45/1,97/4,04 MB; D 1,57/2,09/4,16 MB (1 MB = 10⁶ bytes, redondeado a dos
  decimales; la convención ahora se declara en el epígrafe). La fila de la
  operación 1 de `tab:operations` pasó a «170 KB a 2,76 MB». La diferencia
  C−D sigue por debajo de 0,2 MB, de modo que la lectura de P-04 sobre el
  costo fijo de una frontera se mantiene.
- **Clip registrado:** `0000f77c-6257be58.mov`; contenedor QuickTime, H.264
  en perfil High nivel 4.1, presentación 1280×720, 1217 fotogramas en 40,37 s,
  20 046 247 bytes, SHA-256
  `313eed7b8e46ae388c9d59f4e6068d5ab6fb98ce13e0d63b48b8cdd604d76767`,
  obtenido y verificado el 2026-10-19. Nombre, hash, formato y recuento se
  imprimen en §3.3.2 (el hash con `\seqsplit`) y el manifiesto del artefacto
  repite la ficha.
- **Rotación del archivo.** Los fotogramas se almacenan girados 90° y el
  contenedor declara la rotación en la matriz de la pista: codificado
  720×1280, presentación 1280×720. Se verificó en los diez primeros clips de
  la partición de entrenamiento: los diez son 720×1280 codificados con matriz
  de rotación de 90° (signo variable), `avc1` perfil High nivel 4.1, y
  1202–1223 fotogramas en 40,09–40,72 s, de modo que no es una rareza del
  clip elegido. La dirección alterna entre clips (seis de un signo, cuatro del
  opuesto). §3.3.2 declara
  que la adquisición aplica la matriz; sin eso el fotograma entra en retrato
  y las tres resoluciones dejan de tener sentido. Es un requisito para P-09.
  Atención además con `cv2.CAP_PROP_FPS`: informa 59,94 en tres de los diez
  clips por un `stts` anómalo; la tasa media real es fotogramas/duración
  (29,98–30,20), y no debe usarse esa propiedad para conducir la fuente.

**Extracción reproducible.** `docs/scripts/zipfetch.py` lee el directorio
central del `.zip` por HTTP `Range` y transfiere solo los miembros pedidos:
unos 33 MB por clip en lugar de 1,97 TB. Los diez primeros clips de
entrenamiento quedaron en `~/Downloads/BDD100K`, con `MANIFIESTO.md` y
`sha256sums.txt`; el primero es el que se usa en la campaña y los otros nueve
sirven para revisar propiedades del conjunto.

**Procedencia (por confirmar).** Los portales oficiales no fueron alcanzables
en esta sesión: `bdd-data.berkeley.edu` no respondió y `dl.cv.ethz.ch` no
resuelve. El clip se extrajo, por lectura por rangos del archivo comprimido,
de una copia publicada en Hugging Face (`linxxx3/bdd100k_videos`) de
`bdd100k_videos.zip` (MD5 declarado `253d9a2f9d89d2b09d8d93f397aecdd7`,
1 969 155 915 058 bytes en 19 partes). La extracción se comprobó contra el
CRC-32 que el propio archivo declara en su directorio central. El SHA-256 del
clip es verificable con independencia del origen, pero la equivalencia byte a
byte con la copia del portal oficial **no se comprobó**; si el autor repite la
descarga desde el portal, basta comparar el SHA-256 y, si coincide, el
manifiesto no cambia.

**Decisión sobre el hash.** Se imprime en la memoria, además de quedar en el
manifiesto, porque es lo que hace verificable la identidad del clip sin
depender de una cuenta en el portal. `main.tex` ya carga `seqsplit` desde
P-03 justamente para cortarlo.

**Estado previo (contexto histórico).** §3.6 usaba tres resoluciones
candidatas (320×240, 640×480 y 1280×720) con `\todo{SPECIFY}`, y la tabla
`tab:experimental-matrix` cruzaba tres configuraciones con tres resoluciones.
No se definía con precisión qué significa “resolución de entrada” ni dónde se
aplica.

**Objetivo.** Fijar las tres resoluciones y definir sin ambigüedad en qué punto
de la cadena actúan.

**Decisiones que hay que tomar.**

- Resoluciones finales, en píxeles, compatibles con la fuente de entrada
  (P-01), el modelo (P-03) y el preprocesamiento.
- **Dónde actúa la resolución.** Distinguir explícitamente entre:
  (a) resolución del fotograma de entrada,
  (b) resolución de la imagen que se publica en el primer tópico,
  (c) resolución de entrada del modelo.
  Si el preprocesamiento redimensiona a un tamaño fijo antes de la primera
  frontera, el costo de comunicación no crecerá con la resolución, aunque el
  de inferencia sí. La afirmación del capítulo 3 de que ambos términos escalan
  con la resolución exige que al menos un mensaje transporte una carga útil
  dependiente de la resolución, o bien una corrección de la afirmación.
- Confirmar que las nueve condiciones (3 arquitecturas × 3 resoluciones) se
  ejecutan completas y que no se agregan dimensiones.
- Definir si la resolución es un parámetro de la fuente, del preprocesamiento
  o de ambos, y cómo se registra en los metadatos de cada ejecución.

**Contexto y restricciones.** `docs/plan.md` §10 propone la matriz 3×3 y
advierte que las resoluciones finales dependen de la fuente y del modelo. El
capítulo 3 justifica la dimensión por el costo de inferencia (`szegedi2026`) y
el costo de comunicación (`kronauer2021`, `macenski2022`, `luo2025`). La
matriz no debe crecer durante la campaña final (`docs/plan.md` §17, fase 5).

**Entregable.** §3.6 con las resoluciones exactas, la definición del punto de
aplicación y la tabla actualizada; resumen y abstract solo si nombran las
resoluciones. Actualizar el texto que justifica la dimensión si la definición
elegida cambia el argumento.

**Criterios de aceptación.** Cada resolución tiene un valor exacto y un punto
de aplicación; la matriz coincide con el código de P-09/P-10; no hay
condiciones faltantes ni adicionales; el texto no afirma un escalamiento que
el diseño no produce.

**Dependencias.** Requiere P-03 y P-04. Desbloquea P-06, P-09 y P-13.

**Notas.** Si se descubre que la resolución no afecta la comunicación por el
diseño de las fronteras, es preferible corregir el argumento a agregar
condiciones nuevas.

**Nota (2026-10-19, al cerrar P-03).** P-03 ya resolvió el punto (c) de las
decisiones pendientes: la entrada del modelo queda fija en 640$\times$640 en
todas las condiciones, y por eso se corrigió el argumento de §3.6 —la
resolución ya no se justifica por el costo de inferencia, sino por el volumen
de datos que atraviesa la cadena—. Queda por decidir si la resolución
experimental se aplica al fotograma que se decodifica (a) o a la imagen que se
publica en el primer tópico (b), y queda por registrar el clip concreto de
BDD100K con su SHA-256, contenedor, códec, número de fotogramas y fecha de
descarga; la regla de selección ya está fijada en `sec:input-sequence`.

**Nota (2026-10-19, al cerrar P-04).** P-04 resolvió el punto (b): el primer
tópico transporta el fotograma a la resolución experimental, porque §3.3.2
redimensiona en la etapa de adquisición y la tabla `tab:operations` fija esa
carga útil. La matriz pasó a **4 configuraciones × 3 resoluciones = 12
condiciones** (`tab:experimental-matrix`), de modo que P-05 solo debe fijar
los tres valores de resolución y registrar el clip (nombre, SHA-256,
contenedor, códec, fotogramas, fecha). La tabla `tab:partitioning-payloads` ya
usa las resoluciones candidatas: si cambian, hay que recalcularla junto con la
justificación de §3.6.

---

### P-06 · Diseñar el procedimiento de benchmark

**Estado: completado (2026-10-19).** §3.7 se reescribió y quedó dividida en
cuatro subsecciones: «Modo de conducción de la fuente» (`sec:driving`),
«Política de descarte y denominadores» (`sec:discards`), «Secuencia de la
corrida» (`sec:run-sequence`) y «Hoja de ejecución y registro de
desviaciones» (`sec:run-sheet`). Decisiones fijadas:

- **Conducción: lazo abierto, sin acuses ni barreras.** Se descarta la
  contrapresión clásica porque suprimiría el solapamiento de §3.6.1, haría
  depender la oferta de la variable medida y agregaría un camino de retorno
  que ninguna arquitectura comparada tiene.
- **Dos ventanas de medición por corrida, no dos condiciones.** La *ventana
  saturada* (fuente sin ritmo) mide la tasa de procesamiento, los descartes,
  la utilización de recursos y los fotogramas en vuelo; la *ventana regulada*
  (fuente decimada a `f0 = 30/k` FPS, por debajo de la capacidad de las doce
  condiciones) mide la latencia de extremo a extremo sobre todos los
  fotogramas y sostiene la verificación de equivalencia de §3.5.3. El divisor
  `k` se fija en los pilotos como el menor entero positivo que no produce
  descartes en ninguna condición; la regla garantiza la misma tasa y la misma
  secuencia de fotogramas en las doce condiciones. La razón de separar las
  ventanas es doble: una tasa fija baja trunca la tasa de procesamiento de las
  configuraciones rápidas, y una fuente saturada recorta la distribución de
  latencia por el lado alto, con un recorte que depende de la tasa de cada
  configuración.
- **Política de descarte: se descarta el fotograma más antiguo y se conserva
  el más reciente.** No es una decisión nueva: es la consecuencia de
  `KEEP_LAST` con profundidad 1 (§3.2.1). El texto declara además que el
  piloto verifica si el middleware reemplaza la muestra pendiente o retiene al
  publicador, porque ambas conductas respetan la invariante de §3.6.1 —a lo
  sumo una muestra pendiente por frontera— y ninguna acumula latencia en cola.
- **Denominadores.** `FPS` = fotogramas completados / duración efectiva de la
  ventana; los descartes no entran en el numerador ni en el denominador y se
  informan aparte como tasa de oferta y proporción de descarte por frontera.
  La latencia se compara solo con la ventana regulada; la de la ventana
  saturada se registra como material de diagnóstico, condicionada a la
  aceptación del fotograma. Los descartes se cuentan por índice de fotograma y
  los fotogramas en vuelo se derivan del mismo registro, sin usar marcas
  internas para comparar arquitecturas.
- **Valores concretos.** Calentamiento por meseta térmica antes de *cada*
  ventana: mínimo 120 s, bloques de 60 s, ΔT < 0,5 °C, máximo 300 s. Ventana
  regulada de 60 s; ventana saturada de 120 s. Diez bloques de doce corridas
  en orden aleatorio con semilla versionada; la corrida es la unidad de
  repetición. Validez de la corrida en cinco condiciones (equivalencia,
  ausencia de descartes en la ventana regulada, estabilidad térmica,
  integridad del monitoreo y ventanas completas); una corrida inválida se
  repite al final del bloque y se anota. Reinicio por enfriamiento hasta un
  umbral de reposo fijado en los pilotos. Estimación: 120 corridas, del orden
  de 18 h de máquina.
- **Herencia de P-04 resuelta.** La lista no introduce sincronización que
  suprima el solapamiento, declara la política de descarte y el denominador
  idénticos en las cuatro configuraciones, y agrega el criterio de validez que
  §3.3.1 y §3.5.3 ya prometían: comparación por índice de fotograma contra la
  salida de referencia, con la decisión explícita de repetir la corrida ante
  cualquier discrepancia.
- **Alternativa registrada y rechazada: `KEEP_LAST` de profundidad 10**, que
  es la del perfil por omisión de ROS 2 (`rmw_qos_profile_default`). Se
  evaluó durante P-06 como forma de evitar la ventana regulada, con el
  argumento de que un historial más profundo absorbería la fuente sin ritmo.
  No lo hace: con oferta superior a la capacidad la cola se llena y se queda
  llena, de modo que la profundidad sólo cambia la forma del artefacto (de
  truncamiento a encolamiento de orden `(N-1)/λ`, unos 300 ms con `N = 10` y
  30 FPS, frente a un costo por fotograma de milisegundos). Tampoco acerca al
  caso monolítico: a profundidad 10 la cadena procesa fotogramas de ~1/3 s de
  antigüedad, mientras el bucle monolítico procesa siempre el más reciente.
  Se conserva la profundidad 1 y la decisión se prueba empíricamente con la
  verificación de sensibilidad de los pilotos (§3.7.3, cuatro corridas sobre
  C a 640×360), para responder en la defensa con una medición y no con un
  argumento. Nota: «canónico» no resuelve la elección por sí solo, porque
  ROS 2 tiene dos perfiles habituales para datos de sensor
  (`rmw_qos_profile_default`, profundidad 10 confiable;
  `rmw_qos_profile_sensor_data`, profundidad 5 best-effort).
- **Corrección de §3.2.1.** El texto argumentaba que una profundidad mayor
  que uno «introduciría solapamiento entre etapas». Es incorrecto: con
  profundidad 1 el solapamiento ya existe —una muestra pendiente por frontera
  es justamente lo que permite los `k` fotogramas en vuelo de §3.6.1—. Lo que
  la profundidad mayor agrega es encolamiento cuya ocupación depende del
  desajuste entre oferta y capacidad; el argumento quedó reescrito así, con
  el cálculo de `(N-1)/λ` y el costo de memoria.
- **Corrección de §3.7.2.** El texto afirmaba que la contrapresión
  «eliminaría la distinción entre la capacidad de la cadena y la de su etapa
  más lenta». También es incorrecto: el rendimiento de una cadena solapada es
  el de su cuello de botella con descarte o con bloqueo. Lo que la
  contrapresión destruye es la exogeneidad de la tasa ofrecida (la medición
  pasa a ser un equilibrio consigo misma), los descartes como observable
  (cero por construcción), los fotogramas en vuelo como cantidad emergente, y
  la formulación de la pregunta de despliegue. Además, A no tiene frontera
  donde aplicar la espera. El párrafo quedó reescrito con esos argumentos.
- **Nueva condición de validez.** La ventana saturada exige que la tasa de
  oferta (fotogramas despachados por la etapa de adquisición) exceda con
  holgura la tasa de completación; si se pegan, la fuente quedó estrangulada
  por la espera en las fronteras y la corrida no es una ventana saturada.
  Esto es lo que distingue saturación real de control de flujo, y es la misma
  incógnita que el piloto resuelve sobre la conducta del middleware.
- **Plantilla de corrida.** `docs/plantilla-corrida.md` contiene la hoja de
  ejecución en YAML, las columnas mínimas del registro por fotograma, el
  formato del registro de desviaciones, las decisiones que fija el piloto y
  el diseño de la verificación de sensibilidad al perfil de QoS. Es la
  especificación que P-11 debe materializar.

Ajustes de coherencia en el mismo commit: §3.5.3 pasa a declarar que la salida
de referencia cubre la totalidad del clip (antes «un tramo fijo») y remite la
tasa de prueba a `sec:driving`; §3.6 remite duración y repeticiones a §3.7;
§3.8.2 precisa qué cuenta como fotograma procesado; §3.9 agrega la tasa
regulada y la hoja de ejecución a la lista de reproducibilidad; se actualizó el
comentario de cabecera de `capitulo-3.tex`. Quedaban 6 `\todo` visibles en el
capítulo: los cinco de P-07 (§3.8), que ese pendiente cerró, y uno de P-08
(§3.9), que sigue abierto.

**Propuesta para el autor (no aplicada).** La decisión de medir con dos
ventanas no figura en `docs/plan.md` §11, que describe una sola ejecución por
condición. No se agregó una dimensión experimental —las condiciones siguen
siendo las doce de `tab:experimental-matrix`—, pero cada corrida tiene ahora
dos ventanas. La alternativa simple es una sola ventana saturada: cuesta la
mitad del tiempo de campaña, pero la latencia quedaría medida solo sobre los
fotogramas aceptados, con un recorte que depende de la tasa de cada
configuración y que favorece a las más lentas, que perderían justamente la
cola de su distribución de latencia. Si el autor
prefiere esa vía, se elimina la ventana regulada de §3.7.1 y se ajustan §3.5.3
y §3.7.3 en consecuencia.

**Nota para P-07.** §3.7 le impone tres requisitos: registro por nodo de
(índice de fotograma, instante de recepción, instante de despacho) para contar
descartes y fotogramas en vuelo; marcas de frontera de cadena para la latencia;
y un intervalo de muestreo del monitoreo que no deje huecos dentro de las
ventanas.

**Nota para P-08.** Las diez repeticiones por condición se fijaron pensando en
contrastes pareados por bloque. Si el análisis preespecificado necesita más
potencia, se sube el número de bloques; no se cambia la lógica del
procedimiento ni se reducen las repeticiones.

---

### P-07 · Definir la instrumentación y la medición de métricas

**Estado: completado (2026-10-19).** §3.8 quedó reescrita y sin `\todo`: fija
reloj, puntos de marca, transporte del índice en la cabecera, herramienta,
intervalo y agregación de cada métrica, la decisión sobre potencia y su línea
base, el criterio de integridad del monitoreo y el formato del registro.
La especificación concreta para P-11 —esquema de la base, patrón de código,
rutas de `sysfs`, verificaciones del piloto— está en
`docs/instrumentacion.md`, y la hoja de ejecución de
`docs/plantilla-corrida.md` se ajustó al esquema nuevo.

**Decisiones registradas.**

- **Reloj.** `time.perf_counter_ns()`, que en Linux es
  `clock_gettime(CLOCK_MONOTONIC)` con resolución de 1 ns. Se descarta el
  reloj del sistema porque es ajustable y una corrección NTP en mitad de una
  corrida produciría latencias negativas o infladas; se descarta el reloj de
  ROS 2 porque deriva del reloj del sistema, puede sustituirse por `/clock` y
  devuelve un mensaje, de modo que su origen y su costo no serían los mismos
  que en la implementación monolítica, que no tiene reloj de ROS. Se verificó
  en el equipo que el reloj es comparable entre procesos: una lectura tomada
  en un proceso hijo cae dentro del intervalo medido por el padre. Como el
  reloj monótono no es tiempo de calendario, cada corrida registra su desfase
  con `CLOCK_REALTIME` al inicio y al cierre.
- **Puntos de marca.** Dos por fotograma y por operación: recepción en la
  primera instrucción de la operación y despacho **inmediatamente antes de
  publicar**. La marca de despacho no puede tomarse al retorno del callback:
  la serialización pertenece a la frontera y no al cómputo del nodo. La
  latencia primaria es `t_envio(7) − t_recv(1)` (§3.8.1, incluye la
  adquisición) y se informa además, como descomposición, `t_envio(7) −
  t_envio(1)`, que la excluye; la adquisición en B/C/D también depende de la
  arquitectura porque decodifica en lazo abierto y compite por la CPU.
- **Transporte de la instrumentación.** Solo el índice viaja, en
  `header.frame_id` con formato fijo (`f` + seis dígitos), sin que ninguna
  operación lo modifique. **La marca no viaja**: cada proceso escribe sus dos
  marcas en su propio registro y la consolidación une filas de procesos
  distintos por `(ventana, fotograma)`, porque `CLOCK_MONOTONIC` tiene el
  mismo origen en todos los procesos del anfitrión. `header.stamp` queda sin
  uso como portador de tiempo, de modo que no hay un campo con significado
  falso más allá de `frame_id`, que no designa un marco de `tf2` y así se
  declara en §3.8.1. Se descarta un tipo de mensaje propio porque cambiaría
  los tipos y las cargas útiles de `tab:operations` y agregaría una capa de
  serialización que la implementación monolítica no tiene: el instrumento no
  debe modificar el objeto que mide. La cabecera de ROS 2 no tiene número de
  secuencia, de modo que el índice debe viajar explícitamente: sin él no se
  distinguen descartes de saltos de orden, ni el analizador puede emparejar
  los extremos de la cadena cuando hay descartes.
- **CPU y memoria.** `tegrastats` para el sistema (porcentaje y frecuencia por
  núcleo, RAM en uso y total), más un **ámbito de control (cgroup v2)** creado
  por corrida con `systemd-run --user --scope` para atribuir a la cadena el
  tiempo de CPU (`cpu.stat:usage_usec`, contador acumulado: se lee al abrir y
  al cerrar la ventana, sin error de muestreo) y la memoria (`anon`+`shmem` de
  `memory.stat`, a 1 Hz). El ámbito abarca todos los procesos de la
  configuración, con sus hilos de middleware, y la implementación monolítica
  corre en uno equivalente, de modo que las dos se miden igual. Es la señal
  con la que se contrasta H3, porque el porcentaje de `tegrastats` es del
  sistema completo e incluye el monitoreo. Se descartó el sondeo de
  `/proc/<pid>/stat` (obliga a rastrear PIDs y deja la CPU muestreada) y
  `psutil` (leería lo mismo y agregaría una dependencia al entorno fijado en
  §3.2). En la Orin Nano la memoria es unificada y el GPU no tiene memoria
  separable: §2.6 condicionaba la memoria de GPU a que existiera una medición
  confiable, y la condición no se cumple, de modo que se informa una sola
  cantidad del sistema más la huella de la cadena.
- **GPU.** `GR3D_FREQ` (proporción de tiempo de activación del GPU) más la
  frecuencia del dominio de `devfreq`. No hay `nvidia-smi` en Jetson y el
  controlador no publica ocupación de unidades de ejecución; la cifra se
  informa como activación y no como fracción de capacidad.
- **Potencia: se mide.** `VDD_IN` de `tegrastats` (monitor INA3221 de tres
  canales del módulo: `VDD_IN`, `VDD_CPU_GPU_CV`, `VDD_SOC`), con potencia
  media, máxima, energía por fotograma (`eq:energia-fotograma`) y FPS/W
  (`eq:fps-watio`). Se declara que `VDD_IN` es la potencia del módulo y no la
  del equipo, y que la comparación vale por la identidad del instrumento y del
  estado, no por la exactitud absoluta de la lectura. La potencia no entra en
  H1–H4: se informa como resultado descriptivo. Cada corrida tiene una **línea
  base en reposo**, tomada de los últimos 60 s de la espera de enfriamiento
  que §3.7 paso 8 ya contempla —no agrega tiempo a la campaña—, porque se
  midió que la potencia de entrada se desplaza del orden de 0,4 W en un
  minuto, magnitud comparable a la diferencia que se busca medir. Esto resuelve el `% TODO` de
  `sections/capitulo-2.tex` sobre el método de medición de potencia, que era
  la nota de este pendiente, y agrega dos entradas a `referencias.bib`
  (`nvidiacorporation2026tegrastats`, `nvidiacorporation2026potencia`),
  coordinado con P-19 y P-22.
- **Intervalo de monitoreo: 500 ms.** Elegido con una medición en el equipo y
  no por convención: a 100 ms `tegrastats` no sostiene la cadencia (9,1 Hz
  pedidos 10) y cuesta 1,25 % de un núcleo; a 500 ms sostiene 2,0 Hz con
  desviación del 2 %, cuesta 0,37 % de un núcleo y entrega 120 muestras en la
  ventana regulada y 240 en la saturada. Los campos de media y máximo que
  imprime la herramienta no se usan: se verificó que se acumulan desde el
  arranque de la herramienta y no desde el comienzo de la ventana, de modo que
  la agregación se calcula sobre el valor instantáneo de cada muestra, con
  media ponderada por el intervalo entre muestras.
- **Perturbación.** Marcas y muestras se acumulan en memoria y se escriben al
  cerrar cada ventana; no hay entrada y salida dentro de la ventana. El arnés
  que monitorea es siempre un proceso distinto del que ejecuta la cadena,
  incluso en A, porque de otro modo A cargaría con el costo del monitoreo. El
  costo de la instrumentación se midió en el equipo (1,0 µs por operación
  medida, 7 µs por fotograma: 0,07 % de un fotograma de 10 ms) y el del
  monitoreo también (0,37 % de un núcleo), y ambos se informan para que puedan
  descontarse.
- **Formato.** Una base SQLite por corrida (`corridas/<id>/<id>.db`), más el
  registro crudo de `tegrastats` y la hoja de ejecución; la base de la campaña
  se consolida con un paso reproducible y es regenerable. La columna
  `omitidos` reemplaza al indicador binario `descartado` de la plantilla: los
  descartes de una frontera son la suma de los fotogramas que el productor
  publicó y el consumidor no recibió, y un bit no puede expresarlos.
- **Integridad del monitoreo.** Criterio (iv) de §3.7 cuantificado:
  `N_esp = Δt / mediana(Δt)`; la ventana es válida si
  `N_obs ≥ 0,97 N_esp` y ninguna separación entre muestras supera
  `3 · mediana(Δt)`. La hoja de ejecución registra las cuatro cifras, de modo
  que la comprobación sea auditable.

**Verificación empírica en el equipo (2026-10-19).** Se comprobaron en la
Orin Nano, con L4T R39.2.1 y CPython 3.12.3: los campos que `tegrastats`
reporta y los que no (`EMC_FREQ`, `SWAP`, frecuencia de GPC en `GR3D_FREQ`);
el significado de los tres valores de cada raíl; la cadencia y el costo de la
herramienta a cuatro intervalos; el costo de las marcas; la igualdad del reloj
entre procesos; las rutas de `sysfs` para las frecuencias de GPU
(`17000000.gpu`) y de memoria (`bwmgr`), y la legibilidad de los raíles INA3221
sin privilegios. Los valores están en `docs/instrumentacion.md` §3.1 y §2.4.
Se observó además que el intérprete que resuelve `python3` en el `PATH` del
equipo es uno de Homebrew (3.15.0) y no el del sistema (3.12.3): la cadena y
el arnés deben invocarse con `/usr/bin/python3` o con el intérprete de ROS 2,
y conviene fijarlo por ruta.

**Archivos modificados.** `sections/capitulo-3.tex` §3.8 (ocho subapartados y
dos tablas nuevas: `tab:metric-instrumentation`, `tab:sampling-interval`);
`sections/capitulo-2.tex` §2.6 (cita del método y remisión a `sec:power`);
`referencias.bib` (dos entradas); `docs/instrumentacion.md` (nuevo);
`docs/plantilla-corrida.md` (§1 formatos, §2 hoja con integridad y recursos,
§3 columnas, §5 línea base de potencia por corrida); `AGENTS.md` (índice de
documentos de trabajo).

**Decisiones confirmadas por el autor (2026-10-19) y ya aplicadas.**

1. *Transporte del índice.* Solo el índice viaja, en `header.frame_id`
   (`f%06d`). `header.stamp` **no** se usa como portador de tiempo y la marca
   de adquisición no se transporta: cada proceso escribe sus dos marcas en su
   propio registro y la consolidación une filas por `(ventana, fotograma)`,
   porque `CLOCK_MONOTONIC` tiene el mismo origen en todos los procesos. Se
   descartó el tipo de mensaje propio (cambiaría los tipos y las cargas útiles
   de `tab:operations` y agregaría una capa de serialización que A no tiene) y
   se declaró en §3.8.1 que `frame_id` no designa un marco de `tf2`.
2. *Potencia.* Se incluye como métrica descriptiva, fuera de H1–H4, con
   cláusula de escape: si el piloto muestra lecturas inestables, se informa la
   inestabilidad y la métrica no sostiene conclusiones. `sections/capitulo-2.tex`
   §2.6.6 dejó de llamarla opcional.
3. *Atribución a la cadena.* Se mide, y no por sondeo de `/proc/<pid>/stat`
   como especificaba la primera versión del documento interno, sino por
   **ámbito de control (cgroup v2)** creado por corrida con `systemd-run
   --user --scope`: `cpu.stat:usage_usec` es un contador acumulado (exacto, sin
   error de muestreo) y `memory.stat` da `anon`+`shmem`. Verificado en el
   equipo: cgroup v2 unificado y `systemd-run --user --scope` sin `sudo`;
   con un proceso de 2 s de reloj, `usage_usec` = 1 730 843 µs. Evita rastrear
   PIDs y mantiene la simetría con A, que corre en un ámbito equivalente.
4. *Línea base de potencia.* Una **por corrida**, tomada de los últimos 60 s
   de la espera de enfriamiento que el procedimiento ya contempla (§3.7 paso
   8), de modo que no agrega tiempo a la campaña ni corridas ni condiciones.
   Motivo medido: con 60 s de muestreo, `VDD_IN` se desplazó 0,34 W en torno a
   su media y 0,41 W entre el comienzo y el final de la ventana —del orden de
   la diferencia que se busca medir—, de modo que la potencia absoluta no es
   comparable entre bloques sin referencia.

Aplicado en: `sections/capitulo-3.tex` (§3.8.1 cabecera, §3.8.2 remisión,
§3.8.3 y §3.8.4 ámbito de control, §3.8.6 línea base, §3.8.7, tabla de
instrumentos, §3.7 paso 8), `referencias.bib` (`linuxkernel2026cgroup`),
`docs/instrumentacion.md` (§1 sin pendientes y con las cuatro decisiones, §2.3
reescrito, §3.3 nueva, §4 esquema con el ámbito y la línea base, volcado de
§9) y `docs/plantilla-corrida.md` (bloque `ambito:`, `recursos:` con memoria
del ámbito y potencia atribuible, línea base por corrida).

**Observación para P-02.** El equipo informa OpenCV 4.8.0, mientras
`tab:software-environment` fija 4.6.0. No se toca aquí porque la tabla es de
P-02; hay que verificarla antes de la campaña.

---

### P-08 · Preespecificar el análisis estadístico

**Estado actual.** §3.9 deja los tests como `\todo{SPECIFY}` “una vez conocida
la distribución” (`sections/capitulo-3.tex:354`), enumera el análisis
descriptivo y las diferencias porcentuales, y enuncia H1–H4
(`sections/capitulo-3.tex:356-386`). No define la unidad de análisis ni cómo
se evita la pseudorreplicación.

**Herencia de P-04 (2026-10-19).** La matriz tiene 12 condiciones y las
configuraciones están anidadas. §3.6 ya compromete que el análisis se exprese
como contrastes entre configuraciones consecutivas (A→B, B→C, C→D) y no como
una colección de comparaciones por pares entre las doce condiciones; P-08 debe
preespecificar esos contrastes, su intervalo de confianza y la unidad de
análisis, y declarar por separado la limitación de que la cadena de ROS 2
solapa fotogramas mientras la línea base no (§3.6.1).

**Objetivo.** Fijar un plan de análisis antes de la campaña final, de modo que
las pruebas no se elijan después de ver los resultados.

**Decisiones que hay que tomar.**

- **Unidad de análisis.** Los fotogramas de una misma ejecución no son
  independientes. Definir si se agrega por ejecución (media, mediana, P95) y
  luego se comparan ejecuciones, o si se usa un modelo mixto. No tratar miles
  de fotogramas como miles de réplicas independientes.
- **Diseño.** Las condiciones se miden sobre el mismo equipo y la misma
  entrada; definir si el diseño es pareado (misma ejecución/orden) o
  independiente, y cómo se refleja en la prueba.
- **Pruebas y supuestos.** Prueba de normalidad y homocedasticidad, y la regla
  de decisión entre una prueba paramétrica y una no paramétrica (por ejemplo,
  t pareada vs. Wilcoxon, o ANOVA vs. Kruskal-Wallis), o bootstrapping. Dejar
  la regla escrita, no solo el nombre de la prueba.
- **Tamaño del efecto e intervalos de confianza.** Además del valor p;
  reportar la magnitud de la diferencia, que es lo que la pregunta de
  investigación pide.
- **Comparaciones múltiples.** Tres configuraciones × tres resoluciones ×
  varias métricas: definir corrección (Bonferroni, Holm, FDR) o el enfoque
  jerárquico.
- **Percentiles.** Cómo se calculan P95 y P99 (por ejecución y luego se
  agrega, o sobre el conjunto de fotogramas), y el número mínimo de muestras.
- **Hipótesis.** Mapear H1–H4 a métricas y pruebas concretas. Revisar H3:
  menciona CPU y memoria, pero las métricas incluyen GPU; decidir si se
  amplía o se deja como está.
- **Valores atípicos y datos faltantes.** Regla de exclusión y de reporte.

**Contexto y restricciones.** `docs/plan.md` §13 exige estadísticas
descriptivas, comparación de latencias, tasa de procesamiento y recursos,
diferencias porcentuales y evaluación de la tendencia de particionamiento. El
capítulo 3
ya define la fórmula de sobrecosto (`eq:overhead`). Las hipótesis son
predicciones, no resultados esperados.

**Entregable.** §3.9 con el plan completo, las pruebas y la regla de decisión;
especificación para el script de P-14.

**Criterios de aceptación.** El plan es falsifiable y está fijado antes de la
campaña; cada hipótesis tiene una prueba y un criterio; la unidad de análisis
evita pseudorreplicación; se distingue análisis confirmatorio de exploratorio.

**Dependencias.** Se puede escribir ahora; los detalles de la matriz dependen
de P-05. Desbloquea P-14.

**Notas.** Si durante el análisis surge una prueba no prevista, reportarla
como exploratoria y no reemplazar el plan principal sin dejarlo registrado.

---

## 5. Bloque B — Implementación y experimentos

### P-09 · Implementar la cadena monolítica

**Estado actual.** No hay código de la cadena en este repositorio. El capítulo
3 §3.4 describe la línea base como un único proceso Python con las etapas
`Entrada → Preprocesamiento → Inferencia → Postprocesamiento → Salida`
(`sections/capitulo-3.tex:110-128`).

**Objetivo.** Implementar la línea base monolítica completa, con la misma
carga de trabajo y el mismo runtime que usarán los nodos de ROS 2.

**Requisitos.**

- Leer la fuente de entrada definida en P-01 y aplicar las resoluciones de
  P-05.
- Reutilizar exactamente el mismo código de preprocesamiento, inferencia y
  postprocesamiento que la implementación de ROS 2 (P-10). La única diferencia
  entre arquitecturas debe ser la frontera de comunicación, no el algoritmo.
- Respetar el modelo, los pesos, la precisión y los umbrales de P-03.
- Implementar los calentamientos, las dos ventanas y la política de descarte de
  §3.7 (P-06), con la hoja de ejecución de `docs/plantilla-corrida.md`.
- Registrar por fotograma las marcas de tiempo y los resultados, con el
  esquema de P-07.
- Exponer la configuración por línea de comandos o archivo (resolución,
  fuente, duración, salida), sin valores incrustados.
- No importar ROS 2 ni depender de un daemon de ROS.

**Contexto y restricciones.** La línea base representa el extremo sin
serialización ni transporte entre procesos. Debe ser funcionalmente
equivalente a la cadena de ROS 2 (P-04). No se permite optimizar la línea base
con técnicas que no estén disponibles en la implementación de ROS 2, ni
viceversa: eso destruiría la comparación.

**Entregable.** Código ejecutable, instrucciones de ejecución y una salida de
referencia sobre una secuencia fija de entrada.

**Criterios de aceptación.** Se ejecuta en la Orin Nano con los valores de
P-01/P-02/P-03; procesa la secuencia fija y produce detecciones y marcas de
tiempo; la salida de referencia sirve para verificar P-10; el código queda
versionado (ver P-11); no hay rutas absolutas ni credenciales.

**Dependencias.** Requiere P-03 y P-05. Desbloquea P-10 y P-11.

**Notas.** P-04 decidió (2026-10-19) que la línea base procesa los fotogramas
estrictamente en secuencia: no se le da un pipeline solapado con hilos ni
colas, porque eso introduciría la concurrencia interna como segunda variable
(§3.6.1). El solapamiento de las configuraciones de ROS 2 se declara y se
registra. La implementación debe ejecutar las siete operaciones de
`tab:operations` en el mismo orden que los nodos, con las mismas funciones.

---

### P-10 · Implementar la cadena ROS 2

**Estado actual.** No hay código. El capítulo 3 §3.5 describe nodos rclpy
separados, QoS fija y ejecutor fijo (`sections/capitulo-3.tex:129-160`), pero
el mapeo y la verificación de equivalencia están en `\todo`.

**Objetivo.** Implementar las configuraciones B, C y D como procesos ROS 2
separados, con los tópicos, tipos, QoS y ejecutor definidos en P-02 y P-04.

**Requisitos.**

- Un nodo por operación o grupo de operaciones según `tab:configurations` de
  P-04 (2, 4 y 7 nodos), cada uno como proceso del sistema operativo.
- Los seis tópicos de `tab:operations` con sus tipos y codificaciones
  (`bgr8` en el primero, `rgb8` en el segundo) y la resolución experimental en
  el primero.
- QoS y ejecutor idénticos en todos los nodos y configuraciones (P-02).
- Archivos de lanzamiento o equivalente para arrancar B y C de forma
  reproducible.
- Reutilizar el código de procesamiento de P-09; no duplicar la lógica.
- Parámetros para resolución, fuente, duración y salida.
- Registro de marcas de tiempo y resultados con el esquema de P-07.
- Ningún mecanismo excluido: sin nodos componibles, sin comunicación
  intraproceso, sin transporte por memoria compartida distinto del fijado.

**Contexto y restricciones.** La comparación es entre la arquitectura
ordinaria de nodos multiproceso y el monolito; la composición y la
comunicación intraproceso se discuten como trabajo futuro, no se implementan
aquí. La equivalencia funcional debe comprobarse contra la salida de
referencia de P-09.

**Entregable.** Código de nodos, archivos de lanzamiento, configuración de
QoS y una prueba de equivalencia funcional documentada.

**Criterios de aceptación.** B y C arrancan y procesan la secuencia fija;
las salidas son equivalentes a P-09 dentro de la tolerancia declarada; el
grafo de nodos coincide con el diagrama y con §3.5–§3.6; no se usan
mecanismos fuera de alcance; el código queda versionado.

**Dependencias.** Requiere P-04 y P-09. Desbloquea P-11 y P-12.

**Notas.** Verificar que el ejecutor y la QoS sean realmente los mismos en
todos los nodos; un valor por defecto distinto en un solo nodo invalida la
comparación. Documentar cómo se comprobó.

---

### P-11 · Construir el arnés de benchmark y versionar el artefacto

**Estado actual.** El capítulo 3 §3.10 afirma que “el código fuente y la
configuración del benchmark están bajo control de versiones”
(`sections/capitulo-3.tex:423`), pero no hay código en el repositorio. No hay
esquema de datos, orquestador ni repositorio de resultados.

**Pendiente heredado de P-02.** Antes de la primera corrida, verificar en el
equipo los valores de `tab:software-environment` con los comandos de esa tabla
y registrar el manifiesto de paquetes del paso (iii) de §3.2: `ros-jazzy-*`
7.1.x, `ros-jazzy-fastrtps` 2.14.7, `python3-numpy` 1.26.4 y `python3-opencv`
4.6.0. Si alguno difiere, corregir la tabla de §3.2 antes de ejecutar los
pilotos; el manifiesto se guarda con el artefacto de la corrida.

**Objetivo.** Construir el arnés que ejecuta una condición completa de forma
automática y registrar los datos con metadatos suficientes para reproducirla.

**Requisitos.**

- Orquestador que, para una condición, arranque la configuración A, B o C,
  espere el calentamiento, ejecute la carga durante la duración fijada, recoja
  las métricas, detenga los procesos y guarde los resultados.
- Monitoreo de CPU, RAM, GPU y potencia, con la herramienta y el intervalo de
  P-07 (500 ms), y muestreo propio a 1 Hz de frecuencias y de la memoria del
  ámbito de control.
- Lanzar la cadena dentro de un ámbito de control propio de la corrida
  (`systemd-run --user --scope`), que es lo que permite atribuirle CPU y
  memoria (`docs/instrumentacion.md` §3.3).
- Registro por fotograma y resumen por ejecución; metadatos: fecha, commit,
  versiones de software, modo de energía, temperatura inicial y final,
  resolución, configuración y cualquier desviación.
- Nombres de archivo y estructura de directorios estables; datos crudos
  inmutables; verificación de integridad si es posible.
- Repeticiones y orden según §3.7 (P-06); posibilidad de reanudar una campaña
  interrumpida.
- Un solo comando por condición; nada de pasos manuales no documentados.

**Decisión de repositorio.** Definir dónde vive el código: un repositorio
hermano, un subdirectorio de este repositorio o un repositorio aparte. Debe
quedar versionado, con README de reproducción, dependencias fijadas y licencia
si se publica. Este repositorio es de la memoria; no mezclar datos pesados ni
artefactos de build con el texto.

**Contexto y restricciones.** El artefacto reproducible es una de las
contribuciones declaradas en el capítulo 1. La afirmación de §3.10 debe ser
verdadera al momento de la entrega. El arnés debe tratar A, B y C de la misma
manera para no introducir sesgos. `docs/plan.md` §17 (fase 3) pide
marcas de tiempo, latencia, FPS, CPU, RAM, GPU y registro de datos.

**Entregable.** Arnés ejecutable, esquema de datos documentado, README de
reproducción, repositorio versionado y una corrida de humo que demuestre el
flujo completo.

**Criterios de aceptación.** Una condición se ejecuta de principio a fin con
un comando; los datos incluyen los metadatos necesarios; P-14 puede leerlos sin
transformaciones manuales; el código está versionado y la afirmación de §3.10
es verificable.

**Dependencias.** Requiere P-06, P-07, P-09 y P-10. Desbloquea P-12.

**Notas.** No convertir el arnés en un proyecto aparte más grande que la
memoria. Priorizar reproducibilidad sobre funcionalidades adicionales.

---

### P-12 · Ejecutar experimentos piloto

**Estado actual.** El capítulo 3 menciona los pilotos
(`sections/capitulo-3.tex:256-259`), pero no hay registro de que se hayan
ejecutado.

**Objetivo.** Validar la instrumentación, el procedimiento y las
configuraciones antes de la campaña final.

**Qué debe cubrir.**

- Al menos una resolución completa con A, B y C.
- Verificación de que las marcas de tiempo permiten emparejar entrada y
  salida de cada fotograma.
- Verificación de que la política de descarte y la QoS se comportan como se
  espera.
- Medición de la variabilidad entre repeticiones y de la estabilidad térmica.
- Detección de cuellos de botella inesperados, errores de configuración y
  supuestos incorrectos.
- Medición del costo del propio monitoreo.

**Contexto y restricciones.** El propósito es fijar la metodología, no generar
resultados finales. Los datos de pilotos no deben mezclarse con los de la
campaña final ni reportarse como resultados. Cualquier ajuste a P-05, P-06 o
P-07 debe quedar registrado.

**Entregable.** Reporte breve de pilotos (interno, no parte de la memoria) con
hallazgos, cambios aplicados y problemas abiertos; metodología actualizada.

**Criterios de aceptación.** Las tres configuraciones se ejecutan sin
intervención manual; la instrumentación produce datos utilizables; los
problemas encontrados están resueltos o documentados; la metodología queda
congelada para P-13.

**Dependencias.** Requiere P-09, P-10 y P-11. Desbloquea P-13.

**Notas.** Si un piloto revela que el diseño no responde la pregunta (por
ejemplo, que la comunicación no escala con la resolución), es preferible
corregir el diseño ahora que en la discusión.

---

### P-13 · Ejecutar la campaña experimental final

**Estado actual.** Pendiente.

**Objetivo.** Ejecutar la matriz completa de P-05 con el procedimiento
congelado de P-06 y archivar los datos crudos.

**Requisitos.**

- Todas las condiciones (3 arquitecturas × 3 resoluciones) con el número de
  repeticiones fijado.
- Orden y reinicio según P-06; registrar temperatura, modo de energía y carga
  del sistema.
- Registrar cualquier desviación de la metodología, con fecha y motivo.
- Archivar datos crudos sin editar, con metadatos y, si es posible, checksums.
- Hacer copia de respaldo antes de cualquier análisis.
- No agregar dimensiones ni condiciones nuevas durante la campaña.

**Contexto y restricciones.** `docs/plan.md` §17 (fase 5) prohíbe agregar
dimensiones nuevas por interés durante esta fase. Si una condición falla, se
documenta y se repite; no se reemplaza silenciosamente.

**Entregable.** Conjunto de datos completo, registro de ejecuciones y bitácora
de desviaciones.

**Criterios de aceptación.** La matriz está completa; cada archivo tiene
metadatos; las desviaciones están documentadas; los datos son reproducibles a
partir del arnés y la configuración archivada.

**Dependencias.** Requiere P-12. Desbloquea P-14.

**Notas.** La duración de la campaña depende de P-06; no improvisar repeticiones
adicionales para “mejorar” un resultado.

---

## 6. Bloque C — Resultados y escritura

### P-14 · Analizar datos y generar tablas y figuras

**Estado actual.** Pendiente. El capítulo 3 §3.9 define el análisis, pero no
existe el código de análisis ni las figuras de resultados.

**Objetivo.** Limpiar los datos, aplicar el plan de P-08 y producir las tablas
y figuras que alimentarán el capítulo 4.

**Requisitos.**

- Script de limpieza reproducible: exclusión de calentamiento, valores
  atípicos según P-08 y agregación por ejecución.
- Estadísticas descriptivas por condición: media, mediana, desviación
  estándar, mínimo, máximo, P95 y P99 cuando haya muestras suficientes.
- Comparaciones entre configuraciones y cálculo de sobrecosto con
  `eq:overhead`.
- Figuras y tablas legibles en impresión, con unidades, etiquetas en español,
  títulos y notas; una figura por mensaje, sin saturar.
- Matriz de trazabilidad: cada número del capítulo 4 debe poder rastrearse
  hasta el dato crudo y el script que lo produjo.
- Guardar los resultados intermedios y la versión del script.

**Contexto y restricciones.** El capítulo 2 §2.6 define las métricas; el
capítulo 3 §3.9 define el análisis. No se cambia la definición de una métrica
después de ver los datos. El contrato de estilo de `AGENTS.md` está formulado
para diagramas D2/Graphviz; para las figuras de datos, mantener una paleta y
una tipografía coherentes con el documento.

**Entregable.** Scripts de análisis, tablas y figuras finales, y un documento
interno de trazabilidad.

**Criterios de aceptación.** Todos los resultados son reproducibles desde los
datos crudos; no hay números “a mano”; las figuras están listas para
`\includegraphics`; las tablas usan `booktabs` y son legibles; las etiquetas y
unidades son correctas.

**Dependencias.** Requiere P-13 y P-08. Desbloquea P-15.

**Notas.** Si aparece un resultado inesperado, no se descarta: se documenta y
se discute en el capítulo 5.

---

### P-15 · Redactar el capítulo 4 (Resultados)

**Estado actual.** El capítulo no existe. `main.tex` no lo incluye. El capítulo
1 §1.6 y `docs/plan.md` §16 lo anuncian con las secciones 4.1–4.7.

**Objetivo.** Presentar los resultados experimentales de forma completa y sin
interpretación excesiva.

**Estructura mínima (según el plan).**

- 4.1 Tasa de procesamiento.
- 4.2 Latencia de extremo a extremo.
- 4.3 Utilización de CPU.
- 4.4 Utilización de memoria.
- 4.5 Utilización de GPU.
- 4.6 Consumo de energía, solo si se midió.
- 4.7 Efecto del grado de particionamiento.

**Requisitos.**

- Reportar las condiciones, el número de ejecuciones y la duración; no
  presentar un número sin contexto.
- Incluir tablas y figuras de P-14, referenciadas desde el texto.
- Describir lo observado; reservar causas, comparaciones con la literatura y
  veredictos de hipótesis para el capítulo 5.
- No repetir la metodología; remitir al capítulo 3.
- Mantener el español académico y la terminología del glosario.

**Contexto y restricciones.** El capítulo 4 responde “qué se observó”, no “por
qué”. Las hipótesis se evalúan en el capítulo 5. No se agregan resultados de
pilotos ni datos no incluidos en la campaña final.

**Entregable.** `sections/capitulo-4.tex` incluido en `main.tex`; tablas y
figuras finales; referencias cruzadas.

**Criterios de aceptación.** Todos los resultados de P-14 están presentados;
cada figura y tabla se referencia; no hay interpretación que corresponda al
capítulo 5; no hay números sin trazabilidad; el capítulo compila y aparece en
el índice.

**Dependencias.** Requiere P-14. Desbloquea P-16.

**Notas.** Si el volumen de resultados es grande, usar apéndices para datos
crudos o tablas auxiliares, no para evadir la presentación principal.

---

### P-16 · Redactar el capítulo 5 (Discusión)

**Estado actual.** El capítulo no existe. El capítulo 1 §1.6 y el plan lo
anuncian como interpretación de resultados, evaluación de hipótesis,
comparación con la literatura y discusión de hallazgos inesperados.

**Objetivo.** Interpretar los resultados del capítulo 4 y responder qué
significan para la pregunta de investigación.

**Preguntas que debe abordar (plan §16).**

- ¿Qué magnitud tuvo el sobrecosto de ROS 2?
- ¿Cambió con la resolución?
- ¿Aumentó con el número de fronteras?
- ¿Fue computacionalmente significativo frente al costo de inferencia?
- ¿Qué recurso resultó más afectado?
- ¿Dominó la carga de visión por computador el tiempo total?
- ¿Se apoyaron o contradijeron H1–H4?
- ¿Son consistentes los resultados con la literatura?
- ¿Qué hallazgos inesperados aparecieron?

**Requisitos.**

- Cada afirmación debe apoyarse en un resultado del capítulo 4 o en una fuente
  citada; distinguir observación, inferencia e interpretación.
- Comparar con `kronauer2021`, `macenski2022`, `macenski2023`, `kamiya2025`,
  `luo2025`, `betz2023a`, `betz2024`, `scalcon2024`, `szegedi2026`,
  `tang2026`, y con la literatura de monolito vs. microservicios
  (`blinowski2022`, `tapia2020`, `felisberto2024`) cuando corresponda.
- Evaluar explícitamente H1–H4 con el criterio de P-08; aceptar que una
  hipótesis puede no sostenerse.
- Discutir el factor de confusión entre número de fronteras y tamaño de carga
  útil, el efecto del solapamiento entre fotogramas y la diferencia entre
  latencia y tasa de procesamiento.
- Discutir limitaciones de validez sin convertirlas en disculpas.

**Contexto y restricciones.** No se introducen resultados nuevos. No se
generaliza más allá de la plataforma, la carga y el middleware estudiados. Las
explicaciones deben ser plausibles y contrastables, no especulativas sin
evidencia.

**Entregable.** `sections/capitulo-5.tex` incluido en `main.tex`.

**Criterios de aceptación.** H1–H4 tienen veredicto y justificación; cada
comparación con la literatura es correcta y citada; los hallazgos inesperados
están discutidos; las limitaciones coinciden con el alcance del capítulo 1;
no hay resultados nuevos ni afirmaciones universales.

**Dependencias.** Requiere P-15. Desbloquea P-17.

**Notas.** Es el lugar para explicar por qué el particionamiento puede aumentar
la tasa de procesamiento aunque aumente la latencia (solapamiento entre
etapas), si los datos lo muestran. No forzar esa explicación si no está
respaldada.

---

### P-17 · Redactar el capítulo 6 y cerrar la estructura

**Estado actual.** `sections/conclusiones.tex` contiene solo
`\chapter*{Conclusiones}` y se incluye en `main.tex:120`. El capítulo 1 §1.6
anuncia un capítulo 6 con conclusiones, hallazgos, limitaciones y trabajo
futuro. `docs/plan.md` §16 define 6.1–6.4. La bibliografía se imprime después
de ese archivo y el apéndice después de la bibliografía.

**Objetivo.** Escribir el capítulo 6 y dejar la estructura del documento
coherente con lo que el capítulo 1 promete.

**Tareas.**

- Crear `sections/capitulo-6.tex` como capítulo numerado, con:
  - 6.1 Conclusiones.
  - 6.2 Hallazgos principales.
  - 6.3 Limitaciones.
  - 6.4 Trabajo futuro.
- Reemplazar `sections/conclusiones.tex` (o eliminarlo) e incluir el nuevo
  capítulo en `main.tex` en el orden correcto, antes de la bibliografía.
- Asegurar que el capítulo aparezca en el índice general y que la bibliografía
  también aparezca (ver P-22).
- Responder directamente las preguntas de investigación principal y
  secundaria.
- Resumir los hallazgos cuantitativos más importantes, remitiendo al capítulo 4
  sin repetir todas las tablas.
- Derivar las limitaciones del alcance: una plataforma, una carga, un DDS, una
  QoS, Python/rclpy. No presentarlas como fallas del estudio.
- Redactar el trabajo futuro a partir de `docs/future.md`: DDS, QoS, Zenoh,
  Docker, distribuciones, C++/rclcpp, composición de nodos, comunicación
  intraproceso, copias de memoria, cadenas más largas, nodos en red, otras
  cargas y otro hardware. Mantener el mismo nivel de concreción del documento
  de trabajo futuro y no prometer resultados que el estudio no produjo.

**Contexto y restricciones.** El capítulo 6 debe ser consistente con el
capítulo 1 y con el alcance; no debe abrir nuevas líneas experimentales. La
frase del capítulo 2 sobre composición (“se discute como trabajo futuro en el
Capítulo 6”) debe quedar satisfecha.

**Entregable.** `sections/capitulo-6.tex`, `main.tex` actualizado, índice y
referencias cruzadas coherentes.

**Criterios de aceptación.** Existe un capítulo 6 numerado con las cuatro
secciones; responde ambas preguntas; las limitaciones se derivan del alcance;
el trabajo futuro cubre las exclusiones sin prometer resultados; no quedan
referencias al capítulo 6 sin destino; el índice muestra 1–6, bibliografía y
apéndice.

**Dependencias.** Requiere P-16 (y P-14 para los números). Desbloquea P-18 y
P-25.

**Notas.** No convertir el trabajo futuro en una segunda revisión de
literatura: debe ser breve y concreto.

---

### P-18 · Completar resumen y abstract

**Estado actual.** `sections/resumen.tex` tiene tres `\todo`
(`:22` modelo, `:28` resultados, `:32` conclusión). `sections/abstract.tex`
tiene los equivalentes en inglés (`:19`, `:25`, `:29`). Ambos describen la
metodología y las métricas, pero no el modelo ni los hallazgos.

**Objetivo.** Dejar resumen y abstract completos, alineados entre sí y con el
capítulo 6.

**Requisitos.**

- Nombre del modelo y, si aporta, su runtime y precisión (P-03).
- Hallazgo principal con las magnitudes clave, coherente con el capítulo 4.
- Respuesta a la pregunta de investigación y su implicación práctica, coherente
  con el capítulo 6.
- Misma información en español y en inglés; no traducir literalmente si eso
  produce inglés poco natural.
- Mantener la extensión de un resumen de memoria (no convertirlo en una
  introducción).
- Revisar las palabras clave si el trabajo final cambia el énfasis.

**Contexto y restricciones.** El resumen y el abstract son la cara visible de
la memoria; no deben prometer más de lo que los resultados permiten. No se
incluyen citas ni tablas. El español sigue la guía `academic-spanish`.

**Entregable.** `sections/resumen.tex` y `sections/abstract.tex` sin `\todo`.

**Criterios de aceptación.** No quedan marcadores; ambos textos dicen lo
mismo; las cifras coinciden con el capítulo 4; la conclusión coincide con el
capítulo 6; el inglés es correcto; las palabras clave son pertinentes.

**Dependencias.** Requiere P-17 y P-03.

**Notas.** Si el resultado principal es nulo o contrario a las hipótesis, el
resumen debe decirlo con precisión; no maquillarlo.

---

## 7. Bloque D — Cierre académico y editorial

### P-19 · Cerrar las brechas de citas de los capítulos 1–2

**Estado actual.** Quedan cuatro brechas explícitas; una quinta, la de
potencia, quedó resuelta en P-07:

1. **Privacidad como motivación** (`sections/capitulo-1.tex:31-34`). El
   comentario advierte que la afirmación no está respaldada por las fuentes
   disponibles.
2. **Adopción de Python/rclpy** (`sections/capitulo-1.tex:217-222`). Se afirma
   que “muchos desarrolladores de robótica” usan rclpy; ninguna fuente de la
   biblioteca lo dice explícitamente.
3. **Taxonomía de detectores de una y dos etapas**
   (`sections/capitulo-2.tex:26-33`). No hay una revisión dedicada de detección
   de objetos en la biblioteca; los estudios de borde citados usan solo
   familias de una etapa.
4. **Métodos de medición de potencia en Jetson** — **resuelta en P-07**. Se
   decidió medir y el método se fija en `sec:power`, con las entradas
   `nvidiacorporation2026potencia` y `nvidiacorporation2026tegrastats`; el
   `% TODO` de `sections/capitulo-2.tex` se eliminó.
5. **Atribución de figuras** (`sections/capitulo-2.tex:79` y `:170`). Se
   solapa con P-21; aquí se resuelve la fuente, no la geometría.

**Objetivo.** Que ninguna afirmación quede sin fuente o sin una decisión
explícita de eliminarla.

**Cómo resolver cada una.**

- Privacidad: buscar una fuente dedicada (por ejemplo, un trabajo de edge
  computing que explicite privacidad) con `zotero-cli`; si no aparece, eliminar
  la cláusula o reformularla como consideración general sin atribución.
- rclpy: revisar el texto completo de `portugal2025` (la entrada está en la
  biblioteca) y la documentación oficial de ROS 2; si no hay dato de adopción,
  suavizar (“rclpy es una de las bibliotecas cliente disponibles”) o eliminar
  la comparación implícita.
- Taxonomía: agregar una revisión de detección de objetos a Zotero y a
  `referencias.bib`, o reescribir el pasaje sin la taxonomía general. No citar
  los estudios de borde para una afirmación que no hacen.
- Potencia: hecho en P-07 (fuente del método agregada; `% TODO` eliminado).
- Figuras: agregar la fuente o el crédito que corresponda; si la figura es
  propia, decirlo y conservar la fuente editable.

**Contexto y restricciones.** Usar `zotero-cli` para buscar y leer; no citar de
memoria. Distinguir lo que una fuente dice explícitamente de lo que se infiere.
No agregar citas decorativas. Si se agrega una entrada, exportarla con la misma
convención de claves que `referencias.bib`.

**Entregable.** Capítulos 1 y 2 sin `% TODO` de cita; entradas nuevas en
Zotero y `referencias.bib` si corresponde; texto ajustado.

**Criterios de aceptación.** Cada afirmación tiene fuente o fue eliminada; no
hay citas que no respalden la frase; las claves nuevas existen en la
bibliografía; el documento sigue compilando.

**Dependencias.** Ninguna: el punto de potencia quedó resuelto en P-07.
Coordinar con P-20 y P-22.

**Notas.** No convertir la búsqueda en una revisión bibliográfica nueva: el
objetivo es cerrar brechas puntuales dentro del alcance.

---

### P-20 · Auditar afirmaciones cuantitativas y de novedad

**Estado actual.** El capítulo 1 y el capítulo 2 contienen varias cifras
atribuidas a fuentes: 13 FPS para YOLOv4 con DeepStream en la Orin Nano
(`sections/capitulo-1.tex:53-57`), el “balance global más favorable” de
`alqahtani2026` (`:58-60`), el sobrecosto de hasta 50 % y la pérdida de ~30 %
de `kronauer2021` (`:113-130`), el ahorro de 28 % de CPU y 33 % de RAM de
`macenski2023` (`:131-134`), la latencia P95 de 1 ms/1 MB y 7,85 ms/8 MB de
`macenski2022` (`sections/capitulo-2.tex:491-502`) y la mejora de 5–8 % de
`betz2024` (`:577-580`). También hay una afirmación de novedad: “Hasta donde
llega el conocimiento del autor, ningún estudio…”
(`sections/capitulo-1.tex:211-216`).

**Objetivo.** Verificar que las cifras y la afirmación de novedad resistan una
lectura de la fuente original, y corregir o calificar lo que no.

**Tareas.**

- Abrir cada PDF en Zotero y localizar la cifra exacta; anotar página o
  sección.
- Distinguir si la fuente dice la cifra, la permite inferir o no la respalda.
- Corregir redondeos, unidades y condiciones (por ejemplo, si el 50 % es
  respecto de DDS directo y para mensajes pequeños; si el 13 FPS corresponde a
  un modo de energía y a una resolución concretos).
- Revisar la afirmación de novedad después de la búsqueda de P-19. Si no se
  puede sostener, reformularla como “la literatura revisada no proporciona…”
  en lugar de “ningún estudio”.
- Registrar las verificaciones en una nota interna o en el reporte que
  corresponda; no agregar esas notas al PDF.

**Contexto y restricciones.** Es una auditoría de exactitud, no una nueva
revisión. No se cambia el argumento del capítulo si la cifra es correcta; si no
lo es, se corrige o se elimina. Las fuentes están en Zotero; usar
`zotero-cli` para leer páginas específicas.

**Entregable.** Capítulos 1 y 2 con cifras verificadas y afirmación de novedad
ajustada; lista interna de verificaciones.

**Criterios de aceptación.** Cada cifra tiene página o sección de respaldo; no
hay afirmaciones de novedad absolutas sin sustento; las correcciones no
introducen inconsistencias con el capítulo 3 o el resumen.

**Dependencias.** Ninguna. Coordinar con P-19 y P-22.

**Notas.** Las cifras de los estudios de borde suelen depender de la
resolución, el modo de energía y la precisión; conservar esas condiciones en
la redacción.

---

### P-21 · Corregir figuras, procedencia y referencias cruzadas

**Estado actual.**

- La figura 2.1 (`label fig:cadena-vision-computador`) incluye
  `assets/figures/chapter-2/ciclo-CV.png`, que es un **ciclo cerrado de cuatro
  etapas** sin etapa de salida. El pie describe una cadena lineal con entrada,
  preprocesamiento, inferencia, postprocesamiento y salidas. Existe
  `assets/figures/chapter-2/cadena-vision-computador.png`, que representa la
  cadena lineal con las formas de datos y coincide mejor con el pie, pero **no
  se usa**.
- ~~`assets/figures/chapter-2/ros2-cadena-video.png` y su fuente `.d2` no se
  usan~~ **Resuelto en P-04 (2026-10-19).** Representaban un mapeo descartado
  y se eliminaron. En su lugar, `assets/figures/chapter-3/ros2-particionamiento.dot`
  (Graphviz, por legibilidad del texto al ancho de caja) → `.png`, incluida en
  §3.6 como `fig:partitioning`, con pie, etiqueta y referencia desde el texto.
- La figura del stack de JetPack (`sections/capitulo-2.tex:170-181`) no tiene
  procedencia declarada.
- La figura 2.2 (módulo) y la 2.3 (kit) atribuyen la fotografía a NVIDIA
  Corporation; verificar que el crédito sea suficiente para el uso en una
  memoria.
- Ninguna figura del capítulo 2 se referencia desde el texto, salvo la del kit
  (`fig:jetson-orin-nano-super-devkit`). La tabla `tab:experimental-matrix`
  tampoco se referencia.

**Objetivo.** Que cada figura incluida coincida con su pie, tenga procedencia y
sea referenciada; que no queden fuentes huérfanas.

**Tareas.**

- Decidir si la figura 2.1 debe ser `cadena-vision-computador` (lineal) o
  `ciclo-CV` (ciclo). Si se elige la primera, ajustar el pie si hace falta y
  conservar la fuente `.d2`; si se elige la segunda, reescribir el pie para
  describir el ciclo y explicar por qué no hay etapa de salida.
- Resolver la procedencia de `jetpack-stack.png`: agregar fuente y licencia, o
  redibujarla como figura propia con D2/Graphviz según el contrato de
  `AGENTS.md`.
- ~~Decidir el destino de `ros2-cadena-video`~~: hecho en P-04; se eliminó y
  se reemplazó por `chapter-3/ros2-particionamiento.dot`, ya incluida y
  referenciada. Queda solo revisar que su pie y su etiqueta sigan coincidiendo
  si el mapeo cambia durante los pilotos.
- Referenciar cada figura y tabla desde el texto (`\Cref{fig:...}`,
  `\Cref{tab:...}`), no solo rotularlas.
- Verificar pies, etiquetas, créditos y licencias de todas las figuras.
- Confirmar que cada figura incluida tenga una fuente editable junto al PNG y
  que el PNG haya sido inspeccionado.

**Contexto y restricciones.** El contrato de estilo y el flujo de renderizado
están en `AGENTS.md` (secciones de diagramas). Las figuras de terceros deben
conservar su licencia (por ejemplo, CC BY 4.0 para la documentación de ROS 2).
No se redibujan figuras ajenas sin necesidad.

**Entregable.** Capítulos 2 y 3 con figuras coherentes, procedencia declarada
y referencias cruzadas; assets sin huérfanos injustificados.

**Criterios de aceptación.** Cada figura coincide con su pie; cada figura y
tabla se referencia; cada figura tiene fuente y crédito o declaración de
autoría; no quedan pares fuente/PNG duplicados o sin uso; el PDF compila sin
figuras faltantes.

**Dependencias.** Ninguna. La decisión sobre la figura de ROS 2 quedó cerrada
en P-04.

**Notas.** El reporte interno `docs/reporte-comm-ros2.md` dice que la fuente de
la figura 2.8 es `assets/figures/ros2-ruta-mensaje.d2`, pero la fuente actual es
`assets/figures/chapter-2/ros2-ruta-mensaje.dot`. Actualizar esa referencia si
el reporte se conserva (ver P-24).

---

### P-22 · Depurar la bibliografía y el modo de revisión

**Estado actual.**

- `main.tex:35` tiene `\toggletrue{revisarbib}`. En la versión de entrega debe
  estar en `false`; hoy el PDF imprime las 37 entradas y una sección de
  revisión con marcas ✓/✗.
- `\printbibliography` (`main.tex:121`) no agrega la bibliografía al índice
  general; el `main.toc` no la muestra.
- Cuatro entradas de `referencias.bib` no se citan: `fang2026`,
  `omg2015dds`, `omg2022ddsirtps`, `roshomepage`.
- Los dos `@standard` (`omg2015dds`, `omg2022ddsirtps`) producen
  `Package biblatex Warning: No driver for 'standard'` en el log.
- Las entradas exportadas incluyen campos `file = {/home/nat/Zotero/...}` con
  rutas locales; no son portables y exponen la estructura del equipo.

**Objetivo.** Dejar una bibliografía limpia, completa, consistente con el
estilo IEEE y sin artefactos de depuración.

**Tareas.**

- Decidir con P-19/P-20 si las cuatro entradas sin citar se citan o se
  eliminan. Si se citan las especificaciones OMG (por ejemplo, para las
  historias de escritura/lectura de DDS), cambiar su tipo a uno con driver
  (`@misc`, `@online` o `@report`) o agregar el driver correspondiente.
- Desactivar `\revisarbib` para la entrega; conservar el mecanismo solo como
  herramienta de depuración interna.
- Hacer que la bibliografía aparezca en el índice general, con
  `heading=bibintoc` o `\addcontentsline`.
- Revisar el estilo IEEE: autores, títulos, fechas, DOI/URL, mayúsculas y
  comillas; verificar que no haya campos vacíos ni duplicados.
- Atender la advertencia `Bibliography string 'presentedat' untranslated` del
  log: revisar la localización de biblatex/polyglossia o el campo del evento
  en las entradas de congreso.
- Eliminar o neutralizar los campos `file` con rutas locales antes de publicar
  el repositorio.
- Verificar que no queden entradas duplicadas entre Zotero y `referencias.bib`.
- Limpiar los artefactos `main.bbl-SAVE-ERROR` y `main.bcf-SAVE-ERROR` si el
  build ya es estable.
- Revisar los overfull boxes de la bibliografía: el log reporta uno de
  aproximadamente 93 pt; ajustar títulos, URLs o DOI largos, o permitir cortes
  controlados.

**Contexto y restricciones.** La bibliografía se genera con `biber` y el estilo
IEEE; no editar `main.bbl` a mano. Las claves deben coincidir con las citas del
texto. El modo de revisión es una herramienta de depuración, no parte de la
entrega.

**Entregable.** `main.tex` con el modo de revisión desactivado; bibliografía en
el índice; `referencias.bib` depurado; log sin advertencias de driver.

**Criterios de aceptación.** No hay entradas sin citar (o están justificadas);
no hay advertencias de biblatex por tipo de entrada; la bibliografía aparece en
el índice; el PDF de entrega no muestra la sección de revisión; las rutas
locales no se publican.

**Dependencias.** Requiere las decisiones de P-19 y P-20 para las entradas sin
citar; el resto se puede hacer ahora.

**Notas.** Si se conservan las especificaciones OMG, citarlas donde el texto
afirma la existencia de las dos historias o la dependencia de la QoS; el
reporte interno ya sugiere hacerlo.

---

### P-23 · Decidir el uso del glosario y unificar la terminología

**Estado actual.** `glosario.tex` define 31 entradas, pero **ninguna se invoca
con `\gls`** en los capítulos. `main.tex:109` imprime el glosario completo y
`main.tex:130` usa `\glsaddallunused` para incluir las entradas no citadas. El
comentario del archivo lo describe como “prueba de concepto”. Hay entradas que
no aparecen en el texto (`servicio`, `acción`, `parámetro`, `interfaz`, `grafo
de cómputo`, `paquete`, `espacio de trabajo`, `archivo de lanzamiento`,
`bolsa`) y términos que el texto introduce con `\emph{}` sin enlazar al
glosario (`middleware`, `callback`, `benchmark`).

**Objetivo.** Decidir si la memoria lleva glosario y, si lo lleva, usarlo de
forma coherente; si no, retirarlo o reducirlo.

**Opciones.**

1. **Glosario activo:** usar `\gls` en la primera aparición de cada término en
   los capítulos, revisar la gramática (plurales, mayúsculas, artículos) y
   quitar `\glsaddallunused` si ya no hace falta. Es la opción más costosa,
   pero la más coherente con el archivo actual.
2. **Glosario de referencia:** conservar la lista impresa como referencia de
   terminología, sin `\gls`, y recortar las entradas que no se usan. Requiere
   justificar ante el profesor guía por qué una memoria de ingeniería lleva
   glosario.
3. **Sin glosario:** retirar `\printglossaries`, `\glsaddallunused` y el
   archivo, y mantener la terminología fija solo en el texto. Es la opción más
   simple si el glosario no aporta.

**Tareas adicionales.**

- Verificar que los términos del glosario coincidan con la guía
  `academic-spanish` (por ejemplo, “middleware” conservado, “benchmark”
  conservado, “sobrecosto” calificado, “video” sin tilde).
- Revisar las definiciones que puedan contradecir el texto (por ejemplo,
  “nodo” como proceso, “tópico” como bus, “mensaje” como unidad de datos).
- Unificar la primera aparición de anglicismos: cursiva y glosa una sola vez.
- Decidir si “ROS 1” y “ROS 2” se escriben con espacio duro (`ROS~2`) en todo
  el documento; hoy hay variaciones.

**Contexto y restricciones.** El glosario no debe convertirse en una segunda
introducción. Las definiciones deben ser breves y consistentes con el texto.
No se agregan términos fuera del dominio de la memoria.

**Entregable.** Decisión escrita, `glosario.tex` y `main.tex` coherentes, y
texto con terminología uniforme.

**Criterios de aceptación.** No hay entradas huérfanas ni definiciones
contradictorias; la primera aparición de cada término sigue la guía de estilo;
el glosario, si se imprime, está en el índice y tiene un propósito declarado.

**Dependencias.** Ninguna. Coordinar con P-25.

**Notas.** Si se elige la opción 1, hacer el cambio por capítulo y compilar
después de cada uno; `\gls` puede alterar mayúsculas y artículos.

---

### P-24 · Cerrar el front matter, los anexos y la limpieza del repositorio

**Estado actual.**

- La portada usa `\textsc{Valparaíso, \DTMnow}` (`sections/portada.tex:36`), que
  imprime la fecha de compilación. `main.tex:66` carga `datetime2` con el
  comentario “for debug purposes only remove on final release”.
- `sections/agradecimientos.tex` y `sections/dedicatoria.tex` existen pero
  están comentados en `main.tex:104-105`; contienen texto provisorio.
- `sections/anexos.tex` es un relleno: `\appendix` + `\chapter{Apendice A}`
  (sin tilde).
- `sections/desarrollo.tex` no se incluye en `main.tex` y contiene un
  `\include{chapters/desarrollo/ros}` que apunta a una ruta inexistente.
- `sections/body/` está vacío.
- En la raíz hay artefactos de compilación (`main.bbl-SAVE-ERROR`,
  `main.bcf-SAVE-ERROR`, `LaTeX Compiler.log`) y un reporte interno
  (`docs/reporte-comm-ros2.md`).
- El glosario se imprime **antes** del índice general; el orden habitual es
  índice, listas y luego glosario (o al final). Es una decisión de formato.
- `git status` muestra cambios sin confirmar en `commands.tex`, `main.tex`,
  `referencias.bib`, `sections/capitulo-1.tex`, `sections/capitulo-2.tex` y el
  movimiento de figuras de `assets/figures/` a `assets/figures/chapter-2/`.
- `commands.tex` define `\figstub`, que no se usa.
- No hay metadatos PDF (`pdftitle`, `pdfauthor`).

**Objetivo.** Dejar el documento y el repositorio en un estado de entrega
limpio, sin contenido provisorio ni artefactos confusos.

**Decisiones y tareas.**

- **Fecha de portada.** Fijar el mes y año de la defensa (o una fecha
  institucional) en lugar de `\DTMnow`. Si se conserva `datetime2` para
  borradores, definir una macro de fecha fija para la entrega.
- **Tipografía de la portada.** `\textsc{Valparaíso, ...}` produce la
  advertencia `Font shape TU/LatinModernRoman(0)/m/sc undefined` porque la
  fuente no tiene versalitas; usar mayúsculas normales, otra fuente o cargar
  una fuente con versalitas.
- **Agradecimientos y dedicatoria.** Decidir si se incluyen; si se incluyen,
  escribir el texto final y descomentar las líneas en `main.tex`; si no, dejar
  los archivos fuera del build.
- **Anexos.** Decidir qué contiene el apéndice (por ejemplo, configuración
  completa, esquema de datos, instrucciones de reproducción, tablas auxiliares)
  y corregir “Apéndice”. Si no hay contenido, retirar el apéndice antes de la
  entrega.
- **Orden del front matter.** Decidir si el glosario va antes o después del
  índice; si se mueve, actualizar `main.tex` y verificar la numeración romana.
- **Archivos huérfanos.** Proponer al autor la eliminación de
  `sections/desarrollo.tex`, `sections/body/` y los artefactos `SAVE-ERROR`;
  no borrar sin confirmación. El reporte interno ya quedó en
  `docs/reporte-comm-ros2.md` y se conserva en el repositorio; falta actualizar
  su referencia a la fuente `.d2`/`.dot`.
- **Git.** Confirmar los cambios actuales en commits pequeños y comprensibles
  después de verificar que el build funciona; no perder trabajo del autor. El
  movimiento de figuras debe quedar como un cambio coherente.
- **Metadatos.** Agregar `pdftitle`, `pdfauthor` y palabras clave en
  `\hypersetup` si se desea; no es obligatorio, pero mejora el PDF.
- **Limpieza.** Eliminar `\figstub` si no se usa, o usarlo para figuras
  pendientes; no dejar comandos muertos.

**Contexto y restricciones.** No borrar archivos del autor sin autorización.
Los artefactos de build están en `.gitignore`; no se commitean. La portada y
los anexos son parte de la entrega institucional; consultar el formato de la
universidad si hay dudas.

**Entregable.** Portada con fecha fija, front matter decidido, anexos con
contenido o retirados, repositorio limpio y build reproducible.

**Criterios de aceptación.** No hay texto provisorio visible en la versión de
entrega; la fecha es fija; no hay `\include` rotos; el repositorio no contiene
artefactos confusos; los cambios están confirmados en git; el PDF tiene
metadatos si se decidió agregarlos.

**Dependencias.** Ninguna para la limpieza; la fecha final y el commit de
entrega se hacen al cierre (P-25).

**Notas.** La mudanza de figuras ya está hecha en el sistema de archivos pero
no confirmada en git; verificar que el build use las rutas nuevas antes de
commitear.

---

### P-25 · Revisión final de consistencia y compilación

**Estado actual.** Pendiente. Es la última unidad de trabajo antes de la
entrega.

**Objetivo.** Leer la memoria completa como un todo, verificar consistencia y
producir el PDF final.

**Lista de verificación.**

- **Estructura.** Capítulos 1–6 presentes y numerados; bibliografía y apéndice
  en el índice; conclusión responde las dos preguntas; el capítulo 3 ya no
  dice “la plataforma experimental principal” si hay una sola.
- **Marcadores.** Ningún `\todo` visible; ningún `% TODO` de cita; ningún
  “SPECIFY”, “pendiente” o texto provisorio.
- **Citas.** Todas las claves existen; no hay entradas sin citar (o están
  justificadas); el modo `revisarbib` está desactivado; la bibliografía está en
  el índice; no hay advertencias de driver.
- **Referencias cruzadas.** Todas las figuras, tablas y ecuaciones se
  referencian; no hay `??`; `cleveref` produce los nombres correctos.
- **Figuras y tablas.** Pies descriptivos, unidades, fuentes, licencias;
  ninguna figura huérfana; la figura 2.1 coincide con su pie.
- **Coherencia de hardware.** “Orin Nano”, “Orin Nano Super”, RAM y TOPS
  coinciden en portada, capítulos 1–3, resumen y abstract.
- **Coherencia terminológica.** “video” sin tilde; “visión por computador”;
  “memoria de título” vs. “trabajo”; “sobrecosto” calificado; anglicismos en
  cursiva en la primera aparición; “benchmark” y “benchmarking” consistentes.
- **Hipótesis.** Decidir si H1–H4 se presentan solo en §3.9 o también en el
  capítulo 1; si se mueven, actualizar la organización del capítulo 1 y las
  referencias. No es obligatorio moverlas, pero la ubicación actual debe ser
  deliberada.
- **Afirmación de novedad.** Revisar “Hasta donde llega el conocimiento del
  autor…” después de P-19/P-20; reformular si no se sostiene.
- **Afirmación de versionado.** Verificar que el código y la configuración
  estén realmente bajo control de versiones antes de mantener la frase de
  §3.10.
- **Resumen y abstract.** Sin `\todo`; mismas cifras que el capítulo 4; misma
  conclusión que el capítulo 6; inglés correcto.
- **Español.** Pasar la guía `academic-spanish` por el texto completo;
  revisar coma decimal, unidades, mayúsculas, guiones y comillas.
- **Compilación.** Ejecutar `just nuke && just build` una sola vez al final
  (según `AGENTS.md`), revisar el log y el PDF; corregir overfull boxes
  graves, fuentes faltantes y advertencias de hyperref.
- **Entrega.** Confirmar que el PDF no incluye la sección de revisión
  bibliográfica, que la fecha es la correcta y que el repositorio está en un
  commit de entrega.

**Contexto y restricciones.** No hacer cambios estructurales de último minuto
sin proponerlos. La compilación completa es lenta; evitar recompilaciones
innecesarias. No editar archivos generados.

**Entregable.** PDF final y repositorio en estado de entrega.

**Criterios de aceptación.** Lectura de principio a fin sin placeholders ni
inconsistencias; build limpio; PDF con índice, figuras, tablas, bibliografía y
apéndice correctos; repositorio limpio.

**Dependencias.** Requiere todos los pendientes anteriores.

**Notas.** Si queda poco tiempo, priorizar P-01 a P-18 (contenido y
resultados) sobre la limpieza editorial; sin resultados no hay memoria, pero
sin limpieza la entrega pierde calidad.

---

## 8. Registro de decisiones

Usar esta sección para dejar constancia breve de las decisiones tomadas, de
modo que futuras sesiones no las reviertan por desconocimiento. Cada entrada
debe indicar fecha, pendiente, decisión y dónde quedó documentada.

| Fecha | Pendiente | Decisión | Documentado en |
|---|---|---|---|
| | | | |
