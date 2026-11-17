#!/usr/bin/env bash
# Phase 00: Regenerate mystmd-math-macros.yml from the canonical macro
# source (@resources/markdown/econark-shortcuts.md).
#
# myst.yml's `extends:` includes mystmd-math-macros.yml so KaTeX can
# resolve every paper-defined macro at HTML-render time. Without this
# file, `myst build --strict` errors with hundreds of "Undefined control
# sequence" messages — the file is load-bearing for the published site.
#
# We regenerate every build (cheap, ~50ms) so the YAML never drifts from
# the source. tools/build-myst/lib/math_macros.py does the parsing and
# KaTeX-incompatibility rewrites; see its module docstring.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

OUT="mystmd-math-macros.yml"

# Macro sources, listed in load order (later wins). The base pool comes
# from the econark-shared shortcuts markdown; @local/local.sty layers
# paper-specific overrides on top (e.g. condition macros redefined via
# \BSTcondref). @local/local-tikz.sty adds tikz-figure-only macros.
SOURCES=(
  "@resources/markdown/econark-shortcuts.md"
  "@local/local.sty"
  "@local/local-tikz.sty"
  "tools/build-myst/config/katex-shims.tex"
)

for src in "${SOURCES[@]}"; do
  if [ ! -f "$src" ]; then
    echo "Phase 00 ERROR: macro source not found: $src" >&2
    exit 1
  fi
done

PYTHONPATH="tools/build-myst" \
python3 -m lib.math_macros "$OUT" "${SOURCES[@]}"

n_macros="$(grep -cE "^    '\\\\" "$OUT" || true)"
echo "  emitted $n_macros KaTeX macros to $OUT"
