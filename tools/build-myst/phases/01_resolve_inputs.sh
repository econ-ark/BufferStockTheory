#!/usr/bin/env bash
# Phase 01: Resolve \input{} and \subfile{} chains by recursive in-house
# expansion (latexpand cannot follow econark path macros like \ApndxDir
# through nested levels), then append a freshly-generated .bbl so the
# bibliography is visible to Phase 5.
#
# .bbl provenance:
#   This phase regenerates BufferStockTheory.bbl from current sources by
#   running pdflatex + bibtex into _build/myst/bbl-gen/. It used to read
#   docs/BufferStockTheory.bbl (docs/ was removed on 2026-11-13), a gitignored
#   file kept in sync only by manual intervention, which led to silent staleness
#   (e.g. the harmenbergAggregating cite-key incident — the .bbl was
#   ~18 months out of date and Phase 05 emitted broken citations until
#   noticed by a human). Self-regeneration makes the pipeline robust
#   against that class of bug.
#
#   The .bbl regen is cached: it only re-runs when a tracked .tex or .bib
#   file, or a bibliography database or style file the last BibTeX run
#   read (some live outside the repository, e.g. econark.bst, system.bib),
#   is newer than the existing .bbl. Steady-state cost is a loop of
#   file-date comparisons; cold cost is one pdflatex pass + one bibtex.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

BUILD_DIR="_build/myst"
BBL_DIR="$BUILD_DIR/bbl-gen"
mkdir -p "$BUILD_DIR" "$BBL_DIR"

MASTER_TEX="BufferStockTheory.tex"
MASTER_STEM="BufferStockTheory"
BBL="$BBL_DIR/${MASTER_STEM}.bbl"
BLG="$BBL_DIR/${MASTER_STEM}.blg"
FLAT="$BUILD_DIR/01_flat.tex"

if [ ! -f "$MASTER_TEX" ]; then
  echo "Phase 01 ERROR: master TeX not found: $MASTER_TEX" >&2
  exit 1
fi

# --- .bbl freshness check --------------------------------------------------
# Regenerate if the .bbl is missing or first_newer_input names an input.
#
# The comparison uses the shell's own `-nt` test, which behaves the same on
# Linux and macOS. (It used `stat -f '%m'`, which is BSD syntax: GNU stat
# read `-f` as "file system status" and failed, the failure was discarded,
# and on Linux a cached .bbl was reused indefinitely.)

# Prints the first input newer than the .bbl, or nothing if there is none.
first_newer_input() {
  local f name path
  # Tracked .tex and .bib files only: build artifacts in subdirectories
  # would make the .bbl look stale for no reason.
  while IFS= read -r -d '' f; do
    if [ "$f" -nt "$BBL" ]; then printf '%s\n' "$f"; return; fi
  done < <(git ls-files -z -- '*.tex' '*.bib')
  # The databases and style file the last BibTeX run read, as its log
  # names them, found the way that run found them.
  if [ ! -f "$BLG" ]; then printf '%s\n' "$BLG (missing)"; return; fi
  while IFS= read -r name; do
    path="$(BIBINPUTS="$REPO_ROOT:" kpsewhich "$name" || true)"
    if [ -z "$path" ]; then printf '%s\n' "$name (not found by kpsewhich)"; return; fi
    if [ "$path" -nt "$BBL" ]; then printf '%s\n' "$path"; return; fi
  done < <(sed -n -e 's/^Database file #[0-9]*: //p' -e 's/^The style file: //p' "$BLG")
}

needs_regen=false
if [ ! -f "$BBL" ]; then
  needs_regen=true
  reason="missing"
else
  newer="$(first_newer_input)"
  if [ -n "$newer" ]; then
    needs_regen=true
    reason="$newer is newer than $BBL"
  fi
fi

if [ "$needs_regen" = true ]; then
  echo "  regenerating .bbl ($reason) ..."
  PDFLATEX_LOG="$BBL_DIR/pdflatex-pass1.log"
  BIBTEX_LOG="$BBL_DIR/bibtex.log"

  # The master writes \begin{verbatimwrite}{\EqDir/X}...\end{verbatimwrite}
  # blocks to ./Equations/X.tex and reads them back with
  # \input{\LtxDir\EqDir/X}. With -output-directory the writes are
  # redirected into BBL_DIR, but the reads still look in ./Equations, so
  # on a fresh clone (no Equations/*.tex left by an earlier PDF build)
  # pass 1 failed with "File `./Equations/supfn.tex' not found".
  # BBL_DIR/Equations is therefore a link to the repository's Equations/:
  # the writes land where they are read, as in a plain pdflatex run.
  # Equations/*.tex are gitignored build products.
  # Other redirected writes (e.g. Tables/) need their subdirectories to
  # exist, or pdflatex fails with "I can't write on file".
  mkdir -p Equations "$BBL_DIR/Tables"
  if [ -d "$BBL_DIR/Equations" ] && [ ! -L "$BBL_DIR/Equations" ]; then
    rm -rf "$BBL_DIR/Equations"   # a real directory left by older runs
  fi
  ln -sfn ../../../Equations "$BBL_DIR/Equations"

  # Pass 1: produce .aux with cite keys. -draftmode skips PDF output;
  # -interaction=batchmode + -halt-on-error make non-interactive runs
  # surface their failure clearly. Errors here are fatal — the rest of
  # the pipeline depends on a working .aux.
  if ! pdflatex \
        -draftmode \
        -interaction=batchmode \
        -halt-on-error \
        -output-directory="$BBL_DIR" \
        "$MASTER_TEX" \
        >"$PDFLATEX_LOG" 2>&1; then
    echo "Phase 01 ERROR: pdflatex pass 1 failed during .bbl generation" >&2
    echo "  see $PDFLATEX_LOG and $BBL_DIR/${MASTER_STEM}.log (last 20 lines below):" >&2
    tail -20 "$BBL_DIR/${MASTER_STEM}.log" 2>/dev/null >&2 || tail -20 "$PDFLATEX_LOG" >&2
    exit 1
  fi

  if [ ! -f "$BBL_DIR/${MASTER_STEM}.aux" ]; then
    echo "Phase 01 ERROR: pdflatex produced no .aux at $BBL_DIR/${MASTER_STEM}.aux" >&2
    exit 1
  fi

  # bibtex: read .aux, write .bbl. The .aux references .bib files via
  # paths relative to repo root (e.g. ./BufferStockTheory.bib), so set
  # BIBINPUTS to include repo root for resolution.
  #
  # bibtex returns 2 on per-entry warnings ("Repeated entry", "Missing
  # field", etc.). Those are tolerated: real silent breakage is caught
  # downstream by Phase 05 (unresolved cite key) and Phase 11 (broken
  # cross-ref). Exit 1 = config error (.bib not found at all) — fatal.
  set +e
  BIBINPUTS="$REPO_ROOT:" bibtex "$BBL_DIR/${MASTER_STEM}" >"$BIBTEX_LOG" 2>&1
  bibtex_rc=$?
  set -e
  if [ $bibtex_rc -ne 0 ] && [ $bibtex_rc -ne 2 ]; then
    echo "Phase 01 ERROR: bibtex exited $bibtex_rc during .bbl generation" >&2
    echo "  see $BIBTEX_LOG (last 10 lines below):" >&2
    tail -10 "$BIBTEX_LOG" >&2
    exit 1
  fi

  if [ ! -f "$BBL" ]; then
    echo "Phase 01 ERROR: bibtex did not produce $BBL" >&2
    cat "$BIBTEX_LOG" >&2
    exit 1
  fi

  bbl_lines="$(wc -l < "$BBL")"
  bbl_entries="$(grep -c '^\\harvarditem' "$BBL" || true)"
  echo "  fresh .bbl: $BBL  (${bbl_lines} lines, ${bbl_entries} entries)"
else
  bbl_lines="$(wc -l < "$BBL")"
  bbl_entries="$(grep -c '^\\harvarditem' "$BBL" || true)"
  echo "  cached .bbl (sources unchanged): $BBL  (${bbl_lines} lines, ${bbl_entries} entries)"
fi

# --- recursive \input expansion -------------------------------------------
PYTHONPATH="tools/build-myst" \
python3 tools/build-myst/phases/_01_expand_inputs.py \
  --master "$MASTER_TEX" \
  --bbl    "$BBL" \
  --output "$FLAT" \
  --log    "$BUILD_DIR/01_expand.log"

LINES="$(wc -l < "$FLAT")"
WARN="$(grep -c -E 'WARN' "$BUILD_DIR/01_expand.log" || true)"
echo "  flat tex written: $FLAT (${LINES} lines, ${WARN} unresolved \\input warnings)"
