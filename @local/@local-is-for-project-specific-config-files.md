# `@local/` — paper-specific LaTeX configuration

This directory holds configuration that is specific to *this* paper, as
opposed to material in `@resources/` (which is shared infrastructure
obtained from elsewhere — econark, texlive, etc., and treated as
immutable from this paper's perspective).

The canonical layout is **5 files**, all with paper-agnostic basenames
so the skeleton can be reused across papers without per-paper renames:

| File | Role |
|---|---|
| `local.sty` | Paper-specific style: typography helpers, economics-symbol overrides, theorem environments, body-text vocabulary, hyperlink-style named-condition macros. Loaded by the master via `\usepackage{@local/local}`. New paper-local macros go here. |
| `local-tikz.sty` | Tikz-figure standalone-compilation style. Loaded by `Figures/*_tikzMake.tex` via `\usepackage{local-tikz}`. Necessarily separate because tikz figures use `\documentclass{standalone}` and never load the master preamble. |
| `dir-paths.tex` | Path macros (`\ApndxDir`, `\EqDir`, `\TableDir`, etc.). `\input`-ed (not `\usepackage`-d) so it can run before `\documentclass`. |
| `owner.sty` | `\owner` identity (e.g. `llorracc` vs `econ-ark`). Kept separate so per-clone override is possible without touching `local.sty`. |
| `econtex_onlyinsubfile.tex` | Subfile-mode boilerplate (`\onlyinsubfile{}`, cross-reference setup) `\input`-ed by `Tables/*-subfile.tex` and `Figures-All.tex` when those compile in standalone mode. |

Plus the `auto/` LaTeX cache directory (gitignored) and a `@resources`
symlink to `../@resources` (lets standalone-compiled subfiles find
shared infrastructure when their cwd is here).

## Conventions

- New paper-local macros go in `local.sty`. Do not scatter them into
  body `.tex` files — the pre-commit hook
  (`tools/git-hooks/lint-no-inline-defs.sh`) blocks new inline defs in
  the published body files.
- Material that belongs to shared infrastructure (e.g.
  `econark-shortcuts.sty` in `@resources/texlive/`) is NOT moved here.
- The `\texname` macro, used by `\bibfilesfind{\texname}` and similar
  per-paper-named lookups, is unaffected by the local-side filename
  convention. It still names the master document (here
  `BufferStockTheory`); only `@local/`-side filenames are
  paper-agnostic.

## History

This layout was reached via the cleanup recorded in
`plans_private/20260430-1312h_trim-at-local-sty-files.md`, which
deleted six unused files and renamed `BufferStockTheory.sty` →
`local.sty`, `BufferStockTheory-tikz.sty` → `local-tikz.sty`. Earlier
state used the per-paper basenames and had two short-lived sibling
.sty files (`bst-macros.sty`, `bst-theorems.sty`) which were folded
into `local.sty` by the A5 phase of
`plans_private/20260430-1215h_streamline-tex-source-for-myst.md`.
