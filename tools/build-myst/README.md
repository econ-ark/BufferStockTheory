# `tools/build-myst/` — LaTeX → MyST Markdown Pipeline

Converts the multi-file LaTeX source of `BufferStockTheory` into a single
self-contained MyST Markdown document (`BufferStockTheory.md` at repo root).

Designed to be re-run on every paper edit via a single command.

## Quick start

```bash
cd $(git rev-parse --show-toplevel)
bash tools/build-myst/build.sh           # ~2 minutes warm; longer cold
```

From the repo root:

```bash
make myst              # rebuild BufferStockTheory.md
make myst-clean        # delete _build/myst/ and BufferStockTheory.md
make myst-test         # pytest tools/build-myst/tests/
make myst-validate     # re-run only the validation phase
make myst-site         # rebuild _build/site/ via mystmd CLI (1 page)
make myst-site-clean   # delete _build/site/
make myst-site-check   # assert exactly one content page in the site
```

## Pipeline phases

| # | Phase | Output | Purpose |
|---|---|---|---|
| 01 | `01_resolve_inputs.sh` | `_build/myst/01_flat.tex` | `latexpand` flattens `\input{}` chain (incl. `.bbl`) |
| 02 | `02_strip_conditionals.py` | `_build/myst/02_stripped.tex` | Drop `\ifthenelse{\boolean{Web}}`, `\begin{comment}`, frontmatter machinery |
| 03 | `03_normalize_macros.py` | `_build/myst/03_normalized.tex` | Rewrite custom commands; emit `<<CITE:...>>`, `<<ANCHOR:...>>`, `<<XREF:...>>`, `<<NAMED:...>>` placeholders |
| 04 | `04_pandoc_convert.sh` | `_build/myst/04_raw.md` | Pandoc latex → markdown |
| 05 | `05_resolve_citations.py` | `_build/myst/05_with_cites.md` | `<<CITE:...>>` → inline `(Author, Year)`; emit `## References` section |
| 06 | `06_resolve_xrefs.py` | `_build/myst/06_with_xrefs.md` | `<<ANCHOR:>>`/`<<XREF:>>`/`\eqref`/`\Cref` → MyST forms |
| 07 | `07_theorem_envs.py` | `_build/myst/07_with_theorems.md` | `\begin{theorem}` → `:::{prf:theorem}` |
| 08a | `08a_paragraphs_and_figs.py` | `_build/myst/08a_polished.md` | `\paragraph` → `###`; figure directives |
| 08b | `08b_named_condition_glosses.py` | `_build/myst/08b_glossed.md` | First-occurrence English gloss for `\GIC`, `\PFGIC`, etc. |
| 09 | `09_strip_frontmatter.py` | `_build/myst/09_clean.md` | Drop residual `<div>` blocks, TOC, list-of-figs |
| 10 | `10_assemble_frontmatter.py` | `_build/myst/10_final.md` | Prepend MyST YAML frontmatter |
| 11 | `11_validate.py` | (assertions) | `myst build` smoke test + privacy audit + grep probes |

Final committed artifact: `BufferStockTheory.md` at repo root, copied from
`_build/myst/10_final.md` by `build.sh`.

## Design constraints

- **Idempotent.** Re-running on unchanged source produces bit-identical output.
- **Privacy-safe.** No `*_private*`, `@local/`, `paperpile_private.bib` content reaches output.
- **Self-contained output.** Single `BufferStockTheory.md` + small `_static/` (only `econark-math-macros.tex` plus referenced figure files).
- **Failure-loud.** Any phase failure aborts with clear stderr; partial output never claimed as complete.
- **Per-phase caching.** Each phase records sha256 of its input; unchanged inputs skip re-computation.

## Configuration

| File | Purpose |
|---|---|
| `config/pipeline.yml` | Per-phase toggles, paths |
| `config/named-conditions.yml` | `\GIC` → "growth impatience condition", etc. |
| `config/theorem-mapping.yml` | `\begin{theorem}` → `prf:theorem`, etc. |
| `config/econark-math-macros.tex` | `\newcommand` defs shipped to renderers via `_static/` |
| `config/frontmatter-template.yml` | Skeleton for YAML frontmatter |

## Testing

```bash
pytest tools/build-myst/tests/
```

Unit tests cover each phase in isolation against fixtures in `tests/golden/`.
The end-to-end test runs the full pipeline on a 50–80-line "tiny BST" fixture.

## Troubleshooting

- **Phase fails with "command not found":** ensure `latexpand`, `pandoc`, `myst` are on `$PATH`. On macOS: `brew install pandoc`; `latexpand` ships with TeX Live; `npm i -g mystmd`.
- **Phase 11 reports unresolved citations:** check `_build/myst/05_unresolved_cites.txt` — these are keys cited in the paper but absent from `BufferStockTheory-Add-Refs.bib`. Either add them to the public bib or fix the cite key.
- **Phase 11 privacy audit fails:** look at the audit report — usually a stray local filesystem path or email leaked through. Clean the offending source line and re-run.
- **Want to inspect intermediate output:** every phase's output sits in `_build/myst/` for the lifetime of the build.

## Public site scope (`myst build`)

The `mystmd` CLI (`myst build --html`) is intentionally restricted to the
single page produced by this pipeline.  The contract is:

> Running `myst build --html` must produce exactly the content that
> `pdflatex BufferStockTheory.tex` produces — no more, no less.

This is enforced by two layers in [`myst.yml`](../../myst.yml):

1. **`project.toc`** explicitly lists `BufferStockTheory.md` as the sole page,
   which disables `mystmd`'s default whole-tree auto-discovery.
2. **`project.exclude`** patterns provide defence-in-depth: even if the TOC
   were ever dropped, notebooks under `Code/`, alternate LaTeX variants
   (`BufferStockTheory-Slides.*`, `Appendices-All-Referenced.*`, etc.),
   subfile sources (`Appendices/`, `Introduction.tex`, …), the pipeline
   itself (`tools/`), and private notes (`plans_private/`, `*_private*`)
   are explicitly skipped.

To rebuild and verify the public site:

```bash
make myst-site         # rm -rf _build/site && myst build --html
make myst-site-check   # asserts exactly 1 content page
```

If `make myst-site-check` fails, either `myst.yml` was edited or a new
top-level `.md`/`.ipynb`/`.tex` file was added that matches no `exclude`
pattern.  Update the `exclude:` list to keep the site scoped.

**Note.** When the LaTeX paper itself starts referencing additional content
(e.g. a new `\subfile{}`), the canonical fix is in this pipeline — make the
new content land inside `BufferStockTheory.md`.  Adding new entries to
`project.toc` would silently desynchronise the site from the PDF.
