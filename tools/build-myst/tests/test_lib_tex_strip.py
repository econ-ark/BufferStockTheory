"""Unit tests for `lib.tex_strip`."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.tex_strip import (  # noqa: E402
    find_balanced_brace_block,
    resolve_box_macros,
    strip_argkill_commands,
    strip_comment_envs,
    strip_deprecated_line_cmds,
    strip_ifthenelse_web,
    strip_let_assignments,
    strip_line_comments,
)


# ---------- balanced-brace primitive --------------------------------------- #

def test_find_balanced_brace_block_simple() -> None:
    s = "before {a {b} c} after"
    end = find_balanced_brace_block(s, 7)
    assert s[7:end] == "{a {b} c}"


def test_find_balanced_brace_block_with_escape() -> None:
    s = r"before { \{ inside \} } after"
    end = find_balanced_brace_block(s, 7)
    assert s[7:end] == r"{ \{ inside \} }"


# ---------- comment stripping --------------------------------------------- #

def test_strip_line_comments_keeps_escaped_percent() -> None:
    s = "keep \\% no-comment % this is dropped\nnext line"
    out = strip_line_comments(s)
    assert "this is dropped" not in out
    assert "\\%" in out
    assert "no-comment" in out
    assert "next line" in out


def test_strip_comment_envs_removes_block() -> None:
    s = "before\n\\begin{comment}\nlots of stuff\n\\end{comment}\nafter"
    assert strip_comment_envs(s) == "before\n\nafter"


# ---------- ifthenelse web ------------------------------------------------ #

def test_strip_ifthenelse_web_keeps_else_branch() -> None:
    s = r"AAA\ifthenelse{\boolean{Web}}{web only}{print only}BBB"
    assert strip_ifthenelse_web(s) == "AAAprint onlyBBB"


def test_strip_ifthenelse_web_handles_nested_braces() -> None:
    s = r"\ifthenelse{\boolean{Web}}{a {nested {x}} b}{keep {me} {please}}"
    assert strip_ifthenelse_web(s) == "keep {me} {please}"


# ---------- deprecated line commands -------------------------------------- #

def test_strip_deprecated_keeps_longer_macros() -> None:
    s = r"\par should go but \parbox{w} should stay"
    out = strip_deprecated_line_cmds(s)
    assert "\\par " not in out  # `\par` standalone removed
    assert "\\parbox" in out


def test_strip_deprecated_does_not_break_escaped() -> None:
    s = r"text \\tableofcontents inside escape"
    # The leading `\\` is a LaTeX line break; `\tableofcontents` here is text.
    out = strip_deprecated_line_cmds(s)
    assert "\\tableofcontents" in out  # unchanged


# ---------- arg-killer commands ------------------------------------------- #

def test_strip_argkill_consumes_braced_block() -> None:
    s = r"keep \typeout{drop this {nested too}} more"
    out = strip_argkill_commands(s)
    assert "drop" not in out
    assert "keep" in out and "more" in out


def test_strip_argkill_handles_renewcommand_two_args() -> None:
    s = r"\renewcommand{\foo}{\bar} kept"
    out = strip_argkill_commands(s)
    assert out.strip() == "kept"


def test_strip_argkill_simple_form() -> None:
    s = r"\newcommand{\foo}{baz} kept"
    out = strip_argkill_commands(s)
    assert "kept" in out and "baz" not in out


# ---------- box macros ---------------------------------------------------- #

def test_resolve_box_macros_savebox_keeps_content() -> None:
    s = r"\savebox{\X}{visible content}"
    assert resolve_box_macros(s).strip() == "visible content"


def test_resolve_box_macros_resizebox_keeps_third_arg() -> None:
    s = r"\resizebox{2cm}{!}{some text}"
    assert resolve_box_macros(s).strip() == "some text"


def test_resolve_box_macros_settowidth_drops_all() -> None:
    s = r"before \settowidth{\X}{junk content} after"
    out = resolve_box_macros(s)
    assert "junk content" not in out
    assert "before" in out and "after" in out


def test_resolve_box_macros_parbox_with_optional() -> None:
    s = r"\parbox[t]{3cm}{the body}"
    assert resolve_box_macros(s).strip() == "the body"


# ---------- \let assignments --------------------------------------------- #

def test_strip_let_basic() -> None:
    assert strip_let_assignments(r"\let\foo\bar rest").strip() == "rest"


def test_strip_let_with_equals() -> None:
    assert strip_let_assignments(r"\let\foo=\bar rest").strip() == "rest"
