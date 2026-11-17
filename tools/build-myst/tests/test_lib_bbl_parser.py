"""Unit tests for `lib.bbl_parser`."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.bbl_parser import parse_bbl  # noqa: E402


def test_parses_single_harvarditem() -> None:
    bbl = r"""
\harvarditem{Carroll}{1997}{carrollBSLCPIH}
Carroll, Christopher D (1997): ``Buffer-Stock Saving and the Life
  Cycle/Permanent Income Hypothesis,'' \emph{Quarterly Journal of Economics},
  CXII(1), 1--56.

"""
    entries = parse_bbl(bbl)
    assert "carrollBSLCPIH" in entries
    e = entries["carrollBSLCPIH"]
    assert e.year == "1997"
    assert "Carroll" in e.short_authors
    assert "Buffer-Stock" in e.body
    # \emph rendered to *…*
    assert "*Quarterly Journal of Economics*" in e.body


def test_parses_optional_short_label() -> None:
    bbl = r"""
\harvarditem[Ma et~al.]{Ma, Stachurski, and Toda}{2020}{maUnboundedDP}
Ma, Q., J.~Stachurski, and A.~A. Toda (2020).
\newblock A note on Some Models of Income Fluctuation.

"""
    entries = parse_bbl(bbl)
    e = entries["maUnboundedDP"]
    # `~` collapsed to a space by the cleaner-style transformations.
    assert "Ma et" in e.short_authors and "al." in e.short_authors
    assert "Ma, Stachurski, and Toda" in e.long_authors


def test_strips_textsc_with_nested_braces() -> None:
    bbl = r"""
\harvarditem{Schmitt-Grohe}{2003}{sgu2003}
\textsc{Schmitt-Groh{\'e}, Stephanie, {and} Mart{\'\i}n Uribe} (2003)
"""
    entries = parse_bbl(bbl)
    body = entries["sgu2003"].body
    assert "\\textsc" not in body
    assert "Schmitt" in body and "Uribe" in body


def test_strips_brace_groups() -> None:
    bbl = r"""
\harvarditem{Carroll, et~al.}{2018}{carroll_et_al}
{C}hristopher {D}.~{C}arroll, {A}lexander {M}.~{K}aufman, {and} {M}atthew {N}.~{W}hite (2018).
"""
    entries = parse_bbl(bbl)
    body = entries["carroll_et_al"].body
    assert "{C}hristopher" not in body
    assert "Christopher" in body
    assert "{and}" not in body


def test_handles_multiple_entries() -> None:
    bbl = r"""
\harvarditem{Bewley}{1977}{bewleyPIH}
Bewley, Truman (1977): ``The Permanent Income Hypothesis: A Theoretical Formulation.''

\harvarditem{Deaton}{1991}{deatonLiqConstr}
Deaton, Angus (1991): ``Saving and Liquidity Constraints,'' \emph{Econometrica}, 59(5), 1221--1248.
"""
    entries = parse_bbl(bbl)
    assert set(entries.keys()) == {"bewleyPIH", "deatonLiqConstr"}
    assert all(e.year for e in entries.values())
