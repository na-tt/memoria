# Plantilla de corrida y registro de desviaciones

Documento de trabajo interno. **No forma parte de la memoria** y no debe
incluirse en el PDF.

Propósito: dar forma concreta a la hoja de ejecución de
`sections/capitulo-3.tex` §3.7.4 (`tab:run-manifest`) y al registro de
desviaciones que exige §3.7.3. Es la especificación que el arnés de P-11 debe
materializar; hasta entonces sirve para ejecutar a mano la campaña piloto
(P-12) y la campaña final (P-13) sin decisiones implícitas.

Última revisión: 2026-10-19 (P-06).

---

## 1. Unidades de registro

Cada corrida produce tres piezas, con nombres estables:

| Pieza | Formato | Nombre |
|---|---|---|
| Hoja de ejecución | YAML | `corridas/<id>.yaml` |
| Registro por fotograma | CSV, uno por ventana | `corridas/<id>-regulada.csv`, `corridas/<id>-saturada.csv` |
| Salida del monitoreo | log de texto de `tegrastats` | `corridas/<id>-tegrastats.log` |

El identificador `<id>` es `c<AA><R>-b<BB>-<nn>`: arquitectura
(`a`–`d`), resolución (`1`–`3`), bloque (`01`–`10`) y posición dentro del
bloque (`01`–`12`). El archivo de cada corrida inválida y repetida conserva
su identificador y agrega el sufijo `-r1`, `-r2`, …

Todo el directorio `corridas/`, junto con el código y la semilla del orden, se
versiona con el artefacto experimental.

## 2. Hoja de ejecución

```yaml
# corridas/<id>.yaml
id: c-b2-b03-05
fecha: 2026-11-04T14:32:07-03:00

condicion:
  arquitectura: B           # A | B | C | D
  resolucion: 640x360       # 320x180 | 640x360 | 1280x720
  bloque: 3
  posicion_en_bloque: 5
  semilla_orden: 20261104   # semilla de la permutación del bloque

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
  registro_regulada: corridas/<id>-regulada.csv
  registro_saturada: corridas/<id>-saturada.csv
  monitoreo: corridas/<id>-tegrastats.log
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
| `t_envio_ns` | reloj monótono de despacho |
| `descartado` | `1` si la muestra pendiente fue reemplazada en esa frontera |

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
