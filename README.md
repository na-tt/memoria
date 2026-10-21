# Memoria ELO308

Repositorio de la memoria de título (ELO308). Contiene el documento en LaTeX,
las fuentes de las figuras y material de trabajo interno del proyecto.

El contenido de la tesis y su alcance están definidos en `docs/scope.md` y
`docs/plan.md`; este README describe únicamente el repositorio y cómo
compilarlo.

## Compilación

El documento se compila con **XeLaTeX** (necesario por `fontspec` y
`polyglossia`) y se orquesta con **latexmk**. La bibliografía usa `biblatex`
con backend **biber**, y el glosario se genera con `makeglossaries` (registrado
como dependencia personalizada en `.latexmkrc`).

```sh
latexmk -xelatex main.tex
```

No se invoca `xelatex` a mano: `latexmk` se encarga de las pasadas necesarias,
de ejecutar `biber` y de regenerar el glosario.

### Justfile

Para evitar recordar las invocaciones, el repositorio incluye un `justfile`
con las recetas habituales:

| Receta | Equivalente | Uso |
| --- | --- | --- |
| `just` / `just build` | `latexmk -xelatex main.tex` | compila el PDF |
| `just clean` | `latexmk -c` | borra intermedios, conserva `main.pdf` |
| `just nuke` | `latexmk -C` | borra todo lo generado, incluido el PDF |
| `just view` | `just build && xdg-open main.pdf` | compila y abre el PDF |

`just` es opcional: las recetas solo envuelven los comandos de `latexmk`, así
que se puede compilar igual sin tenerlo instalado.

Una compilación completa es lenta. Conviene compilar una vez y evitar
recompilaciones innecesarias; `just nuke && just build` queda reservado para
cuando el estado de la compilación esté corrupto (por ejemplo, después de
cambiar el glosario o la bibliografía de forma problemática).

### Requisitos

- Una distribución de TeX Live con `xelatex`, `latexmk`, `biber` y
  `makeglossaries`.
- Fuentes Latin Modern (incluidas en TeX Live).
- Opcional: [`just`](https://github.com/casey/just) para las recetas.

### Editor

El flujo de escritura usa VS Code con LaTeX Workshop. La receta por defecto es
`latexmk (xelatex)` y la compilación automática está desactivada; la
configuración vive en `.vscode/settings.json`, que también oculta los archivos
generados en el explorador.

## Estructura

```
main.tex              documento principal (\include de las secciones)
sections/             capítulos, portada, resumen, anexos
  body/               borradores antiguos, NO incluidos en la compilación
assets/figures/       fuentes de figuras (.dot, .d2) y PNG resultantes
docs/                 documentación interna del proyecto (no va en el PDF)
referencias.bib       bibliografía (biblatex + biber)
glosario.tex          entradas del glosario
fancy.tex             encabezados y pies de página
commands.tex          comandos personalizados (\todo, \figstub, ...)
.latexmkrc            dependencia personalizada para makeglossaries
justfile              recetas de compilación
```

Solo se compila lo que aparece en la lista de `\include` de `main.tex`. Antes
de suponer que un archivo forma parte del documento, conviene revisar esa
lista: en particular, `sections/body/` contiene borradores que no se incluyen.

Las figuras se generan desde su fuente (`assets/figures/<nombre>.dot` o `.d2`)
y se incluyen como PNG con `\includegraphics`, siempre con `\caption` y
`\label{fig:...}`.

`docs/` reúne material de trabajo (alcance, plan, pendientes, notas técnicas).
No forma parte del PDF y no debe incluirse en la compilación.

## Artefactos de compilación

Los archivos generados (`main.aux`, `main.bcf`, `main.bbl`, `main.log`,
`main.xdv`, `main.pdf`, etc.) están en `.gitignore`. No se commitean ni se
editan a mano: se regeneran con `just build`.
