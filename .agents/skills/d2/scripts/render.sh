#!/usr/bin/env bash
# render.sh — compile a D2 file with neutral, version-appropriate defaults.
#
# Part of the `d2` skill. Keep this script the single place that encodes the
# default flags, so callers don't have to recall them.
#
# Usage:
#   render.sh [options] <input.d2> [output]
#
# Options:
#   --preview         render a PNG preview to a temp file and print its path
#   --format FMT      output format: svg (default), png, pdf, pptx, gif, txt
#   --layout NAME     layout engine (default: $D2_LAYOUT, else tala)
#   --theme N         theme ID (default: $D2_THEME, else D2's own default)
#   --sketch          hand-drawn style
#   --pad N           padding around the diagram
#   --no-validate     skip the `d2 validate` pre-check
#   -h, --help        show this help
#
# Exit status is D2's; the presence of an output file does NOT mean success.

set -euo pipefail

die() { printf 'render.sh: %s\n' "$*" >&2; exit 2; }

usage() {
  cat <<'EOF'
render.sh — compile a D2 file with neutral, version-appropriate defaults.

Usage: render.sh [options] <input.d2> [output]

Options:
  --preview         render a PNG preview to a temp file and print its path
  --format FMT      output format: svg (default), png, pdf, pptx, gif, txt
  --layout NAME     layout engine (default: $D2_LAYOUT, else tala)
  --theme N         theme ID (default: $D2_THEME, else D2's own default)
  --sketch          hand-drawn style
  --pad N           padding around the diagram
  --no-validate     skip the `d2 validate` pre-check
  -h, --help        show this help

Exit status is D2's; the presence of an output file does NOT mean success.
EOF
}

preview=0
fmt="svg"
layout="${D2_LAYOUT:-tala}"
theme="${D2_THEME:-}"
sketch=0
pad=""
validate=1
input=""
output=""

while [ $# -gt 0 ]; do
  case "$1" in
    --preview)      preview=1; shift ;;
    --format)       fmt="${2:?}"; shift 2 ;;
    --layout)       layout="${2:?}"; shift 2 ;;
    --theme)        theme="${2:?}"; shift 2 ;;
    --sketch)       sketch=1; shift ;;
    --pad)          pad="${2:?}"; shift 2 ;;
    --no-validate)  validate=0; shift ;;
    -h|--help)      usage; exit 0 ;;
    -*)             die "unknown option: $1" ;;
    *)              if [ -z "$input" ]; then input="$1"; else output="$1"; fi; shift ;;
  esac
done

[ -n "$input" ] || die "missing input .d2 file"
command -v d2 >/dev/null 2>&1 || die "d2 not found on PATH"

# --- build flag list (only pass what we mean to override) -------------------
flags=()
[ -n "$layout" ] && flags+=(--layout "$layout")
[ -n "$theme" ]  && flags+=(--theme "$theme")
[ "$sketch" -eq 1 ] && flags+=(--sketch)
[ -n "$pad" ]    && flags+=(--pad "$pad")

# --- validate ---------------------------------------------------------------
if [ "$validate" -eq 1 ]; then
  d2 validate "$input" >/dev/null
fi

# --- choose output ----------------------------------------------------------
if [ "$preview" -eq 1 ]; then
  fmt="png"
  if [ -z "$output" ]; then
    base="$(basename "${input%.d2}")"
    output="$(mktemp -t "d2-${base}-XXXXXX")"
    output="${output}.png"
  fi
elif [ -z "$output" ]; then
  output="${input%.d2}.${fmt}"
fi

d2 "${flags[@]}" "$input" "$output"

if [ "$preview" -eq 1 ]; then
  printf '%s\n' "$output"   # print preview path for the caller to inspect
fi
