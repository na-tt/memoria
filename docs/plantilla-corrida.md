# Plantilla de corrida y registro de desviaciones

Documento de trabajo interno. **No forma parte de la memoria** y no debe
incluirse en el PDF.

Propósito: dar forma concreta a la hoja de ejecución de
`sections/capitulo-3.tex` §3.7.4 (`tab:run-manifest`) y al registro de
desviaciones que exige §3.7.3. Es la especificación que el arnés de P-11 debe
materializar; hasta entonces sirve para ejecutar a mano la campaña piloto
(P-12) y la campaña final (P-13) sin decisiones implícitas.

Última revisión: 2026-10-19 (P-06). Los formatos de archivo y las columnas del
registro por fotograma se revisaron el mismo día en P-07; el detalle de la
instrumentación está en `docs/instrumentacion.md`.

---

## 1. Unidades de registro

Cada corrida produce tres piezas, con nombres estables:

| Pieza | Formato | Nombre |
|---|---|---|
| Hoja de ejecución | YAML | `corridas/<id>/hoja.yaml` |
| Registro por fotograma y muestras del monitoreo | base SQLite | `corridas/<id>/<id>.db` |
| Salida cruda del monitoreo | log de texto de `tegrastats` | `corridas/<id>/tegrastats.log` |

El esquema de la base, el patrón de código de las marcas y las verificaciones
que hay que hacer en el equipo están en `docs/instrumentacion.md` (P-07). La
base se escribe al cerrar cada ventana y nunca durante la ventana.
El identificador `<id>` es `c<AA><R>-b<BB>-<nn>`: arquitectura
(`a`–`d`), resolución (`1`–`3`), bloque (`01`–`10`) y posición dentro del
bloque (`01`–`12`). El archivo de cada corrida inválida y repetida conserva
su identificador y agrega el sufijo `-r1`, `-r2`, …

Todo el directorio `corridas/`, junto con el código y la semilla del orden, se
versiona con el artefacto experimental.

## 2. Hoja de ejecución

```yaml
# corridas/<id>/hoja.yaml
id: c-b2-b03-05
fecha: 2026-11-04T14:32:07-03:00

condicion:
  arquitectura: B           # A | B | C | D
  resolucion: 640x360       # 320x180 | 640x360 | 1280x720
  bloque: 3
  posicion_en_bloque: 5
  semilla_orden: 20261104   # semilla de la permutación del bloque

ambito:
  unidad: cadena-c-b2-b03-05          # systemd-run --user --scope --unit=...
  ruta: /sys/fs/cgroup/user.slice/...  # resuelta con systemctl --user show -p ControlGroup
  procesos_lanzados: 2                 # 1 en A, 2 en B, 4 en C, 7 en D; debe coincidir con pids.current
  cpu_usec_inicio: <n>                 # cpu.stat:usage_usec al arrancar la cadena
  cpu_usec_cierre: <n>                 # al terminar; Delta/Delta t es la CPU de la corrida

procedencia:
  artefacto_commit: <hash>
  clip_sha256: 313eed7b8e46ae388c9d59f4e6068d5ab6fb98ce13e0d63b48b8cdd604d76767
  pesos_version: yolov8n.pt
  pesos_sha256: f59b3d83e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36

ventanas:
  regulada:
    tasa_fps: 15.0          # f0 = 30/k, con k registrado en el manifiesto de campaña
    inicio: <instante_monotonico>
    fin: <instante_monotonico>
    duracion_s: 60.0
    fotogramas_ofrecidos: <n>
    fotogramas_completados: <n>
    descartes_por_frontera: [0, 0, 0, 0, 0, 0]   # una entrada por frontera de la configuración
  saturada:
    tasa_fps: null           # sin ritmo
    inicio: <instante_monotonico>
    fin: <instante_monotonico>
    duracion_s: 120.0
    fotogramas_ofrecidos: <n>
    fotogramas_completados: <n>
    descartes_por_frontera: [<n>, ...]
    fotogramas_en_vuelo_max: <n>
    fotogramas_en_vuelo_promedio: <n>

# Integridad del monitoreo, igual en las dos ventanas (P-07, §3.8.7).
monitoreo:
  regulada:
    muestras_esperadas: 117      # duracion_s / periodo_mediano_ms
    muestras_observadas: <n>
    periodo_mediano_ms: <p>
    separacion_maxima_ms: <g>    # valida si < 3 * periodo_mediano_ms
  saturada:
    muestras_esperadas: 235
    muestras_observadas: <n>
    periodo_mediano_ms: <p>
    separacion_maxima_ms: <g>

# Agregados de recursos por ventana (P-07, docs/instrumentacion.md §3.4).
recursos:
  regulada:
    cpu_sistema_pct_media: <x>      # media de los seis nucleos, ponderada por intervalo
    cpu_sistema_pct_max: <x>
    cpu_cadena_pct_un_nucleo: <x>   # Delta(usage_usec del cgroup)/Delta t
    ram_sistema_mb_media: <x>
    memoria_cadena_mb_media: <x>    # anon + shmem del cgroup, muestreado a 1 Hz
    memoria_cadena_mb_max: <x>
    gpu_activacion_pct_media: <x>
    potencia_reposo_mw: <x>         # linea base: ultimos 60 s del enfriamiento previo
    potencia_media_mw: <x>          # VDD_IN de la ventana
    potencia_maxima_mw: <x>
    potencia_atribuible_mw: <x>     # media de la ventana - potencia_reposo_mw
    energia_por_fotograma_j: <x>
    fps_por_watio: <x>
  saturada:
    cpu_sistema_pct_media: <x>
    cpu_sistema_pct_max: <x>
    cpu_cadena_pct_un_nucleo: <x>
    ram_sistema_mb_media: <x>
    memoria_cadena_mb_media: <x>
    memoria_cadena_mb_max: <x>
    gpu_activacion_pct_media: <x>
    potencia_reposo_mw: <x>
    potencia_media_mw: <x>
    potencia_maxima_mw: <x>
    potencia_atribuible_mw: <x>
    energia_por_fotograma_j: <x>
    fps_por_watio: <x>

estado:
  modo_energia: MAXN_SUPER   # lo que informe nvpmodel -q
  gobernadores: {cpu: performance, gpu: performance, memoria: <por omisión>}
  temperatura_soc_inicio_regulada_c: <t>
  temperatura_soc_fin_regulada_c: <t>
  temperatura_soc_inicio_saturada_c: <t>
  temperatura_soc_fin_saturada_c: <t>
  temperatura_ambiente_c: <t>
  frecuencia_media: {cpu_ghz: <f>, gpu_ghz: <f>, memoria_ghz: <f>}

validez:
  fotogramas_comparados: <n>
  discrepancias: <n>              # cantidad, etiqueta, coordenadas > 1 px, puntaje > 1e-3
  ventana_regulada_sin_descartes: true
  oferta_excede_completacion: true   # solo ventana saturada; ver §6
  delta_temperatura_dentro_de_ventanas: <°C>
  monitoreo_integro: true
  resultado: valida               # valida | repetida | descartada

archivos:
  base: corridas/<id>/<id>.db
  monitoreo_crudo: corridas/<id>/tegrastats.log
desviaciones: []                  # identificadores de entradas del registro de desviaciones
```

Regla de llenado: un campo que no se aplica a la configuración se escribe
`null` (nunca se omite), para que la hoja siga siendo comparable entre A y
B/C/D.

## 3. Registro por fotograma

Una fila por fotograma y por frontera observada, con estas columnas mínimas:

| Columna | Contenido |
|---|---|
| `ventana` | `regulada` \| `saturada` |
| `fotograma` | índice en el clip (0–1216), no la posición en la ventana |
| `nodo` | identificador de la operación que registra la fila (`tab:operations`) |
| `t_recv_ns` | reloj monótono de recepción |
| `t_envio_ns` | reloj monótono de despacho, inmediatamente antes de publicar |
| `omitidos` | fotogramas que la etapa productora publicó entre la fila anterior y esta; los descartes de una frontera son su suma |

`omitidos` reemplaza al indicador binario `descartado` de la versión inicial de
esta plantilla: un bit no puede expresar cuántos fotogramas perdió una
frontera, y el conteo por diferencia de índices es exactamente lo que §3.8
define como descarte en una frontera.
La latencia de extremo a extremo se calcula solo con la fila del primer nodo y
la del último (§3.8.1); las filas internas sirven para contar descartes y
fotogramas en vuelo (§3.7.2).

## 4. Registro de desviaciones

Un archivo `desviaciones.md`, una entrada por evento, en orden cronológico:

```markdown
## <fecha> · <id de corrida> · <condición>
- **Previsto:** ...
- **Ocurrido:** ...
- **Causa:** ... (o «desconocida»)
- **Decisión:** repetición | invalidación | continuación
- **Notas:** ...
```

Ejemplos de eventos que exigen entrada: umbral de reposo no alcanzado dentro
de 300 s, meseta térmica no alcanzada dentro de 300 s, discordancia con la
salida de referencia, descarte en la ventana regulada, interrupción del
monitoreo, ajuste del valor de `k` después de los pilotos, cambio de cualquier
versión fijada en §3.1–§3.2.

## 5. Decisiones que fija la campaña piloto

Se registran una sola vez, al inicio de la campaña final, y no se modifican
durante ella:

| Decisión | Símbolo | Dónde se registra |
|---|---|---|
| Divisor de la tasa regulada y tasa resultante | `k`, `f0` | manifiesto de la campaña |
| Conducta del middleware ante la muestra pendiente | reemplazo \| retención | manifiesto de la campaña |
| Umbral de reposo | temperatura del SoC | manifiesto de la campaña |
| Semilla y orden de cada bloque | `semilla_orden` | hoja de cada corrida |
| Línea base de potencia en reposo, una por corrida | `potencia_reposo_mw` | hoja de cada corrida |

## 6. Verificación de sensibilidad al perfil de QoS

No forma parte de la campaña y no entra en el análisis: son cuatro corridas
sobre una sola condición central (C a 640×360), solo la ventana saturada.

| Corrida | Profundidad | Repetición |
|---|---|---|
| `sens-d1-r1` | 1 (perfil fijado) | 1 |
| `sens-d1-r2` | 1 (perfil fijado) | 2 |
| `sens-d10-r1` | 10 (perfil por omisión de ROS 2) | 1 |
| `sens-d10-r2` | 10 (perfil por omisión de ROS 2) | 2 |

Se usa la misma hoja de ejecución, con `condicion.arquitectura: C`,
`condicion.resolucion: 640x360` y un campo adicional que registra la
profundidad efectiva. Lo que se contrasta:

| Afirmación del diseño | Evidencia esperada con `depth: 1` | Evidencia esperada con `depth: 10` |
|---|---|---|
| La fuente no queda estrangulada | tasa de oferta ≫ tasa de completación | igual |
| Los descartes ocurren en las fronteras | descartes > 0, acotados por frontera | descartes > 0, historial lleno |
| La latencia mide la cadena, no la cola | latencia ≈ costo por fotograma | latencia ≈ (N−1)/λ ≈ 300 ms |
| La conducta del middleware está identificada | se observa reemplazo o bloqueo | se observa reemplazo o bloqueo |

Si la evidencia contradice lo previsto, se documenta la contradicción; no se
ajusta el perfil de QoS ni se repite la verificación hasta obtener el
resultado esperado.
