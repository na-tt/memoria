---
name: d2
description: "Create, edit, and render D2 diagrams (declarative text-to-diagram: architecture, flowcharts, sequence diagrams, ERDs, UML classes, grids). Use when writing or reviewing .d2 files, or when asked to produce or render a diagram, figure, schematic, or architecture/flow chart."
---

# D2 diagrams

D2 is a declarative text-to-diagram language. You write `.d2` source; the `d2`
CLI compiles it to SVG, PNG, PDF, PPTX, GIF, or ASCII.

This skill is neutral and reusable. **Project conventions override it**: if the
repository's `AGENTS.md`, `.latexmkrc`, `justfile`, or docs specify diagram
style, output format, or file locations, follow those instead of the defaults
below.

## Version

The reference files in this skill are verified against **D2 v0.9.0**. Check the
installed version with `d2 --version`. If it differs, re-verify the shape and
style catalogs (a quick loop that compiles one probe per keyword is enough) —
this is called out because the upstream docs have already drifted.

## Core workflow

1. **Write** the `.d2` source (see `references/syntax.md`).
2. **Validate**: `d2 validate file.d2` (fast; catches syntax and vocabulary
   errors without rendering).
3. **Render** to the target format:
   ```sh
   d2 --layout tala --theme 0 input.d2 output.svg
   ```
   - Output format is inferred from the extension. No output → `input.svg`.
   - `-` as input reads stdin; `-` as output writes SVG (or set
     `--stdout-format`).
4. **Inspect the image, not just the source.** Compile a PNG preview and look
   at it, then iterate. Layout problems (sprawl, crossings, a good-looking
   script that renders badly) are invisible in the source.
   ```sh
   d2 --layout tala input.d2 /tmp/preview.png   # then view /tmp/preview.png
   ```
5. **Final export** in the project's required format.

Use `scripts/render.sh` (in this skill's directory) to avoid recalling flags:

```sh
.agents/skills/d2/scripts/render.sh --preview input.d2        # PNG for inspection
.agents/skills/d2/scripts/render.sh --format pdf input.d2 out.pdf
```

Never infer success from the presence of the output file: D2 writes a partial
render even on some errors. Use the **exit status**. This is stated in
`man d2`.

## Defaults (neutral)

- **Theme**: leave the default (theme `0`, Neutral Default) unless the project
  or user asks for one. List themes with `d2 themes`.
- **Layout engine**: prefer **TALA > ELK > Dagre**. Default to `--layout tala`,
  especially for nested containers/architecture diagrams; fall back to `elk`
  or `dagre` when TALA's output is poor. This is a starting preference, not a
  rule — engine choice is per-diagram.
- **Format**: SVG unless the project requires otherwise.
- Other flags and environment variables are documented in `references/cli.md`.

## Gotchas (verified against v0.9.0)

- **No dotted-connection operator.** `a ... b` is a syntax error. A dashed line
  is `a -> b {style.stroke-dash: 3}`.
- **Map entries are separated by newlines or `;`, never commas.**
  `{ layout-engine: tala, theme-id: 4 }` silently makes the value the single
  string `"tala, theme-id: 4"` and fails later with a confusing `D2_LAYOUT ...`
  error.
- **The compiler validates vocabulary and fails loudly** with line:column:
  `unknown shape "..."`, `invalid style keyword: "..."`, and type/range errors
  like `expected "3d" to be true or false`. Trust compile errors over your own
  recall; iterate.
- **Two upstream-doc discrepancies** (compiler is authoritative):
  `style.text-transform` accepts `none | uppercase | lowercase | capitalize`
  (the docs' `title` is wrong), and `style.fill-pattern` also accepts `paper`.
- **`shape: image` requires a valid `icon`** pointing at an existing file/URL.
- **Reserved keywords as keys must be quoted** (e.g. `"label": string`,
  `"width": width`).
- Non-ASCII punctuation that looks like syntax (`：` vs `:`) will not parse as
  syntax; use ASCII `: ; .` in non-English diagrams.

## Where to look when unsure

Read in this order — cheapest first:

1. `man d2` and `d2 --help` — authoritative for the installed version's CLI.
2. `d2 layout` and `d2 layout <engine>` — available engines and their flags.
3. `d2 themes` — theme IDs (light and dark).
4. This skill's reference files:
   - `references/syntax.md` — strings, nodes, containers, connections, vars,
     globs, classes, text, overrides.
   - `references/styles.md` — full style keyword catalog and shape catalog.
   - `references/advanced.md` — sequence diagrams, SQL tables, UML classes,
     composition (layers/scenarios/steps), imports, icons, tooltips/links.
   - `references/cli.md` — flags, env vars, export formats, layouts, fonts.
5. The upstream docs: <https://d2lang.com/tour/intro> and the source behind them
   at <https://github.com/d2lang/d2-docs> (markdown under `docs/tour/`; the
   `.d2` examples under `static/d2/` are runnable and often clearer than the
   rendered page).
6. Icons: <https://icons.d2lang.com>.

If the compiler and the docs disagree, the compiler wins; update the reference
file accordingly.
