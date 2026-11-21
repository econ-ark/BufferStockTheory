# `_ai/` — machine-legible companions to *BufferStockTheory*

This tree holds AI/RAG-oriented artifacts derived from the paper
`BufferStockTheory.md`. It is *generated and curated for machine consumption*
— the artifacts describe, critique, and (in the review layer) propose fixes to
the paper. The subtrees:

## [`concepts/`](concepts/) — the rendered concept atlas

A curated, machine-readable graph of the paper's named scholarly objects
(patience conditions, theorems, definitions) with, for each concept: its
defining equation, an English gloss, typed cross-references to other concepts,
and source anchors back into `BufferStockTheory.md`. The atlas exists to make
the paper's math legible to AI/RAG tooling.

- **What it is:** one rendered `<id>.md` page per concept, plus an
  [`index.md`](concepts/index.md) with a one-line gloss and relation summary
  per concept. Start at the index.
- **Source of truth:** these `.md` pages are **rendered artifacts** — the
  authored source is the YAML in [`../concepts/`](../concepts/) (`<id>.yml`),
  one file per concept, following [`../concepts/_schema.yml`](../concepts/_schema.yml).
  See [`../concepts/README.md`](../concepts/README.md) for authoring and review
  status.
- **How it is regenerated** (PyYAML required; use the interpreter that has it):

  ```
  python3 tools/concepts_validate.py    # schema + no-line-number checks
  python3 tools/concepts_render.py      # regenerates _ai/concepts/*.md + index.md
  python3 tools/concepts_freshness.py   # asserts #YAML == #rendered == #index
  ```

  Never hand-edit the rendered `.md`; edit the YAML and re-render. The
  freshness check is the authority on the concept count (do not trust any
  frozen number in prose).

## [`audit/`](audit/) — the adversarial mathematical audit

A hostile **disprove-or-improve** audit of the paper's mathematics: every
named result was attacked as hard as possible, and the verdicts, genuine gaps,
and machine-checkable probes are recorded. This is where refutations and rigor
gaps live.

- **What it is:** 27 per-result dossiers (`<anchor>.md`), 3 cross-cutting
  documents (`paper-map.md`, `notation-and-assumptions.md`,
  `conditions-lattice.md`), and a consolidated probe harness
  `verify_claims.py`. Start at [`audit/README.md`](audit/README.md), which
  carries the full dossier index, the attack-surface ranking, and the known
  findings.
- **Headline findings:** 2 refutations (fact-xnconvgf false as stated;
  remark-ricstationary C3 clause false), 23 gap-found (true results with
  genuine written-proof holes — most repairable in one line), 1 slack-found
  (claim-gicimpliesharmimp), 1 survived (claim-MPCMAXKleq1).
- **When to re-run:** whenever `BufferStockTheory.md` changes near an audited
  result, or before relying on a dossier's verdict. Run:

  ```
  python3 _ai/audit/verify_claims.py
  ```

  Pure stdlib (no numpy/scipy), <60s. Expect **79 PASS, 3 KNOWN_FAIL, exit 0**;
  the 3 KNOWN_FAIL are documented findings, any *other* FAIL is a regression.

## [`review/`](review/) — the adjudicated review package

The human-facing packaging of the audit: the proposed edits, their adjudication
into concrete LaTeX-source fixes, and the provenance/methodology that document
how the review was produced. Where `audit/` is the raw evidence, `review/` is
what an author reviews and acts on.

- **What it is:** [`PROPOSALS.md`](review/PROPOSALS.md) (the 27 proposed edits,
  ordered high→low severity — start here), [`ADJUDICATION.md`](review/ADJUDICATION.md)
  (each finding expanded into a proposed `.tex` edit naming the source file +
  label), [`PROVENANCE.md`](review/PROVENANCE.md) (which model produced what, on
  which dates), [`METHODOLOGY.md`](review/METHODOLOGY.md) (the protocol and the
  epistemic-status tiers), and [`prompts/`](review/prompts/) (the verbatim
  originating request and the workflow script).
- **Status on this branch:** the proposed fixes **have been applied to the
  LaTeX source** (`sections/`, `Appendices/`), so this branch's
  `BufferStockTheory.md` already incorporates them. The theorem *statements* are
  unchanged; the edits repair written-proof holes and replace the two `refuted`
  auxiliary lemmas with the true statements their use-sites need. Human
  domain-expert adjudication remains the final authority (the review is
  AI-generated).

## [`digests/`](digests/) — digests of the paper for other projects

Self-contained statements of what the paper says, written for a reader who will build something
from it and should not have to read the proofs. Each claim is tagged as stated in the paper (with
its LaTeX label), derived from it, or not in the paper.

- [`digests/buffer-stock-model-for-HARK.md`](digests/buffer-stock-model-for-HARK.md): the model,
  its income process, parameters, conditions, limits and bounds, the liquidity-constrained case,
  what the paper leaves open, and where HARK's `IndShockConsumerType` departs from the paper.
  Written 2026-11-11 for the HARK class `ConsBufferStockModel`. Its check scripts are in
  `digests/checks/`. On 2026-11-12 it gained a section on the appendix "Positive Minimum
  Income", which so far exists only on branch `20261111-positive-minimum-income`.
- Digests are private working documents: nothing in them goes public without Chris's word.

## Relationship between the subtrees

The atlas (`concepts/`) is the **descriptive** layer — what the paper's objects
mean and how they relate. The audit (`audit/`) is the **adversarial** layer —
whether the proofs actually deliver. The review (`review/`) is the
**corrective** layer — the adjudicated fixes, now applied to the LaTeX source.
They cross-reference each other: audit dossiers cite concept ids; several audit
findings flag defects mirrored in atlas glosses (e.g. the `\Reals_+`-vs-`\Reals_{++}`
codomain and the false-`F(s)/s` argument); and `review/ADJUDICATION.md` maps
each finding to the source edit that repairs it.

## Citation discipline (all subtrees)

**Stable anchors only, never line numbers.** Citations point to `eq-…`,
`thm-…`, `prop-…`, `lemma-…`, `claim-…`, `ass-…`, `sec-…` anchors in
`BufferStockTheory.md`. Line-number citations rot across re-renders and are
rejected by `tools/concepts_validate.py`.
