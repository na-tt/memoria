# Graphviz CLI reference

Verified against Graphviz 16.1.0. The `dot` binary is one of several engine
front-ends; `man dot` is authoritative for the installed version.

## Synopsis

```text
dot [-Vv?] [-(GNEA)name=val] [-(KTlso)<val>] <dot files>
```

- Input is read from files or stdin (no file argument).
- Output goes to stdout unless `-o FILE` (or `-O`) is given.
- **Check the exit status**, not the presence of an output file: Graphviz can
  emit a partial render and still fail.

## Output format — `-T`

```sh
dot -Tpng   f.dot -o f.png
dot -Tsvg   f.dot -o f.svg
dot -Tpdf   f.dot -o f.pdf
dot -Tplain f.dot          # laid-out coordinates (see below)
```

Formats reported by 16.1.0 (the list from `dot -T?`):

```
canon cmap cmapx cmapx_np dot dot_json eps fig gd gd2 gif gv imap imap_np
ismap jpe jpeg jpg json json0 kitty kittyz pdf pic plain plain-ext png pov
ps ps2 svg svg_inline svgz tk vrml vt vt-24bit vt-4up vt-6up vt-8up vt-8up2
wbmp webp xdot xdot1.2 xdot1.4 xdot_json
```

Most useful:

| Format | Use |
| --- | --- |
| `png` | raster for documents; scale with `-Gdpi` |
| `svg` | lossless vector, web, interactive (`URL`, `tooltip`) |
| `pdf` | print / vector inclusion |
| `plain`, `plain-ext` | node/edge coordinates as text |
| `json`, `json0` | laid-out geometry as JSON |
| `xdot` / `dot` | Graphviz source with layout info (debugging) |
| `canon` | canonical source, no layout — fast parse check |
| `gv` | `dot` output |

`-T?` is not a valid format; the error message is what lists them.

## Engine — `-K`

```sh
dot -Kneato f.dot -Tpng -o f.png
```

Available engines (usually also installed as standalone binaries):

| Engine | Model | When |
| --- | --- | --- |
| `dot` | hierarchical / layered | flowcharts, schematics, DAGs, ranks |
| `neato` | spring / stress | undirected graphs, small networks |
| `fdp` | force-directed | clusters of undirected nodes |
| `sfdp` | multiscale force | large graphs |
| `twopi` | radial | trees/radial layouts |
| `circo` | circular | cyclic structures |
| `osage` | packed clusters | grouped packing |
| `patchwork` | treemap | hierarchical areas |

For schematic figures with rows/columns and aligned boxes, use **`dot`**. The
attributes in this skill (`rank`, `constraint`, `group`, `fixedsize`) are `dot`
concepts; other engines interpret or ignore some of them.

## Defaults — `-G`, `-N`, `-E`, `-A`

Set attributes from the command line:

```sh
dot -Gdpi=180 -Gbgcolor=white \
    -Nfontname="DejaVu Sans Bold" -Nfontsize=22 \
    -Ecolor="#2f4b7c" -Epenwidth=2 \
    -Tpng f.dot -o f.png
```

- `-Gname=val` graph attribute.
- `-Nname=val` default node attribute.
- `-Ename=val` default edge attribute.
- `-Aname=val` applies to graph, node and edge.
- CLI attributes behave like defaults and can be overridden in the file.

## Other flags

| Flag | Meaning |
| --- | --- |
| `-o FILE` | output file |
| `-O` | derive output name from input (`f.dot` → `f.dot.png`) |
| `-Gdpi=N` | raster resolution (PNG); 96 by default |
| `-sN` | scale input coordinates by N |
| `-y` | invert y coordinates (output space) |
| `-n` | no layout; just emit the graph |
| `-q` / `-ql` | quiet / less verbose |
| `-v` / `-vN` | verbose / set level |
| `-P` | print the plugin graph |
| `-V` | version |
| `-?` | usage |

`-Gsize`, `-Gratio`, `-Gpad` control page/drawing size from the command line.

## Inspecting the result

### `-Tplain`

Text coordinates in **inches**, origin bottom-left, y grows **up**. Format:

```text
graph <scale> <width> <height>
node <name> <x> <y> <width> <height> <label> <style> <shape> <color> <fillcolor>
edge <tail> <head> <n> <x1> <y1> ... <xn> <yn> [label] [style] [color]
stop
```

`<x> <y>` are node **centres**. Equal `x` = same column; equal `y` = same row.
This is the fastest way to prove that an alignment holds:

```sh
dot -Tplain f.dot | awk '$1=="node"{printf "%-12s x=%8.4f y=%8.4f\n",$2,$3,$4}'
```

`plain-ext` adds port names to edges.

### `-Tjson`

Machine-readable version of the same geometry, handy with `jq`:

```sh
dot -Tjson f.dot | jq -r '.objects[] | "\(.name)\t\(.pos)"'
```

### `-Tcanon`

Resolves defaults and normalises the source without computing a layout. Useful
both as a fast parse check and to see which attributes Graphviz actually
applied:

```sh
dot -Tcanon f.dot > /dev/null      # parse check; use the exit status
dot -Tcanon f.dot | grep -A2 'node \[' | head
```

## Recipes

```sh
# Parse check (no layout)
dot -Tcanon input.dot > /dev/null

# Preview to inspect layout
dot -Tpng -Gdpi=180 input.dot -o /tmp/preview.png

# Final raster for LaTeX
dot -Tpng -Gdpi=180 input.dot -o figures/out.png

# Vector
dot -Tsvg input.dot -o figures/out.svg
dot -Tpdf input.dot -o figures/out.pdf

# Verify columns/rows numerically
dot -Tplain input.dot | awk '$1=="node"{print $2, $3}'

# Render with explicit defaults instead of editing the file
dot -Gdpi=200 -Nfontname="DejaVu Sans Bold" -Epenwidth=2 -Tpng in.dot -o out.png
```

## Environment and fonts

- Graphviz has no config file to speak of; pass defaults with `-G/-N/-E` or put
  them in the file.
- Font resolution uses the system font stack (fontconfig on Linux). Use
  `fc-list` to find exact family names.
- For reproducible output across machines, name a concrete family and ship the
  font, or accept that the default `Times,serif` will substitute differently.
