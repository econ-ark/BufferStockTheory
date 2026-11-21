"""Tests for tools/build-myst/lib/math_macros.py."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib import math_macros  # noqa: E402


def test_parse_simple():
    text = r"""
\newcommand{\Rfree}{\mathsf{R}}
\newcommand{\DiscFac}{\beta}
"""
    out = math_macros.parse_newcommands(text)
    assert out == {
        "Rfree": (None, r"\mathsf{R}"),
        "DiscFac": (None, r"\beta"),
    }


def test_parse_args():
    text = r"""
\newcommand{\cnstr}[1]{\grave{#1}}
"""
    out = math_macros.parse_newcommands(text)
    assert out["cnstr"] == (1, r"\grave{#1}")


def test_parse_jekyll_extra_brace():
    """Jekyll source escapes `}}` with an extra `}`; trim it on parse."""
    text = r"\newcommand{\aLvl}{\pmb{a}}}"
    out = math_macros.parse_newcommands(text)
    # Body should be `\pmb{a}`, not `\pmb{a}}`.
    assert out["aLvl"] == (None, r"\pmb{a}")


def test_parse_balanced_nested():
    text = r"\newcommand{\Foo}{\frac{a}{b}}"
    out = math_macros.parse_newcommands(text)
    assert out["Foo"] == (None, r"\frac{a}{b}")


def test_katex_safe_hyperlink():
    body = r"\hyperlink{APFacDefn}{\textrm{APF}}"
    assert math_macros.katex_safe(body) == r"\textsf{\textrm{APF}}"


def test_katex_safe_href():
    body = r"\href{https://example.com}{Click}"
    assert math_macros.katex_safe(body) == "Click"


def test_katex_safe_unicode():
    body = r"\unicode{1417}"
    # Codepoint 1417 == U+0589 (Armenian full stop). The exact char doesn't
    # matter — what matters is that \unicode{NNNN} is replaced with the
    # corresponding character.
    assert math_macros.katex_safe(body) == chr(1417)


def test_katex_safe_passthrough():
    body = r"\mathsf{R}"
    # No rewrites needed.
    assert math_macros.katex_safe(body) == r"\mathsf{R}"


def test_to_macro_map_argless():
    macros = {"Rfree": (None, r"\mathsf{R}")}
    out = math_macros.to_macro_map(macros)
    assert out == {"\\Rfree": r"\mathsf{R}"}


def test_to_macro_map_with_args():
    """Multi-arg macros emit as plain strings; KaTeX infers nargs from #N."""
    macros = {"cnstr": (1, r"\grave{#1}")}
    out = math_macros.to_macro_map(macros)
    assert out == {"\\cnstr": r"\grave{#1}"}


def test_to_macro_map_sorted():
    macros = {"Z": (None, "z"), "A": (None, "a"), "M": (None, "m")}
    out = math_macros.to_macro_map(macros)
    assert list(out.keys()) == ["\\A", "\\M", "\\Z"]


def test_render_yaml_basic():
    mac_map = {"\\Rfree": r"\mathsf{R}"}
    yaml_text = math_macros.render_yaml(mac_map)
    assert yaml_text == (
        "version: 1\n"
        "project:\n"
        "  math:\n"
        "    '\\Rfree': '\\mathsf{R}'\n"
    )


def test_render_yaml_with_args():
    """Parameterised macros emit as plain strings — KaTeX infers nargs."""
    mac_map = {"\\cnstr": r"\grave{#1}"}
    yaml_text = math_macros.render_yaml(mac_map)
    assert yaml_text == (
        "version: 1\n"
        "project:\n"
        "  math:\n"
        "    '\\cnstr': '\\grave{#1}'\n"
    )


def test_render_yaml_quote_escaping():
    """Single quotes in the body must be doubled for YAML single-quoted scalars."""
    mac_map = {"\\Foo": "it's"}
    yaml_text = math_macros.render_yaml(mac_map)
    assert "'\\Foo': 'it''s'" in yaml_text


def test_render_yaml_has_version_and_project():
    """mystmd's `extends:` requires the extended file to be a valid config."""
    mac_map = {"\\X": "x"}
    yaml_text = math_macros.render_yaml(mac_map)
    assert "version: 1" in yaml_text
    assert "project:" in yaml_text
    assert "  math:" in yaml_text


def test_render_yaml_with_header():
    yaml_text = math_macros.render_yaml({"\\X": "x"}, header_comment="Auto-gen.")
    assert yaml_text.startswith("# Auto-gen.\n\nversion: 1\n")


def test_extract_to_yaml_end_to_end(tmp_path):
    src = tmp_path / "shortcuts.md"
    src.write_text(
        "{% raw %}\n"
        r"\newcommand{\Rfree}{\mathsf{R}}" + "\n"
        r"\newcommand{\GIC}{\hyperlink{GIC}{\textrm{GIC}}}" + "\n"
        r"\newcommand{\Thorn}{\unicode{1417}}" + "\n"
        "{% endraw %}\n",
    )
    yaml_text = math_macros.extract_to_yaml(src)
    assert "version: 1" in yaml_text
    assert "project:" in yaml_text
    assert "  math:" in yaml_text
    assert "'\\Rfree': '\\mathsf{R}'" in yaml_text
    # \hyperlink rewritten to \textsf
    assert "'\\GIC': '\\textsf{\\textrm{GIC}}'" in yaml_text
    # \unicode replaced with literal char
    assert "'\\Thorn': '" + chr(1417) + "'" in yaml_text


def test_extract_to_yaml_multiple_sources_later_wins(tmp_path):
    """Later sources override earlier ones (LaTeX \\renewcommand semantics)."""
    a = tmp_path / "a.tex"
    a.write_text(r"\newcommand{\Foo}{first}")
    b = tmp_path / "b.sty"
    b.write_text(r"\providecommand{\Foo}{second}")
    yaml_text = math_macros.extract_to_yaml(a, b)
    assert "'\\Foo': 'second'" in yaml_text
    assert "'first'" not in yaml_text


def test_parse_providecommand_and_renewcommand():
    """All three command-definition forms parse identically."""
    text = "\n".join([
        r"\providecommand{\A}{x}",
        r"\renewcommand{\B}{y}",
        r"\newcommand{\C}{z}",
    ])
    out = math_macros.parse_newcommands(text)
    assert out == {"A": (None, "x"), "B": (None, "y"), "C": (None, "z")}
