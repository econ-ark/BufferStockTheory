#!/usr/bin/env python3
"""Phase 09: Final cleanup of residual frontmatter, raw HTML, and pandoc attributes.

Reads:  _build/myst/08b_named_glosses.md
Writes: _build/myst/09_clean.md

Cleanup operations:

1. Strip residual `<div ...>...</div>` and `<span ...>...</span>` blocks
   that pandoc emitted for unrecognised LaTeX environments.
2. Drop pandoc inline attribute markers:  `{.uri}`, `{.someclass}`, `{#id}`,
   and link attributes appended to the rendered link.
3. Drop the auto-generated heading anchor suffix `{#heading-slug}` because
   the explicit `(label)=` MyST anchors emitted by Phase 6 already provide
   stable cross-reference targets.
4. Strip stray empty `(=` / `()` / `()=` artefacts left by earlier phases.
5. Collapse runs of >2 blank lines.
6. Remove the boilerplate links/acknowledgements block at the very top of
   the document (between the abstract anchor and the first heading) — its
   contents are kept in the YAML frontmatter (Phase 10) under
   `acknowledgements:` and `links:`.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.label_clusters import (  # noqa: E402
    case_normalize_references,
    dedent_indented_label_lines,
    merge_adjacent_label_clusters,
    wrap_labelled_tables_in_directives,
)
from lib.safe_io import build_path, read_text, write_text  # noqa: E402


# Strip <div>...</div> and <span>...</span> with any attributes; non-greedy.
_DIV_RE = re.compile(r"<div\b[^>]*>(.*?)</div>", flags=re.DOTALL | re.IGNORECASE)
_SPAN_RE = re.compile(r"<span\b[^>]*>(.*?)</span>", flags=re.DOTALL | re.IGNORECASE)
# Pandoc inline attributes: `[link](url){.class}`, `[text]{#id}`, `{.uri}`.
_INLINE_ATTR_RE = re.compile(r"\{\.[A-Za-z0-9_-]+\}|\{#[A-Za-z0-9_:.-]+\}")
# Heading anchor suffix `# Heading {#slug}`.
_HEADING_ATTR_RE = re.compile(
    r"^(#{1,6}\s+.*?)\s*\{#[A-Za-z0-9_:.-]+\}\s*$",
    flags=re.MULTILINE,
)
# Stray empty anchors `()=` produced by earlier phases.
_EMPTY_ANCHOR_RE = re.compile(r"^\(\s*\)=\s*$", flags=re.MULTILINE)


def strip_html_blocks(text: str) -> tuple[str, int, int]:
    n_div = len(_DIV_RE.findall(text))
    text = _DIV_RE.sub(lambda m: m.group(1), text)
    n_span = len(_SPAN_RE.findall(text))
    text = _SPAN_RE.sub(lambda m: m.group(1), text)
    return text, n_div, n_span


def strip_attributes(text: str) -> str:
    text = _INLINE_ATTR_RE.sub("", text)
    text = _HEADING_ATTR_RE.sub(r"\1", text)
    return text


def strip_empty_anchors(text: str) -> str:
    return _EMPTY_ANCHOR_RE.sub("", text)


def extract_top_block(text: str, meta: dict) -> tuple[str, dict]:
    """Pull the links/acknowledgements block from the top of the document
    into the metadata dict, removing it from the body.
    """
    # The block sits between (links)= (or (abstract)=) and the first
    # `# Introduction` heading.
    m_anchor = re.search(r"^\(links\)=\s*$", text, flags=re.MULTILINE)
    m_first_h1 = re.search(r"^#\s+\S", text, flags=re.MULTILINE)
    if not (m_anchor and m_first_h1):
        return text, meta
    block = text[m_anchor.end():m_first_h1.start()].strip()
    meta = dict(meta)
    meta["acknowledgements"] = block
    cleaned = text[:m_anchor.start()] + text[m_first_h1.start():]
    return cleaned, meta


def main() -> None:
    src = build_path("08b_named_glosses.md")
    dst = build_path("09_clean.md")
    meta_in = build_path("02_metadata.json")
    meta_out = build_path("09_metadata.json")

    text = read_text(src)
    metadata = json.loads(read_text(meta_in))

    text, n_div, n_span = strip_html_blocks(text)
    text = strip_attributes(text)
    text = strip_empty_anchors(text)

    text, metadata = extract_top_block(text, metadata)

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.lstrip("\n")

    # Dedent indented label lines: when pandoc converts `\label{}` inside
    # a numbered list item, the resulting `(label)=` is indented, and
    # mystmd 1.8.x doesn't register indented labels (`[](#label)` refs
    # then fail). Dedenting preserves the surrounding list structure
    # since labels are zero-width.
    text, n_dedented = dedent_indented_label_lines(text)
    # Collapse adjacent-label clusters before mystmd does. Rewrites every
    # `[](#X)` reference to point at the canonical (first-in-order) name
    # within the cluster — without this, mystmd's auto-collapse leaves
    # dropped names without HTML ids and turns every reference to them
    # into a dead link in the rendered HTML.
    text, aliases = merge_adjacent_label_clusters(text)
    # Wrap labelled markdown tables in `:::{table}` directives. Plain
    # markdown tables in mystmd 1.8.x don't accept preceding `(X)=`
    # labels — they get registered internally but no `id="X"` is
    # emitted, so every cross-reference is dead. The directive form
    # produces the id correctly.
    text, n_tables_wrapped = wrap_labelled_tables_in_directives(text)
    # Case-normalize references: source sometimes writes `[](#calibration)`
    # against an anchor `(Calibration)=`; mystmd's lowercasing of ids in
    # HTML emission doesn't help because pandoc preserves the lowercase
    # in href targets. Rewrite refs to match actual-case labels.
    text, case_aliases = case_normalize_references(text)
    aliases.update(case_aliases)

    write_text(dst, text)
    write_text(meta_out, json.dumps(metadata, indent=2, ensure_ascii=False))

    n_lines = text.count("\n") + 1
    print(f"  cleaned md:    {dst}  ({n_lines} lines)")
    print(f"  divs stripped:  {n_div}")
    print(f"  spans stripped: {n_span}")
    print(f"  label clusters merged: {len(aliases)} ({', '.join(f'{k}->{v}' for k, v in list(aliases.items())[:5])}{', ...' if len(aliases) > 5 else ''})")
    print(f"  tables wrapped in :::{{table}} directives: {n_tables_wrapped}")
    print(f"  indented label lines dedented: {n_dedented}")
    print(f"  metadata:      {meta_out}")


if __name__ == "__main__":
    main()
