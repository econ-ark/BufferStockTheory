#!/usr/bin/env python3
"""Phase 07: Convert pre-pandoc PRFBEGIN/PRFEND sentinels into MyST `prf:`
directives.

Reads:  _build/myst/06_xrefs.md
Writes: _build/myst/07_theorems.md

Phase 3 wrapped each theorem-like LaTeX environment with sentinel paragraphs:

    PRFBEGIN|kind|label|title
    body
    PRFEND

This phase rewrites those into MyST sphinx-proof directive blocks:

    :::{prf:kind} title
    :label: label

    body
    :::

`kind` is mapped through `tools/build-myst/config/theorem-mapping.yml` to a
sphinx-proof directive name (e.g. `claim` → `property`, since sphinx-proof has
no `claim` directive).

If `label` or `title` is empty the corresponding line is omitted.

After pandoc, the sentinel may have been split across multiple lines or
wrapped — we look for any line whose content (after stripping) matches the
PRFBEGIN/PRFEND pattern.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, config_path, read_text, write_text  # noqa: E402


# Sentinel patterns. Match the whole line, allowing leading/trailing
# whitespace. Pandoc may have escaped `|` (to `\|`) and `_` (to `\_`) — we
# permit either escaped or raw delimiters and unescape captured fields below.
_BEGIN_RE = re.compile(
    r"^\s*PRFBEGIN\\?\|([^|]+?)\\?\|([^|]*?)\\?\|(.*?)\s*$"
)
_END_RE = re.compile(r"^\s*PRFEND\s*$")


def _unescape(s: str) -> str:
    """Strip pandoc backslash-escapes (`\\_` → `_`, `\\<` → `<`, etc.)."""
    return re.sub(r"\\(.)", r"\1", s)


def _load_kind_map() -> dict:
    return yaml.safe_load(read_text(config_path("theorem-mapping.yml"))) or {}


def _myst_safe_label(label: str) -> str:
    """Replace `:` with `-` in label names so mystmd doesn't prefix-strip.

    Mirrors the same transform Phase 06 applies — both phases must agree
    or anchors and references get out of sync. See the `_safe_label`
    docstring in phases/06_resolve_xrefs.py for the underlying mystmd
    behaviour.
    """
    return label.replace(":", "-")


def _open_directive(kind: str, label: str, title: str, kind_map: dict) -> str:
    """Emit a MyST `:::{prf:KIND}` directive with optional title and label."""
    prf_kind = kind_map.get(kind, kind)
    head = f":::{{prf:{prf_kind}}}"
    if title:
        head += f" {title}"
    safe = _myst_safe_label(label) if label else ""
    lines: list[str] = []
    if safe:
        # Pre-directive `(label)=` line is a redundant but reliable
        # target — picks up the same dash-form name. Together with the
        # `:label:` below, references resolve regardless of which form
        # mystmd treats as canonical.
        lines.append(f"({safe})=")
    lines.append(head)
    if safe:
        lines.append(f":label: {safe}")
        lines.append("")
    return "\n".join(lines)


def transform(text: str, kind_map: dict) -> tuple[str, int]:
    """Return (transformed_text, num_directives_emitted)."""
    out_lines: list[str] = []
    n_emitted = 0
    for line in text.splitlines():
        bm = _BEGIN_RE.match(line)
        if bm:
            kind = _unescape(bm.group(1)).strip()
            label = _unescape(bm.group(2)).strip()
            title = _unescape(bm.group(3)).strip()
            out_lines.append("")
            out_lines.append(_open_directive(kind, label, title, kind_map))
            n_emitted += 1
            continue
        if _END_RE.match(line):
            out_lines.append(":::")
            out_lines.append("")
            continue
        out_lines.append(line)
    return "\n".join(out_lines), n_emitted


def main() -> None:
    src = build_path("06_xrefs.md")
    dst = build_path("07_theorems.md")

    text = read_text(src)
    kind_map = _load_kind_map()

    n_begins_before = len(re.findall(r"PRFBEGIN", text))
    n_ends_before = len(re.findall(r"PRFEND", text))

    out, n_emitted = transform(text, kind_map)
    out = re.sub(r"\n{3,}", "\n\n", out)

    write_text(dst, out)

    n_begins_after = len(re.findall(r"PRFBEGIN", out))
    n_ends_after = len(re.findall(r"PRFEND", out))
    print(f"  theorems markdown: {dst}")
    print(f"  directives emitted: {n_emitted}")
    print(f"  PRFBEGIN: {n_begins_before} → {n_begins_after}  (expect 0)")
    print(f"  PRFEND:   {n_ends_before} → {n_ends_after}  (expect 0)")


if __name__ == "__main__":
    main()
