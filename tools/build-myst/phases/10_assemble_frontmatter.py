#!/usr/bin/env python3
"""Phase 10: Assemble MyST YAML frontmatter and prepend to the body.

Reads:
  _build/myst/09_clean.md
  _build/myst/09_metadata.json
  tools/build-myst/config/frontmatter-template.yml  (optional)

Writes:
  _build/myst/10_with_frontmatter.md

Cleans LaTeX residue from each metadata field, parses author names, and
emits a YAML block at the top of the document.  The body itself is left
untouched aside from the prepended `---` … `---` block.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml  # type: ignore[import-untyped]

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.bbl_parser import (  # noqa: E402
    CitationEntry,
    _apply_latex_accents,
    _strip_extra_braces_in_emphasis,
    parse_bbl,
)
from lib.safe_io import build_path, read_text, write_text  # noqa: E402


_BACKSLASH_LATEX = re.compile(r"\\\\")               # `\\\\` (newline) → space
_TODAY_RE = re.compile(r"\\today\b")
_CITE_RE = re.compile(r"\\cite[a-z]*\{([^{}]+)\}")
_HREF_RE = re.compile(r"\\href\{([^{}]+)\}\{([^{}]*)\}")
_INCLUDE_RE = re.compile(r"\\includegraphics\{[^{}]*\}")
_LATEX_CMD_RE = re.compile(r"\\[a-zA-Z@]+\b\*?")
_BRACES_RE = re.compile(r"[{}]")
_ANCHOR_RESIDUE = re.compile(r"\([A-Za-z0-9_:.-]+\)=\s*$")
_WS_RE = re.compile(r"\s+")
_HYPHEN_HINT_RE = re.compile(r"\\-")  # bare \- (TeX hyphenation hint)


def _resolve_cite(citations: dict[str, CitationEntry], keys: str) -> str:
    """Render `\\cite{key1,key2}` as ``Author (Year); Author (Year)`` using bbl
    entries. Falls back to the raw key wrapped in `[…]` if the key isn't
    present in the .bbl (so the validator's residual-placeholder check
    catches it downstream).
    """
    parts: list[str] = []
    for k in keys.split(","):
        k = k.strip()
        if not k:
            continue
        entry = citations.get(k)
        if entry is None:
            parts.append(f"[{k}]")
        else:
            parts.append(entry.long)  # "Author (Year)"
    return "; ".join(parts)


def _clean_text(value: str, citations: dict[str, CitationEntry] | None = None) -> str:
    """Strip simple LaTeX commands and condense whitespace.  Suitable for
    short fields like title/keywords; not used on abstract (kept verbatim
    after milder cleanup). When `citations` is provided, `\\cite{}` is
    resolved to "Author (Year)" form rather than the raw key.
    """
    out = _BACKSLASH_LATEX.sub(" ", value)
    out = _TODAY_RE.sub("", out)
    out = _INCLUDE_RE.sub("", out)
    out = _HREF_RE.sub(lambda m: m.group(2) or m.group(1), out)
    if citations is not None:
        out = _CITE_RE.sub(lambda m: _resolve_cite(citations, m.group(1)), out)
    else:
        out = _CITE_RE.sub(lambda m: m.group(1), out)
    out = _HYPHEN_HINT_RE.sub("", out)             # bare \- (hyphenation hint)
    out = _strip_extra_braces_in_emphasis(out)
    out = _apply_latex_accents(out)
    out = _convert_latex_quotes(out)               # `…' → ‘…’; ``…'' → “…”
    out = _LATEX_CMD_RE.sub("", out)
    out = _BRACES_RE.sub("", out)
    out = _WS_RE.sub(" ", out).strip()
    out = _ANCHOR_RESIDUE.sub("", out).strip()
    return out


_BBL_BRACE_LETTER = re.compile(r"\{([A-Za-z]+)\}")
_BBL_TILDE = re.compile(r"~")

# LaTeX-style smart quotes. Source uses `text' (single-quoted) and
# ``text'' (double-quoted); pandoc converts these to ‘text’ / “text”
# in body output. The frontmatter (abstract / acknowledgements) does
# NOT pass through pandoc, so the backticks survive into the rendered
# markdown — where ` is the code-span delimiter, turning `buffer stock'
# into the start of a `<code>` span that closes at the next backtick.
# Convert here before YAML emission so frontmatter renders cleanly.
_LATEX_DOUBLE_QUOTE_OPEN_RE = re.compile(r"``")
_LATEX_DOUBLE_QUOTE_CLOSE_RE = re.compile(r"''")
_LATEX_SINGLE_QUOTE_RE = re.compile(r"`([^`'\n]+?)'")


def _convert_latex_quotes(text: str) -> str:
    # Order matters: convert double-quote markers BEFORE single-quote
    # patterns. Otherwise an input like ``Growth Impatience'' has its
    # inner `Growth Impatience' caught by the single-quote regex and
    # the surrounding ` and ' are left orphaned.
    text = _LATEX_DOUBLE_QUOTE_OPEN_RE.sub("“", text)       # “
    text = _LATEX_DOUBLE_QUOTE_CLOSE_RE.sub("”", text)      # ”
    text = _LATEX_SINGLE_QUOTE_RE.sub("‘\\1’", text)        # ‘…’
    return text


def _clean_block(value: str, citations: dict[str, CitationEntry] | None = None) -> str:
    """Cleanup that preserves paragraph breaks (used for abstract /
    acknowledgements).  Resolves `\\cite{key}` to "Author (Year)" via the
    bbl when `citations` is provided (recommended — otherwise the raw key
    leaks through wrapped in `[…]`). Strips bare `\\-` hyphenation hints,
    converts LaTeX accents to Unicode, and de-doubles `\\emph{{X}}` →
    `*X*`. Keeps newlines intact.
    """
    out = _TODAY_RE.sub("", value)
    out = _INCLUDE_RE.sub("", out)
    if citations is not None:
        out = _CITE_RE.sub(lambda m: _resolve_cite(citations, m.group(1)), out)
    else:
        out = _CITE_RE.sub(lambda m: f"[{m.group(1)}]", out)
    out = _HYPHEN_HINT_RE.sub("", out)
    out = _strip_extra_braces_in_emphasis(out)
    out = _apply_latex_accents(out)
    out = _convert_latex_quotes(out)               # `…' → ‘…’; ``…'' → “…”
    out = _BACKSLASH_LATEX.sub("\n", out)
    out = _BBL_BRACE_LETTER.sub(r"\1", out)        # {C}hristopher → Christopher
    out = _BBL_TILDE.sub(" ", out)                 # ~ → space
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    out = _ANCHOR_RESIDUE.sub("", out).strip()
    return out


_AUTHOR_SPLIT_RE = re.compile(r"\s*(?:,?\s*~?and\s+|,\s*|~and\s+)")


def _parse_authors(raw: str) -> list[dict]:
    """Split a LaTeX author string like
    `Christopher D Carroll~and Akshay Shanker` into a list of `{name: ...}`
    dicts.  Affiliations are not currently extracted (no `\\affil{...}` in
    the BST source); they can be added later by hand or via a richer parse.
    """
    cleaned = _clean_text(raw)
    pieces = [p.strip() for p in _AUTHOR_SPLIT_RE.split(cleaned) if p.strip()]
    return [{"name": p} for p in pieces]


_KEYWORD_SPLIT_RE = re.compile(r"\s*[,;]\s*")


def _parse_keywords(raw: str) -> list[str]:
    cleaned = _clean_text(raw)
    return [k for k in _KEYWORD_SPLIT_RE.split(cleaned) if k]


_LINK_PATTERNS = {
    "remark":    re.compile(r"REMARK[^\n]*?(https?://[^\s`)\]]+)"),
    "html":      re.compile(r"\bhtml[^\n]*?(https?://[^\s`)\]]+)"),
    "pdf":       re.compile(r"\bPDF[^\n]*?(https?://[^\s`)\]]+\.pdf)"),
    "slides":    re.compile(r"\bSlides[^\n]*?(https?://[^\s`)\]]+\.pdf)"),
    "github":    re.compile(r"\bGitHub[^\n]*?(https?://github\.com/[^\s`)\]]+)"),
    "dashboard": re.compile(r"\bDashboard[^\n]*?\(([^\s)]+)\)"),
}


def _extract_links(ack_block: str) -> dict[str, str]:
    links: dict[str, str] = {}
    for key, pat in _LINK_PATTERNS.items():
        m = pat.search(ack_block)
        if m:
            links[key] = m.group(1)
    return links


def _strip_links_lines(ack_block: str) -> str:
    """Remove the leading reproducibility-link table lines from the
    acknowledgements block (REMARK / Dashboard / html / PDF / Slides /
    GitHub) so what remains is the prose acknowledgement paragraph.
    """
    lines = ack_block.splitlines()
    keep: list[str] = []
    for line in lines:
        if re.match(
            r"\s*`?\s*(REMARK|Dashboard|html|PDF|Slides|GitHub)\s*:?\s*`?",
            line,
        ):
            continue
        keep.append(line)
    return "\n".join(keep).strip()


def main() -> None:
    body_src = build_path("09_clean.md")
    meta_src = build_path("09_metadata.json")
    bbl_src  = build_path("04_bbl_only.tex")
    dst = build_path("10_with_frontmatter.md")

    body = read_text(body_src)
    meta = json.loads(read_text(meta_src))

    # Load the bibliography so frontmatter `\cite{}` calls in the abstract
    # and acknowledgements resolve to "Author (Year)" form (matching how
    # Phase 5 renders body citations). Without this, the abstract leaks
    # raw bib keys like `[bewleyPIH]` to readers.
    citations: dict[str, CitationEntry] = parse_bbl(read_text(bbl_src))

    title = _clean_text(meta.get("title", "Untitled"), citations)
    authors = _parse_authors(meta.get("authors", ""))
    keywords = _parse_keywords(meta.get("keywords", ""))
    abstract = _clean_block(meta.get("abstract", ""), citations)

    raw_ack = meta.get("acknowledgements", "")
    links = _extract_links(raw_ack)
    ack_prose = _clean_block(_strip_links_lines(raw_ack), citations)

    jel_raw = meta.get("jelclass", "")
    jel_codes = re.findall(r"\b[A-Z]\d{2}\b", jel_raw)

    frontmatter: dict[str, object] = {
        "title": title,
        "subject": "Economics",
        "subtitle": "",
        "short_title": "BufferStockTheory",
        "authors": authors,
        "keywords": keywords,
        "abstract": abstract,
    }
    if jel_codes:
        frontmatter["jel_codes"] = jel_codes
    if links:
        frontmatter["links"] = links
    if ack_prose:
        frontmatter["acknowledgements"] = ack_prose

    # Drop empty fields.
    frontmatter = {k: v for k, v in frontmatter.items() if v not in ("", None, [], {})}

    yaml_text = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        width=10_000,  # keep long URLs / abstract on single lines
        default_flow_style=False,
    )

    # YAML 'safe_dump' will quote multi-line strings; switch the abstract /
    # acknowledgements blocks to literal block scalars (`|-`) for legibility.
    yaml_text = re.sub(
        r"^(abstract|acknowledgements): '((?:[^']|'')+)'\s*$",
        lambda m: f"{m.group(1)}: |-\n  " + m.group(2).replace("''", "'").replace("\n", "\n  "),
        yaml_text,
        flags=re.MULTILINE,
    )

    body_clean = re.sub(r"^\(abstract\)=\s*\n+", "", body, count=1)
    # mystmd's theme renders the keywords frontmatter block with an
    # auto-generated pilcrow `<a href="#keywords">¶</a>` — but doesn't
    # put `id="keywords"` on the surrounding div. Without an explicit
    # target, the pilcrow click is dead. Inject a body anchor so the
    # link resolves (clicks scroll to top of body, near where keywords
    # are displayed). Same pattern would address `#abstract` etc. if
    # mystmd ever renders those pilcrows broken too.
    body_clean = "(keywords)=\n\n" + body_clean.lstrip()
    out = f"---\n{yaml_text}---\n\n{body_clean}"
    write_text(dst, out)

    print(f"  with-frontmatter md: {dst}")
    print(f"  authors:    {len(authors)}")
    print(f"  keywords:   {len(keywords)}")
    print(f"  jel codes:  {len(jel_codes)}")
    print(f"  links:      {len(links)} ({', '.join(links) or '-'})")
    print(f"  abstract:   {len(abstract)} chars")


if __name__ == "__main__":
    main()
