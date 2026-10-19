# D2 CLI reference

Verified against D2 v0.9.0. `man d2` is authoritative for the installed version.

## Synopsis

```text
d2 [flags] file.d2 [file.svg|.png|.pdf|.pptx|.gif|.txt]
d2 layout [name]
d2 fmt file.d2 ...
d2 validate file.d2
d2 play file.d2
```

- Output format is inferred from the extension; without an output path the
  result is `file.svg`.
- `-` reads stdin as input and, as output, writes SVG to stdout (change with
  `--stdout-format`).
- **Check the exit status for success, never the output file's existence** —
  D2 sometimes writes a partial render on error to aid iteration.
- `d2 validate file.d2` parses without rendering (fast pre-check).
- `d2 fmt file.d2` reformats; `--check` (or `D2_CHECK`) verifies formatting
  without writing.

## Export formats

| Ext / format | Notes |
| ------------ | ----- |
| `.svg`       | default; CSS injected; interactive (tooltips/links); bundled assets by default |
| `.png`       | rendered natively (no browser); useful for the inspect loop; up to 32768 px/dim |
| `.pdf`       | PNG content placed on PDF pages; less interactive than SVG, more than PNG |
| `.pptx`      | presentation export, pairs well with composition |
| `.gif`       | animated export for short compositions |
| `.txt`       | ASCII art (beta since 0.7.1); ELK/TALA only; `--ascii-mode standard|extended` |
| stdout       | `--stdout-format svg|png|pdf|pptx|gif|txt|ascii` |

## Layout engines

Choose per diagram with `--layout` / `D2_LAYOUT`. Discover engines and their
flags with `d2 layout` and `d2 layout <engine>`.

- **tala** (preferred for architecture): orthogonal, not hierarchy-bound,
  first-class container handling, per-container `direction`, `near: <object>`,
  `top`/`left` locking, symmetry-aware, exact SQL row routing. Con: has
  randomness — small edits can cascade into a different layout. Determinism via
  `--tala-seeds` (default `[1,2,3]`).
- **elk**: mature, orthogonal, good crossing minimization, good container
  routing, customizable. Strictly hierarchical. Algorithms via
  `--elk-algorithm` (`layered` default; also `force`, `stress`, `mrtree`,
  `radial`).
- **dagre** (CLI default): fast, hierarchical, battle-tested. Unmaintained,
  curved multi-segment routing, weaker containers, and ancestor↔descendant
  connections are unsupported.

Feature support varies by engine: `near: <object>`, `top`/`left`, on-container
`direction`, and container `width`/`height` (TALA/ELK) depend on the engine.

## Common flags

| Flag | Meaning |
| ---- | ------- |
| `-t, --theme N` | theme ID (default `0`) |
| `--dark-theme N` | theme for dark mode (default −1 = same as `--theme`) |
| `-l, --layout NAME` | layout engine |
| `-s, --sketch` | hand-drawn style |
| `--pad N` | padding around the diagram (default 100) |
| `--center` | center the SVG in its viewBox |
| `--scale F` | scale output (−1 fits SVG to screen) |
| `-b, --bundle` | bundle assets/layers into the SVG (default true) |
| `--target BOARD` | which board(s) to render (`''`, `layers.x`, `layers.x.*`) |
| `--animate-interval MS` | package boards into one animated SVG/GIF |
| `--salt STR` | make SVG element IDs unique (multiple identical diagrams per page) |
| `--no-xml-tag` | omit the XML declaration (direct HTML embedding) |
| `--omit-version` | omit the D2 version from the image |
| `--force-appendix` | add the tooltip/link appendix to SVG too |
| `--timeout N` | render timeout in seconds (default 120; raise for large diagrams) |
| `-w, --watch` | watch and live-reload (`--host`/`--port`, `--browser`) |
| `--font-regular/-italic/-bold/-semibold` | replace main TTFs |
| `--font-mono*` | replace mono TTFs |
| `--ascii-mode standard|extended` | ASCII output characters |
| `-d, --debug` | debug logs |
| `-v, --version`, `-h, --help` | version / usage |

## Environment variables

Flags map to env vars: `D2_LAYOUT`, `D2_THEME`, `D2_DARK_THEME`, `D2_PAD`,
`D2_CENTER`, `D2_SKETCH`, `D2_BUNDLE`, `D2_FORCE_APPENDIX`, `D2_WATCH`,
`D2_TIMEOUT`, `D2_CHECK`, `D2_ASCII_MODE`, `D2_STDOUT_FORMAT`, `D2_NO_XML_TAG`,
`D2_ANIMATE_INTERVAL`, `D2_FONT_*`, `D2_FONT_MONO_*`, `OMIT_VERSION`,
`IMG_CACHE`, `HOST`, `PORT`, `BROWSER`, `DEBUG`.

## Precedence

CLI flags and environment variables take precedence over `vars.d2-config` in the
source file.

## Useful recipes

```sh
# Fast syntax check
d2 validate input.d2

# Preview to inspect layout (open the PNG afterward)
d2 --layout tala input.d2 /tmp/preview.png

# Final vector export with a fixed engine and theme
d2 --layout tala --theme 0 input.d2 figures/out.svg

# PDF for a LaTeX document
d2 --layout tala --theme 0 input.d2 figures/out.pdf

# Diagram from stdin to stdout
echo 'x -> y' | d2 - - > out.svg

# Animated build-up of composition boards
d2 --animate-interval 1000 input.d2 out.svg
```

## SVG export internals (for post-processing)

- Shape elements get base64-encoded ID CSS classes (shape ID `my-shape` →
  class `bXktc2hhcGU`).
- Each diagram gets a deterministic hash prefix (e.g. `d2-1234567890`) used for
  clip paths and gradients, avoiding collisions when several diagrams share a
  page.
