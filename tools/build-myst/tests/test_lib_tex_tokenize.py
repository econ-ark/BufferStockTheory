"""Unit tests for `lib.tex_tokenize`."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.tex_tokenize import iter_segments, replace_in_text  # noqa: E402


def _modes(text: str) -> list[tuple[str, str]]:
    return list(iter_segments(text))


def test_segments_roundtrip() -> None:
    s = r"text $a + b$ more $$E = mc^2$$ tail"
    segments = _modes(s)
    assert "".join(seg for _, seg in segments) == s


def test_inline_math_detected() -> None:
    s = r"alpha $x_1 + x_2$ beta"
    segments = _modes(s)
    assert ("inline_math", "$x_1 + x_2$") in segments


def test_display_math_dollars_detected() -> None:
    segments = _modes(r"a $$\sum x_i$$ b")
    assert any(m == "display_math" for m, _ in segments)


def test_display_math_brackets_detected() -> None:
    segments = _modes(r"a \[ E = mc^2 \] b")
    kinds = [m for m, _ in segments]
    assert "display_math" in kinds


def test_environment_math_detected() -> None:
    s = r"intro \begin{equation} y = x \end{equation} outro"
    segments = _modes(s)
    assert any(m == "display_math" and "equation" in seg for m, seg in segments)


def test_escaped_dollar_is_text() -> None:
    s = r"this costs \$5 dollars"
    segments = _modes(s)
    assert all(m == "text" for m, _ in segments)


def test_replace_in_text_skips_math() -> None:
    s = r"foo $\GIC$ foo"
    out = replace_in_text(s, lambda t: t.replace("foo", "BAR"))
    # `\GIC` inside `$…$` must be untouched, both `foo` outside replaced.
    assert out == r"BAR $\GIC$ BAR"


def test_replace_in_text_preserves_dollar_round_trip() -> None:
    s = r"a $b$ c $$d$$ e \(f\) g \[h\] i \begin{align}j\end{align} k"
    out = replace_in_text(s, lambda t: t)
    assert out == s
