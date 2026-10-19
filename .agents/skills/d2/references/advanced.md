# D2 advanced reference

Verified against D2 v0.9.0.

## Sequence diagrams

Set `shape: sequence_diagram` on an object. No new syntax — same rules as
everywhere else, with two differences:

- **Shared scope**: children of the sequence diagram refer to the same actors
  across the whole diagram (no per-message re-instancing).
- **Order matters**: declaration order is visual order (actors left-to-right,
  messages top-to-bottom). Declare actors explicitly (e.g. `a; b; c; d`) to fix
  order; actors are also called "participants".

```d2
shape: sequence_diagram
alice; bob
alice -> bob: request
bob -> alice: response
```

Features:

- **Spans** (a.k.a. activation bars): connect a nested object on an actor.
- **Groups** (a.k.a. frames/fragments): a container inside the diagram that has
  connections but isn't itself connected. Actors used inside must be declared
  at the top level first.
- **Notes**: a nested object on an actor with no connections.
- **Self-messages**: connect an actor to itself.
- Lifelines inherit the actor's `stroke` / `stroke-dash`.
- Sequence diagrams are ordinary objects: containable, connectable, stylable.

## SQL tables (ERDs)

```d2
users: {
  shape: sql_table
  id: int { constraint: primary_key }
  email: varchar { constraint: [unique; not_null] }
  org_id: int { constraint: foreign_key }
}
orgs: { shape: sql_table; id: int { constraint: primary_key } }
users.org_id -> orgs.id
```

- Each key = a row; its value = the column type.
- `constraint` is shortened when recognized: `primary_key` → PK,
  `foreign_key` → FK, `unique` → UNQ. Any other constraint is shown verbatim.
- Multiple constraints use an array: `constraint: [primary_key; unique]`.
- Quote reserved keywords used as column names: `"label": string`.
- With **TALA or ELK**, connections point at the exact row.

## UML classes

```d2
Shape: {
  shape: class
  +x: int
  -y: int
  #z: int
  +get_area(): float
  +resize(w: int, h: int)
}
```

- Each key is a field or method; the value is its type (a method without a
  value returns void).
- A key containing `(` is a method.
- Visibility prefixes: none or `+` public, `-` private, `#` protected.

## Grid diagrams

```d2
table: {
  grid-rows: 2
  grid-columns: 3
  a; b; c; d; e; f
}
```

- `grid-rows` / `grid-columns`; when both are set, whichever is declared
  **first** is the dominant fill direction.
- Gaps: `grid-gap` (both axes), or override with `vertical-gap` /
  `horizontal-gap`. `grid-gap: 0` is useful for tables/maps.
- Cells in a column share width, cells in a row share height — mismatch causes
  padding; set explicit `width` to even them out.
- Pad a grid with invisible elements to align it.
- Grids, sequence diagrams, and regular diagrams can nest inside each other.
- With Dagre/ELK, connections between grid cells are straight center-to-center;
  with TALA they are routed.

## Composition (multiple boards)

| Keyword      | Inheritance                                  |
| ------------ | -------------------------------------------- |
| `layers`     | none — a new base                            |
| `scenarios`  | inherit from the base layer                  |
| `steps`      | inherit from the previous step               |

```d2
x -> y
layers: {
  detail: { a -> b }
}
scenarios: {
  happy: { x -> z }
}
```

- Render one board: `--target=''` (root), `--target=layers.detail`, or a board
  plus children with a trailing `*` (`--target='layers.detail.*'`).
- Package all boards into an animated SVG/GIF: `--animate-interval <ms>`
  (SVG/GIF only).
- Boards inherit objects; use `null` to remove specific ones.

## Imports

```d2
a: @x              # x.d2 becomes a's value (a map)
a: { ...@x }       # spread x.d2's entries into a's map
a: @x.y            # import only object y from x.d2
```

- Omit the `.d2` extension. Relative paths resolve against the importing file.
- Objects with dots in the filename must be quoted: `@"schema-v0.1.2"`.
- Only `.d2` files can be imported.
- Triple globs (`***`) are the only globs that persist across imports.

Useful patterns: **modular classes** (a `classes.d2` imported for styling),
**model/view** (define a model once, `suspend` everything, `unsuspend` per
view), **version history** (import schema files checked out at different git
tags), **A/B comparison** (import two teams' schemas into one diagram).

## Icons and images

```d2
api: { icon: https://icons.d2lang.com/... }   # icon on a shape
logo: { shape: image; icon: ./logo.png }      # standalone image shape
```

- `icon` accepts any URL or, on the CLI, a local path.
- Hosted icon set: <https://icons.d2lang.com>.
- Icon placement is automatic (containers top-left, leaves centered); adjust
  with `icon.near`.
- `shape: image` requires a valid, existing `icon`.

## Interactive: tooltips and links

```d2
x: {
  tooltip: extra context        # shows on hover
  link: https://example.com     # clickable
}
```

- Link URIs containing `#` must be quoted (`#` starts a comment).
- `tooltip.near: <position>` makes the tooltip permanent (renders inline).
- In PNG/static exports, tooltips become numbered marks plus an appendix;
  `--force-appendix` adds the appendix to SVG too.

## Models: suspend / unsuspend

- `suspend` hides/removes an object; `unsuspend` restores it.
- Define a model once, suspend everything (`**: suspend` and
  `(** -> **)[*]: suspend`), then `unsuspend` the pieces a given view needs.
- Combine with imports and globs for one-model/many-views diagrams.

## Sketch mode

`--sketch` renders hand-drawn style (alternate font pairing, wobbly strokes).
Works with any diagram; often better avoided for precise technical figures.
