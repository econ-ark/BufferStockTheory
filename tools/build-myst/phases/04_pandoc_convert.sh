#!/usr/bin/env bash
# Phase 04: Pandoc convert latex → markdown.
#
# We strip the inlined .bbl from the input first (Phase 5 will read it back
# as raw harvarditem entries) — pandoc cannot render \harvarditem and would
# emit garbled output for the bibliography portion.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

BUILD_DIR="_build/myst"
SRC="$BUILD_DIR/03_normalized.tex"
SPLIT_BODY="$BUILD_DIR/04_body_only.tex"
SPLIT_BBL="$BUILD_DIR/04_bbl_only.tex"
OUT_MD="$BUILD_DIR/04_raw.md"

if [ ! -f "$SRC" ]; then
  echo "Phase 04 ERROR: $SRC missing (Phase 3 did not run?)" >&2
  exit 1
fi

# Split body | inlined-bbl at the fence comment Phase 1 emitted.
awk '
  /^% --- begin inlined bibliography/ { in_bbl=1; next }
  /^% --- end inlined bibliography/   { in_bbl=0; next }
  { if (in_bbl) print > BBL; else print > BODY }
' BODY="$SPLIT_BODY" BBL="$SPLIT_BBL" "$SRC"

# pandoc flags chosen for fidelity:
#   --from latex                : input format
#   --to markdown_strict-...    : MD with all the GFM/MyST-friendly extensions
#   --wrap=preserve             : do not re-wrap paragraphs
#   --markdown-headings=atx     : `# H1` style, easier to grep
#   --shift-heading-level-by=0  : keep \section as #, \subsection as ##, …
#   -o                          : output file
PANDOC_FROM="latex"
PANDOC_TO="markdown_strict+pipe_tables+grid_tables+table_captions+yaml_metadata_block+raw_attribute+tex_math_dollars+definition_lists+fenced_code_attributes+header_attributes+link_attributes+backtick_code_blocks+strikeout+autolink_bare_uris+footnotes+task_lists+inline_notes+multiline_tables+all_symbols_escapable"

pandoc \
  --from="$PANDOC_FROM" \
  --to="$PANDOC_TO" \
  --wrap=preserve \
  --markdown-headings=atx \
  --shift-heading-level-by=0 \
  -o "$OUT_MD" \
  "$SPLIT_BODY"

LINES="$(wc -l < "$OUT_MD")"
echo "  raw markdown:    $OUT_MD ($LINES lines)"
echo "  bbl-only file:   $SPLIT_BBL  (consumed by Phase 5)"
