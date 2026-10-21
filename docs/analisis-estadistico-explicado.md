# §3.9 «Análisis de datos», explicada

Documento interno de estudio. **No forma parte del PDF** y no se incluye en el
build. El texto normativo —el que se defiende ante la comisión— es
`sections/capitulo-3.tex` §3.9; esto es material de apoyo para entender por qué
esa sección dice lo que dice.

Los números de ejemplo que aparecen marcados como *ficticios* están inventados
para mostrar la aritmética. No son resultados de la campaña: la campaña aún no
se ejecuta.

---

## 1. El problema que resuelve §3.9

Una comparación de rendimiento produce, al final, una planilla: doce
condiciones, diez corridas cada una, varias métricas por corrida. Sobre esa
planilla se pueden hacer literalmente cientos de cosas: comparar medias,
medianas, percentiles; agrupar o no agrupar; aplicar una prueba u otra; corregir
o no corregir por comparaciones múltiples. Con datos reales —siempre ruidosos—
casi cualquier colección de decisiones produce *alguna* diferencia
estadísticamente significativa.

El peligro concreto es este: si se miran los datos primero y se elige después la
prueba que arroja el resultado más favorable, el valor *p* publicado deja de
tener sentido, porque ya no es la probabilidad de un resultado bajo una regla
fija, sino el mínimo de muchas probabilidades calculadas sobre los mismos datos.
El lector no tiene forma de distinguir una decisión de método de una decisión de
resultado.

La solución que adopta §3.9 es **preespecificar**: escribir antes de la campaña
qué se va a calcular, con qué prueba, con qué umbral y con qué regla se decide.
Una prueba no prevista se puede hacer, pero se informa como *exploratoria* y no
reemplaza a la que el plan declara. Esto tiene un costo —se renuncia a la
libertad de elegir después— y una ventaja: cualquier lector puede reproducir la
cadena de decisiones y comprobar que el resultado no depende de ellas.

La sección tiene entonces dos mitades:

1. **Qué se calcula** (el listado de seis pasos al comienzo de §3.9).
2. **Cómo se decide** (§3.9.1 a §3.9.9): la unidad de análisis, los contrastes,
   las pruebas, la magnitud, la corrección, los criterios, los atípicos, la
   potencia y la especificación del script.

---

## 2. El experimento en una página

| Elemento | Valor |
| --- | --- |
| Configuraciones arquitectónicas | 4: A monolítica, B (2 nodos), C (4 nodos), D (7 nodos) |
| Resoluciones | 3: 320×180, 640×360, 1280×720 (área ×4 por paso) |
| Condiciones experimentales | 4 × 3 = **12** |
| Bloques | **10**; en cada bloque se corre una vez cada condición, en orden aleatorio |
| Corridas | 12 × 10 = **120** |
| Ventana regulada | 60 s, con la fuente a tasa fija *f₀*: de aquí sale la **latencia** |
| Ventana saturada | 120 s, sin ritmo: de aquí salen la **tasa** y los **recursos** |
| Réplica (unidad de análisis) | la **corrida**, no el fotograma |

Dos hechos del diseño que gobiernan todo el análisis:

- **Las condiciones están pareadas por bloque.** En el bloque 7, A y B se
  ejecutaron con el mismo equipo, la misma temperatura de partida y el mismo
  estado del sistema. Comparar A con B *dentro* del bloque cancela esa
  variación; comparar la media de todas las A con la media de todas las B no la
  cancela.
- **Las fronteras no están equiespaciadas.** A tiene 0 fronteras, B tiene 1, C
  tiene 3 y D tiene 6. Los pasos consecutivos agregan +1, +2 y +3 fronteras. Y
  el volumen que cruza tampoco es proporcional: B lleva 0,17/0,69/2,76 MB por
  fotograma según resolución, C lleva 1,45/1,97/4,04 MB y D lleva
  1,57/2,09/4,16 MB. El paso C→D agrega tres fronteras y menos de 0,2 MB: es
  casi puro costo fijo de frontera.

---

## 3. Caja de herramientas: los conceptos, uno por uno

### 3.1 Población, muestra, estimador, ruido

La *población* sería el conjunto infinito de corridas que se podrían hacer con
esta cadena en este equipo. La *muestra* son las diez que se hacen. Un
*estimador* es la regla que convierte la muestra en un número: «la media de las
diez latencias». El *ruido* es todo lo que hace que la corrida 4 no dé
exactamente lo mismo que la corrida 5 aunque nada haya cambiado.

La estadística inferencial responde una sola pregunta: **dado el ruido
observado, ¿cuánto puede moverse el número que reporto?** Todo lo demás en §3.9
—intervalos, pruebas, umbrales— son formas de responder eso.

### 3.2 Distribución, cola, media, mediana, percentil

Una *distribución* es cómo se reparten los valores: muchas latencias parecidas
y unas pocas muy altas. La *cola derecha* es ese puñado de valores altos. En
latencia casi siempre hay cola: el promedio es estable, pero de vez en cuando un
fotograma tarda el triple (una falla de caché, una interrupción del
planificador).

- **Media**: suma dividida por la cantidad. Usa toda la información, y por eso
  es la más eficiente; también es la más sensible a la cola.
- **Mediana**: el valor del medio cuando se ordenan. Robusta a la cola, menos
  eficiente.
- **Percentil 95 (P95)**: el valor bajo el cual cae el 95 % de los casos. «Uno de
  cada veinte fotogramas tardó más que esto». P99, lo mismo con uno de cada cien.

§3.9 usa la **media** como estadístico primario de latencia —porque es con la
que está escrita la ecuación del sobrecosto— y la **mediana** como verificación
exploratoria. Los percentiles son descriptivos: no se contrastan como prueba
principal, porque su variabilidad con pocas observaciones es enorme.

### 3.3 Dispersión: varianza, desviación estándar, IQR

La *varianza* es el promedio de las distancias al cuadrado respecto de la media;
la *desviación estándar* (DE) es su raíz, y vuelve a estar en las unidades de la
métrica (ms, fotogramas/s). El *rango intercuartílico* (IQR) es Q3 − Q1, la
amplitud del 50 % central, y no lo afectan los valores extremos.

En §3.9 la dispersión aparece en tres lugares: la DE de las *diferencias* entre
corridas pareadas (que es la que entra en la prueba *t*), el IQR para marcar
corridas atípicas, y la variabilidad entre corridas que estima la campaña piloto
para el cálculo de potencia.

### 3.4 Réplica e independencia: la pseudorreplicación

Dos observaciones son *independientes* cuando la información de una no dice nada
sobre la otra. Los fotogramas de una misma corrida **no** son independientes: si
la corrida tuvo el equipo caliente, todos los fotogramas lo tuvieron; si la
memoria quedó fragmentada, todos lo notaron.

*Pseudorreplicación* es tratar como independientes observaciones que no lo son.
Su efecto es aritmético y brutal: el error estándar de una media es
`DE/√n`. Si en lugar de `n = 10` corridas se usa `n = 1200` fotogramas, el error
estándar se divide por `√120` ≈ 11, y los intervalos de confianza se vuelven once
veces más estrechos sin que se haya aprendido nada nuevo.

*Ejemplo ficticio.* Supóngase que la DE entre corridas de la diferencia A→B (en
escala logarítmica) es 0,079, de modo que el error estándar con diez pares es
0,025. Si además se sabe que la DE entre fotogramas es 0,15 y se usaran 2400
fotogramas como réplicas, el error estándar saldría 0,0043: casi seis veces más
pequeño, y cualquier diferencia minúscula parecería «significativa». Por eso la
unidad de análisis es la corrida: cada corrida aporta **un** valor por métrica.

### 3.5 Pareado vs. independiente

- **Diseño independiente:** dos grupos distintos de unidades (sujetos A y
  sujetos B) y se compara el promedio de cada grupo.
- **Diseño pareado:** cada unidad se mide en las dos condiciones y se compara
  *la diferencia dentro de la unidad*.

El pareado es más potente porque elimina la variación que ambas mediciones
comparten. Si la corrida 7 tuvo el equipo lento por cualquier razón, esa lentitud
afecta a A y a B por igual y desaparece de la diferencia. En la práctica: con 10
pares se detecta un efecto que con dos grupos independientes de 10 exigiría
bastantes más.

El pareamiento aquí no se elige al analizar: es una propiedad del diseño, porque
cada bloque ya contiene una corrida de cada condición.

### 3.6 Hipótesis nula y valor *p*

La *hipótesis nula* es la afirmación «no hay diferencia» (o, con más precisión,
«la diferencia promedio es cero»). El *valor p* es:

> la probabilidad de observar una diferencia al menos tan grande como la
> observada **si la hipótesis nula fuera cierta**.

Tres cosas que el valor *p* **no** es:

- No es la probabilidad de que la hipótesis nula sea cierta.
- No es la probabilidad de haberse equivocado.
- No mide el tamaño del efecto. Con suficientes observaciones, una diferencia
  irrelevante da *p* pequeño; con pocas, una diferencia enorme puede no darlo.

§3.9 informa el *p* y además la magnitud con su intervalo, justamente porque el
*p* solo no alcanza para decidir si conviene adoptar una arquitectura.

### 3.7 Error de tipo I, error de tipo II, nivel de significancia

- **Error de tipo I (falso positivo):** declarar una diferencia que no existe.
  Su probabilidad se controla con el nivel α (0,05).
- **Error de tipo II (falso negativo):** no detectar una diferencia que sí
  existe. Su complemento es la **potencia**.

Bajar α reduce los falsos positivos y aumenta los falsos negativos, y viceversa.
Con 10 pares no se puede tener todo: el diseño apunta a detectar efectos grandes,
no matices, y eso está declarado en §3.9.8.

### 3.8 Intervalo de confianza

Un intervalo de confianza (IC) al 95 % es un rango construido con un
procedimiento que, repetido muchas veces, contendría el valor verdadero el 95 %
de las veces. En la práctica se lee así: «el efecto está en algún lugar de este
rango, y los valores fuera de él son poco compatibles con los datos».

Es más informativo que el *p*, porque muestra **cuánto** y **con cuánta
precisión**. Un IC estrecho y alejado de cero es evidencia fuerte; un IC ancho
que cruza el cero es «no se sabe»; un IC estrecho pegado a cero es «no hay efecto
apreciable» (esto último requiere un margen de equivalencia, que §3.9
explícitamente no fija).

### 3.9 Normalidad y la prueba de Shapiro–Wilk

Muchas pruebas clásicas suponen que los datos siguen una distribución normal (la
campana de Gauss). Shapiro–Wilk contrasta esa suposición: su hipótesis nula es
«los datos son normales», de modo que un *p* pequeño indica **no normalidad**.

En §3.9 se aplica a las **diez diferencias**, no a las latencias, porque es la
diferencia la que entra en la prueba *t* pareada. Y se aplica con nivel 0,10 (no
0,05) porque con diez observaciones la prueba tiene poca potencia: es fácil que
no detecte una no normalidad real. Usar un nivel más exigente para rechazar la
normalidad sería equivocarse hacia el lado equivocado.

### 3.10 La prueba *t* pareada

Convierte la pregunta «¿A y B difieren?» en «¿el promedio de las diez
diferencias es distinto de cero, dado el ruido de esas diferencias?». El
estadístico es

```
t = media de las diferencias / (DE de las diferencias / √10)
```

y se compara con una distribución de referencia (*t* de Student) con 9 grados de
libertad (n − 1). Si |t| supera el valor crítico —2,262 para α = 0,05
bilateral—, se rechaza la hipótesis nula.

La prueba *t* **no** exige que las latencias sean normales, ni que A y B tengan
la misma varianza: exige que las *diferencias* sean aproximadamente normales.

### 3.11 Wilcoxon de rangos con signo y el *p* mínimo alcanzable

Cuando las diferencias no son normales, se usa una prueba que no supone forma:

1. Se toma el valor absoluto de cada diferencia y se le asigna un **rango**
   (1 al más pequeño, 10 al más grande).
2. Se suman los rangos de las diferencias positivas (estadístico W⁺).
3. Se compara W⁺ con lo que se esperaría si los signos fueran al azar.

Con 10 pares hay `2¹⁰ = 1024` combinaciones de signos posibles. El resultado más
extremo posible (las 10 diferencias con el mismo signo) tiene probabilidad
`1/1024` en cada cola, de modo que el **menor *p* bilateral alcanzable es
`2/1024 ≈ 0,002`**. Ese es el piso de la prueba: por grande que sea el efecto, el
*p* no baja de ahí.

Esta cifra es la que obliga a razonar con cuidado los umbrales corregidos: un
umbral por debajo de 0,002 haría que la prueba **nunca** pueda rechazar. Ver §6
de este documento.

### 3.12 Tamaño del efecto: *d_z* y el desplazamiento de Hodges–Lehmann

Un *p* pequeño dice «hay señal»; el tamaño del efecto dice «cuánta». Para datos
pareados, el tamaño del efecto estandarizado es

```
d_z = media de las diferencias / DE de las diferencias
```

Es un número sin unidades: 0,2 se considera pequeño, 0,5 mediano, 0,8 grande
(convenciones, no leyes). Aquí sirve además para leer la potencia: con 10 pares
solo se detectan efectos de ~1,0.

En la rama no paramétrica se informa en cambio el **desplazamiento de
Hodges–Lehmann**: la mediana de todos los promedios por pares de las diferencias.
Es «la diferencia típica» sin suponer normalidad.

### 3.13 *Bootstrap* y BCa

El *bootstrap* construye el intervalo de confianza por remuestreo: se toman
muchas muestras nuevas del propio conjunto de datos (con reemplazo), se recalcula
el estadístico en cada una y se mira la distribución de resultados. La variante
**BCa** (corregida por sesgo y aceleración) ajusta el intervalo cuando el
estadístico está sesgado o su variabilidad depende del valor.

En §3.9 el *bootstrap* se usa **solo** para los intervalos de los percentiles,
que son descriptivos. Para los contrastes confirmatorios se prefiere una
construcción exacta y consistente con la prueba (el desplazamiento de
Hodges–Lehmann y su intervalo, §3.12 de este documento). La razón es que con
diez pares un intervalo remuestreado y una prueba exacta son dos procedimientos
distintos y podrían señalar cosas opuestas; si el IC excluyera el cero y el *p*
exacto no, no habría criterio para decidir a cuál atenerse.

### 3.14 Comparaciones múltiples: FWER, Bonferroni, Holm, FDR

Si se hacen 42 pruebas al 5 %, la probabilidad de al menos un falso positivo no
es 5 %: con todas las hipótesis nulas ciertas sería
`1 − 0,95⁴² ≈ 88 %`. La *tasa de error por familia* (FWER) es la probabilidad de
cometer **al menos un** falso positivo dentro de un conjunto de pruebas.

- **Bonferroni:** exige `p < α/m` a todas. Controla la FWER, pero es muy
  conservador cuando hay muchas pruebas.
- **Holm:** ordena los *p* de menor a mayor y compara el *i*-ésimo con
  `α/(m − i + 1)`. Es decir, el más pequeño se compara con `α/m`, el segundo con
  `α/(m−1)`, y así. En cuanto uno no rechaza, todos los siguientes se declaran
  no significativos. Controla la
  misma FWER y siempre rechaza al menos tanto como Bonferroni.
- **FDR (Benjamini–Hochberg):** controla la *proporción* esperada de falsos
  positivos entre los rechazos. Sirve para cribar cientos de hipótesis y tolerar
  que algunas sean falsas; no es el criterio adecuado cuando cada rechazo se
  interpreta por separado.

*Ejemplo ficticio de Holm con una familia de nueve pruebas.* Los umbrales
sucesivos son 0,05/9 = 0,00556; 0,05/8 = 0,00625; 0,05/7 = 0,00714, …

| i | p ordenado | umbral α/(m−i+1) | ¿rechaza? |
| --- | --- | --- | --- |
| 1 | 0,0004 | 0,00556 | sí |
| 2 | 0,0019 | 0,00625 | sí |
| 3 | 0,0040 | 0,00714 | sí |
| 4 | 0,0060 | 0,00833 | sí |
| 5 | 0,0110 | 0,01000 | no → se detiene |

Los cuatro primeros se rechazan y los cinco restantes se declaran no
significativos, aunque alguno tuviera un *p* menor que 0,05. Eso es exactamente
lo que la corrección compra: la garantía de que, si nada fuera cierto, la
probabilidad de rechazar algo sería ≤ 5 %.

### 3.15 Potencia y efecto mínimo detectable

La *potencia* es la probabilidad de detectar un efecto de un tamaño dado cuando
existe. La convención es 80 %. El *efecto mínimo detectable* (MDE) es el tamaño
que, con esa potencia y ese α, apenas se distingue del ruido.

Con 10 pares y α = 0,05 bilateral:

```
MDE = (t crítico + t de potencia) / √n = (2,262 + 0,883) / 3,162 ≈ 1,0
```

Es decir: si el efecto real es de ~1 desviación estándar de las diferencias, hay
80 % de probabilidad de detectarlo. Con el umbral de Holm (0,0056) el MDE sube a
≈1,45. De ahí la frase de §3.9.8: «el diseño detecta efectos grandes y no
matices», y la regla de agregar bloques si el piloto muestra que la variabilidad
es alta.

### 3.16 Logaritmos y cocientes

La latencia no crece por suma sino por multiplicación: pasar de 40 a 44 ms es
+10 %; de 400 a 404 es +1 %. Comparar diferencias en milisegundos mezcla esas
escalas. El logaritmo las iguala, porque

```
ln(b) − ln(a) = ln(b/a)
```

Consecuencias prácticas, que §3.9 usa todo el tiempo:

- La diferencia de logaritmos **es** el logaritmo del cociente. Exponenciarla
  devuelve un porcentaje: `e^{0,096} − 1 = 10,1 %`.
- El intervalo de confianza de esa diferencia, exponenciado, es el intervalo del
  porcentaje.
- El promedio de diferencias de logaritmos equivale a comparar **medias
  geométricas**, que es lo natural para una métrica multiplicativa.
- Las colas derechas se vuelven más simétricas, lo que hace más razonable el
  supuesto de normalidad de la prueba *t* (sobre las diferencias).

---

## 4. Recorrido por §3.9, subsección por subsección

### 4.1 Cabecera: los seis pasos y las cuatro hipótesis

El listado inicial es el índice de cálculos: limpiar calentamiento, describir,
comparar latencias, comparar tasa y recursos, calcular diferencias porcentuales
(incluida `eq:overhead`), y examinar si el particionamiento produce una tendencia
consistente.

Después se enuncian **H1–H4** como *predicciones*, no como expectativas a
confirmar:

- **H1 (latencia):** ROS 2 será más lento de extremo a extremo que A.
- **H2 (tasa):** A alcanzará una tasa igual o mayor.
- **H3 (recursos):** ROS 2 consumirá más CPU y memoria.
- **H4 (particionamiento):** más fronteras → más sobrecosto → más latencia.

El texto agrega que un resultado que contradiga una hipótesis sigue siendo
válido. Esa frase parece retórica y no lo es: es lo que distingue una predicción
de una conclusión pre escrita.

### 4.2 §3.9.1 Unidad de análisis, diseño e interpretación

Responde tres preguntas y evita un error:

1. **¿Cuál es la réplica?** La corrida. (Ver §3.4 de este documento.)
2. **¿Cómo se comparan dos condiciones?** Sobre el par de corridas del mismo
   bloque: la diferencia dentro del bloque. (Ver §3.5 de este documento.)
3. **¿En qué escala?** En logaritmos, porque los contrastes son cocientes.
   (Ver §3.16 de este documento.)

Y el error que evita: **pseudorreplicación** al contar fotogramas.

Además declara dos límites de interpretación que conviene tener presentes:

- La diferencia de **tasa** entre A y ROS 2 no es sobrecosto de comunicación
  puro: las configuraciones de ROS 2 solapan fotogramas (mientras un nodo
  procesa el fotograma *n*, otro puede estar con el *n+1*), la monolítica
  procesa en estricta secuencia. La diferencia de tasa mezcla fronteras y
  paralelismo; se informa porque responde a la pregunta de despliegue, pero no se
  etiqueta como sobrecosto.
- La diferencia de **recursos** mezcla costo por fotograma y cantidad de
  fotogramas completados. Por eso se informa al lado el tiempo de CPU **por
  fotograma**, que separa ambos términos.

Y una decisión de medición importante: la latencia se toma **solo de la ventana
regulada**. En la ventana saturada, los fotogramas descartados no producen
muestra de latencia, de modo que lo que sobrevive está recortado por la tasa de
cada configuración, y el recorte favorece a las configuraciones más lentas justo
en la cola que se quiere comparar.

### 4.3 §3.9.2 Contrastes y pruebas preespecificadas

Es el corazón técnico de la sección. Define:

- los contrastes primarios: **nueve incrementos** (A→B, B→C, C→D por cada una de
  las tres resoluciones);
- el contraste de **tendencia** (un número por resolución que resume los cuatro
  niveles como pendiente);
- el contraste de **interacción** con la resolución (si el sobrecosto cambia al
  cambiar el tamaño del fotograma);
- la **regla de prueba**: Shapiro–Wilk sobre las diferencias → *t* pareada si no
  rechaza; Wilcoxon exacto si rechaza;
- qué NO se hace: Mann–Whitney, ANOVA/Kruskal–Wallis (suponen independencia entre
  condiciones) y modelo mixto con fotogramas anidados en corridas (la unidad ya
  es la corrida; el efecto aleatorio tendría diez niveles y no aportaría nada).
- Los contrastes A→C y A→D se informan como descriptivos: dos fronteras a la vez
  no separan el costo fijo de una frontera del costo de transportar el mensaje
  intermedio.

La lógica de fondo: **nueve incrementos dicen qué pasó en cada paso; la tendencia
dice si hay un patrón; la interacción dice si el patrón depende de la resolución.**
Las tres cosas son distintas y ninguna reemplaza a las otras.

### 4.4 §3.9.3 Estadísticos, magnitud del efecto e intervalos

Fija qué número representa a una corrida y qué se informa por contraste:

| Cantidad | Para qué |
| --- | --- |
| ρ (sobrecosto relativo) + IC 95 % | la magnitud principal, en porcentaje |
| diferencia absoluta en ms/µs | para que la magnitud no quede solo en % |
| *d_z* (rama paramétrica) | tamaño del efecto estandarizado |
| Hodges–Lehmann + IC (rama no paramétrica) | desplazamiento típico, sin supuestos |
| los diez valores por corrida | trazabilidad: el lector puede recalcular |

Y la regla de percentiles: P95 por corrida si hay al menos 100 fotogramas en la
ventana; P99 exige 1000, porque con menos el percentil queda determinado por un
puñado de valores y su variabilidad entre corridas no es estimable.

*Ejemplo de la regla, ficticio.* A 30 fps, 60 s dan 1800 fotogramas: P95 y P99 se
estiman por corrida. A 10 fps dan 600: P95 sí, P99 no, y P99 se informa solo
agrupado y descriptivo.

### 4.5 §3.9.4 Comparaciones múltiples

Cinco familias, Holm dentro de cada una, sin corrección entre familias. La
justificación es doble:

- **De contenido:** cada familia contrasta una hipótesis distinta sobre un
  resultado distinto, y el lector las interpreta por separado. Una corrección
  global respondería «¿es falsa alguna de las 42 afirmaciones?», que no es la
  pregunta del trabajo.
- **De cantidad:** con 42 pruebas el umbral más exigente sería 0,05/42 ≈ 0,0012,
  por debajo del piso de Wilcoxon (0,002): ningún contraste podría rechazar
  nunca. Una corrección que hace inalcanzable el rechazo no controla el error,
  deja la prueba sin capacidad de decidir.

El costo de esa decisión está declarado con su cifra: si todas las hipótesis
nulas fueran ciertas, la probabilidad de al menos un falso positivo en la
campaña es `1 − 0,95⁵ ≈ 0,23`. Es un intercambio consciente: 23 % de riesgo de
algún falso positivo, a cambio de que los contrastes que importan puedan
rechazar.

### 4.6 §3.9.5 Hipótesis, métricas y criterios de decisión

La regla de cuatro categorías:

| Etiqueta | Condición |
| --- | --- |
| sostenida | todas las pruebas de la hipótesis son significativas tras la corrección y con el signo predicho |
| parcialmente sostenida | los signos coinciden en todas, pero alguna no es significativa tras la corrección |
| contradicha | alguna prueba significativa tiene el signo contrario al predicho |
| no resuelta | el resto |

Siempre se publica el patrón completo, no solo la etiqueta.

Dos precisiones que valen oro en la defensa:

- **H2 no se convierte en equivalencia.** «A ≥ ROS 2» no se demuestra por
  ausencia de diferencia significativa. La conclusión se enuncia como «no se
  observó que ROS 2 fuera más rápido», con el intervalo diciendo cuánto más
  lento podría ser.
- **La etiqueta es más exigente en familias grandes.** H1 y H2 se deciden con
  nueve pruebas y H3 con dieciocho: «sostenida» pide en H3 el doble de rechazos
  consistentes. Es probable que H3 quede en «parcialmente sostenida» con signos
  enteramente favorables, y en ese caso lo que se interpreta es el patrón.

### 4.7 §3.9.6 Atípicos, faltantes y sensibilidad

- La única exclusión por regla es el **calentamiento**, que ya descarta el
  procedimiento. No se recortan fotogramas lentos: la cola es el objeto de P95 y
  P99.
- Una corrida no se excluye por el valor de sus métricas (excluir la corrida
  lenta sesga el resultado a favor de la condición que produce menos sorpresas).
  Se **marca**: fuera de `[Q1 − 3·IQR, Q3 + 3·IQR]` respecto de las diez corridas
  de su condición. El análisis primario la **incluye**; además se repite sin ella
  y sin su bloque, como sensibilidad predeclarada. Si la conclusión cambia, se
  informan las dos versiones y se dice cuál cambió.
- Faltantes: **bloques completos**. Un contraste se estima solo con los bloques
  en que ambas condiciones tienen corrida válida; no se imputa nada y se informa
  cuántos bloques entraron.

*Ejemplo de la regla de atípicos, ficticio.* Diez latencias medias de una
condición: Q1 = 40,25 ms, Q3 = 42,13 ms, IQR = 1,88 ms. Cercas:
40,25 − 3·1,88 = 34,63 ms y 42,13 + 3·1,88 = 47,75 ms. Una corrida con 49 ms se
marca (y se incluye igual en el análisis primario).

### 4.8 §3.9.7 Confirmatorio y exploratorio

**Confirmatorio (42 pruebas):** 9 de latencia (F1), 9 de tasa (F2), 18 de
recursos (F3), 3 de tendencia (F4), 3 de interacción (F5). Se informan como
respuesta a las hipótesis, con la corrección que corresponda.

**Exploratorio (todo lo demás):** P99 agrupado, mediana de la latencia, latencia
sin la adquisición, latencia de la ventana saturada, CPU por fotograma, CPU del
sistema completo, GPU, potencia, energía por fotograma, fotogramas por vatio,
temperatura, descartes por frontera, fotogramas en vuelo, contrastes A→C y A→D,
efecto de la posición dentro del bloque y la verificación de QoS del piloto. Se
informan con su intervalo y **sin *p* ajustado**.

La lista no prohíbe mirar otros datos: declara que, si se informan, se informan
con esa etiqueta. La versión del plan que se aplica es la del commit registrado en
la hoja de ejecución de cada corrida.

### 4.9 §3.9.8 Potencia y número de bloques

Con diez bloques: MDE ≈ 1,0 desviación estándar de las diferencias (α = 0,05);
≈ 1,45 con el umbral de Holm. La regla con el piloto: se calcula cuántos bloques
harían falta para 80 % de potencia frente al efecto observado en el incremento
A→B en la resolución mayor —el contraste que combina una frontera con el mensaje
más grande—; si excede diez, se agregan bloques completos. Nunca se baja de diez,
nunca se repiten corridas para mejorar un resultado, y el número final queda en el
manifiesto antes de empezar.

### 4.10 §3.9.9 Especificación para la implementación

Seis pasos para el script, con dos propiedades: no vuelve a decidir la validez de
una corrida (la lee tal como la dejó el procedimiento) y es determinista (semilla,
orden de filas, formato de cifras). Si un contraste no alcanza el mínimo de
bloques o de diferencias no nulas, emite «no estimable» en lugar de un *p*.

---

## 5. Las ecuaciones, una por una

### 5.1 `eq:overhead` — el sobrecosto relativo

```
sobrecosto (%) = (L_ROS − L_mono) / L_mono × 100
```

Es la diferencia porcentual clásica, aplicada a la latencia media de cada
condición. Si A tarda 40,0 ms y B tarda 44,0 ms, el sobrecosto es
(44 − 40)/40 = 10 %.

Para qué sirve: es la cifra que se comunica («cuesta 10 % más»). Su limitación:
es una razón de **medias aritméticas**, que con diez corridas ruidosas puede
diferir de la razón de medias geométricas. §3.9 informa las dos y declara la
diferencia cuando es visible.

### 5.2 `eq:contrast` — la diferencia entre dos configuraciones

```
d_b    = ln Y_B,b − ln Y_A,b          (una diferencia por bloque)
θ      = E[d_b]                        (su promedio poblacional)
R      = e^θ                           (razón entre las dos condiciones)
ρ      = R − 1                         (el sobrecosto, como proporción)
```

Lectura: en cada bloque, se calcula el cociente de la métrica entre las dos
condiciones y se toma su logaritmo. El promedio de esos diez logaritmos,
exponenciado, es la **razón entre las medias geométricas**. Si R = 1,10, la
condición de llegada es 10 % más lenta (o más rápida, si R < 1); ρ = 0,10 es el
mismo número como proporción.

*Ejemplo ficticio completo, con las diez diferencias ya calculadas:*

```
d (log) = 0,02  0,15  −0,03  0,22  0,08  0,19  0,05  0,13  0,11  0,04
media   = 0,0960        DE = 0,0786        error estándar = 0,0249
t       = 0,0960 / 0,0249 = 3,86        (crítico con 9 gl: 2,262)  → significativo
p       ≈ 0,004
d_z     = 0,0960 / 0,0786 = 1,22
R       = e^{0,0960} = 1,101            → ρ = 10,1 %
IC 95 % = 0,0960 ∓ 2,262 × 0,0249 = [0,0398; 0,1522]
        → tras exponenciar: razón [1,041; 1,164] → de 4,1 % a 16,4 % más lenta
```

Cómo se lee el resultado completo: «la diferencia típica es de 10 %, el
intervalo compatible con los datos va de 4 % a 16 %, y la evidencia es
suficiente para descartar que la diferencia sea nula».

Nótese lo que hace el intervalo: con la misma media y el doble de dispersión entre
corridas, el IC iría de −2 % a +23 % y la conclusión pasaría a ser «no se sabe»,
aunque la media fuera exactamente la misma. La información no está en la media
sino en su comparación con el ruido.

### 5.3 `eq:trend` — la tendencia del particionamiento

El problema: hay cuatro niveles con 0, 1, 3 y 6 fronteras, y se quiere **un solo
número** que diga cuánto cuesta cada frontera.

La idea es la de una recta de mínimos cuadrados: si se dibuja `ln Y` en el eje
vertical y el número de fronteras en el horizontal, la pendiente de la recta que
mejor pasa por los cuatro puntos es el efecto por frontera. Y esa pendiente se
puede escribir como una suma ponderada de los cuatro valores:

```
T_b = (1/42) · Σ c_k ln Y_k,b ,        c = (−5, −3, 1, 7)
```

¿De dónde salen esos coeficientes? De los niveles, no de una elección libre:

| Configuración | Fronteras n | n − n̄ | c = 2(n − n̄) |
| --- | --- | --- | --- |
| A | 0 | −2,5 | −5 |
| B | 1 | −1,5 | −3 |
| C | 3 | +0,5 | +1 |
| D | 6 | +3,5 | +7 |

- La media de los niveles es n̄ = 2,5.
- Los coeficientes son proporcionales a la distancia de cada nivel a esa media.
  Un nivel con muchas fronteras pesa a favor de la tendencia (positivo); uno con
  pocas, en contra (negativo). Y no es casual que los incrementos sucesivos de
  `c` sean 2, 4, 6: son el doble de las fronteras que agrega cada paso (+1, +2,
  +3).
- El divisor 42 = ½(25 + 9 + 1 + 49) = ½·84 es el que convierte la suma en una
  pendiente, es decir, en «log-efecto por frontera». Cualquier múltiplo de los
  coeficientes da el mismo resultado si se ajusta el divisor; lo importante es
  que `T` quede en unidades de **una** frontera.

*Verificación ficticia.* Latencias 40, 44, 52 y 62 ms:

```
ln Y = 3,6889  3,7842  3,9512  4,1271
T    = (−5·3,6889 − 3·3,7842 + 1·3,9512 + 7·4,1271) / 42 = 0,0725
e^T  = 1,075   →  +7,5 % por frontera
```

Y tiene sentido, porque los porcentajes por paso son 10,0 % (A→B), 8,7 % por
frontera en B→C (el 18,2 % del paso, repartido entre dos) y 6,0 % por frontera en
C→D (el 19,2 % del paso, repartido entre tres): el resumen de +7,5 % cae entre
esos extremos. El contraste de tendencia **promedia** esos tres pasos; no los
reemplaza.

Dos advertencias que la tesis ya incorpora:

1. **La tendencia supone linealidad.** Si el costo por frontera no es constante
   —y el diseño espera que no lo sea, porque C→D agrega fronteras que mueven
   decenas de KB y B→C una imagen grande—, `e^T` es un resumen y no una
   descripción exacta. La desviación se ve en los nueve incrementos, que se
   informan al lado.
2. **La versión anterior de esta ecuación estaba mal en dos cosas** (se corrigió
   el 2026-10-20): usaba coeficientes equiespaciados `(−3,−1,1,3)` —válidos para
   niveles 0, 1, 2, 3, no para 0, 1, 3, 6— y dividía por 3, lo que devolvía un
   factor 6,67 veces mayor. Con el ejemplo de arriba, la fórmula antigua habría
   dado `e^T = 1,64` (64 % por frontera) en lugar de 1,075.

### 5.4 `eq:interaction` — ¿el sobrecosto depende del tamaño del fotograma?

```
I_b = Σ w_l · d_{k→k',b} ,     w = (−1, 0, 1)
```

`d` es la diferencia de logaritmos de un mismo incremento (por ejemplo A→B) en
cada una de las tres resoluciones, ordenadas de menor a mayor área. Con
`w = (−1, 0, 1)`:

```
I = (log-razón en la resolución grande) − (log-razón en la resolución chica)
```

es decir, cuánto **cambia** la razón entre configuraciones al pasar de la
resolución menor a la mayor. Y como entre ambas hay dos pasos de un factor cuatro
en el área, `I/2` es el cambio por cuadruplicación, de modo que `e^{I/2}` es el
factor en que se multiplica la razón por cada cuadruplicación del fotograma.

*Ejemplo ficticio.* Razones A→B de 1,05, 1,08 y 1,14 para las tres resoluciones:

```
I = ln(1,14) − ln(1,05) = 0,0822
e^{I/2} = 1,042   →  por cada cuadruplicación del área, el sobrecosto se
                     multiplica por 1,04 (es decir, crece ~4 %)
```

Si `e^{I/2}` fuera 1,00, el sobrecosto sería el mismo en las tres resoluciones y
la interacción no aportaría nada. Su ausencia de dirección predicha es deliberada:
el trabajo no afirma de antemano si el sobrecosto crece con el tamaño del
fotograma, solo lo mide.

---

## 6. Los números que hay que saber de memoria

| Número | Qué es |
| --- | --- |
| 12 / 120 | condiciones / corridas |
| 10 | pares (bloques) por contraste; grados de libertad = 9 |
| 42 | pruebas confirmatorias: 9 + 9 + 18 + 3 + 3 |
| 0,05/9 = 0,0056 | umbral de Holm más exigente en las familias de nueve pruebas (F1, F2); en F4 y F5, de tres pruebas, es 0,0167 |
| 0,05/18 = 0,0028 | umbral de Holm más exigente en F3 |
| 0,05/42 ≈ 0,0012 | umbral hipotético con corrección global — **por debajo del piso**, por eso se descarta |
| 0,002 | piso de Wilcoxon con 10 pares (2/2¹⁰) |
| 0,0039 | el siguiente *p* alcanzable (4/2¹⁰) |
| 2,262 | *t* crítico bilateral con 9 gl y α = 0,05 |
| ≈ 1,0 / ≈ 1,45 | efecto mínimo detectable (α = 0,05 / α = 0,0056), en DE de las diferencias |
| 1 − 0,95⁵ ≈ 0,23 | error global declarado al no corregir entre familias |
| 0, 1, 3, 6 | fronteras de A, B, C, D |
| (−5, −3, 1, 7) / 42 | coeficientes y divisor del contraste de tendencia |
| (−1, 0, 1), `e^{I/2}` | contraste de interacción y su lectura |

Regla de alcanzabilidad, que es la que amarra todo: **con n diferencias no nulas,
el menor *p* bilateral posible es 2/2ⁿ**. De ahí:

| n no nulas | p mínimo | ¿alcanza 0,0056 (familia de 9)? | ¿alcanza 0,0028 (familia de 18)? |
| --- | --- | --- | --- |
| 5 | 0,0625 | no | no |
| 6 | 0,031 | no | no |
| 8 | 0,0078 | no | no |
| 9 | 0,0039 | sí | no |
| 10 | 0,0020 | sí | sí (solo el desenlace extremo) |

Por eso la regla de §3.9.2 dice: por debajo de nueve diferencias no nulas (diez en
la familia de dieciocho) no se aplica prueba; y por eso en F3 la rama no
paramétrica solo rechaza si las diez diferencias tienen el mismo signo.

---

## 7. Un contraste de principio a fin

Flujo completo, con el ejemplo ficticio de §5.2 de este documento:

1. **Leer la tabla de corridas:** dos filas por bloque (A y B), con la latencia
   media de la ventana regulada de cada corrida. La validez ya está decidida.
2. **Descartar bloques incompletos.** Si el bloque 6 perdió la corrida de B, ese
   bloque no entra: quedan 9 pares y se informa.
3. **Calcular las diferencias** `d_b = ln Y_B − ln Y_A` (9 o 10 valores).
4. **Verificar el supuesto:** Shapiro–Wilk sobre las diferencias.
   - Si *p* > 0,10 → prueba *t* pareada bilateral; IC por *t* con 9 gl; informar
     *d_z*.
   - Si *p* ≤ 0,10 → Wilcoxon exacto; descartar diferencias nulas y contarlas;
     si quedan menos de nueve (diez en la familia de dieciocho), «no estimable»;
     si no, IC por inversión de la prueba e informar el desplazamiento de
     Hodges–Lehmann.
5. **Calcular la magnitud:** ρ = e^(media de d) − 1, el IC, la diferencia
   absoluta en ms y los diez valores.
6. **Corregir:** Holm dentro de F1 (nueve pruebas), con el *p* sin ajustar y el
   ajustado, y el tamaño de la familia.
7. **Clasificar la hipótesis** con la regla de cuatro categorías y publicar el
   patrón de los nueve contrastes.
8. **Registrar la trazabilidad:** qué corridas, qué estadística, qué versión del
   script.

---

## 8. Preguntas frecuentes

**¿Por qué no ANOVA de medidas repetidas?**
Sería una alternativa válida en abstracto, pero el plan se comprometió con
contrastes puntuales porque cada uno responde a una pregunta concreta (cada paso
del particionamiento) y porque con diez bloques un ANOVA factorial de 4 × 3
necesitaría supuestos de esfericidad que no se pueden verificar con ese tamaño.
Lo que sí se descarta explícitamente es el ANOVA de un factor y Kruskal–Wallis
entre condiciones: suponen observaciones independientes, que aquí no lo son.

**¿Por qué no Mann–Whitney?**
Porque compara grupos independientes. Aquí cada bloque da un par A/B; usar
Mann–Whitney descartaría el pareamiento y perdería la potencia que el diseño ya
pagó.

**¿Por qué no un modelo mixto con fotogramas anidados en corridas?**
Porque la unidad de análisis ya es la corrida. Agregar fotogramas como nivel
añadiría un supuesto distribucional y un efecto aleatorio de diez niveles, sin
grados de libertad que la agregación por corrida no dé.

**¿Por qué logaritmos y no diferencias en ms?**
Porque el efecto es multiplicativo (§3.16 de este documento): un 10 % de 40 ms
no es lo mismo que
un 10 % de 400 ms. En logaritmos, el cociente se vuelve diferencia y el IC se lee
en porcentaje.

**¿Por qué la media y no la mediana?**
Porque la ecuación del sobrecosto está escrita con medias, y porque la media usa
toda la información. La mediana se informa y el análisis se repite sobre ella como
verificación exploratoria: si la conclusión cambia, hay que decirlo.

**¿Por qué cinco familias y no una sola corrección?**
Ver §4.5 de este documento: contenido (cada familia responde a una hipótesis
distinta) y cantidad
(una corrección global dejaría el umbral por debajo del piso de Wilcoxon). El
costo —23 % de error global— está declarado.

**«No significativo», ¿significa que no hay diferencia?**
No. Significa que la diferencia observada es compatible con el ruido. Para
afirmar equivalencia haría falta un margen fijado de antemano y una prueba de
equivalencia; el trabajo no los fija y por eso H2 se enuncia como «no se observó
que ROS 2 fuera más rápido», no como «son iguales».

**¿Por qué no se excluye la corrida atípica?**
Porque excluir la corrida lenta sesga el resultado a favor de la condición que
produce menos sorpresas. Se marca, se incluye en el análisis primario y se repite
el análisis sin ella como sensibilidad predeclarada.

**¿Por qué el efecto mínimo detectable importa si el efecto resultó grande?**
Porque el MDE fija qué se puede afirmar cuando el resultado es «no
significativo». Con MDE ≈ 1, un contraste no significativo es compatible con un
efecto nulo y también con un efecto real de ese tamaño que la muestra no alcanzó
a distinguir del ruido (eso ocurre en el 20 % de los casos, por definición de
potencia 80 %). Por eso un resultado no significativo nunca se informa como «sin
efecto»: se informa con su intervalo, que es el que acota cuánto podría ser.

**¿Qué pasa si el piloto muestra que la variabilidad es enorme?**
Se agregan bloques completos (regla de §3.9.8) y el número final queda registrado
antes de la campaña. Lo que no se hace es repetir corridas hasta que el resultado
convenga.

**¿Qué pasa si aparece una pregunta interesante que no estaba en el plan?**
Se contesta y se informa como exploratoria: con su intervalo, sin *p* ajustado y
sin reemplazar a la prueba preespecificada.

---

## 9. Cómo se verá la tabla de resultados

Plantilla de una fila (los números son el ejemplo ficticio de §5.2 de este
documento), para tener
claro qué significa cada columna cuando la campaña exista:

| Contraste | Res. | n pares | Estadístico | ρ | IC 95 % de ρ | *p* | *p* Holm | Efecto | Prueba |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A→B | 1280×720 | 10 | 41,16 → 45,32 ms | +10,1 % | +4,1 % a +16,4 % | 0,004 | 0,034 | *d_z* = 1,22 | *t* pareada |

Lo que se lee, en orden: qué se comparó, con cuántos pares, en qué unidades, la
magnitud principal con su incertidumbre, la evidencia, y el tamaño del efecto. El
*p* sin ajustar y el ajustado se informan juntos para que la corrección sea
auditable; los diez valores por corrida van en el anexo de trazabilidad.

---

## 10. Glosario de símbolos

| Símbolo | Significado |
| --- | --- |
| `Y_k,b` | valor de la métrica en la corrida de la configuración *k*, bloque *b* |
| `k ∈ {A, B, C, D}` | configuración arquitectónica |
| `r` | resolución (tres niveles) |
| `n_k` | número de fronteras de la configuración *k* (0, 1, 3, 6) |
| `d_b` | diferencia de logaritmos entre dos configuraciones en el bloque *b* |
| `θ`, `R`, `ρ` | media poblacional de `d`, razón `e^θ`, y sobrecosto `R − 1` |
| `T`, `c` | contraste de tendencia y sus coeficientes (−5, −3, 1, 7) |
| `I`, `w` | contraste de interacción y sus pesos (−1, 0, 1) |
| `s_d` | desviación estándar de las diferencias |
| `d_z` | tamaño del efecto pareado: media de diferencias / `s_d` |
| `α` | nivel de significancia (0,05) |
| `m` | tamaño de la familia de pruebas |
| FWER | tasa de error por familia (probabilidad de ≥ 1 falso positivo) |
| MDE | efecto mínimo detectable con 80 % de potencia |
| `f₀` | tasa fija de la fuente en la ventana regulada |
| `k` (en §3.7 de la tesis) | divisor de la tasa de la fuente — no confundir con `k` de configuración |

---

## 11. Autoevaluación

1. ¿Por qué la réplica es la corrida y no el fotograma? ¿Qué error concreto se
   comete si se usan los fotogramas?
2. ¿Qué gana el diseño pareado frente a comparar medias de grupo?
3. ¿Qué supuesto exige la prueba *t* pareada, y sobre qué datos se verifica?
4. ¿Por qué se usa el logaritmo de la métrica y no la métrica?
5. Con diez pares, ¿cuál es el menor *p* que puede dar la prueba de Wilcoxon? ¿Por
   qué importa esa cifra para elegir la corrección?
6. ¿Por qué las configuraciones no admiten coeficientes equiespaciados en el
   contraste de tendencia? ¿De dónde salen (−5, −3, 1, 7) y el 42?
7. ¿Qué significa exactamente `e^{I/2}` y por qué se divide por 2?
8. ¿Qué se informa además del *p*, y por qué?
9. ¿Qué se hace con una corrida atípica y qué no se hace?
10. ¿Por qué «no significativo» no autoriza a decir «son equivalentes»?

<details>
<summary>Respuestas breves</summary>

1. Porque los fotogramas de una corrida comparten temperatura, memoria y estado;
   contarlos como réplicas estrecha los intervalos sin información nueva
   (pseudorreplicación).
2. Elimina la variación compartida por las dos mediciones del bloque (temperatura,
   sesión del equipo) y por lo tanto reduce el ruido de la diferencia.
3. Que las **diferencias** sean aproximadamente normales; se verifica con
   Shapiro–Wilk sobre las diez diferencias, con nivel 0,10.
4. Porque el efecto es multiplicativo: `ln(b) − ln(a) = ln(b/a)`. Así el cociente
   se vuelve diferencia, el IC se exponencia y se lee en porcentaje, y las colas
   se simetrizan.
5. `2/2¹⁰ ≈ 0,002`. Importa porque un umbral corregido por debajo de ese valor
   haría que la prueba no pudiera rechazar nunca (0,05/42 ≈ 0,0012).
6. Porque tienen 0, 1, 3 y 6 fronteras: los niveles no están equiespaciados. Los
   coeficientes son proporcionales a la distancia de cada nivel a la media (2,5),
   y 42 = ½Σc² es el divisor que los convierte en pendiente por frontera.
7. Es el factor en que se multiplica la razón entre configuraciones por cada
   cuadruplicación del área del fotograma; se divide por 2 porque entre la
   resolución menor y la mayor hay dos pasos de un factor cuatro.
8. La magnitud (ρ con su IC), la diferencia absoluta, el tamaño del efecto y los
   diez valores por corrida: el *p* dice si hay señal, no cuánta.
9. Se marca con la regla de las cercas `Q1 − 3·IQR` / `Q3 + 3·IQR`; se incluye en
   el análisis primario; se repite el análisis sin ella y sin su bloque como
   sensibilidad predeclarada. No se excluye por su valor.
10. Porque la ausencia de evidencia no es evidencia de ausencia: haría falta un
    margen de equivalencia fijado de antemano y una prueba de equivalencia.

</details>

---

## 12. Para profundizar

- Demšar (2006), *Statistical comparisons of classifiers over multiple data
  sets*: por qué pruebas no paramétricas pareadas con corrección por
  multiplicidad en comparaciones de algoritmos.
- Hoefler y Belli (2015) y Georges, Buytaert y Eeckhout (2007): por qué una
  medición de rendimiento se informa con repeticiones e intervalos.
- Holm (1979): el procedimiento de corrección y su dominancia sobre Bonferroni.
- Lakens (2013): tamaño del efecto en diseños pareados (*d_z*).
- Wasserstein y Lazar (2016): qué no dice el valor *p*.
- Efron y Tibshirani (1994): *bootstrap* y BCa.

Todas están en `referencias.bib` y en la biblioteca de Zotero del proyecto.
