"""End-to-end smoke tests against the live BufferStockTheory pipeline output.

These tests assume `bash tools/build-myst/build.sh` (or `make myst`) has been
run at least once. The full pipeline takes ~2 seconds, but we still skip the
tests rather than triggering the pipeline from inside pytest.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path  # noqa: E402


def _require(path: Path) -> Path:
    if not path.exists():
        pytest.skip(f"{path} not built; run `make myst` first")
    return path


@pytest.fixture(scope="module")
def final_md() -> str:
    return _require(build_path("10_with_frontmatter.md")).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def validation() -> dict:
    return json.loads(_require(build_path("11_validation.json")).read_text(encoding="utf-8"))


def test_no_residual_placeholders(validation: dict) -> None:
    assert validation["n_residual_placeholders"] == 0


def test_no_residual_latex_commands(validation: dict) -> None:
    assert validation["n_residual_latex_commands"] == 0


def test_no_draft_markers(validation: dict) -> None:
    assert validation["n_draft_markers"] == 0


def test_frontmatter_parses(validation: dict) -> None:
    assert validation["frontmatter_ok"] is True


def test_frontmatter_has_required_keys(validation: dict) -> None:
    keys = set(validation["frontmatter_keys"])
    for required in ("title", "authors", "abstract", "keywords"):
        assert required in keys, f"missing frontmatter key: {required}"


def test_anchor_count_in_expected_range(validation: dict) -> None:
    """The paper has many sections, equations, theorems, figures.
    Anchor count should be substantial (>200) and not absurdly large.
    """
    n = validation["n_anchors"]
    assert 200 <= n <= 1000, f"unexpected anchor count: {n}"


def test_references_section_present(final_md: str) -> None:
    assert "## References" in final_md


def test_introduction_heading_present(final_md: str) -> None:
    assert re.search(r"^#\s+Introduction\b", final_md, flags=re.MULTILINE)


def test_named_conditions_glossed(final_md: str) -> None:
    """At least one named-condition gloss should appear (e.g.
    "RIC (return impatience)").  Phase 8b reports >50 substitutions.
    """
    body = final_md.lower()
    assert "return impatience" in body or "ric" in body


def test_proof_directives_emitted(final_md: str) -> None:
    """Theorem/lemma directives should be present (Phase 7 emits ~60)."""
    n = len(re.findall(r":::\{prf:[a-z]+\}", final_md))
    assert n >= 30, f"expected >=30 prf directives, found {n}"


def test_figure_directives_emitted(final_md: str) -> None:
    n = len(re.findall(r":::\{figure\}", final_md))
    assert n >= 5
