# D2 shapes and styles reference

Verified against D2 v0.9.0 by compiling one probe per keyword. If
`d2 --version` differs, re-verify.

## Shape catalog

Set with `x.shape: <name>`. Default is `rectangle`.

| Category        | Shapes                                            |
| --------------- | ------------------------------------------------- |
| Basic           | `rectangle`, `square`, `page`, `parallelogram`    |
| Data / infra    | `document`, `cylinder`, `queue`, `package`, `stored_data` |
| Flow            | `step`, `callout`, `diamond`, `hexagon`           |
| Actors / cloud  | `person`, `c4-person`, `cloud`                    |
| Geometric       | `oval`, `circle`                                  |
| Media / text    | `image` (requires `icon`), `text` (no Markdown)   |

- **1:1 shapes** (`circle`, `square`): width always equals height.
- **Special shapes** (see `references/advanced.md`): `class`, `sql_table`,
  `sequence_diagram`.

`c4-person` is spelled with a hyphen (keys may still be quoted if needed).

## Style keywords

Set under `style`. For an edge, put the body on the connection:

```d2
a -> b: { style.stroke-dash: 3 }
```

| Keyword          | Accepted values                                        | Notes |
| ---------------- | ------------------------------------------------------ | ----- |
| `opacity`        | number 0.0–1.0                                         | |
| `stroke`         | CSS color name, hex `#rrggbb`, or `linear-gradient(…)` | |
| `fill`           | color / gradient                                       | shape only; on `sql_table`/`class` it colors the header |
| `fill-pattern`   | `none`, `dots`, `lines`, `grain`, `paper`              | shape only; `paper` is valid though the docs omit it |
| `stroke-width`   | integer 1–15                                           | |
| `stroke-dash`    | integer 0–10                                           | this is how you get dashed/dotted lines |
| `border-radius`  | integer 0–20                                           | very high values → pill; also affects edge corners on corner-routing engines |
| `shadow`         | `true` / `false`                                       | shape only |
| `3d`             | `true` / `false`                                       | `rectangle`/`square` only |
| `multiple`       | `true` / `false`                                       | shape only; stacked-shape effect |
| `double-border`  | `true` / `false`                                       | rectangles and ovals |
| `font`           | `mono`                                                 | only `mono` is supported |
| `font-size`      | integer 8–100                                          | |
| `font-color`     | color / gradient                                       | on `sql_table`/`class` only the header text |
| `animated`       | `true` / `false`                                       | |
| `bold`, `italic`, `underline` | `true` / `false`                         | |
| `text-transform` | `none`, `uppercase`, `lowercase`, `capitalize`         | **not** `title` (docs are wrong) |
| `fill: transparent` | | makes a shape background-transparent |

For `sql_table` and `class`, `stroke` is applied as the **body fill** (because
`fill` is already used for the header).

### Root-level styles

Some styles apply to the whole diagram at the root (unprefixed):

- `style.fill` — diagram background
- `style.fill-pattern` — background pattern
- `style.stroke`, `style.stroke-width`, `style.stroke-dash` — frame
- `style.double-border` — two frames

Frames usually want extra padding (`--pad`, default 100).

## Fonts

D2 ships four families: Source Sans Pro (labels/body), Source Code Pro (code and
`class` bodies), and a hand-drawn pairing for `--sketch`. Override the main TTFs
on the CLI with `--font-regular`, `--font-italic`, `--font-bold`,
`--font-semibold` (and `--font-mono*` for mono). Supply **all or none**; missing
styles silently fall back to Source Sans Pro.

## Themes

- Default is theme `0` (Neutral Default). List with `d2 themes`.
- Light IDs: 0, 1, 3–8, 100–105, 300–303. Dark IDs: 200, 201.
- `--theme N` / `D2_THEME`; `--dark-theme N` / `D2_DARK_THEME` for system-pref
  dark mode (off by default).
- A dark theme ID passed to `--theme` just forces dark.
- Some themes do more than color: e.g. the `Terminal` theme forces caps lock,
  no border radius, mono font, dotted container fills, and a double border.

### Customizing / overriding a theme

Use `d2-config` in `vars` with the theme's color codes:

```d2
vars: {
  d2-config: {
    theme-overrides: {
      B1: "#2E7D32"
      B2: "#66BB6A"
      AA2: "#0D47A1"
      AB4: "#F44336"
    }
  }
}
```

`dark-theme-overrides` does the same for dark mode. Flags/env override
`d2-config`.

### Changing theme defaults with globs

```d2
**.style.fill: "#f8fafc"
**.style.stroke: "#334155"
```

## Colors

Anywhere a color is accepted: CSS color name (`orange`), hex (`#f0ff3a`), or a
subset of CSS gradients (`linear-gradient(red, blue)`). `transparent` is also
accepted for `fill`.
