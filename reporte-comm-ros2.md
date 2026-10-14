# Reporte: cómo viaja un mensaje entre dos nodos de ROS 2

**Fecha:** 2025-10-14
**Motivo:** revisión de la figura 2.8 (`fig:ros2-ruta-mensaje`) del Capítulo 2, a raíz
de una duda sobre si el publicador tiene búfer de salida y sobre el rol real de DDS.
**Estado:** figura, pie de figura y una frase del cuerpo corregidos; este reporte no
forma parte del documento de la memoria.

**Nota sobre las citas de este reporte:** las citas textuales provienen de páginas
web, de archivos `.rst` de repositorio y de extracción automática de PDF. Se
normalizaron los espacios y los artefactos de formato (marcas de negrita sueltas de
la extracción), sin alterar el texto. Cada cita indica su origen y, donde la
extracción fue automática, se advierte que conviene confirmarla en el documento
original.

---

## 1. Motivo de la revisión

La primera versión de la figura 2.8 no se basaba en ninguna fuente: se derivó de la
prosa que ya existía en la sección 2.4, que describía la ruta como *serialización →
transporte → búfer en las colas del suscriptor → deserialización → callback*. Esa
descripción es incompleta y sugiere algo que no ocurre: que el publicador entrega el
mensaje directamente al búfer del suscriptor, y que el middleware solo aporta
descubrimiento y un canal de transporte.

Se verificó la ruta contra la documentación oficial de ROS 2, la documentación de
diseño de ROS 2, la especificación RTPS (OMG), el código de `rclpy` y la literatura
ya citada en la memoria (Kronauer et al., 2021). Conclusión: **hay un búfer a cada
lado, ambos los gestiona el middleware, y DDS tiene un rol activo que va mucho más
allá del descubrimiento.**

---

## 2. Respuesta corta a las dos dudas

**a) ¿Hay un búfer de salida en el publicador?**
Sí. Cada operación de escritura agrega un `CacheChange` a la `HistoryCache` del
*RTPS Writer* correspondiente al `DataWriter` (búfer de salida). Su tamaño y su
retención los fija la QoS, no el código del nodo, y es precisamente la estructura
que hace posible retransmitir con `reliable` y entregar muestras a *suscriptores
tardíos* con `durability: transient-local`.

**b) ¿DDS solo descubre, o gestiona también la comunicación?**
Gestiona la comunicación completa entre las dos aplicaciones:
descubrimiento y emparejamiento, serialización de los tipos, transporte,
las dos historias (búferes), las retransmisiones y la notificación de datos
disponibles. La biblioteca cliente (`rclpy`) no escribe en el otro proceso: escribe
en su `DataWriter` y lee de su `DataReader`. La capa `rmw` es una interfaz delgada
sobre el middleware, no un canal propio.

---

## 3. Ruta corregida, paso a paso

| # | Etapa | Quién la ejecuta | Fuente principal |
|---|---|---|---|
| 1 | El nodo construye un mensaje ROS en memoria (`sensor_msgs/Image`) | código del nodo (`rclpy`) | — |
| 2 | El mensaje se convierte en una muestra del middleware (serialización CDR del tipo) | capa `rmw` + *type support* del middleware | ROS 2 docs (interfaces internas); `design.ros2.org`; Kronauer et al. (categoría `rmw`) |
| 3 | La muestra se deposita en la **historia de escritura** del `DataWriter` (búfer de salida). `history` (`keep last`/`keep all`), `depth`, `reliability` y `durability` deciden qué se conserva y por cuánto tiempo | DDS / RTPS Writer | OMG DDSI-RTPS 2.5 §8.2.1, §8.2.1.1, §8.2.2; ROS 2 docs (QoS) |
| 4 | El RTPS Writer transfiere el cambio a la historia de todos los RTPS Readers emparejados por el transporte (sockets/UDP o memoria compartida; fragmentación y retransmisión según QoS) | DDS / RTPS | OMG DDSI-RTPS 2.5 §8.2.1, §8.2.8 |
| 5 | La muestra llega a la **historia de lectura** del `DataReader` (búfer de entrada), también dimensionada por la QoS | DDS / RTPS Reader | OMG DDSI-RTPS 2.5 §8.2.1.1, §8.2.2; ROS 2 docs (QoS) |
| 6 | El middleware **avisa** que hay datos disponibles; el ejecutor está esperando en el *wait set* de la biblioteca cliente | DDS → `rcl`/`rmw` → ejecutor | ROS 2 docs (ejecutores): «A *wait set* is used to inform the Executor about available messages on the middleware layer»; Kronauer et al. (`Rclcpp Notification Delay`) |
| 7 | El ejecutor **toma** la muestra: `rcl_take`/`dds_take`, con deserialización al mensaje ROS | ejecutor + `rcl`/`rmw` | Kronauer et al. (Fig. 2, secuencia `dds_take` → `handle_message`) |
| 8 | Se invoca el *callback* con el mensaje ROS | ejecutor | ROS 2 docs (ejecutores) |

Observaciones que se derivan de la tabla:

- Los pasos 3 y 5 son **del mismo tipo de entidad** (una `HistoryCache`), uno en el
  lado del Writer y otro en el lado del Reader. La figura corregida los pinta con el
  mismo color para marcar que ambos pertenecen a la capa `rmw`/DDS.
- Los pasos 6 y 7 son **dos momentos distintos**: la notificación no transporta
  datos. Por eso Kronauer et al. miden por separado el `Rclcpp Notification Delay`
  («the time difference between the notification of DDS to ROS2 that new data is
  available and triggering of its actual retrieval»), y esa categoría aparece entre
  las dos mayores fuentes de latencia para cargas útiles pequeñas.
- Con `durability: transient-local` la retención de muestras para quien se conecta
  tarde ocurre en el **lado del publicador** (paso 3), no en el suscriptor.

---

## 4. Evidencia, fuente por fuente

### 4.1 Documentación oficial de ROS 2 — interfaces internas

> «The `rmw` API is the interface between the ROS 2 software stack and the
> underlying middleware implementation. The underlying middleware used for ROS 2 is
> either a DDS or RTPS implementation, and is responsible for **discovery, publish
> and subscribe mechanics, request-reply mechanics for services, and serialization
> of message types**.»

Además: «The implementation of the `rmw` API is provided by a middleware
implementation specific package, e.g. `rmw_fastrtps_cpp`, the library of which is
compiled against vendor specific DDS interfaces and types».

- URL: <https://docs.ros.org/en/rolling/ROS-Framework/client-libraries/About-Internal-Interfaces/About-Internal-Interfaces.html>
- Texto fuente: `ros2_documentation`, `source/ROS-Framework/client-libraries/About-Internal-Interfaces/About-Internal-Interfaces.rst`
- Licencia del repositorio: CC BY 4.0
- Uso: apoya que la serialización es responsabilidad del middleware y que `rmw` es
  una interfaz específica por implementación, no un transporte propio.

### 4.2 Documentación oficial de ROS 2 — ajustes de QoS

Pasajes textuales de la página de QoS (formato de lista del original):

> «**History** — *Keep last*: only store up to N samples, configurable via the queue
> depth option. / *Keep all*: store all samples, subject to the configured resource
> limits of the underlying middleware.»
> «**Depth** — *Queue size*: only honored if the "history" policy was set to "keep last".»
> «**Reliability** — *Best effort*: attempt to deliver samples, but may lose them if
> the network is not robust. / *Reliable*: guarantee that samples are delivered, may
> retry multiple times.»
> «**Durability** — *Transient local*: **the publisher becomes responsible for
> persisting samples for "late-joining" subscriptions.** / *Volatile*: no attempt is
> made to persist samples.»
> «The "history" and "depth" policies in ROS 2 combine to provide functionality akin
> to the queue size in ROS 1.»
> «The "durability" policy "transient local", combined with any depth, provides
> functionality similar to that of "latching" publishers.»

- URL: <https://docs.ros.org/en/rolling/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.html>
- Texto fuente: `source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst`
- Uso: es la evidencia más directa de que existen colas con profundidad y de que la
  retención de muestras para suscriptores tardíos recae en el publicador. Nota: la
  página describe las políticas desde ROS 2, sin nombrar las `HistoryCache`; la
  correspondencia con las historias de RTPS se establece con la especificación
  (§4.4).

### 4.3 Documentación oficial de ROS 2 — ejecutores

> «A *wait set* is used to inform the Executor about available messages on the
> middleware layer, with one binary flag per queue.»
> «The wait set mechanism reports only very little information about these queues to
> the Executor.»
> «Execution management in ROS 2 is handled by Executors. An Executor uses one or
> more threads of the underlying operating system to invoke the callbacks of
> subscriptions, timers, service servers, action servers, etc. on incoming messages
> and events.»

- URL: <https://docs.ros.org/en/rolling/ROS-Framework/client-libraries/About-Executors/About-Executors.html>
- Texto fuente: `source/ROS-Framework/client-libraries/About-Executors/About-Executors.rst`
- Uso: apoya el paso 6 (el aviso al ejecutor es un mecanismo explícito, el *wait
  set*) y el nombre «conjunto de espera» usado en la figura. Es también el origen
  de la imagen `executors_basic_principle.png` empleada en la figura 2.6.

### 4.4 OMG DDSI-RTPS 2.5 (especificación normativa)

> §8.2.1: «The HistoryCache forms the interface between the DDS Entities and their
> corresponding RTPS Entities. For example, each write operation on a DDS DataWriter
> adds a CacheChange to the HistoryCache of its corresponding RTPS Writer. The RTPS
> Writer subsequently transfers the CacheChange to the HistoryCache of all matching
> RTPS Readers.»
>
> §8.2.1.1 (Tabla 8.1, propósito de `HistoryCache`): «... On the Writer side it
> contains the history of the changes to data-objects made by the Writer. ... what is
> needed is the partial history required to service **existing and future matched**
> RTPS Reader endpoints. ... On the Reader side it contains the history of the changes
> to data-objects made by the matched RTPS Writer endpoints.»
>
> §8.2.2: «On the writer side, the HistoryCache contains the partial history of
> changes to data-objects made by the corresponding DDS Writer that are needed to
> service existing and future matched RTPS Reader endpoints. The partial history
> needed **depends on the DDS Qos** and the state of the communications with the
> matched RTPS Reader endpoints.»
>
> §8.2.8: «Its role is to transfer all CacheChange changes in its HistoryCache to the
> HistoryCache of the matching remote RTPS Readers.»
>
> Tabla 8.10: «WHC — HistoryCache of RTPS Writer»; «RHC — HistoryCache of RTPS Reader».

- URL: <https://www.omg.org/spec/DDSI-RTPS/2.5/PDF>
- Uso: es la fuente que fija los dos búferes y su carácter dependiente de QoS, y la
  base del comentario `%` que acompaña al archivo `.d2` de la figura.
- **Advertencia de verificación:** estas citas se obtuvieron mediante extracción
  automática del PDF (el documento tiene cientos de páginas). La numeración de
  secciones y la redacción deben confirmarse en el PDF antes de citarlo en la
  memoria.

### 4.5 `design.ros2.org` — «ROS on DDS» (documento de diseño)

> «DDS uses the "Interface Description Language (IDL)" as defined by the Object
> Management Group (OMG) for message definition and serialization.»
> «DDS provides discovery, message definition, message serialization, and
> publish-subscribe transport. Therefore, DDS would provide discovery,
> publish-subscribe transport, and at least the underlying message serialization for
> ROS.»
> «... the `.msg` files would be converted into `.idl` files so that they could be
> used with the DDS transport. Language specific files would be generated for both
> the `.msg` files and the `.idl` files as well as conversion functions for
> converting between ROS and DDS in-memory instances.»

- URL: <https://design.ros2.org/articles/ros_on_dds.html>
- **Caveat:** el propio artículo advierte que se escribió *antes* de que se decidiera
  usar DDS/RTPS como base de ROS 2. Sirve como justificación de diseño y para el rol
  de la serialización, no como descripción del estado actual de la implementación.
  Aun así, su contenido es coherente con la documentación y con la especificación.
- No está en Zotero (ver §8).

### 4.6 Kronauer et al., 2021 (ya citado en la memoria; clave Zotero `R3MKQWHQ`)

La Fig. 2 del artículo lista la secuencia de llamadas del camino de publicación y
suscripción, extremo a extremo:

- Publicador: `Publisher::publish` → `rcl_publish` → `rmw_publish` → `dds_write`
  → «to network».
- Suscriptor: `Executor::wait_for_work` → `rcl_wait` → `rmw_wait` → `dds_wait`
  ← `DDS_ON_DATA` (aviso) → **[Rclcpp Notification Delay]** → `rcl_take` →
  `dds_take` → … → `handle_message` → *callback*.

Definiciones de las categorías de perfilado (texto del artículo):

> «**DDS**: This category only contains latency entailed by the DDS transport via
> network and by the function call to actually receive the message.»
> «**Subscriber rmw** and **Publisher rmw**: Latency attributed to the rmw layer.
> Middleware-specific conversions from ROS2 messages to DDS messages that might
> require DDS utility functions but are not used for the transport of the message
> itself are contained in this category.»
> «**Rclcpp Notification Delay**: The time difference between the notification of DDS
> to ROS2 that new data is available and triggering of its actual retrieval.»

Y sobre la dependencia del tamaño de la carga útil:

> «For a payload of 128 B, the largest amount of latency can be attributed to the
> categories DDS and Rclcpp Notification Delay ...»
> «Using a payload of 500 KB, one can clearly see that for all middlewares, the major
> part of the latency is due to the DDS middleware.»

- Uso: (i) respalda la existencia y el orden de las etapas 5–7, incluida la
  notificación como etapa propia y medible; (ii) ubica la conversión de mensajes ROS
  a mensajes DDS en la capa `rmw`, lo que respalda el paso 2; (iii) ya está citado en
  la sección 2.4 de la memoria, de modo que la figura queda alineada con la prosa que
  la rodea.

### 4.7 Código de `rclpy` (detalle fino de dónde se deserializa)

- `rclpy/rclpy/serialization.py` expone `serialize_message()` y
  `deserialize_message()` sobre `rclpy_serialize`/`rclpy_deserialize`.
- `rclpy/src/rclpy/subscription.cpp`, `Subscription::take_message(pymsg_type, raw)`:
  con `raw = True` usa `rcl_take_serialized_message()` y devuelve *bytes*; con el
  valor por defecto (`raw = False`) usa `rcl_take()`, que entrega un mensaje ROS ya
  deserializado.
- URL: <https://github.com/ros2/rclpy> (rama `rolling`), archivos citados.

**Inferencia (no verificada en el código del middleware):** en el camino
predeterminado la deserialización ocurre por debajo de `rcl` (en la capa `rmw` y el
*type support* del middleware), mientras que con suscripciones «crudas» el buffer
serializado se deserializa más arriba, en la biblioteca cliente. Ambos casos son
compatibles con la figura, que solo rotula «Toma y deserialización». Si la memoria
necesita precisión fina para `rclpy`, conviene rastrear
`rmw_fastrtps_cpp`/`rmw_cyclonedds_cpp` antes de afirmarlo.

### 4.8 Corroboración secundaria de terminología

La documentación de eProsima Fast DDS nombra clases `WriterHistory` y `ReaderHistory`
en su capa RTPS, y expone `DurabilityQosPolicy`, `HistoryQosPolicy` y
`ReliabilityQosPolicy` en su capa DDS, con lo que la nomenclatura «historia de
escritura / historia de lectura» es la de las implementaciones reales, no solo la de
la especificación:

- <https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/rtps/history/history.html>

**Fuentes descartadas:** en la búsqueda aparecieron páginas de *DeepWiki* sobre el
almacenamiento interno de Cyclone DDS (WHC/RHC) y sobre el camino de escritura y
lectura. Son generadas por terceros y no se usaron como fuente; sirvieron solo como
pista para llegar a la especificación RTPS. No deben citarse en la memoria.

---

## 5. Qué estaba mal en la memoria

1. **Faltaba el búfer de salida.** La prosa y la figura partían de que el publicador
   serializaba y enviaba, sin historia intermedia. Con eso, la retención por
   `history`/`depth` y la entrega a suscriptores tardíos (`transient-local`) quedaban
   sin representación, pese a que el párrafo anterior de la misma sección ya menciona
   «una profundidad de historial reducida combinada con la entrega confiable puede
   causar fallas de retransmisión» \cite{fernandez2020,kronauer2021}.
2. **El búfer del suscriptor aparecía como propiedad del nodo** («las colas del
   suscriptor»), cuando es la historia de lectura del `DataReader`, gestionada por el
   middleware y dimensionada por QoS.
3. **DDS quedaba reducido a un «transporte»**, omitiendo que también aporta el
   emparejamiento, la serialización, las dos historias y las retransmisiones.
4. **La notificación no aparecía**, aunque la prosa que sigue a la figura depende de
   ella y la literatura la mide como categoría propia.

---

## 6. Cambios aplicados en el repositorio

| Archivo | Cambio |
|---|---|
| `assets/figures/ros2-ruta-mensaje.d2` | Reescrito: dos procesos delimitados, historia de escritura y de lectura dentro de la capa DDS, transporte como frontera, aviso de disponibilidad como línea discontinua. El encabezado documenta la fuente normativa (RTPS §8.2.1, §8.2.2). |
| `assets/figures/ros2-ruta-mensaje.png` | Regenerado con `d2 --layout tala` (2682 × 2292). |
| `sections/capitulo-2.tex` | Pie de la figura 2.8 reescrito (búferes a ambos lados, QoS como determinante, aviso antes de la toma); frase del cuerpo sobre la ruta corregida y con `\cite{rosjazzydocs}`; las citas de atribución de las figuras 2.5–2.7 se mantienen. |

Pendiente de decisión del autor: si se agrega la especificación RTPS a la
bibliografía (§8), corresponde citarla también en el pie o en la prosa de la
sección 2.4.

---

## 7. Lo que quedó sin verificar

1. **Texto normativo de `DURABILITY`/`TRANSIENT_LOCAL` en la especificación DDS 1.4.**
   La extracción automática del PDF se truncó en la página 100 y las secciones
   2.2.3.4 (`DURABILITY`) y 2.2.3.18 (`HISTORY`) quedaron fuera. La retención para
   suscriptores tardíos se apoya, por ahora, en la documentación de QoS de ROS 2
   (§4.2) y en RTPS §8.2.1.1/§8.2.2 (§4.4).
2. **Redacción y numeración exactas de las citas de RTPS** (obtenidas por extracción
   automática; ver §4.4).
3. **Dónde deserializa exactamente el camino predeterminado de `rclpy`** (dentro del
   *type support* de `rmw_fastrtps_cpp` o en `rclpy`). Verificado: `rcl` ofrece
   `rcl_take` y `rcl_take_serialized_message`, y `rclpy` usa el primero salvo en
   suscripciones `raw=True`.
4. **Mecanismo concreto de notificación en `rmw_wait`** (condiciones, *guard
   conditions*, *listeners*): no se rastreó. Verificado solo que el *wait set* es el
   mecanismo que informa al ejecutor (§4.3) y que el retardo asociado es medible
   (§4.6).
5. **Mensajes prestados (*loaned*) y copias evitables** en memoria compartida: no se
   verificó aquí; es relevante para los experimentos de la memoria y aparece en la
   literatura ya citada (`kamiya2025`), pero excede esta revisión.

---

## 8. Fuentes: biblioteca Zotero frente a fuentes externas

Dentro de la biblioteca:

| Fuente | Clave | Uso en esta revisión |
|---|---|---|
| Kronauer et al., *Latency Analysis of ROS2 Multi-Node Systems* (2021) | `R3MKQWHQ` / `kronauer2021` | Secuencia de llamadas, categorías de perfilado, *notification delay*, conversiones ROS→DDS en `rmw` |
| ROS 2 Jazzy Documentation (entrada genérica del sitio) | `9CHJERH8` / `rosjazzydocs` | Citada en la frase corregida del cuerpo |
| Gambo et al., *A Systematic Literature Review of DDS Middleware in Robotic Systems* (2025) | `HSSMHC3X` / `gambo2025` | Consultada, **sin aporte para este punto**: en el texto que se pudo recuperar desde la biblioteca no aparecen las historias internas ni el rol de los búferes. La extracción disponible parece parcial (≈35 mil caracteres para una revisión de 44 páginas), de modo que este resultado negativo no es concluyente sobre el artículo completo |

Fuera de la biblioteca (usadas para verificar, no todas citables):

| Fuente | Tipo | Estado |
|---|---|---|
| OMG, *DDSI-RTPS 2.5* | Especificación normativa | **Se sugiere agregar** a Zotero y a `referencias.bib` si se cita la existencia de las historias |
| OMG, *DDS 1.4* | Especificación normativa | Opcional; solo si se necesita la definición normativa de `DURABILITY`/`HISTORY` |
| `design.ros2.org`, «ROS on DDS» | Documento de diseño | **Se sugiere agregar**; tiene advertencia de antigüedad |
| ROS 2 docs: *About Quality of Service settings*, *About Internal ROS 2 interfaces*, *About Executors* | Documentación | Cubiertas por la entrada genérica `rosjazzydocs`; se pueden agregar como entradas propias si se quiere precisión por página. Licencia CC BY 4.0 |
| `ros2/rclpy` (código, rama `rolling`) | Código fuente | Solo para verificación; no requiere cita |
| eProsima Fast DDS docs (API `WriterHistory`/`ReaderHistory`) | Documentación | Corroboración secundaria |
| DeepWiki (Cyclone DDS) | Wiki generada por terceros | **Descartada**; no citar |

Ninguna de las fuentes externas se usó para afirmar resultados experimentales, y
ninguna afirmación de la memoria se apoyó en una fuente no verificada sin quedar
marcada en §7.

---

## 9. Sugerencias para la memoria (no aplicadas salvo lo indicado en §6)

1. **Citar la especificación RTPS** allí donde la sección afirma la existencia de las
   dos historias y su dependencia de la QoS, si se decide incorporarla a la
   bibliografía.
2. **Hacer explícito en 2.4** que el búfer cuyo desborde o retransmisión menciona el
   párrafo de QoS es la historia de escritura del publicador. Hoy se deduce del
   contexto (figura 2.8 y el pie corregido), pero no se dice con esas palabras.
3. **Alineación con la experimentación:** para las mediciones de la memoria, las
   magnitudes relevantes del lado del middleware son la profundidad de historia en
   cada extremo, el tamaño de los mensajes (fragmentación) y las copias introducidas
   en la conversión ROS↔DDS; conviene fijarlas y documentarlas junto con las políticas
   de QoS, como ya se planea en el Capítulo 3.
4. **Cuidado con la terminología:** en la memoria conviene distinguir «historia de
   escritura / historia de lectura» (concepto del middleware) de «cola» (*queue*, la
   profundidad dentro de la política `history`) y evitar «búfer del suscriptor» como
   si fuera una estructura de la aplicación.

---

## Anexo: procedencia de las imágenes del Capítulo 2

Las figuras 2.5–2.7 se tomaron de la documentación oficial de ROS 2
(repositorio `ros2/ros2_documentation`, CC BY 4.0) y llevan la ruta de origen en un
comentario `%` sobre cada entorno `figure`, además del crédito en el pie; la figura
2.5 está adaptada (se eliminó el texto explicativo incrustado). La figura 2.8 es
propia y su fuente editable es `assets/figures/ros2-ruta-mensaje.d2`.
