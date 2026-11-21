# Converting Complex LaTeX to MyST Markdown — A Practical Guide

**For maintainers (and future-me) of `tools/build-myst/`.**

This document distils what is currently known, publicly and from direct experiment, about converting a complex LaTeX academic paper into MyST Markdown — with particular attention to the constraints of `BufferStockTheory.tex`. It is intended as the single durable reference for decisions about the pipeline. When the world changes (new `mystmd` features, new tools, new bugs), update this file rather than re-discovering everything.

| Field | Value |
|---|---|
| Subject paper | `BufferStockTheory.tex` (~3,700 line MyST output, ~104 custom math macros, AMS theorems, `\harvarditem` bibliography, `\subfile` structure, `\ifthenelse{\boolean{Web}}` conditionals) |
| Targeted toolchain | `mystmd` v1.8.x (the JS/TypeScript CLI from `jupyter-book/mystmd`); pandoc as the core LaTeX→MD step |
| Last reviewed | 2026-04-28 |
| Sources | MyST official docs (`mystmd.org/guide`); the `jupyter-book/mystmd` issue tracker; the `econ-ark/REMARK` tracker; TU Delft TeachBooks; SciPy Proceedings; Curvenote engineering blog; LaTeXML; KaTeX; pandoc; `unified-latex` |

A note on scope: this guide is descriptive, not prescriptive. It catalogs what *is*, with enough sourcing that the reader can re-verify any claim. The current pipeline's design rationale is in `tools/build-myst/README.md`; this file complements that with the *why* and the *what-else*.

A note on location: this file lives at `tools/build-myst/CONVERSION-GUIDE.md`, beside the pipeline it documents.

---

## 1. Executive summary — the ten most important findings

1. **There is no shortcut. `myst init` over `BufferStockTheory.tex` does not produce a usable MyST file.** The mystmd LaTeX importer (`tex-to-myst`, built on `unified-latex`) handles maybe 70–80% of the paper's constructs cleanly, but the remaining 20–30% are exactly the parts that distinguish BST: Harvard-style bibliography (`\harvarditem`), conditional content (`\ifthenelse{\boolean{Web}}`), `subfiles` package, custom packages, cross-file text macros, optional-argument macros. The MyST docs themselves state this plainly: *"While MyST effectively handles a wide range of LaTeX documents, particularly scientific articles, it is not a full LaTeX renderer and is not aspiring to be one. As such, there will always be limitations on this approach."* — [mystmd.org/guide/writing-in-latex](https://mystmd.org/guide/writing-in-latex).

2. **We are not the first economists to walk this path.** [`econ-ark/REMARK#152`](https://github.com/econ-ark/REMARK/issues/152) is the Econ-ARK team's tracking issue with mystmd, opened by mystmd lead Rowan Cockett (`@rowanc1`) on 2024-03-26 and explicitly listing `BufferStockTheory` (cc'd `@llorracc`) under "Examples" with two checkboxes — "Conversion v1" and "Conversion v2" (linking to `BufferStockTheory-Latest/issues/135`). Many features the paper needs were added because of this push: recursive `\input` (PR #1082), shared math macros across files (PR #1156), the `extends:` mechanism (PRs #1215, #1251). What still has open boxes: `subfiles` package support, multi-argument math macros.

3. **The canonical place to declare math macros is `project.math:` in `myst.yml`, factored out via `extends:` into a separate file.** This is documented at [mystmd.org/guide/math#math-macros](https://mystmd.org/guide/math#math-macros) and at [mystmd.org/guide/configuration](https://mystmd.org/guide/configuration). Single-quote the YAML values to avoid backslash-escaping. The same definitions feed both KaTeX (HTML view) and the LaTeX export (PDF). Inline `$\newcommand{\a}{\alpha}$` does **not** work in current `mystmd` ([issue #2388](https://github.com/jupyter-book/mystmd/issues/2388)); macros from `\input`-ed files only flow into math contexts, not text contexts ([issue #1326](https://github.com/jupyter-book/mystmd/issues/1326)). The frontmatter is the only fully reliable channel.

4. **KaTeX is the HTML math renderer; everything must be KaTeX-compatible.** The official statement: *"The default MyST themes use KaTeX to render math in websites. […] Almost all math should work the exact same way [as MathJax], but if you were using more custom LaTeX or MathJax workflows, you may need to investigate how to port them to KaTeX."* — [mystmd.org/guide/math](https://mystmd.org/guide/math). KaTeX rejects `\if…/\else/\fi`, `\unicode{nnn}`, `\hyperlink`, `\DeclareMathOperator` (use `\operatorname{}`), `\verb` (partial), TikZ, and many text-mode T1-encoding glyph macros. There is no `\trust:true` opt-in in MyST, so `\href` inside math also fails. KaTeX's full support table is at [katex.org/docs/support_table](https://katex.org/docs/support_table).

5. **`\harvarditem` and `.bbl` files are unsupported by every tool in the chain.** mystmd, sphinxcontrib-bibtex, pandoc, and `unified-latex` all expect proper BibTeX (or BibLaTeX, CSL JSON, CSL YAML). The pragmatic path is to *generate a BibTeX file once* and reference it via `project.bibliography:` — or, where DOIs are present, to use MyST's automatic DOI resolution: `[](doi:10.5281/...)` is looked up against [doi.org](https://doi.org) and cached locally in `_build/`.

6. **AMS theorem environments map to MyST `:::{prf:*}` directives.** The official set is `prf:algorithm`, `prf:axiom`, `prf:assumption`, `prf:conjecture`, `prf:corollary`, `prf:criteria`, `prf:definition`, `prf:example`, `prf:lemma`, `prf:observation`, `prf:property`, `prf:proposition`, `prf:proof`, `prf:remark`, `prf:theorem` ([mystmd.org/guide/proofs-and-theorems](https://mystmd.org/guide/proofs-and-theorems)). Mapping is "Same as Sphinx Proof"; numbering is automatic, per-type by default.

7. **Conditional content (`\ifthenelse`, `\ifdvi`) must be stripped before mystmd sees the source.** No native MyST primitive matches `\ifthenelse{\boolean{Web}}{...}{...}`. The closest discussion is the AST-level "alternation" / `only` node concept in [PR #1961](https://github.com/jupyter-book/mystmd/pull/1961), not yet a stable user-facing feature. Pre-resolve at the source level.

8. **`\subfiles` is a *still-open* item on the Econ-ARK tracking list.** mystmd handles `\input` (recursively, since PR #1082) but not `\subfile{}`. Flatten upstream — which our existing Phase 1 already does.

9. **MyST gives genuinely good diagnostics — use `--debug --strict`.** Every error has a rule ID; severities can be tuned in `project.error_rules:`. The most important rules for BST are `math-renders` (KaTeX rejected an equation), `tex-parses`, `directive-known`, `reference-target-resolves`, `link-resolves`, and `bib-file-exists`. Run `myst --debug build --strict --check-links` in CI to fail loudly on any of them.

10. **The current 11-phase Python pipeline is the right architecture.** Three independent surveys (this guide's research base) converge on the same conclusion: keep pandoc + custom Python phases as the core; do not try to migrate to `myst init` alone. The pipeline encodes domain knowledge about Harvard bibliography, conditional content, and cross-file macro use that no off-the-shelf tool currently has. The right *augmentations* are: (a) add a generated math-macros YAML referenced from `myst.yml` via `extends:`; (b) extend Phase 11 to fail on KaTeX errors via `--strict`; (c) optionally migrate Phases 6–9 from string regex to pandoc Lua filters once string maintenance becomes painful.

---

## 2. The mystmd ecosystem

### 2.1 Two MySTs (do not confuse)

| Project | Language | Role | Status |
|---|---|---|---|
| `executablebooks/MyST-Parser` | Python | A Sphinx/Docutils extension that parses MyST Markdown into Sphinx's AST. Powers Jupyter Book v1. **No LaTeX import.** | Maintained, slower-moving |
| `jupyter-book/mystmd` | TypeScript | The standalone CLI (`myst`, `myst init`, `myst start`, `myst build`). Powers Jupyter Book v2. Includes `tex-to-myst`, `myst-to-tex`, JATS, Typst, Word, PDF export. | Active, monthly releases |

This guide assumes `mystmd` (the JS CLI). If a reader is searching the web and lands on a `myst-parser.readthedocs.io` page, that is the *other* project; only some semantics carry over.

### 2.2 Architecture under `myst build`

Per [mystmd.org/guide/writing-in-latex](https://mystmd.org/guide/writing-in-latex):

```
LaTeX source -> @unified-latex (PEG parser, by Jason Siefken)
                    |
                tex-to-myst (TS handlers per macro/env)
                    |
Markdown source -> markdown-it-myst (parser)
                    |
                MyST AST (myst-spec)
                    |
                transforms (links, citations, math macros, images, plugins)
                    |
        +---------+---------+---------+---------+
   myst-to-react  -tex      -typst    -docx     -jats
   (HTML site)   (PDF via  (PDF via  (Word)    (JATS XML)
                  jtex)     Typst)
```

Math is handled in a slightly distinct way: math nodes preserve raw TeX from the source verbatim, and KaTeX renders them at HTML emit time with `frontmatter.math` macros loaded as a dictionary. The same macros are also injected into the LaTeX preamble during `myst-to-tex` export (so the PDF gets `\newcommand{...}{...}` lines automatically).

### 2.3 The `tex-to-myst` capability envelope

The full official supported list lives at [mystmd.org/guide/writing-in-latex](https://mystmd.org/guide/writing-in-latex) under "Supported Environments and Macros". That page renders dynamically from the `tex-to-myst` package itself, so it is always current. Categories:

- **Macros** (~140): layout/whitespace, doc preamble, sectioning, inline formatting, cross-refs/links, citations (full natbib), diacritics & special chars, lists, float/figure machinery, footnotes, bibliography, includes (`\input`, *not* `\include`/`\subfile`), units (`siunitx`), algorithm/pseudocode (`algorithmicx`).
- **Environments** (~44): `document`, `abstract`, all major AMS math environments, lists, quotes, floats, tables (`tabular`/`tabularx`/`longtable` etc.), algorithms.

The macros explicitly handled include `\newcommand`, `\renewcommand`, `\providecommand`, `\def`, `\newtheorem`. They are stored in `state.data.macros` and registered as dynamic handlers — but with the cross-file caveat in §3.4 below.

What is *not* in the list (relevant to BST): `\subfile`, `\include`, `\ifthenelse`, `\ifdvi`, `\harvarditem`, `\bibitem`, `\nocite`, the `\Thorn` text-mode glyph (any of `wasysym`'s extras), `\xspace`, `\protect`, `\onlyinsubfile`, the entire `subfiles` package, the entire `harvard` package.

### 2.4 The `unified-latex` parser

Documented at [siefkenj.github.io/unified-latex](https://siefkenj.github.io/unified-latex/). Author Jason Siefken's own caveat (from the README): *"parsing LaTeX isn't possible since it effectively has no grammar, unified-latex makes some practical assumptions. It should work on your code, unless you do complicated things like redefine control sequences or embed complicated TeX-style macros."* Specifically does *not* handle `\def` argument signatures (admitted in the source comment: "it is too difficult to parse the argument signature of commands defined with `\def`").

Useful API for our purposes: `listNewcommands(tree)`, `expandMacros(tree, macros)`, `expandMacrosExcludingDefinitions(tree, macros)`. Could in principle support a "pre-expand all macros, then convert" workflow — but at the cost of the macro names being lost from the output.

---

## 3. Math and macros — the central topic

### 3.1 Schema (canonical)

From [mystmd.org/guide/math](https://mystmd.org/guide/math#math-macros):

```yaml
math:
  '\dobs':  '\mathbf{d}_\text{obs}'
  '\dpred': '\mathbf{d}_\text{pred}\left( #1 \right)'
  '\mref':  '\mathbf{m}_\text{ref}'
```

Rules (verbatim from the docs and from issue #2388):

- The key is the command **including the leading `\`**.
- Use **single quotes** around values. *"The single quote yaml syntax means you do not have to text-escape the strings, otherwise backslashes `\f`, `\n`, `\b`, `\r`, `\t` and other symbols have to be escaped which is difficult to remember and leads to all sorts of strange errors."*
- Arguments use `#1`, `#2`, … in the body. Argument count is inferred from the highest `#N` used.
- Macros may reference other macros (transitive closure resolved by KaTeX at render time).

### 3.2 `extends:` factoring (the recommended pattern at scale)

Documented at [mystmd.org/guide/configuration](https://mystmd.org/guide/configuration). For a project with >=30 macros, factor them out:

```yaml
# bst-math-macros.yml  (sibling of myst.yml)
version: 1
project:
  math:
    '\Rfree':         '\mathsf{R}'
    '\DiscFac':       '\beta'
    '\PermGroFac':    '\Gamma'
```

```yaml
# myst.yml
version: 1
extends:
  - bst-math-macros.yml
project:
  toc:
    - file: BufferStockTheory.md
```

Constraints (must follow):

1. The extended file must itself be a valid `myst.yml`-shaped document — it must include `version: 1` and `project:` (or `site:`).
2. **Avoid relative paths inside extended files.** Verbatim warning from the docs: *"Avoid using relative paths in extended configuration. Using relative paths in the configuration you're extending can lead to unpredictable outcomes, especially if the file you're extending is in a different folder or remote location."*
3. List fields in extended files are *concatenated*; dictionary fields are merged with later keys winning.
4. Closed by PRs [#1215](https://github.com/jupyter-book/mystmd/pull/1215) and [#1251](https://github.com/jupyter-book/mystmd/pull/1251); supported since `mystmd` >=1.5.

One reported caveat: a user noted in [issue #336](https://github.com/jupyter-book/mystmd/issues/336) that `extends:` was "ignored during PDF export" in at least one configuration. **Test PDF export early, not last.**

### 3.3 KaTeX rejection cheat-sheet (curated for BST)

KaTeX accepts almost all standard math, all AMS environments, all common Greek/script/blackboard fonts, all common operators. It rejects:

| Construct | Why | Fix |
|---|---|---|
| `\if…/\else/\fi`, `\ifx`, `\ifnum`, `\ifdvi` | KaTeX has no conditional machinery | Pre-strip from source |
| `\unicode{nnn}` | Not implemented | Embed the Unicode literal inside `\text{...}` |
| `\hyperlink{X}{Y}` | KaTeX has no hyperlink in math | Rewrite to `\textsf{Y}` (drop link; cross-refs are MyST anchors anyway) |
| `\DeclareMathOperator` | Not in KaTeX ([KaTeX#221](https://github.com/KaTeX/KaTeX/issues/221)) | Use `\operatorname{name}` directly, or define via `math:` as `'\name': '\operatorname{name}'` |
| `\TH`, `\AA`, T1-encoding text glyphs | KaTeX is math-only | Use `\text{...}` with a literal Unicode |
| `\verb`, `\verbatim` | Partial support | Move to code blocks (MyST handles those at the markdown level) |
| TikZ / pgfplots | Not implemented | Convert to image (export from LaTeX, embed via `\includegraphics`) |
| `\href`, `\color`, `\textcolor` (in math) | Requires `trust:true`, which MyST doesn't pass through | Use markdown link syntax outside math; for color, accept the warning or pre-render |
| `\mbox{...}` | Falls back to `\text{...}` automatically | Acceptable; KaTeX rewrites internally |

**For BST specifically**: the macros that demand translation rules are `\Thorn` (currently mis-defined in our orphan stub as `\unicode{1417}`, which is U+0589 Aramaic full stop — not a thorn), the `\hyperlink`-based `\GICRaw`/`\GICMod`/`\GICHarm`/`\FVAC`/`\RIC` family from `BufferStockTheory.sty`, and the few macros from the `econark-shortcuts.sty` package that wrap `\unicode{...}`.

### 3.4 The cross-file macro bug ([#1326](https://github.com/jupyter-book/mystmd/issues/1326))

Open since 2024-06-17. Verbatim:

> "If you have a macro that, for example, defines some text `\newcommand{\foo}{Bar}`, that will work fine in both a math and text context if they are on the same page. If the macro is included on the page (e.g. via an `input`) then that will work in math, but not in text. The macro creates a `state.data.dynamicHandlers` on the tex parser, which is not passed up to the parent TexProprietary. Only the frontmatter macros are shared, and then the math is re-parsed using katex."

**Implication for BST**: the paper's macros are spread across 7+ files (`econark-shortcuts.sty`, `local-macros.sty`, `BufferStockTheory.sty`, `econark-theorems.sty`, plus inline `\providecommand`s in `BufferStockTheory.tex`, `Introduction.tex`, and `Appendices/ApndxMTargetIsStable.tex`). Even if we kept LaTeX as the source of truth and used `myst init`, mystmd would only pick up macros from the file it's currently parsing. The frontmatter `math:` block — populated by us, from the canonical `.sty` files — is the one mechanism that works reliably across all files.

### 3.5 Macros that take arguments

`#1`, `#2` … in the YAML body, just like `\newcommand`. Marked as a "Stretch Goal — not yet supported" in REMARK#152: *"math macros (multiple arguments)"*. Single-argument is fine; double-argument may have issues. Verify per macro.

For BST, a quick survey shows most custom macros are zero-argument (`\Rfree`, `\DiscFac`, `\Ex`, `\GIC`, etc.) — but `\Rnd[1]{\pmb{#1}}` and a few wrappers are one-argument. Test these specifically when the YAML is generated.

### 3.6 The macro generator (`sty2myst.py`, prospective)

The recommended generator implementation:

1. **Walk `BufferStockTheory.tex` like LaTeX would**. Honour `\usepackage{...}` / `\input{...}` / `\subfile{...}` recursively. Honour `\ifthenelse`/`\ifdvi`/`\Draft{}` conditionals (re-using Phase 2's evaluator).
2. **Record every `\newcommand`, `\providecommand`, `\renewcommand`, `\DeclareMathOperator`, `\def\name{...}` encountered**, with `(name, body, file:line, kind)`. Honour real LaTeX scoping:
   - `\newcommand` overwrites unconditionally;
   - `\providecommand` only sets if not already set;
   - `\renewcommand` overwrites only if previously set, else log a warning.
3. **Apply translation rules** (the cheat-sheet in §3.3) to each body before emission.
4. **Closure-check**: every `\macro` referenced in any body must resolve to either another macro in the dictionary, a KaTeX builtin, or a deliberately-allowed external. Cycle-detect.
5. **Emit `bst-math-macros.yml`** as a `version: 1` + `project: math:` document, sorted by macro name for stable diffs, with single-quoted YAML scalars.
6. **Reference from `myst.yml`** via `extends: [bst-math-macros.yml]` (a one-line edit).

### 3.7 The orphan stub problem (root cause of the rendering bug)

Our pipeline currently has:

- `tools/build-myst/config/econark-math-macros.tex` — hand-curated, ~40 entries, **never plumbed in** (no Phase ever copies it to `_static/`, and there is no `_static/`).
- `tools/build-myst/config/frontmatter-template.yml` — has a `math:` block (~30 entries), but Phase 10 (`10_assemble_frontmatter.py`) doesn't read it.

Both are *dead artefacts that gave a false sense of completeness*. Delete after the generator lands.

The fundamental error in the original plan: it assumed *"KaTeX/MathJax in MyST renderers resolve them via `_static/econark-math-macros.tex` `\newcommand` definitions"*. That mechanism does not exist. MyST's only macro mechanism is the YAML `math:` block.

---

## 4. Bibliography — the second-hardest problem for BST

### 4.1 Supported formats

Per [mystmd.org/guide/citations](https://mystmd.org/guide/citations):

- **BibTeX `.bib`** — yes, fully supported.
- **BibLaTeX in `.bib`** — most types work via `citation-js` under the hood.
- **CSL JSON / CSL YAML** — supported indirectly through the same citation engine.
- **`.bbl`** — *unsupported*. The format is not mentioned anywhere in the docs, and `tex-to-myst` has no `\bibitem` handler.
- **`\harvarditem`** — *unsupported*. The `harvard` package is not in any tool's recognized package list (pandoc, `tex-to-myst`, `unified-latex`, Quarto, none of them).

### 4.2 The BST-specific challenge

`BufferStockTheory.tex` uses Harvard-style citations rendered through the `harvard` LaTeX package, which produces `.bbl` files containing `\harvarditem{Aiyagari (1994)}{Aiyagari}{1994}{aiyagari1994}{...}` entries. The original `.bib` file likely exists upstream, but the pipeline currently consumes the post-`bibtex` `.bbl` artefact.

The pragmatic options:

1. **Convert `.bbl` to MyST-AST citations once** (current Phase 5 in `lib/bbl_parser.py` does this — parses `\harvarditem` entries and emits hand-rolled citation markup). Continue this approach. It has zero dependency on upstream tools.
2. **Locate and use the original `.bib`** (if it exists) via `project.bibliography:`. Lower-friction but requires the upstream source.
3. **DOI-based citation** (`[](doi:10.1234/abc)`) where DOIs are present. MyST auto-resolves against `https://doi.org` and caches in `_build/`. Useful for new citations that don't have BibTeX entries yet.
4. **Pandoc round-trip**: `pandoc refs.bib -s -f biblatex -t csljson > refs.json` to convert non-BibTeX bibliographies. Documented at [pandoc.org/demo/example33/9.1-specifying-bibliographic-data.html](https://pandoc.org/demo/example33/9.1-specifying-bibliographic-data.html). Useful if the upstream is some other format.

The current pipeline's choice (Phase 5 parses `.bbl` directly) is the right one for the existing source. If the original `.bib` ever surfaces, switching to `bibliography:` is a one-line change.

### 4.3 Citation styles

> "The default citations are narrative, for numbered citations, these can be set in the `site.options.numbered_references` in your `myst.yml`."  
> — [mystmd.org/guide/citations](https://mystmd.org/guide/citations)

```yaml
site:
  options:
    numbered_references: true
```

There is **no documented CSL knob** for switching to APA/Chicago/Harvard. citation-js (under the hood) defaults to APA-ish. For a Harvard-style economics paper this is usually close enough, but expect minor formatting differences from the LaTeX print version.

### 4.4 BibTeX gotcha: `@string` macros

[Issue #2797](https://github.com/jupyter-book/mystmd/issues/2797), open as of April 2026, label `bug`: certain `@string{nt/f = ...}` macro names cause `Error: invalid syntax at line 1 col 11`, and `@string` definitions do not propagate across multiple `.bib` files. Workaround: pre-expand `@string` substitutions in the `.bib` before passing to MyST.

### 4.5 Citations inside figure captions

Known LaTeX-side build failure pattern: `! Argument of \Hy@tempa has an extra }` when a `\cite` appears inside `\caption{}`. Fix is preamble-side ([`AtBeginEnvironment{figure}{\pretocmd{\hyperlink}{\protect}{}{}}`](https://github.com/jupyter-book/jupyter-book/issues/1710)). Affects PDF export only; HTML output is unaffected.

---

## 5. Theorem environments and named conditions

### 5.1 The `prf:*` family

The full set ([mystmd.org/guide/proofs-and-theorems](https://mystmd.org/guide/proofs-and-theorems)):

`prf:algorithm`, `prf:axiom`, `prf:assumption`, `prf:conjecture`, `prf:corollary`, `prf:criteria`, `prf:definition`, `prf:example`, `prf:lemma`, `prf:observation`, `prf:property`, `prf:proposition`, `prf:proof`, `prf:remark`, `prf:theorem`.

Syntax (note: directives are wrapped in `:::` fences):

```
:::{prf:theorem} Title (optional)
:label: thm:contraction

Body of theorem here. Math via $...$ or $$...$$.
:::
```

Cross-reference with `[](#thm:contraction)` (renders as "Theorem 1") or `{prf:ref}` followed by a backtick-quoted label.

The implementation is documented as "Same as Sphinx Proof", so [Sphinx Proof tutorials](https://sphinx-proof.readthedocs.io/) apply.

### 5.2 Mapping LaTeX -> MyST

Our existing Phase 7 (`07_theorem_envs.py`) handles this. The mapping is mechanical:

| LaTeX | MyST |
|---|---|
| `\begin{theorem}[Title]\label{thm:foo}` | `:::{prf:theorem} Title` then `:label: thm:foo` |
| `\begin{lemma}` | `:::{prf:lemma}` |
| `\begin{corollary}` | `:::{prf:corollary}` |
| `\begin{definition}` | `:::{prf:definition}` |
| `\begin{proof}` | `:::{prf:proof}` |
| `\begin{remark}` | `:::{prf:remark}` |
| `\begin{proposition}` | `:::{prf:proposition}` |

`tex-to-myst` itself recognizes `\newtheorem{name}{Label}` and stores `state.data.theorems[name]`, then dispatches `\begin{name}` to a `proof` AST node with `kind: name`. So *if* we ever switch to `myst init`, this works for vanilla `\newtheorem` invocations. **Custom counter-based hand-rolled theorems** (e.g. `\newcounter{thm}\newcommand{\NewTheorem}[1]{...}`) are *not* recognized — see [issue #1606](https://github.com/jupyter-book/mystmd/issues/1606).

BST uses the standard `\newtheorem` machinery from `econark-theorems.sty`, so this would work even with `myst init`. Our explicit Phase 7 is doing the same job earlier in the pipeline.

### 5.3 Numbering

By default, each `prf:` kind gets its own counter. To make all theorem-like environments share one counter (LaTeX-typical behaviour), use the Sphinx-side option `prf_realtyp_to_countertyp` — but this is only available in the `myst-parser`/Sphinx path, not in `mystmd` JS CLI. For mystmd, accept per-type numbering or post-process labels manually.

### 5.4 Named conditions (BST-specific)

Macros like `\GIC`, `\FVAC`, `\GICMod`, etc. are *not* mathematical objects — they're stylistic shorthand for "Growth Impatience Condition," etc. The pipeline already handles this with two separate mechanisms:

1. **Text-mode contexts** (Phase 8b, `08b_named_condition_glosses.py`) — replaces `\GIC` in prose with English glosses from `tools/build-myst/config/named-conditions.yml`. First occurrence inserts the long form parenthetically; subsequent occurrences become markdown anchor links (`[growth impatience](#GIC)`).

2. **Math-mode contexts** — should be defined as frontmatter `math:` macros like `'\GIC': '\textsf{GIC}'`. These *bypass* Phase 8b (which only touches text contexts) and let KaTeX render the symbol consistently when used in equations.

Verified counts in the current `BufferStockTheory.md`: Phase 8b handles most named-condition occurrences (`\GIC`=0 surviving, `\FVAC`=0, `\GICMod`=0). What remains are math-mode occurrences: `\GICRaw` (5), `\RIC` (8), `\WRIC` (1), `\FHWC` (10), `\PFFVAC` (2). The math-macro YAML must define these.

---

## 6. Conditional content and subfiles

### 6.1 `\ifthenelse{\boolean{Web}}{...}{...}` and friends

Not handled by any tool in the chain. mystmd's `unified-latex` parses the tokens but does not evaluate them; the conditional and both branches are passed through (or hit `unhandled`). Pandoc's LaTeX reader handles only a small subset of TeX expansion semantics. KaTeX has no conditional machinery at all.

The closest MyST primitive is the `{raw:tex}` directive (one-direction injection of LaTeX-only content into PDF output, [issue #613](https://github.com/jupyter-book/mystmd/issues/613)) and the AST-level "alternation" nodes proposed in [PR #1961](https://github.com/jupyter-book/mystmd/pull/1961) — neither yet a stable user-facing feature.

**Pre-strip at the source level** (our existing Phase 2 does this). For BST, the `Web=true` branch is the one we want, since the goal is web rendering.

### 6.2 `\subfiles`

Listed as "Stretch Goal — not yet supported" in [REMARK#152](https://github.com/econ-ark/REMARK/issues/152). Open issue. mystmd handles `\input{file}` (recursively, since PR #1082) but not `\subfile{file}`.

**Flatten upstream** (our existing Phase 1, `_01_expand_inputs.py`). The flattening is a 50-line script and works.

### 6.3 The `\onlyinsubfile`/`\notinsubfile` pattern

BST uses a custom pattern: `\providecommand{\onlyinsubfile}{}\renewcommand{\onlyinsubfile}[1]{#1}` (i.e., expand to argument when in subfile context, expand to nothing otherwise). Pre-resolve in Phase 2, taking the `notinsubfile` branch (since we're flattening into the master).

---

## 7. Cross-references and figures

### 7.1 Anchor syntax

Per [mystmd.org/guide/cross-references](https://mystmd.org/guide/cross-references), labels are placed before the target. For a heading, place `(my-section)=` on the line immediately before the heading. For a directive, use the `:label:` option inside the `:::` fence. The `:label:` and `:name:` options are aliases for *every* directive.

### 7.2 LaTeX -> MyST mapping

| LaTeX | MyST |
|---|---|
| `\label{foo}` (in math env) | preserved by `tex-to-myst`; emits `:label: foo` |
| `\ref{foo}` | `[](#foo)` (preferred markdown link form) |
| `\eqref{foo}` | `[](#foo)` (renders as `(1)` for equations) |
| `\cref{foo}`, `\Cref{foo}` | `[](#foo)` (auto-fills "Figure 3" / "Theorem 2" / "Equation (1)") |
| `\autoref{foo}` | `[](#foo)` |
| `\nameref{foo}` | `[{name}](#foo)` |
| `\pageref{foo}` | dropped (web has no pages) |
| `\hyperref[foo]{text}` | `[text](#foo)` |

All the LaTeX side commands are in `tex-to-myst`'s supported list — so existing `\Cref{thm:contraction}` calls will convert automatically *if* the target has a label.

> "Note that targets without the `#` will resolve, however, they throw a deprecation warning. By including the `#` there is a better chance of your content working in other markdown renderers like GitHub or VSCode."  
> — [mystmd.org/guide/cross-references](https://mystmd.org/guide/cross-references)

Always use `[](#label)` form, not the deprecated `[](label)`.

### 7.3 Numbering of figures, equations, theorems

Default: figures, equations, tables, math, code blocks all numbered automatically; headings *not* numbered. Configured via `numbering:` in frontmatter:

```yaml
numbering:
  figure: true
  equation:
    enabled: true
    continue: true
  table: true
  headings: false
  enumerator: A1.%s
```

For BST, the equation-numbering convention is single-counter consecutive across the whole document — set `equation.continue: true`.

### 7.4 Figures with custom paths

LaTeX `\FigDir` macros: substituted at parse time by mystmd's macro engine (so `\includegraphics{\FigDir/foo.png}` becomes `\includegraphics{Figures/foo.png}`). Path must be a real, accessible file — relative to the source `.tex` for LaTeX builds, relative to the rendered `.md` for MyST.

Image-format support: PNG/JPG/GIF universal; SVG/PDF/EPS builder-specific. mystmd auto-converts where possible (via `imagemagick` and `inkscape` if on `$PATH`). For PDF output, animated GIFs cause issues in older Jupyter Book ([#627](https://github.com/jupyter-book/jupyter-book/issues/627)).

### 7.5 Subfigures

Supported in current mystmd. From the docs:

> "Subfigures can be created by omitting the directive argument to figure, and having the body contain one or more images or figures. These will be numbered as Figure 1a and Figure 1b, etc."

Caveat: subfigure labels are auto-generated as `<parent-label>-a`, `<parent-label>-b`. Cross-references work, but if the parent figure has *no* label, subfigure references fail silently. **Always label parent figures.**

### 7.6 External cross-references (`xref:`)

For linking to other MyST/Sphinx projects ([mystmd.org/guide/external-references](https://mystmd.org/guide/external-references)):

```yaml
project:
  references:
    spec: https://mystmd.org/spec
    python: https://docs.python.org/3.13/
```

Then `[Tables](xref:spec/tables#example)` or `xref:python#library/abc` (the latter for intersphinx). Each external project is downloaded once and cached in `_build/` as `myst.xref.json` (MyST projects) or `objects.inv` (Sphinx projects).

For BST's federation goal (linking to the future Bellman-DDSL hub), this is the natural mechanism.

---

## 8. Build, validation, and diagnostics

### 8.1 The `_build/` layout

```
project/
  _build/
    exports/        # PDFs, .docx, .tex, .md outputs
    site/
      content/    # AST JSON for each page
      public/     # static images, CSS, JS bundle
      config.json # site config snapshot
    temp/           # scratch space for tex/pdf builds
    templates/      # downloaded site/jtex templates
```

`myst clean --all` clears templates and the cache; `myst clean --templates --cache` is the same. By default `myst clean` keeps templates/cache.

### 8.2 Useful `myst build` flags

| Flag | What it does |
|---|---|
| `myst build` | Builds all configured exports + the site |
| `myst build --html` / `--site` | The static site bundle |
| `myst build --pdf` | PDF only (LaTeX path, requires `latexmk`) |
| `myst build --typst` | PDF via Typst |
| `myst build --docx` | Word only |
| `myst build --tex` | Raw LaTeX bundle |
| `myst build --md` | MyST markdown round-trip |
| `myst build --check-links` | Walks all external URLs, reports broken |
| `myst build --strict` | Exit non-zero on any error-level rule |
| `myst build --doi-bib` | Resolve DOIs and write `myst.doi.bib` |
| `myst --debug build` | Verbose logs, prints rule IDs |

For CI, `myst --debug build --strict --check-links` catches everything that matters.

### 8.3 Error rules and severity tuning

Configured under `project.error_rules:`. The relevant ones for BST:

| Rule | Default | Meaning |
|---|---|---|
| `math-renders` | error | KaTeX rejected the equation (the *primary* signal that macros are missing/wrong) |
| `math-eqnarray-replaced` | warn | `\begin{eqnarray}` rewritten to `align` |
| `math-equation-env-removed` | warn | nested `\begin{equation}` removed |
| `math-label-lifted` | warn | inner `\label{…}` extracted to MyST label |
| `directive-known` | error | unknown directive name |
| `role-known` | error | unknown role name |
| `reference-target-resolves` | warn | dangling `[](#foo)` |
| `link-resolves` | error | external URL 404 |
| `bib-file-exists` | error | bibliography file missing |
| `citation-renders` | error | citation-js failed on a key |
| `tex-parses` | error | input `.tex` did not parse |

To silence a specific URL pattern (e.g., a flaky external):

```yaml
project:
  error_rules:
    - rule: link-resolves
      severity: ignore
      keys:
        - 'https://flaky.example/**'
```

To find a rule ID for any logged message: `myst --debug build` prints rule IDs and keys with each event.

### 8.4 The "validator parses KaTeX output" pattern

Recommended for our pipeline: extend Phase 11 (`11_validate.py`) to invoke `myst build --html --strict`, parse stderr for "Undefined control sequence" / `math-renders` / KaTeX warnings, and assert zero of them. This is more authoritative than a static `katex-builtins.txt` allowlist — it uses KaTeX's actual parser to validate.

---

## 9. Patterns to follow

### 9.1 Single-source LaTeX, generated MyST

This is the workflow the [TU Delft TeachBooks team](https://teachbooks.tudelft.nl/jupyter-book-manual/helper_code/converter.html) uses for two converted textbooks, and the model implicit in [REMARK#152](https://github.com/econ-ark/REMARK/issues/152). Key principles:

- LaTeX is canonical (it produces the journal PDF; it's what we already maintain).
- MyST output is regenerated on every commit by the Python pipeline.
- The MyST output (`BufferStockTheory.md`) is committed to the repo for reviewability and durability, but never hand-edited.
- The pipeline's intermediate artefacts (`_build/`) are gitignored and regenerable.

The TU Delft team's framing: *"PDF generation: Jupyter Book is able to generate a PDF. However, if you have a LaTeX file it is better to construct your PDF from there."* — meaning the LaTeX pipeline already produces the print-quality PDF; MyST's job is only the web view.

### 9.2 Validate at every layer

The strongest signal that a conversion has silently regressed is "the build still passes but the output is wrong." Defences:

1. **Phase 11 (validator)** — `myst build --strict` ensures KaTeX errors surface.
2. **`make myst-site-check`** — asserts only one page is produced (matches `pdflatex`).
3. **Macro-coverage check** — every `\macro` token in the body is defined or KaTeX-built-in.
4. **Theorem-count check** — number of `:::{prf:theorem}` blocks in the output equals number of `\begin{theorem}` in the source.
5. **Citation-count check** — every `\cite{…}` becomes a `[](#cite-…)` anchor.
6. **`pre-commit` hook** — runs the document reproduction; commits fail if the regenerated output doesn't match the committed.

The current pipeline implements (1)–(2) and parts of (3)–(6). Each new generator (e.g. `sty2myst.py`) should add its own validator.

### 9.3 Pin the canonical sources, then derive

The maintenance burden of hand-curating is what kills these projects. The discipline:

- **Macros**: derive from `.sty` and `.tex` source via `sty2myst.py`. Don't hand-edit the YAML.
- **Bibliography**: derive from `.bbl` (or `.bib`) via Phase 5. Don't hand-edit the citations.
- **Cross-references**: derive from `\label`/`\ref` via Phase 6. Don't hand-edit the anchors.
- **Theorems**: derive from `\begin{theorem}` via Phase 7. Don't hand-edit the directives.
- **Frontmatter**: derive from `\title`/`\author`/`\abstract`/etc. via Phase 10.

The body of `BufferStockTheory.md` is *output*, not source. Treating it as source is how silent drift happens.

### 9.4 Explicit federation seam

`extends:` accepting URLs means the macro YAML can be hosted at a stable URL once Bellman-DDSL needs the same macros:

```yaml
# Bellman-DDSL's myst.yml
extends:
  - https://raw.githubusercontent.com/econ-ark/macros/main/econark-math-macros.yml
```

Build the seam now (single source repo, one URL), even if it's only used by BST initially.

---

## 10. Pitfalls to avoid

### 10.1 The "two canonicals" trap

Several public accounts (Ulysses-Pandoc thesis, Markdown-LaTeX templates, mystquarto) have one universal lesson: **maintaining two canonical sources is unsustainable.** Pick one. Generate the other. The Curvenote/journal model and the TU Delft model are both clear: LaTeX-canonical, MyST-generated.

### 10.2 Hand-curated subset files

The orphan stub `tools/build-myst/config/econark-math-macros.tex` is the cautionary example. ~40 hand-typed entries, never plumbed in, with at least one wrong glyph (`\Thorn = \unicode{1417}` is U+0589 Aramaic full stop, not a thorn). Any time someone says "we'll just maintain a small subset by hand," something like this is the eventual state.

The fix: derivative artefacts (the macro YAML) are *generated*, *committed*, and *regenerated automatically*. A `make ...-check` target in CI verifies the committed copy matches a fresh generation.

### 10.3 Silent KaTeX failures

KaTeX's default behaviour on an undefined macro is to render an error span and *continue*. The build doesn't fail; the page just has broken math. Without `myst build --strict` and parsing the warnings, you don't see this until you open the rendered HTML in a browser.

This is exactly how the original BST pipeline shipped a result that "looked good in the green-checkmark logs" but had broken math throughout. Don't repeat.

### 10.4 Inline `\providecommand` in body files

`Appendices/ApndxMTargetIsStable.tex` defines `\providecommand{\difFunc}{\pmb{\zeta}}` literally inside a paragraph. If the input-flattening phase passes this through unchanged, pandoc emits it as stray markup, the macro definition is lost, and KaTeX sees `\difFunc` undefined.

The fix: during `sty2myst.py` extraction, scan the source files line-by-line *and harvest these inline definitions too*. Then have Phase 2 strip them from the body before pandoc.

### 10.5 Trusting `myst init` over a complex paper

Three independent signals agree this doesn't work:

- The mystmd docs themselves: *"While MyST effectively handles a wide range of LaTeX documents, particularly scientific articles, it is not a full LaTeX renderer and is not aspiring to be one."*
- SciPy Proceedings (the most production-deployed real-world MyST workflow): *"Custom LaTeX macros are not supported and some packages may not be supported."*
- The Econ-ARK team's [REMARK#152](https://github.com/econ-ark/REMARK/issues/152) spent ~14 days of mystmd-feature work to make BST tractable, and `\subfiles` and multi-arg math macros are still open boxes.

`myst init` produces ~70–80% useable output for BST with a long error log. The remaining 20–30% is exactly the parts that would otherwise have been the pipeline's reason for existing.

### 10.6 Mistaking `myst-parser` for `mystmd`

When debugging, double-check which CLI is in use. `myst-parser` (Python, Sphinx) is *not* the same project as `mystmd` (TS, standalone). They share most of the markdown syntax but differ on extensions, math handling, theorem rendering details, and LaTeX import (only `mystmd` has it). A workaround that fixes one may not fix the other.

### 10.7 Macros defined in math but used in text (or vice versa)

mystmd issue [#1326](https://github.com/jupyter-book/mystmd/issues/1326): cross-file text-context macros silently fail. Putting the macros in frontmatter `math:` works for *math-context* uses everywhere, including across files. For text-context macros (e.g., `\econark` for inline branding text), the workaround is to define them via project-level `math:` *and* always use them inside `$...$` (single-character math mode) — or to expand them in a pre-processing step (Phase 2/3).

### 10.8 Latexmkrc breakage

[Issue #1855](https://github.com/jupyter-book/mystmd/issues/1855): a global `~/.latexmkrc` can hijack `myst build --pdf`. Ensure project-local `.latexmkrc` overrides or pass `-norc` if needed.

---

## 11. The BufferStockTheory.tex specifics

### 11.1 The macro inventory (verified 2026-04-28)

| Source file | `\newcommand`+`\providecommand` count | Notes |
|---|---|---|
| `@resources/texlive/texmf-local/tex/latex/econark-shortcuts.sty` | 309 | Econ-ARK community macros (`\Rfree`, `\DiscFac`, `\Ex`, `\APFac`, `\Thorn`, `\GIC`, `\FVAC`, …) |
| `@local/local-macros.sty` | 133 | Project-local DDSL/three-stage notation |
| `@local/BufferStockTheory.sty` | 57 | Paper-specific named conditions and bounds (uses `\hyperlink{}{\textrm{}}` heavily) |
| `BufferStockTheory.tex` | inline `\providecommand{\Thorn}{\pmb{\TH}}` | Defines `\Thorn` via wasysym/T1 fallback |
| `Introduction.tex` | inline `\newcommand{\APFacRaw}` | Body-file inline macro |
| `Appendices/ApndxMTargetIsStable.tex` | inline `\providecommand{\difFunc}{\pmb{\zeta}}` | Inside paragraph! |
| `econark-theorems.sty` | 5 (`\def\liminf`, `\def\var`, `\def\cov`, `\def\std`, `\def\argmax`) | Math-operator defs |
| `econark_demacro_demacro.sty` | 286 | **NOT** loaded by this paper; ignore |

Macros actually referenced in `BufferStockTheory.md` (post-pipeline): 207 distinct tokens; 92 KaTeX builtins; 104 real custom macros; 12 stragglers (mix of KaTeX builtins my heuristic missed and inline-defined macros not yet harvested). 0 currently defined in the YAML frontmatter.

### 11.2 The conversion-v2 connection

`BufferStockTheory` is listed in [REMARK#152](https://github.com/econ-ark/REMARK/issues/152) under "Examples":

```
- https://github.com/econ-ark/BufferStockTheory (and latest)
  - [x] new theorem support
  - [ ] Conversion v1
  - [ ] Conversion v2 - https://github.com/llorracc/BufferStockTheory-Latest/issues/135
```

Both conversion checkboxes are open; Conversion v2 explicitly references the repo this guide lives in. The work this pipeline is doing *is* the Conversion v2 effort.

Practical implication: file specific minimal-reproducer issues against `jupyter-book/mystmd` whenever we hit limits. The maintainers are receptive — most of the "checked" features in the tracker were added because of this issue. This is not a hostile project.

### 11.3 What's already in the pipeline (high level)

| Phase | Script | Job |
|---|---|---|
| 1 | `_01_expand_inputs.py` + `01_resolve_inputs.sh` | Recursively inline `\input{}` and `\subfile{}` |
| 2 | `02_strip_conditionals.py` | Resolve `\ifthenelse{\boolean{Web}}{...}{...}`, `\Draft{}`, `\onlyinsubfile`, etc. |
| 3 | `03_normalize_macros.py` | Pre-expand text-context macros; emit named-condition placeholders |
| 4 | `04_pandoc_convert.sh` | Pandoc LaTeX->MD with carefully chosen extensions |
| 5 | `05_resolve_citations.py` | Parse `\harvarditem` from `.bbl`; emit MyST citation markup |
| 6 | `06_resolve_xrefs.py` | `\ref`/`\eqref`/`\Cref` -> `[](#anchor)` |
| 7 | `07_theorem_envs.py` | `\begin{theorem}` -> `:::{prf:theorem}` |
| 8a | `08a_paragraphs_and_figs.py` | Figure directives, paragraph cleanup |
| 8b | `08b_named_condition_glosses.py` | `\GIC` (text) -> "growth impatience condition" + anchor links |
| 9 | `09_strip_frontmatter.py` | Remove residual LaTeX preamble from body |
| 10 | `10_assemble_frontmatter.py` | Build YAML frontmatter from `\title`/`\author`/etc. |
| 11 | `11_validate.py` | End-to-end checks |

### 11.4 What's missing (as of 2026-04-28)

1. **Math macros in frontmatter** — the central finding of this guide. Add a Phase 0a (`sty2myst.py`) and an `extends:`-referenced `bst-math-macros.yml`.
2. **Phase 11 KaTeX-error parsing** — the validator currently checks structure, not rendering. Add `myst build --strict` + stderr parsing.
3. **Inline-`\providecommand`-in-body harvesting** — the `\difFunc` and `\Thorn` cases.
4. **Cycle/closure check** in the macro generator — to catch macros that reference undefined macros transitively.

### 11.5 What's intentionally not in the pipeline

- **Direct `myst init` over `BufferStockTheory.tex`** — covered in §10.5. Won't work.
- **LaTeXML as a parser** — would handle the hardest constructs (Harvard, conditionals, custom packages) at the cost of Perl + per-package binding files. Heavyweight; defer until something specific demands it.
- **Pandoc Lua filters replacing Phases 6–9** — would simplify some regex code but adds Lua as a maintenance language. Defer until string maintenance becomes painful.
- **Quarto** — no LaTeX-input advantage over MyST; same pandoc limitations.

---

## 12. Decisions reference card

When in doubt, default to:

| Question | Answer |
|---|---|
| Where do macros live? | `bst-math-macros.yml` (sibling of `myst.yml`), referenced via `extends:` |
| How are macros generated? | `sty2myst.py`, walking `BufferStockTheory.tex`'s `\usepackage`/`\input` graph |
| Where do citations come from? | `.bbl` parsing in Phase 5 (no `.bib` available; `\harvarditem` handled directly) |
| What's the source of truth for the body? | `BufferStockTheory.tex` and its included files. Never hand-edit `BufferStockTheory.md`. |
| What's the canonical PDF path? | `pdflatex BufferStockTheory.tex` (LaTeX-side). `myst build --pdf` is for the web preview if ever needed. |
| Web math renderer? | KaTeX 0.16.x, bundled with `mystmd` |
| Build CLI for CI? | `myst --debug build --strict --check-links` |
| When does a build fail? | Any error-level rule fires (math-renders, link-resolves, bib-file-exists, etc.) |
| Where do downloaded templates live? | `_build/templates/` (gitignored) |
| Where does the published site live? | `_build/site/` (gitignored, regenerable) |
| What's committed? | `BufferStockTheory.md`, `myst.yml`, `bst-math-macros.yml`, `tools/build-myst/`, `references.bib` if present |

---

## 13. Sources, with URLs and accessed dates (2026-04-28)

### Official MyST documentation

- [mystmd.org/guide](https://mystmd.org/guide) — Top-level
- [mystmd.org/guide/math](https://mystmd.org/guide/math) — *the* math reference
- [mystmd.org/guide/writing-in-latex](https://mystmd.org/guide/writing-in-latex) — LaTeX-import support envelope (live, regenerated dynamically from `tex-to-myst`)
- [mystmd.org/guide/configuration](https://mystmd.org/guide/configuration) — `myst.yml` schema, `extends:`
- [mystmd.org/guide/frontmatter](https://mystmd.org/guide/frontmatter) — Field reference
- [mystmd.org/guide/citations](https://mystmd.org/guide/citations) — Bibliography
- [mystmd.org/guide/cross-references](https://mystmd.org/guide/cross-references) — `[](#label)` mechanics
- [mystmd.org/guide/proofs-and-theorems](https://mystmd.org/guide/proofs-and-theorems) — `prf:*` directive family
- [mystmd.org/guide/settings](https://mystmd.org/guide/settings) — Error rules catalogue (95+ rules)
- [mystmd.org/guide/external-references](https://mystmd.org/guide/external-references) — `xref:` mechanism for federation
- [mystmd.org/guide/creating-pdf-documents](https://mystmd.org/guide/creating-pdf-documents) — PDF export via jtex
- [mystmd.org/guide/plugins](https://mystmd.org/guide/plugins) — Extension hooks

### `jupyter-book/mystmd` issue tracker (canonical bug references)

- [#336 "Separate math macros file"](https://github.com/jupyter-book/mystmd/issues/336) — closed by `extends:` (PRs #1215, #1251)
- [#1326 "LaTeX: Text based macros not working"](https://github.com/jupyter-book/mystmd/issues/1326) — open; cross-file text macros
- [#2388 "Inline `$\newcommand{...}{...}$` not honoured"](https://github.com/jupyter-book/mystmd/issues/2388) — open
- [#1606 "Custom proof environments from LaTeX"](https://github.com/jupyter-book/mystmd/issues/1606) — open
- [#280 "Support optional arguments in math macros"](https://github.com/jupyter-book/mystmd/issues/280) — open
- [#2797 "BibTeX `@string` replacements"](https://github.com/jupyter-book/mystmd/issues/2797) — open, label `bug`
- [#1855 "global latexmkrc breaks PDF"](https://github.com/jupyter-book/mystmd/issues/1855)
- [#2442 "MathJax vs KaTeX"](https://github.com/jupyter-book/mystmd/issues/2442)
- [PR #1961 "Parse Markdown and LaTeX outputs into AST"](https://github.com/jupyter-book/mystmd/pull/1961) — discusses `only` AST nodes for conditional content
- [PR #1156 "Frontmatter in `include` files"](https://github.com/jupyter-book/mystmd/pull/1156) — math/abbreviations across files

### Econ-ARK / BST-specific

- [econ-ark/REMARK#152 "Improvements to MyST Markdown"](https://github.com/econ-ark/REMARK/issues/152) — *the* tracking issue, lists BufferStockTheory under "Examples" with "Conversion v2" still open

### Real-world conversion case studies

- TU Delft TeachBooks: [latextomarkdown.py + cleanlatex.py](https://teachbooks.tudelft.nl/jupyter-book-manual/helper_code/converter.html) (converted two textbooks)
- SciPy Proceedings 2024–2026: [github.com/scipy-conference/scipy_proceedings](https://github.com/scipy-conference/scipy_proceedings/blob/2026/README.md) (warns "Custom LaTeX macros are not supported")
- Curvenote launch blog: [How to use LaTeX with MyST Markdown](https://curvenote.com/blog/how-to-use-latex-with-myst-markdown) (Aug 2022, by Rowan Cockett, mystmd lead)
- QuantEcon: [github.com/quantecon/lecture-python.myst](https://github.com/quantecon/lecture-python.myst) (major real-world economics MyST deployment)
- Tingkai Liu: [latex-to-myst Pandoc filter](https://www.tingkai-liu.org/latex-to-myst/readme.html) (one-author Pandoc filter, Nov 2021, v0.0.1, *not* actively maintained)

### Tooling references

- [pandoc.org/MANUAL.html](https://pandoc.org/MANUAL.html) — pandoc User's Guide
- [pandoc.org/lua-filters.html](https://pandoc.org/lua-filters.html) — Lua filter reference
- [pandoc.org/demo/example33/8.15-latex-macros.html](https://pandoc.org/demo/example33/8.15-latex-macros.html) — `latex_macros` extension
- [pandoc.org/demo/example33/9.1-specifying-bibliographic-data.html](https://pandoc.org/demo/example33/9.1-specifying-bibliographic-data.html) — Bibliography conversion
- [github.com/siefkenj/unified-latex](https://github.com/siefkenj/unified-latex) — The TS LaTeX parser under mystmd
- [siefkenj.github.io/unified-latex](https://siefkenj.github.io/unified-latex/) — `unified-latex` API docs
- [github.com/brucemiller/LaTeXML](https://github.com/brucemiller/LaTeXML) — Perl LaTeX->XML converter (highest-fidelity, used by arXiv/DLMF)
- [katex.org/docs/support_table](https://katex.org/docs/support_table) — KaTeX command support matrix (alphabetical)
- [katex.org/docs/supported.html](https://katex.org/docs/supported.html) — KaTeX command support matrix (categorical)
- [github.com/KaTeX/KaTeX/issues/221](https://github.com/KaTeX/KaTeX/issues/221) — Why KaTeX has no `\DeclareMathOperator`

### Background reading

- [sphinx-proof.readthedocs.io](https://sphinx-proof.readthedocs.io/) — Reference for mystmd's `prf:*` directives
- [jupyterbook.org](https://jupyterbook.org) — Jupyter Book v2 (built on mystmd)
- [jtex (mystmd's LaTeX templating engine)](https://mystmd.org/jtex/) — `myst-to-tex` underpinnings

---

## 14. Maintenance protocol

When updating this document:

1. **Add the new finding to the relevant section.** Don't reorganise; reorganisation is what makes guides go stale.
2. **Cite the source URL and the date you accessed it.** Even mystmd's own docs change every release; what was true six months ago may not be now.
3. **Update §1 (Executive summary)** if the new finding contradicts or refines one of the ten points.
4. **Update §11 (BST-specifics)** if the new finding affects our specific paper.
5. **Update §12 (Decisions reference card)** if the new finding changes a default.
6. **Update the date in the front matter.**

If the world has changed enough that this guide is more wrong than right, archive it (rename to `*-2026-04-28-archived.md`) and write a new one rather than patching extensively.

---

*End of guide. Generated from three parallel research passes on 2026-04-28: MyST official documentation deep-read, community case-study survey (TU Delft, SciPy, Curvenote, REMARK, et al.), and tooling landscape comparison (pandoc, mystmd, unified-latex, LaTeXML, Quarto).*
