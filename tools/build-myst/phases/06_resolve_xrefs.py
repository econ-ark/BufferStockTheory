#!/usr/bin/env python3
"""Phase 06: Resolve cross-reference placeholders into MyST forms.

Reads:  _build/myst/05_cited.md
Writes: _build/myst/06_xrefs.md

Placeholder shapes emitted by Phase 3 (and possibly pandoc-escaped):

    <<ANCHOR:X>>          (label-only, placed wherever \\hypertarget/\\label was)
    <<XREF:X>>            (`\\ref{X}` / `\\autoref{X}`)
    <<XREF:X|Y>>          (`\\hyperlink{X}{Y}`)
    <<EQREF:X>>           (`\\eqref{X}`)
    <<CREF:X,Y,Z>>        (`\\Cref{X,Y,Z}`)
    <<NAMEREF:X>>         (`\\nameref{X}`)

After pandoc, every `<` `>` `_` may be backslash-escaped:

    \\<\\<ANCHOR:eq\\:foo\\>\\>      etc.

Conversions (all to standard Markdown / MyST):

    <<ANCHOR:X>>     →  `(X)=` on its own line.  Math-mode anchors (those
                        emitted from `\\label{X}` inside an equation) are
                        LIFTED OUT of the math block to a `(X)=` line
                        immediately preceding the equation.
    <<XREF:X|Y>>     →  `[Y](#X)`
    <<XREF:X>>       →  `[](#X)`            (MyST resolves the link text)
    <<EQREF:X>>      →  `[](#X)`            (MyST renders as `(N)` for equations)
    <<CREF:X,Y,Z>>   →  `[](#X), [](#Y), [](#Z)`
    <<NAMEREF:X>>    →  `[](#X)`
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, read_text, write_text  # noqa: E402


# ---------------------------------------------------------------------------
# Placeholder regex helpers
# ---------------------------------------------------------------------------

# Match `<<` (raw), `\<\<` (pandoc escape), or `&lt;&lt;` (pandoc HTML-block).
_OPEN  = r"(?:\\<\\<|&lt;&lt;|<<)"
_CLOSE = r"(?:\\>\\>|&gt;&gt;|>>)"

# Innermost-only body: forbid `<` so we never accidentally close on an
# inner placeholder. Backslash escapes for pandoc (\_, \&) are tolerated.
# `*?` (not `+?`) lets us also match empty-body cases like `<<ANCHOR:>>`
# which arise from `\hypertarget{}{...}` artefacts.
# Iterate to convergence so nested placeholders are unfolded inside-out.
_BODY = r"(?:[^<>\\]|\\[^<>])*?"


def _make(prefix: str) -> re.Pattern:
    return re.compile(_OPEN + prefix + r":(" + _BODY + r")" + _CLOSE)


# Permissive prefix-only matcher used to tally remaining placeholders and to
# detect "empty" anchors (`<<ANCHOR:>>`) that pandoc may emit.
_REMAINING_RE = re.compile(
    r"(?:\\<\\<|&lt;&lt;|<<)(?:CITE|ANCHOR|XREF|EQREF|CREF|NAMEREF):"
    r"[^<>]*?(?:\\>\\>|&gt;&gt;|>>)"
)


_ANCHOR_RE   = _make("ANCHOR")
_XREF_RE     = _make("XREF")
_EQREF_RE    = _make("EQREF")
_CREF_RE     = _make("CREF")
_NAMEREF_RE  = _make("NAMEREF")


def _unesc(s: str) -> str:
    """Strip pandoc backslash-escapes from a captured placeholder body."""
    return re.sub(r"\\(.)", r"\1", s)


def _safe_label(label: str) -> str:
    """Produce a label suitable for `(label)=` and `[](#label)`.

    Replaces anything that isn't a letter, digit, `-`, `_`, or `.` with
    `-`, then collapses consecutive separators. **Critical**: colons
    are also replaced with `-`. mystmd 1.8.x interprets a colon in a
    label name as a "kind prefix" (`eq:`, `thm:`, etc.) and silently
    strips everything before it during target registration — so
    `(eq:Foo)=` becomes target `Foo`, and `[](#eq:Foo)` references then
    fail to resolve. Using hyphens throughout (`(eq-Foo)=`,
    `[](#eq-Foo)`) sidesteps the prefix-strip behaviour.

    The resulting labels are no less informative — readers see
    `eq-Foo` or `ass-FVAC` and the prefix still clearly tags the kind.
    """
    out = re.sub(r"[^A-Za-z0-9_.\-]", "-", label.strip())
    out = re.sub(r"-+", "-", out).strip("-")
    return out


# ---------------------------------------------------------------------------
# Math-mode anchor lifting
# ---------------------------------------------------------------------------

# Match `$$ ... $$` blocks (multi-line) and `$ ... $` inline math.
# We lift any <<ANCHOR:X>> found inside out, prepending `(X)=` on a line
# immediately before the math block.
_DOLLARS_BLOCK_RE = re.compile(r"\$\$(.+?)\$\$", flags=re.DOTALL)
_DOLLARS_INLINE_RE = re.compile(r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)")


def _lift_math_anchors_block(match: re.Match) -> str:
    body = match.group(1)
    anchors: list[str] = []

    def _take(m: re.Match) -> str:
        anchors.append(_safe_label(_unesc(m.group(1))))
        return ""

    cleaned_body = _ANCHOR_RE.sub(_take, body)
    if not anchors:
        return match.group(0)
    prefix = "\n".join(f"({a})=" for a in anchors) + "\n"
    return f"{prefix}$${cleaned_body}$$"


def _lift_math_anchors_inline(match: re.Match) -> str:
    body = match.group(1)
    anchors: list[str] = []

    def _take(m: re.Match) -> str:
        anchors.append(_safe_label(_unesc(m.group(1))))
        return ""

    cleaned_body = _ANCHOR_RE.sub(_take, body)
    if not anchors:
        return match.group(0)
    prefix = "".join(f"({a})= " for a in anchors)
    return f"{prefix}${cleaned_body}$"


def lift_math_anchors(text: str) -> str:
    text = _DOLLARS_BLOCK_RE.sub(_lift_math_anchors_block, text)
    text = _DOLLARS_INLINE_RE.sub(_lift_math_anchors_inline, text)
    return text


# ---------------------------------------------------------------------------
# Text-mode placeholder substitution
# ---------------------------------------------------------------------------

def _anchor(m: re.Match) -> str:
    raw = _unesc(m.group(1)).strip()
    if not raw:
        return ""  # empty anchors (`\hypertarget{}{...}` artefacts) → drop.
    return f"\n({_safe_label(raw)})=\n"


def _xref(m: re.Match) -> str:
    body = _unesc(m.group(1))
    if "|" in body:
        target, _, visible = body.partition("|")
        visible = visible.strip()
        target_label = _safe_label(target)
        if not visible:
            return f"[](#{target_label})"
        return f"[{visible}](#{target_label})"
    return f"[](#{_safe_label(body)})"


def _eqref(m: re.Match) -> str:
    return f"[](#{_safe_label(_unesc(m.group(1)))})"


def _cref(m: re.Match) -> str:
    body = _unesc(m.group(1))
    keys = [_safe_label(k) for k in body.split(",") if k.strip()]
    return ", ".join(f"[](#{k})" for k in keys)


def _nameref(m: re.Match) -> str:
    return f"[](#{_safe_label(_unesc(m.group(1)))})"


_REPLACERS = (
    (_EQREF_RE,    _eqref),
    (_CREF_RE,     _cref),
    (_NAMEREF_RE,  _nameref),
    (_XREF_RE,     _xref),
    (_ANCHOR_RE,   _anchor),
)


_RAW_LINK_COLON_RE = re.compile(r"\]\(#([A-Za-z][A-Za-z0-9_.\-]*):([A-Za-z0-9_.:\-]+)\)")

# Markdown links inside \text{...} math wrappers — KaTeX rejects them.
_MD_LINK_RE = re.compile(r"\[([^\[\]]*)\]\(#([A-Za-z0-9_.\-]+)\)")


def _strip_links_in_text_math(text: str) -> str:
    r"""Replace `[](#X)` and `[Visible](#X)` *inside* `\text{...}` blocks
    with just text (the visible label or the bare anchor name).

    KaTeX's `\text{}` mode does not parse markdown link syntax — every
    occurrence triggers "Expected 'EOF', got '#'". Pandoc occasionally
    emits this when a LaTeX `\ref{}` or `\hyperref{}` lives inside a
    `\text{}` (often inside `\underbrace{...}_{\text{...}}` etc.).
    Stripping the link to plain text loses click-through but keeps
    the math renderable; per the project's robustness mandate this
    is the right tradeoff.

    Implemented with balanced-brace scanning so nested `\text{}` blocks
    are handled; the regex match is scoped to brace contents.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    needle = r"\text{"
    while i < n:
        idx = text.find(needle, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        cursor = idx + len(needle)
        depth = 1
        while cursor < n and depth > 0:
            ch = text[cursor]
            if ch == "\\" and cursor + 1 < n:
                cursor += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        body = text[idx + len(needle):cursor]
        # Replace each [vis](#X) with vis or X.
        rewritten = _MD_LINK_RE.sub(
            lambda m: m.group(1).strip() if m.group(1).strip() else m.group(2),
            body,
        )
        out.append(needle + rewritten + "}")
        i = cursor + 1
    return "".join(out)


def replace_text_mode(text: str, max_passes: int = 6) -> str:
    """Convert text-mode placeholders to MyST/Markdown forms.

    Iterates so that nested placeholders (e.g. `<<XREF:A|<<XREF:B>>...>>`)
    are unfolded inside-out: the innermost placeholder is replaced first
    (because the body regex forbids `<`), then the next pass finds the
    now-outer placeholder, and so on.
    """
    out = text
    for _ in range(max_passes):
        prev = out
        for regex, replacer in _REPLACERS:
            out = regex.sub(replacer, out)
        if out == prev:
            break
    # Final sweep: pandoc emits some markdown links like
    # `[text](#def:nondegeneracy)` directly when it converts \hyperref or
    # \autoref calls — those bypass our placeholder pipeline. Apply the
    # same colon→dash transform so they resolve under the (label)= /
    # `:label:` targets emitted earlier in this phase.
    out = _RAW_LINK_COLON_RE.sub(
        lambda m: f"](#{m.group(1)}-{m.group(2).replace(':', '-')})",
        out,
    )
    # Strip markdown links from inside \text{} math wrappers. Run AFTER
    # the colon→dash rewrite so we operate on canonicalised anchor names.
    out = _strip_links_in_text_math(out)
    # Deduplicate `(X)=` anchor lines: source LaTeX often calls
    # \hypertarget{X}{...} multiple times for the same X (e.g. PFFVAC
    # appears 6+ times in body). Each emits a `(X)=` line, and mystmd
    # then fires "label X replaced with Y" for every duplicate, often
    # silently retargeting cross-references. Keep only the first
    # occurrence of each anchor.
    out = _dedupe_anchor_markers(out)
    # NOTE: Adjacent-label cluster-merge runs in Phase 09 (after Phase
    # 07 emits theorem-directive labels) — see _merge_adjacent_label_clusters
    # below; it is invoked from 09_strip_frontmatter.py.
    return out


_ANCHOR_LINE_RE = re.compile(r"^[ \t]*\(([A-Za-z0-9_.\-]+)\)=\s*$", flags=re.MULTILINE)


def _dedupe_anchor_markers(text: str) -> str:
    """Drop repeat `(label)=` lines, keeping only the first per label."""
    seen: set[str] = set()

    def _keep_first(m: re.Match) -> str:
        label = m.group(1)
        if label in seen:
            return ""  # collapse to empty; surrounding newlines stay
        seen.add(label)
        return m.group(0)

    return _ANCHOR_LINE_RE.sub(_keep_first, text)


# Cluster-merge logic moved to lib/label_clusters.py and invoked from
# Phase 09 (which runs after Phase 07 emits its theorem-directive labels).


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    src = build_path("05_cited.md")
    dst = build_path("06_xrefs.md")

    text = read_text(src)

    n_before = len(_REMAINING_RE.findall(text))

    text = lift_math_anchors(text)
    text = replace_text_mode(text)

    # Collapse runs of >2 blank lines that anchor injection introduces.
    text = re.sub(r"\n{3,}", "\n\n", text)

    write_text(dst, text)

    n_after = len(_REMAINING_RE.findall(text))
    print(f"  xref-resolved md: {dst}")
    print(f"  placeholders before: {n_before}")
    print(f"  placeholders after:  {n_after}  (expect 0)")


if __name__ == "__main__":
    main()
