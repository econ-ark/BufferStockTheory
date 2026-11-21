#!/usr/bin/env python3
"""Phase 08b: Resolve `<<NAMED:NAME>>` placeholders to plain-text condition names.

Reads:  _build/myst/08a_paragraphs_figs.md
        tools/build-myst/config/named-conditions.yml
Writes: _build/myst/08b_named_glosses.md

Behaviour: every text-mode occurrence of `<<NAMED:X>>` is replaced with
the `short` form for X (e.g. `GIC`, `FHWC`, `RIC`). That's it.

The previous implementation also injected a parenthetical long form on
first occurrence ("GIC (growth impatience condition)"), but the
behaviour was load-bearing on document-order traversal and tied to
named-conditions.yml maintenance — every new condition macro added to
LaTeX needed a YAML entry, and forgetting one produced an undetected
silent fallback to raw `\\macroname`. Robustness > fidelity: emit the
short form unconditionally, error loudly on anything missing from the
config.

The placeholder may appear in any of the pandoc-escaped forms
`<<NAMED:X>>`, `\\<\\<NAMED:X\\>\\>`, or `&lt;&lt;NAMED:X&gt;&gt;`.

Math-mode occurrences (`$\\GIC$`) are NOT placeholders; they are raw math
macros rendered by KaTeX/MathJax. Phase 3 emitted placeholders only for
text-mode occurrences.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, config_path, read_text, write_text  # noqa: E402


_NAMED_RE = re.compile(
    r"(?:\\<\\<|&lt;&lt;|<<)NAMED:((?:[^<>\\]|\\[^<>])+?)(?:\\>\\>|&gt;&gt;|>>)"
)


def _unescape(s: str) -> str:
    return re.sub(r"\\(.)", r"\1", s)


def replace_named(text: str, table: dict) -> tuple[str, dict[str, int], set[str]]:
    """Replace each `<<NAMED:X>>` with its `short` form.

    Returns (text, counts, unknown) where `counts[name]` is occurrence
    count and `unknown` is the set of names not present in `table`.
    Unknown names are LEFT UNCHANGED (so the validator's residual-
    placeholder check fires) — this is intentional: silent fallback
    to raw text was the original failure mode and we want to surface it.
    """
    counts: dict[str, int] = {}
    unknown: set[str] = set()

    def _sub(m: re.Match) -> str:
        name = _unescape(m.group(1)).strip()
        counts[name] = counts.get(name, 0) + 1
        entry = table.get(name)
        if entry is None:
            unknown.add(name)
            return m.group(0)  # leave placeholder; validator will catch.
        return entry.get("short", name)

    return _NAMED_RE.sub(_sub, text), counts, unknown


def main() -> None:
    src = build_path("08a_paragraphs_figs.md")
    dst = build_path("08b_named_glosses.md")

    text = read_text(src)
    table = yaml.safe_load(read_text(config_path("named-conditions.yml"))) or {}

    text, counts, unknown = replace_named(text, table)

    write_text(dst, text)

    total = sum(counts.values())
    unique = len(counts)
    print(f"  named-glossed md: {dst}")
    print(f"  placeholders replaced: {total} (unique names: {unique})")
    if counts:
        for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            tag = "" if name in table else "  (NOT IN CONFIG)"
            print(f"    {name:10}  ×{n}{tag}")
    if unknown:
        print(
            f"Phase 08b ERROR: {len(unknown)} named-condition placeholder(s) "
            f"not in config/named-conditions.yml: {sorted(unknown)}",
            file=sys.stderr,
        )
        print(
            "  Add them to named-conditions.yml or remove the source \\macroname "
            "that emits them.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
