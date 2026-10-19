---
name: academic-spanish
description: Produce formal academic Spanish for the thesis (Latin American, specifically Chilean variant; undergraduate memoria de título). Use whenever generating or reviewing Spanish text, whether translating English source material into Spanish or writing Spanish directly from English sources — titles, abstracts, chapters, figure captions, and academic correspondence. Covers register, Chilean vs. Peninsular usage, when to keep English terms, and a domain glossary for ROS 2, computer vision, benchmarking, and embedded platforms.
---

# Academic Spanish (Latin America / Chile, formal register)

Produce **Latin American Spanish, specifically the Chilean academic variant** —
never Peninsular (Spain) Spanish. The output must read like formal academic
writing for an undergraduate thesis (*memoria de título*): precise, denotative,
impersonal, and terminologically consistent.

The guidance below is a single, uniform standard for all thesis Spanish, and
applies to every way Spanish text gets produced:

- **Translating** English source text (papers, notes, abstracts, figures) into
  Spanish — the most common case.
- **Writing Spanish directly**, from English sources or from your own analysis,
  with no explicit translation step in between. This is common: you may read
  English material, reason in English, and need to author the Spanish file as
  the final step.
- **Revising or copy-editing** existing Spanish for register, variant,
  terminology, and consistency.

Do not treat "translation" as the only trigger. Whenever Spanish is the output,
apply this document — the register, terminology policy, and glossary below hold
for all three modes.

## Register and style

- Prefer impersonal and passive-reflexive constructions: "se implementó",
  "se midió", "se observó que…". Use first-person plural ("implementamos")
  only if the institutional style guide calls for it — and then consistently.
- Never use *vosotros*; use *ustedes* or impersonal forms. No voseo, no
  colloquialisms, no contractions of the spoken register.
- Formal connectors: "sin embargo", "por lo tanto", "en consecuencia",
  "además", "por otra parte".
- One idea per sentence where possible; avoid long chained clauses. Keep the
  source's paragraph structure and emphasis — do not restructure content.
- Faithfulness first: never strengthen, weaken, or invent claims while
  translating. If the source is ambiguous or a sentence seems wrong, translate
  faithfully and **flag the issue** in a note rather than resolving it silently.
- Orthography per RAE (current norm): "guion", "fenómeno" (plural "fenómenos"),
  etc. Chilean standard: **video** without accent (never Spain's "vídeo").

### Chilean / Latin American preferences over Peninsular forms

| Do not use (Spain) | Use (Chile / LatAm) |
|---|---|
| ordenador | computador |
| vídeo | video |
| sistemas incrustados | sistemas embebidos |
| vosotros / os | ustedes / se (impersonal) |

### Numbers, units, and typographic conventions

- Decimal separator: **coma decimal** ("3,5 ms"). If the surrounding document
  already uses a different convention consistently, match it and note the
  discrepancy.
- Keep unit symbols and quantities intact: ms, FPS, %, W, GB. In LaTeX prefer
  `siunitx` (`\SI{3,5}{ms}`) when available.
- Italics for kept English terms: `\emph{middleware}` / `*middleware*`, on
  first mention; plain afterwards.
- Acronyms: keep the English acronym, and on first use give the Spanish
  expansion in parentheses — "QoS (calidad de servicio, *quality of
  service*)".

## Terminology policy: translate or keep English?

Decide in this order:

1. **Proper nouns and product names are never translated**: ROS 2, rclpy,
   Python, CUDA, TensorRT, GStreamer, OpenCV, NVIDIA Jetson Orin Nano, Linux.
2. **Keep the English term** (italicized on first use, optionally with a
   Spanish gloss in parentheses) when:
   - it is the established term of art in Spanish-language robotics/CS
     literature (e.g. *middleware*, *framework*, *callback*);
   - the available Spanish translations are awkward, contested, or ambiguous;
   - it names a concrete artifact of the implementation (e.g. *benchmark* as
     a test suite, *dataset* as a released corpus when citing its name).
3. **Translate** when a stable, standard Spanish term exists (latencia, nodo,
   mensaje, serialización, inferencia).
4. **Consistency is non-negotiable**: once the glossary fixes a choice, use it
   everywhere in the document — never alternate between the English term and
   its translation.

Grammar of kept anglicisms: masculine article ("el/los *middleware*",
"el *framework*"), pluralize with -s ("los *frameworks*"), do not invent
hybrids ("los softwares" → "el software" / "los sistemas de software").

## Glossary

Choices marked ★ are already established by the thesis's own Spanish title and
must not be changed. This glossary extends — never overrides — terminology
already fixed in the thesis documents; check them first when in doubt.

### Fixed translations

| English | Spanish | Notes |
|---|---|---|
| thesis | memoria de título / memoria / trabajo | choose by context: **memoria de título** on first mention and in front matter; **memoria** in running text; **trabajo** ("el presente trabajo", "este trabajo") to avoid repetition or when *thesis* is used generically. Avoid **tesis** as the default — in Chile it denotes graduate-level work |
| pipeline | cadena de procesamiento | ★ (thesis title). *pipeline* italic allowed only as a first-mention gloss |
| performance | rendimiento | ★ (thesis title); never "desempeño" in this thesis |
| video | video | ★ no accent |
| computer vision | visión por computador | standard in Chilean CS academia |
| node | nodo | |
| topic (ROS 2) | tópico | ROS Spanish usage; "tema" acceptable if institution requires |
| publisher / subscriber | publicador / suscriptor | |
| message | mensaje | |
| serialization / deserialization | serialización / deserialización | |
| inference | inferencia | |
| preprocessing / postprocessing | preprocesamiento / postprocesamiento | |
| object detection | detección de objetos | |
| deep learning | aprendizaje profundo | *deep learning* italic as gloss on first use |
| machine learning | aprendizaje automático | |
| model (ML) | modelo | |
| dataset | conjunto de datos | keep English name when citing a specific corpus |
| fine-tuning | ajuste fino | |
| latency | latencia | |
| end-to-end (latency) | de extremo a extremo (latencia) | |
| throughput | tasa de procesamiento | *throughput* italic as first-mention gloss |
| frame / FPS | fotograma / fotogramas por segundo | FPS kept as unit symbol |
| overhead | sobrecosto | never bare — always qualified by mechanism or resource; first-mention gloss "(en inglés, *overhead*)" |
| communication overhead | sobrecosto de comunicación | qualifier = mechanism |
| serialization overhead | sobrecosto de serialización | qualifier = mechanism |
| latency overhead | sobrecosto de latencia | qualifier = resource |
| performance overhead | sobrecosto en rendimiento | "en", not "de" (rendimiento is the measured dimension, not the resource spent); for the generic sense, the title's phrasing "impacto sobre el rendimiento" often reads best |
| overload (saturation) | sobrecarga | reserved exclusively for saturation; never for overhead |
| communication boundary | frontera de comunicación (entre nodos) | |
| trade-off | compromiso | "compromiso entre X y Y"; *trade-off* italic acceptable once |
| workload | carga de trabajo | |
| real time | tiempo real | |
| embedded platform / system | plataforma / sistema embebido | never "incrustado" |
| (development) board | placa (de desarrollo) | |
| power consumption | consumo de energía | |
| resource utilization | utilización de recursos | |
| single-process | de proceso único | "implementación de proceso único" |
| monolithic | monolítico | |
| partitioning (of the pipeline) | particionamiento (de la cadena) | |
| deployment | despliegue | |
| edge computing | computación en el borde | *edge computing* italic as first-mention gloss |
| speedup | aceleración | |
| jitter | fluctuación (de latencia) | *jitter* italic as gloss |
| outlier | valor atípico | |
| memory footprint | huella de memoria | |
| state of the art | estado del arte | |
| benchmarking | evaluación comparativa de rendimiento | *benchmarking* italic as first-mention gloss |
| benchmark (test artifact) | *benchmark* | keep English, masculine, italic on first use |
| bounding box | cuadro delimitador | |
| profiling | perfilado (de rendimiento) | |

### Kept in English

| Term | Treatment |
|---|---|
| middleware, framework, software, hardware, firmware | keep, masculine; no translation ("marco de trabajo" → avoid) |
| callback | keep; gloss once as "función de retrollamada" |
| executor | ejecutor (translate) — but keep `Executor` in code/API names |
| QoS | keep; first use: "QoS (calidad de servicio)" |
| zero-copy | keep, italic; gloss "copia cero" |
| ROS 2, rclpy, CUDA, TensorRT, GStreamer, OpenCV, Python, Jetson Orin Nano | proper nouns; never translate or inflect |

API and code identifiers (topic names, parameter names, class names like
`ImageSubscriber`) are never translated, even inside Spanish sentences.

## Procedure

1. **Before writing or translating**, check the thesis documents (`scope.md`,
   `plan.md`, chapters) for terminology already used in Spanish-facing text;
   the glossary's ★ entries come from there.
2. Write (or translate) with the register, variant, and glossary above. Do not
   translate inside LaTeX commands, labels, `\cite`/`\ref` keys, math, code
   listings, URLs, or file paths; keep TODO-style comments as-is unless asked.
3. When a recurring technical term is **not** in the glossary, apply the
   terminology policy, note the decision in your reply, and propose adding it
   to the glossary table in this file so future text stays consistent.
4. Deliver the Spanish text plus a short list of: English terms deliberately
   kept, any flagged ambiguities in the source, and proposed glossary
   additions. When the task was a translation, this includes the translation
   itself.
