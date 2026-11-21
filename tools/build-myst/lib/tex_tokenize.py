"""Math-mode-aware text walking for LaTeX source.

Phases that need to act on text-mode-only occurrences of macros (e.g. Phase 3d
emitting `<<NAMED:GIC>>` placeholders for `\\GIC` in text but not `$\\GIC$` in
math) use `iter_segments(text)` which yields pairs `(mode, segment)` where
mode is one of the literals "text", "inline_math", "display_math".

The tokenizer is deliberately pragmatic, not a full LaTeX parser:

- handles `$...$` (single-dollar inline math)
- handles `$$...$$` (double-dollar display math)
- handles `\\(...\\)` (paren inline math)
- handles `\\[...\\]` (bracket display math)
- handles `\\begin{equation|equation*|align|align*|gather|gather*|multline|multline*|eqnarray|eqnarray*|displaymath|math}...\\end{...}`
- treats `\\$` as a literal dollar sign (escaped), NOT a math delimiter
- comments (`% ... \\n`) are passed through verbatim because Phase 1 already
  stripped them via `latexpand --keep-comments=false`.

`replace_in_text(text, fn)` is a convenience: it applies `fn(segment)` only to
the text-mode segments and re-emits math segments unchanged.
"""

from __future__ import annotations

import re
from typing import Callable, Iterable, Iterator, List, Tuple

# Math environments that delimit display math via \begin{name}...\end{name}.
_MATH_ENVS = (
    "equation", "equation*",
    "align", "align*",
    "gather", "gather*",
    "multline", "multline*",
    "eqnarray", "eqnarray*",
    "displaymath", "math",
    "alignat", "alignat*",
    "flalign", "flalign*",
)

_BEGIN_MATH_RE = re.compile(
    r"\\begin\{(" + "|".join(re.escape(e) for e in _MATH_ENVS) + r")\}"
)


def iter_segments(text: str) -> Iterator[Tuple[str, str]]:
    """Yield (mode, segment) pairs covering the whole input.

    mode in {"text", "inline_math", "display_math"}.
    Segments concatenate back to the original input exactly.
    """
    i = 0
    n = len(text)
    buf: List[str] = []
    cur_mode = "text"

    def flush(mode: str) -> Iterator[Tuple[str, str]]:
        if buf:
            yield mode, "".join(buf)
            buf.clear()

    while i < n:
        c = text[i]

        # Escaped dollar / brackets — keep as literal text, advance past escape.
        if c == "\\" and i + 1 < n and text[i + 1] in ("$", "(", ")", "[", "]"):
            # But \( \[ ARE math delimiters in LaTeX — distinguish.
            nxt = text[i + 1]
            if nxt == "$":
                buf.append("\\$")
                i += 2
                continue
            if nxt == "(":
                yield from flush(cur_mode)
                end = text.find(r"\)", i + 2)
                if end == -1:
                    end = n
                else:
                    end += 2
                yield "inline_math", text[i:end]
                i = end
                continue
            if nxt == "[":
                yield from flush(cur_mode)
                end = text.find(r"\]", i + 2)
                if end == -1:
                    end = n
                else:
                    end += 2
                yield "display_math", text[i:end]
                i = end
                continue
            # \) and \] without an opener — treat as literal.
            buf.append(text[i:i + 2])
            i += 2
            continue

        # Display math via $$...$$
        if c == "$" and i + 1 < n and text[i + 1] == "$":
            yield from flush(cur_mode)
            end = text.find("$$", i + 2)
            if end == -1:
                end = n
            else:
                end += 2
            yield "display_math", text[i:end]
            i = end
            continue

        # Inline math via $...$
        if c == "$":
            yield from flush(cur_mode)
            j = i + 1
            while j < n:
                if text[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if text[j] == "$":
                    j += 1
                    break
                j += 1
            yield "inline_math", text[i:j]
            i = j
            continue

        # \begin{equation}...\end{equation} etc.
        if c == "\\":
            m = _BEGIN_MATH_RE.match(text, i)
            if m:
                env = m.group(1)
                end_marker = "\\end{" + env + "}"
                end = text.find(end_marker, m.end())
                if end == -1:
                    end = n
                else:
                    end += len(end_marker)
                yield from flush(cur_mode)
                yield "display_math", text[i:end]
                i = end
                continue

        buf.append(c)
        i += 1

    yield from flush(cur_mode)


def replace_in_text(text: str, fn: Callable[[str], str]) -> str:
    """Apply fn to text-mode segments only; pass math through unchanged."""
    out: List[str] = []
    for mode, seg in iter_segments(text):
        if mode == "text":
            out.append(fn(seg))
        else:
            out.append(seg)
    return "".join(out)


def text_segments(text: str) -> Iterable[str]:
    """Yield only the text-mode segments (skipping math)."""
    for mode, seg in iter_segments(text):
        if mode == "text":
            yield seg
