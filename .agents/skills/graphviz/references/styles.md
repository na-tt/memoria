# Graphviz styles reference

Verified against Graphviz 16.1.0. Attributes are case-insensitive in name, but
keep the conventional spelling.

## Colours

Anywhere a colour is accepted:

- X11/CSS name: `red`, `steelblue`, `transparent`, `none`.
- Hex: `#rrggbb` (also `#rrggbbaa` where alpha is supported).
- **Colour lists**: `color="red:blue"` produces a gradient; `fillcolor` on a
  filled shape or cluster interpolates along the list. A `;` separates
  weight/colour stops (`"red;0.3:blue"`). Use `style=filled` for `fillcolor` to
  apply.

On a node: `color` is the **border**; `fillcolor` is the interior (needs
`style=filled`). On an edge: `color` is the line, `fontcolor` the label. On a
cluster: `color` is the border, `fillcolor` the background (needs
`style=filled`).

## Node shapes

`shape=<name>`; default `ellipse`.

| Group | Shapes |
| --- | --- |
| Basic | `box`, `rect`, `rectangle`, `square`, `ellipse`, `oval`, `circle`, `point`, `egg` |
| Polygons | `triangle`, `diamond`, `trapezium`, `parallelogram`, `house`, `pentagon`, `hexagon`, `septagon`, `octagon`, `doublecircle`, `doubleoctagon`, `tripleoctagon`, `invtriangle`, `invtrapezium`, `invhouse`, `Mdiamond`, `Msquare`, `Mcircle`, `star` |
| Text/media | `plaintext`, `plain`, `none`, `underline`, `note`, `tab`, `folder` |
| Data/infra | `cylinder`, `box3d`, `component`, `cds`, `promoter` |
| Biology | `assembly`, `signature`, `insulator`, `ribosite`, `rnastab`, `proteasesite`, `proteinstab`, `rpromoter`, `rarrow`, `larrow`, `lpromoter`, `terminator`, `utr`, `primersite`, `restrictionsite`, `fivepoverhang`, `threepoverhang`, `noverhang` |

- `square` and `circle` are 1:1: width and height are forced equal.
- There is **no** "rounded rectangle" shape. Use
  `shape=box, style="rounded,filled"`.
- `plaintext` draws only the label (no border/fill); `none` draws nothing at
  all (useful as a layout spacer, together with `style=invis`).

## Node styles

`style="a,b,c"` combines values:

| Style | Effect |
| --- | --- |
| `filled` | paint the interior with `fillcolor` |
| `rounded` | rounded corners (boxes and similar) |
| `dashed`, `dotted` | border pattern |
| `bold` | thicker border (or use `penwidth`) |
| `solid` | default |
| `invis` | do not draw the node (still laid out) |
| `diagonals` | diagonal lines inside the shape (specific shapes) |
| `tapered` | tapered edges (edges, specific shapes) |

`striped` / `wedged` are documented for some shapes but not supported by every
renderer/version (16.1.0 warns and ignores `striped`). Prefer explicit
`fillcolor`/`color`.

Useful node attributes:

| Attribute | Meaning |
| --- | --- |
| `label` | text (or HTML `<...>`) |
| `xlabel` | external label, outside the node geometry |
| `width`, `height` | minimum size in inches |
| `fixedsize` | `true` fixes the size to `width`/`height`, ignoring the label |
| `margin` | padding between label and border (`"0.3,0.2"` = x,y inches) |
| `penwidth` | border width |
| `fontname`, `fontsize`, `fontcolor` | text |
| `tooltip`, `URL`, `target` | SVG interactivity |
| `group` | alignment hint (see `references/layout.md`) |
| `rank` | same as `{rank=...}` for that node |
| `ordering` | order of incident edges |

## Edge styles and arrows

| Attribute | Meaning |
| --- | --- |
| `style` | `solid`, `dashed`, `dotted`, `bold`, `tapered`, `invis` |
| `penwidth` | line width |
| `color` | line colour |
| `arrowhead`, `arrowtail` | arrow shape |
| `dir` | `forward` (default), `back`, `both`, `none` |
| `arrowsize` | arrow scale |
| `label`, `xlabel`, `headlabel`, `taillabel` | text |
| `fontname`, `fontsize`, `fontcolor` | label text |
| `labeldistance`, `labelangle` | label placement |
| `weight` | layout hint: higher = straighter/shorter |
| `constraint` | `false` removes the edge from ranking (see `layout.md`) |
| `minlen`, `len` | minimum/desired rank span |
| `lhead`, `ltail` | attach to a cluster (needs `compound=true`) |

Arrow shapes: `normal`, `inv`, `dot`, `odot`, `invodot`, `none`, `tee`,
`empty`, `invempty`, `diamond`, `odiamond`, `ediamond`, `crow`, `box`, `obox`,
`open`, `halfopen`, `vee`.

`dir=back` keeps the edge's rank/ordering direction but draws the arrowhead at
the **tail** — the key to mirrored rows.

## Clusters

Cluster attributes (graph attributes inside `subgraph cluster_*`):

| Attribute | Meaning |
| --- | --- |
| `label` | title |
| `labeljust` | `l`, `c`, `r` |
| `labelloc` | `t`, `c`, `b` |
| `style` | `dashed`, `rounded`, `filled`, `bold`, `invis` |
| `color`, `fillcolor`, `penwidth` | border, background, width |
| `margin` | space between contents and border |
| `fontname`, `fontsize`, `fontcolor` | title text |

Combine border styles: `style="dashed,rounded,filled"`.

## Graph attributes

| Attribute | Meaning |
| --- | --- |
| `bgcolor` | canvas background |
| `pad` | drawing margin around the whole graph (inches or `"x,y"`) |
| `margin` | page margin (different from `pad`) |
| `dpi` | raster resolution (PNG) |
| `size` | maximum drawing size (inches) |
| `ratio` | aspect handling (`fill`, `compress`, `expand`, `auto`, numeric) |
| `rankdir`, `splines`, `nodesep`, `ranksep`, `newrank`, `compound` | layout (see `layout.md`) |
| `outputorder` | `breadthfirst` (default) or `nodesfirst`/`edgesfirst` for z-order |
| `fontname`, `fontsize`, `fontcolor` | default text |

## Fonts

Graphviz's built-in default is **`Times,serif` at 14pt**. Always set a concrete
family for reproducible figures:

```dot
node [fontname="DejaVu Sans Bold", fontsize=22];
```

- There is **no bold/italic attribute**: pick a family variant
  (`"DejaVu Sans Bold"`, `"DejaVu Sans Oblique"`) as the `fontname`.
- Use a concrete installed family, not a generic alias, or output differs
  across machines. List families with `fc-list` on Linux.
- The family must contain the glyphs used (`→`, accented Spanish letters,
  `×`, `≤`). A box instead of a glyph means the font lacks it — change
  `fontname`, not the text.
- `fontname` accepts an optional `:bold` / `:italic` suffix in some versions
  (`"DejaVu Sans:bold"`), but an explicit family name is more portable.

## Project style

If the repository defines a style contract (palette, typography, node/edge
conventions), use it and encode it once as `node`/`edge` defaults at the top of
the file. Otherwise fix one palette and one font per document and reuse them —
consistency across figures matters more than the specific values.
