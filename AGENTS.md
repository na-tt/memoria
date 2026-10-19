# Thesis Agent Instructions

This repository contains an academic undergraduate thesis project.

## Guiding documents

Before making substantive suggestions or changes, consult the files in the 'docs/' directory:

- `scope.md` — authoritative definition of the thesis scope and explicit exclusions.
- `plan.md` — authoritative current plan and detailed thesis structure.
- `future.md` — deliberately out-of-scope research directions and rationale for
  postponing them.
- `spanish.md` — thin pointer to the authoritative guide on Spanish academic
  writing, terminology, and translation, maintained as the `academic-spanish`
  skill (`.agents/skills/academic-spanish/SKILL.md`).

These documents are the primary source of truth for project direction.

### Working documents

The same directory also holds internal working material that is **not** part of
the thesis PDF and must never be included in the build:

- `docs/pendientes.md` — task backlog. Each entry is a self-contained unit of
  work (current state, open decisions, constraints, deliverable, acceptance
  criteria). Read the relevant entry, not the whole file.
- `docs/fuentes-video.md` — internal note on the candidate video sources for
  the workload of the detection chain.
- `docs/reporte-comm-ros2.md` — internal report on how a message travels between
  two ROS 2 nodes; backs figure `fig:ros2-ruta-mensaje`.

## Scope discipline

Do not expand the thesis scope merely because a potentially interesting
research direction is discovered.

If an idea appears useful but falls outside the current scope:

1. Identify it as out of scope.
2. Check `future.md` before suggesting it as new work.
3. Do not incorporate it into the thesis plan unless explicitly requested.

## Planning discipline

Treat `plan.md` as the current intended execution plan.

You may identify problems, inconsistencies, missing steps, or opportunities
to improve the plan, but distinguish these from the existing plan rather than
silently changing it.

## Academic research

Do not invent sources, citations, experimental results, or claims.

When discussing literature, distinguish between:

- what a source explicitly says,
- what can reasonably be inferred from it,
- and the agent's own suggestion or interpretation.

When a claim depends on literature, use the project's source library
(Zotero) to verify it whenever possible.

## Writing

Help develop the thesis according to the structure in `plan.md`.

Do not restructure chapters or sections merely for stylistic reasons.
Propose structural changes separately before applying them.

## Experiments

Never invent experimental results.

Clearly distinguish:

- planned experiments,
- completed experiments,
- observed results,
- expected results,
- hypotheses,
- and interpretations.

## Git

Do not discard or overwrite the user's work without explicit instruction.
Prefer small, understandable changes.

## LaTeX build

The thesis is a XeLaTeX document whose entry point is `main.tex`. Do not
hand-roll `xelatex`/`pdflatex` invocations; use the `justfile` recipes, which
encode the intended workflow:

- `just` / `just build` — build the PDF (`latexmk -xelatex main.tex`).
- `just clean` — remove intermediate files, keep `main.pdf` (`latexmk -c`).
- `just nuke` — remove all generated files including the PDF (`latexmk -C`).
- `just view` — build, then open `main.pdf`.

Implementation notes:

- Engine is **XeLaTeX** (fontspec/polyglossia), driven by `latexmk`.
- `.latexmkrc` registers a custom dependency so `makeglossaries` runs to build
  the glossary (the `glossaries` package: `glosario.tex` + `\printglossaries`).
- Bibliography uses `biblatex` with the **biber** backend (`\printbibliography`,
  `referencias.bib`); `\nocite{*}` pulls in all entries.
- VS Code + LaTeX Workshop is the editor workflow; the default recipe is
  `latexmk (xelatex)` (`.vscode/settings.json`), which also hides build
  artifacts from the explorer.

Build hygiene:

- All build artifacts (`*.aux`, `*.bbl`, `*.log`, `*.xdv`, `*.pdf`, …) are
  gitignored — never commit them, and do not edit generated files
  (`main.aux`, `main.bbl`, `main.gls`, `main.ist`, …) by hand.
- A full build is slow. Avoid repeated recompiles; prefer a single `just build`
  and reserve `just nuke && just build` for when the build state looks
  corrupted or a clean rebuild is genuinely needed.
- The built sources are `main.tex` and `sections/*.tex`. `sections/body/` holds
  older drafts that are **not** included in the build — check the `\include`
  list in `main.tex` before assuming a file is part of the document.

<!-- BEGIN zotero-cli skill (managed by `zotero-mcp install-skill`) -->

## Zotero library access

Read and write a Zotero library from the shell with the `zotero-cli` command - search papers by keyword or meaning, read PDF full text and page ranges, get and set metadata, manage collections, tags, notes and annotations, add items by DOI/URL/ISBN, and export bibliographies. Use whenever the user asks about their Zotero library, references, citations, papers they have saved, or their reading notes.

Read `.agents/skills/zotero-cli/SKILL.md` before using it. Prefer it over the Zotero MCP server when you have shell access: the MCP tool schemas cost ~13k tokens of context on every request, this costs only what you run.

Quick check that it is set up: `zotero-cli config`. Pass `--json` whenever you will parse the output.

<!-- END zotero-cli skill -->

## Diagrams

Tool mechanics live in the skills (general, reusable):

- `.agents/skills/graphviz/SKILL.md` — Graphviz / `dot`, with references and a
  `render.sh`.
- `.agents/skills/d2/SKILL.md` — D2, with references and a `render.sh`.

The **project policy** and **style contract** below override the skills'
defaults. They are the source of truth for *which* tool to use and *how* the
figures must look.

### Choosing the tool

Pick by the constraints of the figure, not by habit. If the user names a tool,
use that tool.

- **Graphviz (`dot`)** — default when the figure needs geometry you can verify:
  rows/columns that must line up, arrows that must be collinear, a secondary
  edge that must not disturb the layout (`constraint=false`), mirrored rows, or
  two groups of equal size. Its layout is deterministic and `dot -Tplain`
  reports coordinates, so alignment is checked, not guessed.
- **D2** — default for architecture/stack/container diagrams where a clean
  automatic layout is enough and pixel alignment is not required. Better
  out-of-the-box styling (themes, sketch mode) with less boilerplate.
- **Mermaid** — only for READMEs and quick docs, never for thesis figures.

Signals to switch:

- If you start pinning absolute coordinates or fighting the engine's layout in
  D2 (`top`/`left`, repeated re-renders to nudge a box), move to Graphviz.
- If a simple flow diagram has no alignment requirement and you are hand-tuning
  ranks/constraints, D2 is usually faster.

Mixing tools across figures is fine; the style contract keeps them consistent.
Use `.dot` for Graphviz sources and `.d2` for D2 sources.

### Style contract

All figures share one visual language. Encode it once per file (D2 classes,
Graphviz `node`/`edge` defaults); do not restyle per figure. The palette is
semantic: choose the fill by the *role* of the element, not by taste.

| Role | Fill | Stroke | Meaning |
| --- | --- | --- | --- |
| Application / stage | `#e8eef7` | `#2f4b7c` | code the node runs |
| Middleware / DDS | `#cfdcef` | `#2f4b7c` | rmw/DDS-owned objects (buffers, writers/readers) |
| Process / frontier | `#f4f7fb` | `#2f4b7c` | grouping of stages; dashed border |
| Data edge | — | `#2f4b7c` | solid, width 2 |
| Control/notification edge | — | `#2f4b7c` | dashed, width 2, label `#676C7E` |

Geometry and typography:

- Rounded rectangles (`border-radius: 8` in D2, `style="rounded,filled"` in
  Graphviz).
- Node stroke width 2.
- Node labels bold, ~24 px (D2) / ~22 pt (Graphviz); container titles ~22 px.
- Edge labels italic, ~18–20 px, muted grey (`#676C7E`).
- Typeface: D2 keeps its built-in Source Sans Pro; Graphviz must name a
  concrete family, so it uses `DejaVu Sans` (Bold/Oblique). Both are bold
  humanist sans — the shared constants are weight and size, not the exact
  typeface.
- Solid arrow = data flow; dashed arrow = notification/availability (e.g. the
  DDS *notification delay*).
- White canvas; no shadows, no gradients, no 3D.
- Spanish labels (see `academic-spanish`); glossary terminology.

Canonical D2 preamble:

```d2
vars: { d2-config: { layout-engine: tala } }
classes: {
  etapa:   { shape: rectangle; style: { fill: "#e8eef7"; stroke: "#2f4b7c"; stroke-width: 2; border-radius: 8; font-size: 24; bold: true } }
  dds:     { shape: rectangle; style: { fill: "#cfdcef"; stroke: "#2f4b7c"; stroke-width: 2; border-radius: 8; font-size: 24; bold: true } }
  flujo:   { style: { stroke: "#2f4b7c"; stroke-width: 2; font-size: 18 } }
  aviso:   { style: { stroke: "#2f4b7c"; stroke-width: 2; stroke-dash: 4; font-size: 20 } }
  proceso: { style: { fill: "#f4f7fb"; stroke: "#2f4b7c"; stroke-width: 2; stroke-dash: 4; border-radius: 12; font-size: 22; bold: true } }
}
```

Canonical Graphviz preamble:

```dot
node [shape=box, style="rounded,filled", fillcolor="#e8eef7",
      color="#2f4b7c", penwidth=2, fontname="DejaVu Sans Bold",
      fontsize=22, margin="0.30,0.20"];
edge [color="#2f4b7c", penwidth=2, arrowsize=0.9];
// DDS nodes:            fillcolor="#cfdcef"
// clusters:             style="dashed,rounded,filled"; fillcolor="#f4f7fb";
//                        color="#2f4b7c"; penwidth=2; margin=66
// notification edge:    style=dashed; fontname="DejaVu Sans Oblique";
//                        fontcolor="#676C7E"
```

### Output and LaTeX

- One source per figure, next to its raster:
  `assets/figures/<name>.d2` or `assets/figures/<name>.dot` →
  `assets/figures/<name>.png`.
- PNG is the inclusion format for `\includegraphics` (XeLaTeX). SVG/PDF only
  when a specific need arises.
- Render with the skill script so flags (engine, dpi) are consistent; do not
  hand-roll `d2`/`dot` invocations.
- Inspect the PNG before calling a figure done.
- If two tools are being compared for one figure, render the alternate as
  `<name>-<tool>.png` and delete the losing source once decided — never keep
  two defaults that write the same `<name>.png`.
- Every figure needs `\caption` + `\label{fig:...}`; reference it via `\ref`.

### Rendering

```sh
.agents/skills/graphviz/scripts/render.sh assets/figures/<name>.dot   # → <name>.png
.agents/skills/d2/scripts/render.sh --format png assets/figures/<name>.d2
```

The Graphviz script defaults to PNG at 180 dpi. The D2 script defaults to SVG;
pass `--format png` for LaTeX inclusion.
