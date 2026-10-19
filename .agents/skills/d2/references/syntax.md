# D2 syntax reference

Verified against D2 v0.9.0. If `d2 --version` differs, re-verify.

## Strings and punctuation

- **Unquoted strings** are the norm; leading/trailing whitespace is trimmed.
  `Office Bulb: Philips`.
- **Quote** (`'...'` or `"..."`) when the text contains reserved characters
  (`: ; . { } | # @ - ->` etc.). Use double quotes if the text contains a single
  quote and vice versa; escape with `\` if it contains both.
- **Reserved keywords as keys** must be quoted: `"label": string`,
  `"width": width`.
- **Semicolons** put multiple declarations on one line: `SQLite; Cassandra`,
  `a: 1; b: 2`.
- **Newlines or `;` separate map entries — commas do not.** A comma becomes part
  of the value.
- **Comments**: `# line comment` (own line or end of line); block comments use
  `""" ... """`.
- Use **ASCII** `: ; .` in non-Latin diagrams; lookalike Unicode punctuation is
  not recognized.

## Nodes

```d2
x                      # shape with label "x"
pg: PostgreSQL         # key pg, label "PostgreSQL"
x.shape: cylinder      # set a shape type
```

Keys are case-insensitive (`postgresql` == `postgreSQL`). Connections to
undeclared keys create the shape implicitly.

## Containers

Nesting a map under a key creates a container (subgraph):

```d2
cloud: Google Cloud {        # shorthand container label
  db: { shape: cylinder }
  api
}
```

- Container label via shorthand (`cloud: Google Cloud { ... }`) or the reserved
  keyword (`cloud: { label: Google Cloud; ... }`).
- Reference nested nodes with dots: `cloud.db`.
- **`_` refers to the parent** scope, to reach outward from inside a container.
- Repeated declarations of the same shape **merge** (see Overrides).

## Connections

Exactly four operators:

| Operator | Meaning                         |
| -------- | ------------------------------- |
| `->`     | directed (arrow at target)      |
| `<-`     | directed (arrow at source)      |
| `<->`    | bidirectional                   |
| `--`     | undirected (plain line)         |

- Label: `a -> b: Kept in sync` or `a -> b: |pipe label|`.
- Connect a shape's **key**, not its label. `Backend -> Frontend` would create
  two new shapes if `be`/`fe` are the real keys.
- **Chaining** is allowed: `a -> b -> c`.
- **Cycles** are fine. **Repeated** connections add new edges; they don't
  overwrite.
- **Edge bodies** style individual edges:
  ```d2
  a -> b: label {
    style.stroke-dash: 3
    style.animated: true
  }
  ```
- **Reference an edge by index** to modify it later:
  `(a -> b)[0].style.stroke: red`.
- **Arrowheads** via reserved shapes `source-arrowhead` / `target-arrowhead`:
  ```d2
  a -> b: {
    source-arrowhead.shape: diamond
    target-arrowhead.shape: arrow
  }
  ```
  Shapes: `triangle` (default; `style.filled: false` for hollow), `arrow`,
  `diamond`, `circle`, `box` (the last three: `style.filled: true` when solid),
  `cf-one`, `cf-one-required`, `cf-many`, `cf-many-required`, `cross`.
  A source/target arrowhead needs the connection to have that endpoint.

## Direction

`direction: up | down | left | right` at the root, or per container **on TALA
only**. Other engines are strictly hierarchical (one global direction).

## Dimensions and positioning

- `width` / `height` on most shapes. On **containers** only TALA and ELK honor
  them (TALA may grow to fit children).
- **1:1 shapes** (`circle`, `square`) keep width == height; setting both uses
  the larger.
- `near: top-left | top-center | top-right | center-left | center-right |
  bottom-left | bottom-center | bottom-right` pins an object (e.g. a title or
  legend) to a diagram region. Nest it under `label`/`icon` to position those;
  prefixes `outside-` and `border-` are supported (note `outside-left-center`,
  not `outside-center-left`).
- `near: <absolute-id>` places an object near another object — **TALA only**.
- `top` / `left` lock an object's position — **TALA only** (set both together).

## Text

- Standalone text and labels are **Markdown** (so labels can be bold, link,
  list, etc.; HTML must be well-formed, e.g. `<br/>`).
- **Non-Markdown text**: `shape: text`.
- **Block strings** for multi-line code/markdown, tagged by language:
  ```d2
  code: |go
    func main() {}
  |
  ```
  Use a different delimiter character after the first pipe if `|` occurs in the
  content, e.g. `|`ts ... `|` (any non-alphanumeric, non-space, non-`_` char).
  Aliases: `md`, `tex`/`latex`, `js`, `go`, `py`, `rb`, `ts`.
- **LaTeX** blocks (`tex`/`latex`) render via MathJax — math notation only, not
  document layout. Size with `\tiny \small \large \huge`, not `font-size`.

## Variables and substitutions

```d2
vars: {
  color: "#1d4ed8"
}
x: { style.fill: ${color} }
```

- Reference with `${...}`; nested paths use dots (`${a.b}`).
- **Scoped** like programming languages: inner can read outer, not vice versa;
  innermost wins.
- **Single quotes bypass substitution**: `'${color}'` stays literal.
- **Spread**: `...${m}` expands a map/array into the surrounding map/array.
- **Config**: `vars.d2-config` can set `layout-engine`, `theme-id`,
  `dark-theme-id`, `pad`, `sketch`, `center`, `theme-overrides`,
  `dark-theme-overrides`, and a free-form `data` map.
  **CLI flags and env vars take precedence over `d2-config`.**
- **Legend**: `vars.d2-legend` declares a legend; give it a label to rename it.

## Classes

Aggregate reusable attributes; a class is a styling mixin:

```d2
classes: {
  svc: { style.fill: "#dbeafe"; shape: rectangle }
}
a.class: svc
b.class: [svc; other]   # applied left-to-right
```

An object's own attributes override the class. Classes are also written to the
SVG as `class` attributes (useful for post-processing / custom CSS).

## Globs

One-line global rules. Apply backwards and forwards, are case-insensitive, and
are scope-local unless global.

```d2
*.style.fill: yellow          # all in scope
**.shape: cylinder            # recursive
***.style.fill: white         # global (crosses layers and imports)
**.class: svc
* -> *: connect               # edges between all leaf pairs (skips self)
*.style.fill: red & shape: circle   # filter by reserved keyword
*.style.fill: red & leaf: true      # property filters: leaf, connected
!& shape: circle              # inverse filter
```

`** -> **` and recursive connection globs apply to non-container (leaf) shapes
only. Filtering supports `&` (AND across lines) and endpoint filters
(`&src:`, `&dst:` with absolute IDs). The common use case is changing a theme's
defaults. See `references/styles.md`.

## Overrides and null

- Redeclaring a shape **merges**; the latest explicit `label` wins.
- `null` **deletes** a shape, edge, or attribute: `x: null`,
  `(a -> b)[0]: null`, `x.style.fill: null`.
- Nulling a shape also nulls its edges and descendants.

## Composition (multiple boards)

`layers` (no inheritance), `scenarios` (inherit from their layer), `steps`
(inherit from the previous step). Render a specific board with `--target`, or
package boards into an animated SVG/GIF with `--animate-interval`. See
`references/advanced.md`.

## Imports

```d2
a: @x              # entire file x.d2 becomes the value of a (a map)
a: { ...@x }       # spread the file's contents into a's map
a: @x.y            # import only object y from x.d2
```

- Imports omit the `.d2` extension; quote names containing dots.
- Relative imports resolve relative to the importing file.
- Triple globs (`***`) persist across imports; normal globs and classes usually
  do not.
