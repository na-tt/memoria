# Instrumentación y medición de métricas

Documento de trabajo interno. **No forma parte de la memoria** y no debe
incluirse en el PDF.

Especificación concreta de la instrumentación que fija P-07 y que P-11 debe
materializar. `sections/capitulo-3.tex` §3.8 fija lo que la memoria declara:
qué se mide, con qué herramienta, a qué intervalo y con qué agregación. Este
documento fija lo que la memoria no necesita declarar: los nombres de los
campos, el esquema de la base, el patrón de código, las rutas de `sysfs` y las
verificaciones que hay que hacer en el equipo. Se complementa con
`docs/plantilla-corrida.md` (hoja de ejecución y registro de desviaciones,
P-06).

Última revisión: 2026-10-19 (P-07).

Los valores marcados **medidos** se tomaron en el equipo experimental
(Jetson Orin Nano 8 GB Super, JetPack 7.2.1, L4T R39.2.1, CPython 3.12.3) el
2026-10-19, con el equipo en carga ligera pero no en reposo; son una cota
superior y se vuelven a medir en reposo durante P-12. Las fuentes de las
afirmaciones sobre el equipo son la documentación de NVIDIA para esta misma
versión (`nvidiacorporation2026tegrastats`, `nvidiacorporation2026potencia`).

---

## 1. Decisiones fijadas

| Decisión | Valor | Alternativa descartada y por qué |
|---|---|---|
| Reloj de las marcas | `time.perf_counter_ns()` = `CLOCK_MONOTONIC`, ns | `CLOCK_REALTIME`: ajustable (NTP) → marcas desplazadas; reloj de ROS 2: deriva del reloj del sistema, puede sustituirse por `/clock` y devuelve un mensaje |
| Granularidad de las marcas | dos por fotograma y por operación (recepción, despacho) | una sola por fotograma: no permite contar descartes ni fotogramas en vuelo |
| Punto de la marca de despacho | inmediatamente **antes** de publicar | después del retorno del callback: la serialización se atribuiría al cómputo del nodo en vez de a la frontera |
| Instrumentación en A y en B/C/D | el mismo módulo, las mismas dos marcas | medidas distintas por arquitectura: rompe la comparación |
| Transporte del índice | solo el índice, en `header.frame_id` = `f` + 6 dígitos | tipo de mensaje propio: cambiaría los tipos y las cargas útiles de `tab:operations` y agregaría una capa de serialización que A no tiene |
| Dominio de la marca | la marca **no** viaja: se escribe en el registro local de cada proceso y la consolidación une filas por `(ventana, fotograma)` | transportarla: duplica un dato que la fila del productor ya tiene y obliga a ocupar `header.stamp` con un valor que no es tiempo de ROS |
| `header.stamp` | se deja sin uso como portador de tiempo | ponerlo en tiempo de ROS: costo de lectura y significado engañoso en una cadena que no usa `tf2` |
| Herramienta de recursos | `tegrastats` (P-01), más lectura directa de `sysfs` y del ámbito de control | `jtop`/`jetson-stats` (servicio extra, descartado en P-01); `psutil` (lee el mismo `/proc/stat` y agrega una dependencia) |
| Intervalo de `tegrastats` | 500 ms | 100 ms: costo triple y el equipo no sostiene la cadencia; 1000 ms: pocas muestras para máximos y para la serie térmica |
| Complemento para frecuencias | muestreador propio a 1 Hz (`sysfs`) | solo `tegrastats`: no reporta frecuencia de memoria en esta versión |
| Atribución de CPU y memoria a la cadena | ámbito de control (`cgroup` v2) propio de la corrida: `cpu.stat` acumulado y memoria `anon`+`shmem` | sondeo de `/proc/<pid>/stat` por proceso: hay que rastrear PIDs y la CPU queda muestreada en vez de contada; `tegrastats` solo: cifra del sistema completo, no atribuible |
| Línea base de potencia | una por corrida, del último minuto de la espera de enfriamiento (coste cero) | una por bloque: 10 min de campaña y ciega a la deriva intra-bloque; ninguna: la potencia absoluta no es comparable entre bloques |
| Agregación | media ponderada por intervalo, máximo de las muestras, P95 cuando corresponde | media aritmética: sesgada cuando la cadencia efectiva varía |
| Volcado | en memoria durante la ventana; escritura a disco al cerrar cada ventana | escritura por fotograma: introduce entrada y salida dentro de la medición |
| Formato | una base SQLite por corrida, más el registro crudo de `tegrastats` | CSV por ventana: un archivo por proceso por ventana y consultas por texto |
| Potencia | **se mide** (`VDD_IN`), con carácter descriptivo | excluirla: se pierde una métrica que la plataforma ya expone sin costo adicional |

Las cuatro decisiones que quedaban abiertas las confirmó el autor el
2026-10-19: el índice viaja solo en `header.frame_id` y las marcas se
consolidan por índice; la potencia se incluye como métrica descriptiva; la CPU
y la memoria se atribuyen a la cadena por ámbito de control; y la línea base
de potencia se toma por corrida.

---

## 2. Reloj y marcas de tiempo

### 2.1 Reloj

`time.perf_counter_ns()` es, en Linux, `clock_gettime(CLOCK_MONOTONIC)` con
resolución de 1 ns (**medido**: `time.get_clock_info` lo declara con
`implementation='clock_gettime(CLOCK_MONOTONIC)', resolution=1e-09`). Es el
mismo reloj en todos los procesos del anfitrión, de modo que las marcas de
extremos distintos de la cadena son comparables sin sincronización ni
protocolo. **Medido**: una lectura tomada en un proceso hijo cae dentro del
intervalo `[antes, después]` medido por el padre en el mismo instante.

`CLOCK_MONOTONIC` no es tiempo de calendario y no se ajusta, pero cuenta desde
el arranque: cada corrida registra el desfase con `CLOCK_REALTIME`
(`time.time_ns() - time.monotonic_ns()`) al inicio y al cierre, que es lo que
permite cruzar las marcas con la fecha de la hoja de ejecución y con la línea
de `tegrastats` (que solo trae hora de pared con resolución de 1 s).

### 2.2 Puntos de marca

Una marca de **recepción** en la primera instrucción de la operación y una de
**despacho** inmediatamente antes de publicar. Para la operación 7, que no
publica, la marca de despacho es el instante en que el resultado queda
disponible en el búfer de salida.

```
operación k:  t_recv(k) ──── cómputo ──── t_envio(k) ─▶ publish ─▶ frontera ─▶ t_recv(k+1)
                                                                  └── serialización,
                                                                      transporte,
                                                                      despertar
```

Consecuencias que la implementación debe respetar:

- `t_envio(k) − t_recv(k)` es el tiempo de cómputo de la operación.
- `t_recv(k+1) − t_envio(k)` es el costo de la frontera, e incluye la
  serialización, porque la marca de despacho precede a la llamada de
  publicación.
- La latencia de extremo a extremo primaria (§3.8.1) es
  `t_envio(7) − t_recv(1)`; incluye la obtención del fotograma.
- La latencia sin adquisición, que se informa como descomposición, es
  `t_envio(7) − t_envio(1)`.

### 2.3 Transporte del índice

Cada operación copia la cabecera recibida en el mensaje que publica, sin
modificarla. Lo único que viaja es el índice:

- `header.frame_id` = `"f%06d" % indice` (índice en el clip, 0–1216).
- `header.stamp` = sin uso como portador de tiempo. Se deja como esté (el
  productor no lo escribe); nada lo consume.

La marca de adquisición **no** viaja. Cada proceso escribe en su propia base
las dos marcas de cada fotograma, y la consolidación une filas de procesos
distintos por `(ventana, fotograma)`: `CLOCK_MONOTONIC` tiene el mismo origen
en todos los procesos del anfitrión (§2.1), de modo que restar la marca de
recepción del consumidor a la de despacho del productor para el mismo índice
da la latencia de la frontera sin necesidad de transporte. Transportar la
marca duplicaría en el mensaje un dato que la fila del productor ya tiene.

No se usa un tipo de mensaje propio: cambiaría los tipos y los tamaños de
carga útil declarados en `tab:operations` y agregaría una capa de
serialización que ninguna de las dos arquitecturas tiene. La comparación mide
el costo de las fronteras, y el instrumento no debe cambiar el objeto medido.
`std_msgs/Header` de ROS 2 no tiene número de secuencia, de modo que el índice
debe viajar explícitamente; sin él un suscriptor que recibe el fotograma 42
después del 39 no puede distinguir un descarte de un desfase de orden, ni el
analizador puede emparejar los extremos.

Desviación declarada en §3.8.1: `frame_id` no designa un marco de `tf2`. La
cadena no publica transformaciones ni tiene consumidores que lo interpreten
así; si en el futuro se agregara uno, el índice tendría que mudarse a un campo
propio.

### 2.4 Patrón de código

El cálculo se separa de la publicación para que la marca de despacho quede
donde corresponde. No se usa un decorador que envuelva el callback completo:
sellaría después del retorno y atribuiría al nodo el tiempo de serialización
y de transporte.

```python
# instrumentacion.py — único módulo de instrumentación; lo importan A y los nodos
import time, array
_S = time.perf_counter_ns          # CLOCK_MONOTONIC, ns

class Registro:
    """Marcas de una operación. Acumula en memoria; vuelca al cerrar la ventana."""
    __slots__ = ("nodo", "_v", "_f", "_r", "_e", "_o", "_ultimo")
    def __init__(self, nodo):
        self.nodo = nodo
        self._v = array.array("b"); self._f = array.array("q")
        self._r = array.array("q"); self._e = array.array("q")
        self._o = array.array("i"); self._ultimo = -1

    def abre(self, fotograma, ventana):
        t = _S()
        omitidos = 0 if self._ultimo < 0 else fotograma - self._ultimo - 1
        self._ultimo = fotograma
        self._v.append(ventana); self._f.append(fotograma)
        self._r.append(t);       self._o.append(omitidos)
        return t

    def cierra(self):
        self._e.append(_S())

    def vuelca(self, con, ventana):
        con.executemany(
            "INSERT INTO etapa(ventana,fotograma,nodo,t_recv_ns,t_envio_ns,omitidos)"
            " VALUES (?,?,?,?,?,?)",
            ((v, f, self.nodo, r, e, o) for v, f, r, e, o in
             zip(self._v, self._f, self._r, self._e, self._o) if v == ventana))
        del self._v[:], self._f[:], self._r[:], self._e[:], self._o[:]
        self._ultimo = -1            # se reinicia tras el volcado
```

`zip` trunca a la longitud del búfer más corto: una fila cuyo `cierra()` no
se ejecutó cuando la ventana se cierra —el fotograma estaba dentro de la
operación— no se inserta. Es el comportamiento buscado, no un error: para esa
ventana el fotograma no completó la operación.

Uso en un nodo de ROS 2 (`nodo` = número de operación de `tab:operations`):

```python
registro = Registro(nodo=3)
def callback(self, msg):
    fotograma = int(msg.header.frame_id[1:])
    registro.abre(fotograma, ventana)
    salida = self.procesar(msg)          # cómputo puro, sin ROS
    salida.header = msg.header           # propagación sin modificar
    registro.cierra()                    # marca de despacho
    self.pub.publish(salida)             # serialización y transporte
```

En la implementación monolítica el patrón es idéntico, con una llamada a
función en lugar de una publicación: la marca de despacho de la operación *k*
y la de recepción de la *k+1* quedan separadas por dos lecturas del reloj
(~0,5 µs).

**Costo medido** en el equipo, con CPython 3.12.3 y el `Registro` de arriba:
lectura del reloj entre 0,18 y 0,23 µs; etapa medida completa (dos marcas,
cinco `append` y el `return`) 1,1 µs sobre 0,18 µs de una llamada sin medir.
Con siete operaciones por fotograma, 7,6 µs por fotograma: 0,08 % de un
fotograma de 10 ms y 0,015 % de uno de 50 ms. El búfer ocupa 29 bytes por
fila; para la corrida más exigente (ventana saturada con ~12 000 fotogramas)
son ~350 KB por proceso.

---

## 3. Monitoreo de recursos

### 3.1 `tegrastats`

Un solo proceso hijo del orquestador, arrancado al verificar el estado inicial
(§3.7 paso 1) y detenido al cerrar el registro (§3.7 paso 6):

```sh
tegrastats --interval 500
```

Sin `--logfile`: el orquestador lee `stdout`, sella **cada línea** con
`perf_counter_ns()` al leerla y la escribe tal cual en `tegrastats.log`. Ese
sello es lo que pone las muestras en el mismo dominio de tiempo que las marcas
de los fotogramas; la hora de pared que trae la línea (resolución de 1 s) solo
sirve para auditoría. **Medido**: las líneas llegan de una en una, sin ráfagas
(no hace falta `stdbuf`).

Campos presentes en este equipo y su uso:

| Campo | Uso |
|---|---|
| `RAM X/YMB (lfb NxZ)` | memoria del sistema en uso y total |
| `CPU [x%@f,…]` (seis entradas) | porcentaje por núcleo y frecuencia por núcleo |
| `GR3D_FREQ x%` | proporción de tiempo de activación del GPU |
| `cpu@g`, `gpu@g`, `soc0@g`, `soc1@g`, `soc2@g`, `tj@g` | temperaturas (valor instantáneo y media desde el arranque de la herramienta) |
| `VDD_IN`, `VDD_CPU_GPU_CV`, `VDD_SOC` | potencia en mW; primer valor = instantáneo |

Ausencias verificadas en esta versión, que hay que declarar en §3.8 en lugar
de suponer que la tabla de la guía se cumple entera:

- `EMC_FREQ` no se reporta. La frecuencia de memoria se toma de
  `/sys/class/devfreq/bwmgr/cur_freq` (**medido**: 2 133 MHz).
- `SWAP` no aparece porque el equipo no tiene área de intercambio
  (`/proc/swaps` vacío). No se configura swap: hacerlo introduciría una
  variable nueva.
- `GR3D_FREQ` se reporta sin frecuencia de GPC (`x%` y no `x%@[f]`). La
  frecuencia del GPU se toma de `/sys/class/devfreq/*gpu*/cur_freq`
  (**medido**: `/sys/class/devfreq/17000000.gpu/cur_freq` = 1 020 MHz con
  gobernador `performance`).
- `NVDEC`, `NVJPG`, `VIC`, `APE`, `MTS` aparecen solo cuando el motor se usa.
  No se usan como señal: la decodificación del clip es parte de la adquisición
  y su costo queda dentro de la latencia.

**Los campos de media y máximo de `tegrastats` no se usan.** La herramienta
imprime, tras el valor instantáneo, la media y un tercer valor que la guía no
documenta; **medido** con 55 muestras consecutivas, la media coincide con la
media acumulada desde el arranque de la herramienta y el tercer valor se
mantiene en el máximo observado desde el arranque. Ninguno de los dos
corresponde a la ventana, de modo que la agregación se calcula siempre sobre
el primer valor de cada raíl.

Intervalo de 500 ms (**medido**, 8 s por intervalo, equipo en carga ligera):

| Intervalo | Cadencia efectiva | Periodo mediano / máximo | Costo |
|---|---|---|---|
| 100 ms | 9,1 Hz | 109 ms / 120 ms | 1,25 % de un núcleo |
| 200 ms | 4,7 Hz | 209 ms / 228 ms | 0,75 % de un núcleo |
| **500 ms** | **2,0 Hz** | **510 ms / 515 ms** | **0,37 % de un núcleo** |
| 1000 ms | 1,0 Hz | 1 008 ms / 1 011 ms | 0,12 % de un núcleo |

A 100 ms la herramienta no sostiene la cadencia que se le pide; a 500 ms la
sostiene con una desviación del 2 % y entrega 120 muestras en la ventana
regulada y 240 en la saturada, suficientes para medias, máximos y para la
serie térmica que exige el criterio de validez. El costo es además el mismo en
las cuatro configuraciones, de modo que no sesga la comparación, y se informa
para poder descontarlo.

### 3.2 Muestreador propio a 1 Hz

Un hilo del orquestador, con el mismo reloj, lee una vez por segundo:

| Señal | Origen |
|---|---|
| Frecuencia de CPU por núcleo | `/sys/devices/system/cpu/cpu<n>/cpufreq/scaling_cur_freq` |
| Frecuencia de GPU | `/sys/class/devfreq/*gpu*/cur_freq` |
| Frecuencia de memoria | `/sys/class/devfreq/bwmgr/cur_freq` |
| Memoria de la cadena | `memory.current` del ámbito, menos caché (`anon` + `shmem` de `memory.stat`) |

El tiempo de CPU de la cadena **no** se muestrea: se lee el contador
acumulado `cpu.stat:usage_usec` del ámbito al abrir y al cerrar la ventana, de
modo que `Δusage_usec / Δt` es exacto y sin error de muestreo. Es la señal con
la que se contrasta H3, porque el porcentaje de `tegrastats` es del sistema
completo e incluye la propia herramienta de monitoreo.

Costo del muestreador: tres lecturas de archivos por segundo para las
frecuencias, más tres por segundo para la memoria del ámbito, ~20 µs cada una,
del orden de 0,01 % de un núcleo.

### 3.3 Ámbito de control de la cadena

**Verificado en el equipo** (kernel 6.8.12-tegra, Ubuntu 24.04.5): cgroup v2
unificado (`cgroup2fs`) con los controladores `cpu`, `io`, `memory` y `pids`, y
`systemd-run --user --scope` funciona sin `sudo`. El orquestador lanza la
cadena —dos procesos en B, cuatro en C, siete en D, uno en A— como hijo de:

```sh
systemd-run --user --scope --quiet --unit=cadena-<id> -- <comando de la cadena>
```

Los hijos heredan el ámbito, de modo que un solo comando lo cubre todo,
incluido el intérprete de ROS 2 y los hilos de DDS. El código de salida del
comando se propaga. El ámbito queda en
`/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/cadena-<id>.scope/`
(la ruta se resuelve con `systemctl --user show -p ControlGroup --value
cadena-<id>.scope`, no se construye a mano).

Señales del ámbito y qué se hace con ellas:

| Archivo | Contenido | Uso |
|---|---|---|
| `cpu.stat` → `usage_usec` | tiempo de CPU acumulado, en µs, exacto | se lee al abrir y cerrar la ventana; `Δ/Δt` es la utilización atribuida a la cadena |
| `memory.stat` → `anon`, `shmem` | memoria anónima y compartida, en bytes | se muestrea a 1 Hz; media y máximo por ventana |
| `memory.current` | memoria total del ámbito (incluye caché de archivos) | solo auditoría: no es huella de la cadena |
| `memory.peak` | máximo de `memory.current` desde la creación del ámbito | cota superior, se registra y no se analiza |
| `pids.current` | procesos del ámbito | verificación: debe coincidir con los procesos lanzados |
| `cpu.max`, `memory.max` | límites | **no se fijan**: un límite cambiaría el comportamiento medido |

**Medido**: con un proceso que ocupa un núcleo durante 2 s de reloj,
`usage_usec` = 1 730 843 µs; `memory.current` = 3,8 MB y `memory.peak` =
4,3 MB. El contador es acumulado y monótono, de modo que la lectura al cierre
menos la lectura al inicio es exacta: no hay error de muestreo, a diferencia
del sondeo de `/proc/<pid>/stat`, que además exigiría rastrear los PIDs de los
siete nodos y de sus hijos.

Un ámbito por corrida y no uno por configuración: el ámbito se crea al lanzar
la cadena y muere con ella, de modo que `memory.peak` y `usage_usec` son de esa
corrida y no arrastran estado.

### 3.4 Agregación por ventana

Con las muestras `(t_i, x_i)` de la ventana `[t_0, t_1]` y
`Δt_i = t_{i+1} − t_i` (la última muestra usa la mediana de `Δt`):

- **Media**: `Σ x_i·Δt_i / Σ Δt_i`. La media aritmética solo coincide con esta
  cuando la cadencia es constante, y no lo es (510 ms de mediana, 515 ms de
  máximo).
- **Máximo**: máximo de las muestras crudas, sin suavizado.
- **P95**: percentil de las muestras con interpolación lineal, solo para CPU y
  latencia por fotograma.
- **CPU del sistema por muestra**: media de los seis porcentajes de núcleo.
  El máximo se informa sobre esa misma cantidad, y aparte el núcleo más
  cargado.
- **Energía por fotograma**: `E = P̄ · (t_1 − t_0) / N`, en J, con `N` los
  fotogramas completados de la ventana.
- **Rendimiento por vatio**: `FPS / (P̄ / 1000)`.
- **Temperatura**: máximo y variación `|T(t_1) − T(t_0)|` de `tj` y de
  `soc0`–`soc2`; es la cantidad que decide el criterio (iii) de validez.

### 3.5 Integridad del monitoreo

Criterio (iv) de validez de §3.7, cuantificado:

- `N_esperadas = (t_1 − t_0) / mediana(Δt)`.
- La ventana es válida si `N_observadas ≥ 0,97 · N_esperadas` y ninguna
  separación entre muestras consecutivas supera `3 · mediana(Δt)` (1,5 s con
  el intervalo fijado).
- La hoja de ejecución registra `N_esperadas`, `N_observadas`, la mediana y la
  máxima separación, de modo que la comprobación sea auditable y no un juicio
  del operador.

---

## 4. Esquema de la base

Una base por corrida, `corridas/<id>.db`, creada por el orquestador antes de
arrancar la cadena. Escribe cada participante al cerrar cada ventana, en una
sola transacción y nunca durante la ventana. `journal_mode=DELETE` (el valor
por omisión) para que el archivo quede autocontenido, sin `-wal` ni `-shm`.

```sql
CREATE TABLE corrida(
  id TEXT PRIMARY KEY, fecha TEXT NOT NULL,
  arquitectura TEXT NOT NULL, resolucion TEXT NOT NULL,
  bloque INTEGER, posicion INTEGER, semilla INTEGER,
  artefacto_commit TEXT, clip_sha256 TEXT, pesos_sha256 TEXT,
  intervalo_ms INTEGER NOT NULL,
  desfase_realtime_inicio_ns INTEGER, desfase_realtime_fin_ns INTEGER,
  ambito TEXT,                         -- unidad de systemd de la cadena
  reposo_inicio_ns INTEGER, reposo_fin_ns INTEGER,
  reposo_p_mw REAL, reposo_n INTEGER,  -- línea base de potencia (§7)
  modo_energia TEXT, gobernadores TEXT, resultado TEXT);

CREATE TABLE ventana(
  ventana TEXT PRIMARY KEY,            -- 'regulada' | 'saturada'
  t_inicio_ns INTEGER NOT NULL, t_fin_ns INTEGER NOT NULL,
  tasa_fps REAL,                       -- NULL en la saturada
  fotogramas_ofrecidos INTEGER, fotogramas_completados INTEGER,
  cadena_cpu_usec_ini INTEGER, cadena_cpu_usec_fin INTEGER);  -- cgroup cpu.stat

CREATE TABLE etapa(                    -- una fila por fotograma y operación
  ventana TEXT NOT NULL, fotograma INTEGER NOT NULL, nodo INTEGER NOT NULL,
  t_recv_ns INTEGER NOT NULL, t_envio_ns INTEGER NOT NULL,
  omitidos INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (ventana, fotograma, nodo)) WITHOUT ROWID;

CREATE TABLE muestreo(                 -- una fila por línea de tegrastats
  t_ns INTEGER PRIMARY KEY,
  ram_usada_mb INTEGER, ram_total_mb INTEGER, lfb_mb INTEGER,
  gr3d_pct INTEGER,
  vdd_in_mw INTEGER, vdd_cpu_gpu_cv_mw INTEGER, vdd_soc_mw INTEGER,
  temp_cpu_c REAL, temp_gpu_c REAL,
  temp_soc0_c REAL, temp_soc1_c REAL, temp_soc2_c REAL, temp_tj_c REAL,
  linea TEXT NOT NULL);                -- línea cruda, para auditar el analizador

CREATE TABLE muestreo_cpu(
  t_ns INTEGER NOT NULL, nucleo INTEGER NOT NULL,
  pct INTEGER NOT NULL, mhz INTEGER NOT NULL,
  PRIMARY KEY (t_ns, nucleo)) WITHOUT ROWID;

CREATE TABLE estado(                   -- 1 Hz de sysfs
  t_ns INTEGER PRIMARY KEY,
  gpu_mhz INTEGER, emc_mhz INTEGER,
  cadena_anon_kb INTEGER, cadena_shmem_kb INTEGER,
  cadena_pids INTEGER, cadena_peak_kb INTEGER);  -- pids y pico, solo auditoría

CREATE TABLE resumen(                  -- agregados de §3.4
  ventana TEXT NOT NULL, metrica TEXT NOT NULL,
  valor REAL NOT NULL, unidad TEXT NOT NULL,
  PRIMARY KEY (ventana, metrica));
```

Decisiones del esquema:

- `omitidos` cuenta los fotogramas que el productor publicó y el consumidor no
  recibió, deducidos del salto entre índices. Sustituye a la columna booleana
  `descartado` de la plantilla, que no puede expresar cuántos fotogramas
  perdió una frontera. Los descartes de una frontera son `Σ omitidos` de las
  filas del nodo consumidor.
- La tabla `etapa` es la que lee P-14. La latencia primaria es
  `t_envio_ns(nodo máx.) − t_recv_ns(nodo 1)` para el mismo `fotograma`.
- `linea` duplica la información de las columnas numéricas a propósito: si el
  analizador se equivoca, el registro crudo permite rehacerlo.
- El tiempo de CPU de la cadena no está en `estado`: es el contador
  acumulado del ámbito leído en los extremos de la ventana, de modo que vive
  en `ventana` y no en el muestreo.
- La base de la campaña, `resultados.db`, se construye con el mismo esquema a
  partir de las bases de cada corrida (`ATTACH` + `INSERT … SELECT`). Es
  regenerable y por eso no se versiona; las bases por corrida sí.

---

## 5. Archivos y nombres

```
corridas/<id>/
├── hoja.yaml           # hoja de ejecución (plantilla-corrida.md §2), la completa el orquestador
├── <id>.db             # marcas y muestras (tablas de §4)
└── tegrastats.log      # registro crudo de tegrastats, línea por línea
```

`<id>` conserva el formato de la plantilla (`c<AA><R>-b<BB>-<nn>`, con sufijo
`-r1`, `-r2` para las repeticiones de una corrida inválida). La hoja de
ejecución se completa **después** de cerrar la base, a partir de ella: los
campos de ventanas, validez y frecuencias medias no se escriben a mano.

---

## 6. Orquestador

Un proceso Python sin ROS, el mismo para las cuatro configuraciones. Nunca
ejecuta la cadena dentro de sí mismo, ni siquiera en la configuración A: si A
corriera dentro del orquestador, cargaría con el costo del monitoreo y la
comparación dejaría de ser entre arquitecturas.

Secuencia por corrida (§3.7 pasos 1–8):

1. Verifica `nvpmodel -q`, los gobernadores de CPU y de GPU y los hashes;
   crea `corridas/<id>.db` con el esquema y una fila en `corrida`.
2. Arranca `tegrastats --interval 500`, el hilo lector y el muestreador de
   1 Hz.
3. Arranca la cadena como hijo de un ámbito de control propio de la corrida
   (`systemd-run --user --scope --unit=cadena-<id>`, §3.3), con la
   configuración de la condición. Registra la ruta del ámbito en `corrida`.
   Si el ámbito no se crea o `pids.current` no coincide con los procesos
   lanzados, la corrida se aborta antes de medir.
4. La cadena conduce sus propias ventanas: la operación 1 (o A) marca el
   inicio y el fin de cada una y escribe la fila de `ventana`. Los demás nodos
   registran de forma continua y el analizador asigna cada fila a una ventana
   por su marca de tiempo, de modo que no hace falta sincronizar procesos para
   abrir y cerrar ventanas.
5. Al terminar la cadena, detiene `tegrastats`, lee el `cpu.stat` de cierre,
   agrega (§3.4), escribe `resumen`, evalúa la validez, completa `hoja.yaml`
   y cierra la base.
6. Deja el equipo en reposo y espera el umbral de temperatura leyendo
   `tj-thermal` a 1 Hz, fuera de la base. Durante los **últimos 60 s** de esa
   espera lee `VDD_IN` de `tegrastats` —lo arranca para esa ventana— y
   registra `reposo_p_mw`, `reposo_n` y los extremos en `corrida`: es la línea
   base de potencia de la corrida siguiente (§7).

El enfriamiento y la verificación del estado inicial no necesitan
`tegrastats`: se leen las zonas térmicas directamente, de modo que el
monitoreo de la corrida no se solape con el de la espera.

---

## 7. Verificaciones para P-12

Se ejecutan en el piloto, se registran en el manifiesto de la campaña y no
modifican la lógica del procedimiento.

| Verificación | Cómo | Resultado esperado |
|---|---|---|
| El monitoreo no altera la medición | una corrida de la condición central con y sin `tegrastats` (dos corridas, solo piloto) | latencia media dentro de la dispersión entre repeticiones de la misma condición |
| La instrumentación no altera la medición | la misma corrida con y sin el módulo de marcas | ídem; el costo calculado es de 7,6 µs por fotograma |
| Las marcas cruzan procesos | comparar `t_recv(2) − t_envio(1)` con la distribución de latencia de frontera | sin valores negativos; ningún salto sistemático de reloj |
| El índice viaja intacto | comparar la secuencia de `frame_id` de la operación 7 con la referencia de P-09 | misma secuencia en las doce condiciones de la ventana regulada |
| Los descartes se cuentan | contrastar `Σ omitidos` por frontera con la diferencia de índices publicados y recibidos | coinciden; en la ventana regulada, cero |
| La cadencia se sostiene | mediana y máximo de `Δt` de `tegrastats` en reposo y en carga | ≥ 0,97 de las muestras esperadas; sin separaciones > 1,5 s |
| La frecuencia de memoria es la efectiva | `bwmgr/cur_freq` contra el valor de la tabla de `nvpmodel` | coherente con el escalado por omisión del dominio de memoria |
| El ámbito cubre la cadena | `pids.current` contra los procesos lanzados, al inicio y al cierre | coincide; ningún proceso de la cadena queda fuera |
| El ámbito no arrastra estado | `usage_usec` del ámbito en el instante de crearlo | < 5 ms |
| La atribución es coherente | `Δusage_usec/Δt` de la cadena contra el porcentaje de `tegrastats` | la cadena nunca excede al sistema; la diferencia es el resto del equipo |
| La línea base de potencia es estable | 60 s en reposo al final de cada enfriamiento | dispersión menor que la diferencia que se busca medir; la deriva entre bloques queda registrada |

Las tres filas del ámbito y la de la línea base son mediciones nuevas. La
línea base **no agrega tiempo a la campaña**: se toma del último minuto de la
espera de enfriamiento que el procedimiento ya contempla (§3.7 paso 8), de modo
que hay una por corrida y no una por bloque. Es la única adición de este
pendiente al procedimiento de P-06.

---

## 8. Herramientas opcionales

`resultados.db` se puede consultar con `sqlite3`, con `pandas.read_sql_query`
y, si se quiere una vista durante el piloto, con un panel que lea SQLite en
solo lectura. Ninguna de esas herramientas forma parte del método: las tablas
y figuras de la memoria salen del análisis de P-14 sobre `resultados.db`, y
una eventual instalación de paneles no debe introducir escrituras en la base
ni procesos adicionales durante una corrida.

---
