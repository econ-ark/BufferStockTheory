"""Unit tests for `lib.myst_emit`."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.myst_emit import (  # noqa: E402
    anchor,
    cite_role,
    directive,
    eq_ref,
    figure_directive,
    md_link,
    num_ref,
    proof_directive,
)


def test_anchor() -> None:
    assert anchor("sec:intro") == "(sec:intro)="


def test_directive_minimal() -> None:
    out = directive("note")
    assert out.startswith(":::{note}")
    assert out.endswith(":::")


def test_directive_with_arg_and_body() -> None:
    out = directive("note", arg="Heads-up", body="Body text")
    lines = out.splitlines()
    assert lines[0] == ":::{note} Heads-up"
    assert "Body text" in lines
    assert lines[-1] == ":::"


def test_directive_with_options() -> None:
    out = directive("figure", arg="img.png", options={"width": "80%", "alt": "x"},
                    body="caption")
    assert ":width: 80%" in out
    assert ":alt: x" in out
    assert "caption" in out


def test_proof_directive_label_emitted() -> None:
    out = proof_directive("theorem", name="MyThm", label="thm:my", body="body")
    assert ":::{prf:theorem} MyThm" in out
    assert ":label: thm:my" in out


def test_figure_directive_basic() -> None:
    out = figure_directive("img.png", label="fig:x", width="50%", caption="cap")
    assert ":::{figure} img.png" in out
    assert ":label: fig:x" in out
    assert ":width: 50%" in out
    assert "cap" in out


def test_eq_ref_and_num_ref() -> None:
    assert eq_ref("eq:foo") == "{eq}`eq:foo`"
    assert num_ref("fig:bar") == "{numref}`fig:bar`"


def test_md_link() -> None:
    assert md_link("Section 2", "sec:two") == "[Section 2](#sec:two)"


def test_cite_role_joins_keys() -> None:
    assert cite_role("cite:p", ["a", "b"]) == "{cite:p}`a, b`"
