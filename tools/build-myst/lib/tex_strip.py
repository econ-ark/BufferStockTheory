"""Primitives for stripping TeX comments and conditional blocks.

Used by Phase 2 (whole-file conditional stripping) and re-used by tests.
"""

from __future__ import annotations

import re
from typing import List


_COMMENT_RE = re.compile(r"(?<!\\)%[^\n]*")


def strip_line_comments(text: str) -> str:
    """Remove `% ... \\n` comments while preserving escaped `\\%`.

    Phase 1 (`latexpand --keep-comments=false`) usually handles this, but the
    helper is exposed for use on snippets that did not pass through latexpand.
    """
    return _COMMENT_RE.sub("", text)


def find_balanced_brace_block(text: str, start: int) -> int:
    """Given text[start] == '{', return index *after* matching '}'."""
    if start >= len(text) or text[start] != "{":
        raise ValueError(f"expected '{{' at offset {start}")
    depth = 0
    i = start
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError(f"unbalanced '{{' starting at {start}")


def strip_ifthenelse_web(text: str) -> str:
    r"""Strip Web-conditional content, keeping the print branch.

    Handles three equivalent surface forms (B2 added the alias macros):
        \ifthenelse{\boolean{Web}}{ ... web ... }{ ... print ... }
        \BothVersions{ ... web ... }{ ... print ... }
        \WebOnly{ ... web ... }       -> drop entirely
        \PDFOnly{ ... print ... }     -> keep contents

    Each call balances {} brace depth via find_balanced_brace_block,
    which ignores braces that are part of \\macro tokens.
    """
    # First pass: \ifthenelse{\boolean{Web}}{...}{...} and \BothVersions{...}{...}.
    text = _strip_two_arg_web_macro(text, r"\ifthenelse{\boolean{Web}}", keep="second")
    text = _strip_two_arg_web_macro(text, r"\BothVersions",              keep="second")
    # Second pass: \WebOnly{...} -> drop; \PDFOnly{...} -> keep contents.
    text = _strip_one_arg_web_macro(text, r"\WebOnly", keep=False)
    text = _strip_one_arg_web_macro(text, r"\PDFOnly", keep=True)
    return text


def _strip_two_arg_web_macro(text: str, pat: str, keep: str) -> str:
    """Strip a 2-arg conditional macro. `keep` is "first" or "second"."""
    assert keep in ("first", "second")
    out: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        idx = text.find(pat, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        cursor = idx + len(pat)
        while cursor < n and text[cursor].isspace():
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            out.append(text[idx:cursor])
            i = cursor
            continue
        first_start = cursor + 1
        first_end = find_balanced_brace_block(text, cursor)
        cursor = first_end
        while cursor < n and text[cursor].isspace():
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            i = cursor
            continue
        second_start = cursor + 1
        second_end = find_balanced_brace_block(text, cursor)
        if keep == "first":
            out.append(text[first_start:first_end - 1])
        else:
            out.append(text[second_start:second_end - 1])
        i = second_end
    return "".join(out)


def _strip_one_arg_web_macro(text: str, pat: str, keep: bool) -> str:
    """Strip a 1-arg conditional macro. `keep`=True keeps contents, False drops."""
    out: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        idx = text.find(pat, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        cursor = idx + len(pat)
        while cursor < n and text[cursor].isspace():
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            out.append(text[idx:cursor])
            i = cursor
            continue
        arg_start = cursor + 1
        arg_end = find_balanced_brace_block(text, cursor)
        if keep:
            out.append(text[arg_start:arg_end - 1])
        i = arg_end
    return "".join(out)


_COMMENT_ENV_RE = re.compile(
    r"\\begin\{comment\}.*?\\end\{comment\}",
    flags=re.DOTALL,
)

_DEPRECATED_LINE_CMDS = (
    r"\maketitle",
    r"\titlepagefinish",
    r"\tableofcontents",
    r"\listoffigures",
    r"\listoftables",
    r"\pagebreak",
    r"\newpage",
    r"\clearpage",
    r"\cleardoublepage",
    r"\bigskip",
    r"\medskip",
    r"\smallskip",
    r"\noindent",
    r"\null",
    r"\sloppy",
    r"\appendix",
    r"\centering",
    r"\raggedright",
    r"\raggedleft",
    r"\onehalfspacing",
    r"\singlespacing",
    r"\doublespacing",
    r"\par",
    r"\@",
    r"\titlepagefinish",
)


def strip_comment_envs(text: str) -> str:
    return _COMMENT_ENV_RE.sub("", text)


def strip_deprecated_line_cmds(text: str) -> str:
    """Remove standalone control sequences from `_DEPRECATED_LINE_CMDS`.

    Uses a per-command word-boundary regex so that `\\par` does not eat
    `\\parbox`, `\\appendix` does not eat `\\appendixpage`, etc.

    A negative lookbehind on `\\` ensures we do not strip e.g. `\\tableofcontents`
    when it appears as `\\\\tableofcontents` (LaTeX line break followed by
    literal text), which would corrupt the surrounding braced argument.
    """
    out = text
    for cmd in _DEPRECATED_LINE_CMDS:
        # Escape backslash + name; require a non-alphabetic non-@ char after,
        # and refuse to match when the preceding char is a backslash (escape).
        pat = re.compile(r"(?<!\\)" + re.escape(cmd) + r"(?![A-Za-z@])")
        out = pat.sub("", out)
    return out


# Single-arg commands whose argument we want to delete entirely.
_ARG_KILLERS = (
    r"\hypersetup",
    r"\typeout",
    r"\pagenumbering",
    r"\setcounter",
    r"\renewcommand",
    r"\providecommand",
    r"\newcommand",
    r"\newif",
    r"\xrsetup",
    r"\externaldocument",
    r"\thispagestyle",
    r"\pagestyle",
    r"\subname",
    r"\keywords",
    r"\jelclass",
    r"\usepackage",
    r"\bibfilesfind",
    r"\bibliographystyle",
    r"\bibliography",
    r"\addcontentsline",
    r"\AddToShipoutPicture",
    r"\addtolength",
    r"\setlength",
    r"\appendixpage",
    r"\chead",
    r"\rhead",
    r"\lhead",
    r"\cfoot",
    r"\rfoot",
    r"\lfoot",
    r"\setboolean",
    r"\provideboolean",
    r"\titleformat",
    r"\titlespacing",
    r"\captionsetup",
)


def resolve_box_macros(text: str) -> str:
    r"""Inline LaTeX typesetting wrappers that pandoc cannot parse.

    Specifically:
      \savebox{\X}{Y}     -> Y          (keep content, drop the box-name binding)
      \sbox{\X}{Y}        -> Y
      \usebox{\X}         -> (empty)    (already inlined where defined)
      \resizebox{W}{H}{Y} -> Y
      \settowidth{\X}{Y}  -> (empty)
      \framebox{Y}        -> Y
      \framebox[W][P]{Y}  -> Y
      \makebox{Y}         -> Y
      \makebox[W][P]{Y}   -> Y
      \parbox[P]{W}{Y}    -> Y
      \parbox{W}{Y}       -> Y
      \mbox{Y}            -> Y
      \fbox{Y}            -> Y

    The replacements are done with balanced-brace awareness so multi-line
    bodies (typical for \savebox{\TblBox}{ \begin{tabular}...\end{tabular} })
    are handled correctly.
    """
    # Spec: list of (cmd, n_required_braced_args_before_keep, optional_brackets,
    # n_braced_args_after_keep, keep_index)
    # keep_index is the 1-based index of the {…} group whose contents we keep,
    # or None to drop everything.
    SPECS = [
        # name,            n_opt_brackets, brace_args_total, keep_index_or_None
        ("savebox",        0, 2, 2),
        ("sbox",           0, 2, 2),
        ("usebox",         0, 1, None),
        ("resizebox",      0, 3, 3),
        ("settowidth",     0, 2, None),
        ("framebox",       2, 1, 1),
        ("makebox",        2, 1, 1),
        ("parbox",         1, 2, 2),
        ("mbox",           0, 1, 1),
        ("fbox",           0, 1, 1),
    ]
    for name, n_opt, n_braces, keep in SPECS:
        text = _apply_box_spec(text, name, n_opt, n_braces, keep)
    return text


def _apply_box_spec(text, name, n_opt, n_braces, keep_index):
    out: list[str] = []
    i = 0
    n = len(text)
    needle = "\\" + name
    while i < n:
        idx = text.find(needle, i)
        if idx == -1:
            out.append(text[i:])
            break
        # Word-boundary check.
        end_idx = idx + len(needle)
        if end_idx < n and (text[end_idx].isalpha() or text[end_idx] == "@"):
            out.append(text[i:end_idx])
            i = end_idx
            continue
        out.append(text[i:idx])
        cursor = end_idx
        # Skip any number of optional [...] groups (up to n_opt).
        opts_seen = 0
        while opts_seen < n_opt:
            while cursor < n and text[cursor] in (" ", "\t"):
                cursor += 1
            if cursor < n and text[cursor] == "[":
                depth = 0
                j = cursor
                while j < n:
                    if text[j] == "[":
                        depth += 1
                    elif text[j] == "]":
                        depth -= 1
                        if depth == 0:
                            cursor = j + 1
                            break
                    j += 1
                opts_seen += 1
            else:
                break
        # Now consume n_braces braced groups.
        groups: list[tuple[int, int]] = []
        for _ in range(n_braces):
            while cursor < n and text[cursor] in (" ", "\t", "\n"):
                cursor += 1
            if cursor >= n or text[cursor] != "{":
                break
            try:
                end = find_balanced_brace_block(text, cursor)
            except ValueError:
                break
            groups.append((cursor + 1, end - 1))
            cursor = end
        if len(groups) < n_braces:
            # Malformed; emit literal and advance.
            i = cursor
            continue
        if keep_index is not None and 1 <= keep_index <= len(groups):
            s, e = groups[keep_index - 1]
            out.append(text[s:e])
        i = cursor
    return "".join(out)


_LET_RE = re.compile(
    r"\\let\s*"
    r"\\[A-Za-z@]+\s*"      # first control sequence
    r"=?\s*"                # optional `=`
    r"\\[A-Za-z@]+"         # second control sequence
)


def strip_let_assignments(text: str) -> str:
    r"""Remove `\let\foo\bar` (and `\let\foo=\bar`) — 2-token TeX assignments.

    Pandoc cannot parse these and they have no semantic meaning in the output.
    """
    return _LET_RE.sub("", text)


def strip_argkill_commands(text: str) -> str:
    """Remove `\\cmd{...}` (and any leading `[...]` option) for cmds in _ARG_KILLERS.

    Recognises `\\newcommand{name}{def}` etc. (consumes both braced groups).
    """
    out: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        # Match longest first.
        match = None
        for cmd in _ARG_KILLERS:
            if text.startswith(cmd, i):
                # Must not be a prefix of a longer macro name — check next char.
                end_idx = i + len(cmd)
                if end_idx < n and (text[end_idx].isalpha() or text[end_idx] == "@"):
                    continue
                if match is None or len(cmd) > len(match):
                    match = cmd
        if not match:
            out.append(text[i])
            i += 1
            continue
        cursor = i + len(match)
        # Skip whitespace
        while cursor < n and text[cursor].isspace():
            cursor += 1
        # Optional [...]
        if cursor < n and text[cursor] == "[":
            depth = 0
            j = cursor
            while j < n:
                if text[j] == "[":
                    depth += 1
                elif text[j] == "]":
                    depth -= 1
                    if depth == 0:
                        cursor = j + 1
                        break
                j += 1
            while cursor < n and text[cursor].isspace():
                cursor += 1
        # Now consume any number of {...} groups (1 or 2 typical)
        groups_consumed = 0
        while cursor < n and text[cursor] == "{":
            cursor = find_balanced_brace_block(text, cursor)
            groups_consumed += 1
            while cursor < n and text[cursor].isspace():
                cursor += 1
            if groups_consumed >= 3:
                break
        i = cursor
    return "".join(out)
