#!/usr/bin/env python3
"""Phase 05: Resolve `<<CITE:STYLE:keys>>` placeholders into inline prose.

Reads:
    _build/myst/04_raw.md          (pandoc output, with placeholders)
    _build/myst/04_bbl_only.tex    (the .bbl block split out of Phase 1)

Writes:
    _build/myst/05_cited.md        (inline citations + appended ## References)

Placeholder format (emitted by Phase 3):
    <<CITE:STYLE:keys>>
    <<CITE:STYLE/opt:keys>>

After pandoc, every `<` `>` `_` may be backslash-escaped (e.g.
`\\<\\<CITE:p:carroll\\_et\\_al-proc-scipy-2018\\>\\>`). The matcher tolerates
both forms.

STYLE encoding (from `CITE_STYLES` in Phase 3):
    p   → `(Author, Year)`        — \\citep, \\cite
    t   → `Author (Year)`         — \\citet
    a   → `Author`                — \\citeauthor
    y   → `Year`                  — \\citeyear
    yp  → `(Year)`                — \\citeyearpar
    alp → `Author, Year`          — \\citealp (no parens)
    alt → `Author Year`           — \\citealt
    P   → like p (capitalized variant)
    T   → like t (capitalized variant)

Multi-key citations are joined with `; ` inside one paren pair (for `p`/`P`)
or with `; ` between separate `Author (Year)` units (for `t`/`T`).

Each emitted citation links to the entry in the appended References section
via a placeholder `[<rendered>](#cite-<key>)`.  Only the LAST key in a
multi-key citation gets the link target — the rendered text is unbroken
prose, which matches reader expectations.

The References section is appended at the end of the document with one
paragraph per cited entry, ordered alphabetically by short_authors then year.
Each entry is preceded by a `<<ANCHOR:cite-<key>>>` placeholder so Phase 6
can wire it up to the inline links.

Only entries actually cited by the body are emitted, to keep the document
honest about its references.
"""

from __future__ import annotations

import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.bbl_parser import CitationEntry, parse_bbl  # noqa: E402
from lib.safe_io import build_path, read_text, write_text  # noqa: E402


# ---------------------------------------------------------------------------
# Placeholder matching
# ---------------------------------------------------------------------------

# Match either `<<CITE:...>>` (pre-pandoc) or `\<\<CITE:...\>\>` (post-pandoc).
# Body content can include backslash-escaped chars (`\_`, `\<`, etc.) which we
# normalise after capture.
_CITE_RE = re.compile(
    r"(?:\\<\\<|<<)CITE:((?:[^>\\]|\\.)+?)(?:\\>\\>|>>)"
)


def _unescape(s: str) -> str:
    """Undo pandoc backslash escapes inside a placeholder body.

    Pandoc emits `\\_`, `\\<`, `\\>`, `\\&`, etc.  Within our placeholder
    body these are noise — restore the original characters.
    """
    return re.sub(r"\\(.)", r"\1", s)


def _parse_placeholder(body: str) -> tuple[str, str, list[str]]:
    """Parse `STYLE[/opt]:keys` body into (style, opt, [key1, key2, ...])."""
    body = _unescape(body)
    head, _, keys_part = body.partition(":")
    style, _, opt = head.partition("/")
    keys = [k.strip() for k in keys_part.split(",") if k.strip()]
    return style, opt, keys


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _render_one(entry: CitationEntry, style: str) -> str:
    """Render a single CitationEntry under a given style."""
    if style in ("p", "P", "alp"):
        return f"{entry.short_authors}, {entry.year}"
    if style in ("t", "T"):
        return f"{entry.long_authors} ({entry.year})"
    if style == "alt":
        return f"{entry.short_authors} {entry.year}"
    if style == "a":
        return entry.long_authors
    if style == "y":
        return entry.year
    if style == "yp":
        return f"({entry.year})"
    return f"{entry.short_authors}, {entry.year}"


def _render_group(
    entries: list[CitationEntry],
    style: str,
    opt: str,
    keys: list[str],
    missing: set[str],
) -> str:
    """Render a (possibly multi-key) citation."""
    parts: list[str] = []
    for key, entry in zip(keys, entries):
        if entry is None:
            missing.add(key)
            parts.append(f"[?{key}]")
        else:
            parts.append(_render_one(entry, style))

    if style in ("p", "P", "yp"):
        joined = "; ".join(parts)
        if opt:
            joined = f"{joined}, {opt}"
        return f"({joined})"
    if style == "t" or style == "T":
        return "; ".join(parts)
    if style == "alp":
        joined = "; ".join(parts)
        if opt:
            joined = f"{joined}, {opt}"
        return joined
    return "; ".join(parts)


def _attach_anchor_link(rendered: str, key: str) -> str:
    """Wrap rendered text so the LAST author group is a link to #cite-<key>.

    For a single-key citation this is just `[rendered](#cite-key)`.
    For a multi-key, only the last name+year unit gets linked — but to keep
    the implementation simple and the prose readable, we link the entire
    rendered string to the last key's anchor.
    """
    safe_key = re.sub(r"[^A-Za-z0-9_-]", "-", key)
    return f"[{rendered}](#cite-{safe_key})"


# ---------------------------------------------------------------------------
# References section
# ---------------------------------------------------------------------------

def _format_reference_entry(entry: CitationEntry) -> str:
    """One paragraph per entry, with anchor placeholder for Phase 6."""
    safe_key = re.sub(r"[^A-Za-z0-9_-]", "-", entry.key)
    body = entry.body or ""
    body = body.strip()
    return f"<<ANCHOR:cite-{safe_key}>>{body}"


def _sort_entries(cited: dict[str, CitationEntry]) -> list[CitationEntry]:
    return sorted(
        cited.values(),
        key=lambda e: (e.short_authors.lower(), e.year, e.key.lower()),
    )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    md_path = build_path("04_raw.md")
    bbl_path = build_path("04_bbl_only.tex")
    out_path = build_path("05_cited.md")

    md_text = read_text(md_path)
    bbl_text = read_text(bbl_path)
    citations = parse_bbl(bbl_text)

    cited_keys: "OrderedDict[str, CitationEntry]" = OrderedDict()
    missing: set[str] = set()
    n_replaced = 0

    def _replace(m: re.Match) -> str:
        nonlocal n_replaced
        n_replaced += 1
        style, opt, keys = _parse_placeholder(m.group(1))
        entries = [citations.get(k) for k in keys]
        for k, e in zip(keys, entries):
            if e is not None:
                cited_keys.setdefault(k, e)
        rendered = _render_group(entries, style, opt, keys, missing)
        # Link the rendered text to the *last* cited key's anchor.
        last_real = next(
            (k for k, e in zip(reversed(keys), reversed(entries)) if e is not None),
            None,
        )
        if last_real is None:
            return rendered
        return _attach_anchor_link(rendered, last_real)

    body = _CITE_RE.sub(_replace, md_text)

    # Build References section.
    sorted_entries = _sort_entries(cited_keys)
    refs_lines = ["", "", "## References", ""]
    for entry in sorted_entries:
        refs_lines.append(_format_reference_entry(entry))
        refs_lines.append("")
    refs_block = "\n".join(refs_lines)

    write_text(out_path, body.rstrip() + "\n" + refs_block + "\n")

    print(f"  cited markdown:  {out_path}")
    print(f"  citations replaced: {n_replaced}")
    print(f"  unique works cited: {len(cited_keys)}")
    print(f"  bbl entries total: {len(citations)}")
    if missing:
        # Fatal: a \cite{key} that doesn't resolve means the published markdown
        # has a broken citation link with no anchor. Either the key is a typo
        # or the .bbl is out-of-sync with the .bib. Either way, surface it.
        import sys
        print(
            f"Phase 05 ERROR: {len(missing)} unresolved cite key(s): "
            f"{sorted(missing)}",
            file=sys.stderr,
        )
        print(
            "  Either fix the typo in the source or regenerate the .bbl with "
            "all cited keys present.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
