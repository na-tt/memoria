#!/usr/bin/env bash
# render.sh — compile a Graphviz file with neutral, version-appropriate defaults.
#
# Part of the `graphviz` skill. Keep this script the single place that encodes
# the default flags, so callers don't have to recall them.
#
# Usage:
#   render.sh [options] <input.dot> [output]
#
# Options:
#   --preview         render a PNG preview to a temp file and print its path
#   --format FMT      output format: png (default), svg, pdf, ...
#   --engine NAME     layout engine (default: $GV_ENGINE, else dot)
#   --dpi N           raster resolution (default: $GV_DPI, else 180)
#   --pad N           padding around the drawing, in inches (graph `pad`)
#   --no-validate     skip the `dot -Tcanon` pre-check
#   -h, --help        show this help
#
# Exit status is Graphviz's; the presence of an output file does NOT mean success.

set -euo pipefail

die() { printf 'render.sh: %s\n' "$*" >&2; exit 2; }

usage() {
  cat <<'EOF'
render.sh — compile a Graphviz file with neutral, version-appropriate defaults.

Usage: render.sh [options] <input.dot> [output]

Options:
  --preview         render a PNG preview to a temp file and print its path
  --format FMT      output format: png (default), svg, pdf, ...
  --engine NAME     layout engine (default: $GV_ENGINE, else dot)
  --dpi N           raster resolution (default: $GV_DPI, else 180)
  --pad N           padding around the drawing, in inches (graph `pad`)
  --no-validate     skip the `dot -Tcanon` pre-check
  -h, --help        show this help
EOF
}

preview=0
fmt="png"
engine="${GV_ENGINE:-dot}"
dpi="${GV_DPI:-180}"
pad=""
validate=1
input=""
output=""

while [ $# -gt 0 ]; do
  case "$1" in
    --preview)      preview=1; shift ;;
    --format)       fmt="${2:?}"; shift 2 ;;
    --engine)       engine="${2:?}"; shift 2 ;;
    --dpi)          dpi="${2:?}"; shift 2 ;;
    --pad)          pad="${2:?}"; shift 2 ;;
    --no-validate)  validate=0; shift ;;
    -h|--help)      usage; exit 0 ;;
    -*)             die "unknown option: $1" ;;
    *)              if [ -z "$input" ]; then input="$1"; else output="$1"; fi; shift ;;
  esac
done

[ -n "$input" ] || die "missing input .dot file"
command -v dot >/dev/null 2>&1 || die "dot not found on PATH"

# --- build flag list (only pass what we mean to override) -------------------
flags=()
[ -n "$engine" ] && flags+=(-K"$engine")
[ -n "$dpi" ]    && flags+=(-Gdpi="$dpi")
[ -n "$pad" ]    && flags+=(-Gpad="$pad")

# --- validate ---------------------------------------------------------------
# `-Tcanon` parses and canonicalises without computing a layout.
if [ "$validate" -eq 1 ]; then
  dot -Tcanon "$input" >/dev/null || die "parse check failed: $input"
fi

# --- choose output ----------------------------------------------------------
if [ "$preview" -eq 1 ]; then
  fmt="png"
  if [ -z "$output" ]; then
    base="$(basename "${input%.dot}")"; base="${base%.gv}"
    output="$(mktemp -t "gv-${base}-XXXXXX")"
    output="${output}.png"
  fi
elif [ -z "$output" ]; then
  stem="${input%.dot}"; stem="${stem%.gv}"
  output="${stem}.${fmt}"
fi

dot "${flags[@]}" -T"$fmt" "$input" -o "$output"

if [ "$preview" -eq 1 ]; then
  printf '%s\n' "$output"   # print preview path for the caller to inspect
fi
