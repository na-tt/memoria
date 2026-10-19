---
name: graphviz
description: "Create, edit, and render Graphviz diagrams with the `dot` layout engine (declarative text-to-diagram: flowcharts, architecture, box/arrow schematics, dependency graphs, state machines, trees, aligned rows/columns). Use when writing or reviewing .dot/.gv files, when a figure needs verifiable geometry (aligned rows and columns, collinear arrows, an edge that must not disturb the layout, mirrored or equal-sized groups), or when asked to produce or render a diagram with Graphviz/dot."
---

# Graphviz diagrams

Graphviz takes a declarative graph description (`.dot`, also written `.gv`) and
computes a layout with one of several engines — `dot` (hierarchical), `neato`,
`fdp`, `sfdp`, `twopi`, `circo`, `osage`, `patchwork` — rendering to PNG, SVG,
PDF, JSON, plain text, and more.

`dot` is the engine of interest for schematic figures: it is **hierarchical,
deterministic, and constraint-driven**. When a figure needs rows and columns to
line up, arrows to be collinear, or one edge to stay out of the layout's way,
Graphviz gives you editable, verifiable control instead of a black-box layout.

This skill is neutral and reusable. **Project conventions override it**: if the
repository's `AGENTS.md`, `justfile`, or docs specify diagram style, palette,
output format, or file locations, follow those instead of the defaults below.

## Version

Verified against **Graphviz 16.1.0** (`dot -V`). Re-verify attribute behavior
after a major upgrade: a few attributes interact subtly (see *Gotchas*), and
some are engine-specific.

## Core workflow

1. **Write** the `.dot` source (see `references/syntax.md`).
2. **Parse-check** (fast, no layout):
   ```sh
   dot -Tcanon file.dot > /dev/null    # exit status is what matters
   ```
3. **Render and inspect the image** — never trust the source alone. Layout
   problems (sprawl, crossings, a well-formed file that renders badly) are
   invisible in the source.
   ```sh
   dot -Tpng -Gdpi=180 file.dot -o /tmp/preview.png   # then view /tmp/preview.png
   ```
4. **Verify geometry when alignment matters.** `dot -Tplain` prints node
   coordinates in inches, so you can *check* that columns line up instead of
   eyeballing:
   ```sh
   dot -Tplain file.dot | awk '$1=="node"{print $2, $3}'
   ```
5. **Final export** in the project's required format.

Use `scripts/render.sh` (in this skill's directory) so the flags are consistent:

```sh
.agents/skills/graphviz/scripts/render.sh --preview file.dot    # PNG for inspection
.agents/skills/graphviz/scripts/render.sh --format svg file.dot out.svg
```

Never infer success from the output file existing — check the **exit status**.
Graphviz can emit a partial render and still fail.

## Defaults (neutral)

- **Engine**: `dot`, with `rankdir=TB`. Use `neato`/`sfdp` for force layouts,
  `circo` for circular, `osage`/`patchwork` for packed/treemap layouts.
- **Format**: `png` for raster inclusion (LaTeX), `svg` when vector matters,
  `pdf` for print.
- **dpi**: Graphviz's PNG default is 96; set it explicitly
  (`-Gdpi=150`–`200`) for figures. `dpi` scales the raster, not the layout.
- **Fonts**: the built-in default is `Times,serif` 14pt. Always override with a
  concrete family so output is reproducible (see *Gotchas*).
- Other flags and defaults: `references/cli.md`.

## The mechanisms that matter

These are the four things that make `dot` the right tool for schematic figures.
Full detail in `references/layout.md`.

- **`rank=same`** puts nodes on one row (with `rankdir=TB`). This is *the*
  alignment primitive. To span clusters it needs **`newrank=true`**.
- **`constraint=false`** removes an edge from rank assignment. This is how a
  *secondary* edge (a notification, a legend link, an annotation) is drawn
  without letting it deform the layout.
- **Flat edges** (same rank) order nodes left-to-right by their direction. Use
  **`dir=back`** to keep that order while reversing the arrowhead — this is how
  you mirror a row (arrows pointing the other way while columns stay put).
- **`group` + equal `fixedsize` widths** align columns across ranks. `group` is
  a soft hint that propagates along edges; equal widths make mirrored rows the
  same length, which also makes their clusters the same size.

## Style

Neutral defaults are deliberately minimal. For thesis/project figures, use the
repository's style contract (palette, typography, node/edge conventions). If
there is none, pick one palette and one font and encode it once as `node`/`edge`
defaults at the top of the file, then only override per element when a role
changes (e.g. a differently coloured layer).

## Gotchas (verified against 16.1.0)

- **Attribute lists are comma-separated** — `[a=b, c=d]` — and statements end
  with `;` or a newline. A missing comma silently produces one attribute whose
  value contains the rest.
- **Comments** are `//` (line) and `/* ... */` (block). A line starting with
  `#` is treated as a C preprocessor line marker and ignored; `#` mid-line is
  **not** a comment.
- **Quote any ID** containing whitespace or punctuation, and always quote
  labels with special characters.
- **Label line breaks**: `\n` (centered), `\l` (left-aligned), `\r`
  (right-aligned). Substitutions: `\N` node name, `\G` graph name, `\E` edge
  name, `\T` tail, `\H` head, `\L` object label. HTML-like labels use
  `<...>` (with `<BR/>`, `<B>`, `<FONT ...>`); they are only enabled when the
  label starts with `<`.
- **There is no "rounded rectangle" shape.** Use
  `shape=box, style="rounded,filled"`.
- **`splines=ortho` does not place edge labels** (it warns). Use `xlabel`
  instead of `label` for edges under `ortho`.
- **`rank=same` across clusters without `newrank=true`** emits
  `Warning: X was already in a rankset, deleted from cluster` and pulls the
  nodes out of their cluster. Set `newrank=true` at graph level.
- **Cluster size is computed, never set.** There is no "make these two clusters
  the same size"; make the rows equal width (equal `fixedsize` widths) and the
  clusters follow.
- **`-Tplain` uses Graphviz's coordinate system**: origin bottom-left, y grows
  *upward*, units are inches (72 per inch).
- **Fonts and Unicode**: use a concrete installed family name (e.g.
  `"DejaVu Sans Bold"`), not a generic alias, or output is not reproducible
  across machines. The family must contain the glyphs (`→`, accented letters).
  Graphviz has no italic/bold attribute — pick the family variant as the
  `fontname`.

## Where to look when unsure

Read in this order — cheapest first:

1. `man dot`, `dot -?` — CLI flags and usage for the installed version.
2. `dot -T?` — the valid output formats (listed in the error message).
3. This skill's reference files:
   - `references/syntax.md` — graph/digraph, nodes, edges, attributes,
     subgraphs/clusters, ports, labels, IDs, examples.
   - `references/layout.md` — the `dot` rank model, alignment, mirroring,
     non-layout edges, clusters, splines, cluster/edge routing.
   - `references/styles.md` — colours, shapes, node/edge/cluster/graph style
     attributes, arrows, fonts.
   - `references/cli.md` — flags, output formats, engines, `-G/-N/-E`,
     inspection formats (`plain`, `json`, `xdot`).
4. The official references: <https://graphviz.org/doc/info/attrs.html> (every
   attribute), <https://graphviz.org/doc/info/shapes.html> (shapes and
   arrowheads), <https://graphviz.org/doc/info/command.html> (CLI).
5. `dot -Tdot file.dot` or `dot -Tcanon file.dot` to see how defaults were
   resolved; `dot -Tjson` to read the laid-out geometry programmatically.

If the installed version and these notes disagree, the installed version wins —
update the reference file accordingly.
