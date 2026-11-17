#!/usr/bin/env bash
# Orchestrate the LaTeX → MyST pipeline. See tools/build-myst/README.md.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

PIPELINE_DIR="tools/build-myst"
BUILD_DIR="_build/myst"
mkdir -p "$BUILD_DIR"

PHASES=(
  "00_emit_math_macros.sh"
  "01_resolve_inputs.sh"
  "02_strip_conditionals.py"
  "03_normalize_macros.py"
  "04_pandoc_convert.sh"
  "05_resolve_citations.py"
  "06_resolve_xrefs.py"
  "07_theorem_envs.py"
  "08a_paragraphs_and_figs.py"
  "08b_named_condition_glosses.py"
  "09_strip_frontmatter.py"
  "10_assemble_frontmatter.py"
  "11_validate.py"
)

# Use a Python that has PyYAML on the import path. Default order:
#   1. $BST_MYST_PYTHON if set
#   2. /usr/bin/python3 (Apple system Python, has pyyaml on macOS)
#   3. python3 from $PATH
# Override via `BST_MYST_PYTHON=/path/to/python` if neither default works.
choose_py() {
  local candidates=()
  if [ -n "${BST_MYST_PYTHON:-}" ]; then
    candidates+=("$BST_MYST_PYTHON")
  fi
  candidates+=("/usr/bin/python3" "python3")
  for c in "${candidates[@]}"; do
    if "$c" -c "import yaml" >/dev/null 2>&1; then
      echo "$c"
      return 0
    fi
  done
  echo "ERROR: no python3 with PyYAML found. Tried: ${candidates[*]}" >&2
  echo "  Install PyYAML, or set BST_MYST_PYTHON to a python with it." >&2
  exit 1
}
PY="$(choose_py)"
echo "  python: $PY"

echo "▶ tools/build-myst pipeline starting"
echo "  repo: $REPO_ROOT"
echo "  build dir: $BUILD_DIR"
echo

for phase in "${PHASES[@]}"; do
  ext="${phase##*.}"
  echo "─── phase: $phase ───"
  case "$ext" in
    sh) bash "$PIPELINE_DIR/phases/$phase" ;;
    py) "$PY" "$PIPELINE_DIR/phases/$phase" ;;
    *)  echo "Unknown phase extension: $ext" >&2; exit 1 ;;
  esac
done

FINAL="$BUILD_DIR/10_with_frontmatter.md"
if [ ! -f "$FINAL" ]; then
  echo "ERROR: $FINAL not produced" >&2
  exit 1
fi

cp "$FINAL" BufferStockTheory.md
LINES="$(wc -l < BufferStockTheory.md)"
echo
echo "✔ BufferStockTheory.md regenerated (${LINES} lines)"
