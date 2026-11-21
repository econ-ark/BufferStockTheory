#!/usr/bin/env python3
"""Phase 03: Normalise custom commands to placeholder forms that survive pandoc.

Reads:  _build/myst/02_stripped.tex
Writes: _build/myst/03_normalized.tex

Sub-passes (in order):

3a. Generic-text macro substitution (\\REMARK → REMARK, \\ARKurl → Econ-ARK, ...).
    These can be safely expanded at the source level since they have no
    rendering subtleties.

3b. Citation placeholder emission. Every \\cite[X]{k1,k2}, \\citep[X]{k}, etc.
    becomes <<CITE:STYLE:keys>> where STYLE encodes the variant the source
    used. Phase 5 converts these to inline (Author, Year) prose. Done so that
    citations survive Pandoc unscathed (Pandoc otherwise drops or mangles them).

3c. Cross-reference placeholder emission. \\hypertarget{X}{Y} becomes
    <<ANCHOR:X>> Y; \\hyperlink{X}{Y} becomes <<XREF:X|Y>>; \\label{X} becomes
    <<ANCHOR:X>>; \\ref{X} / \\eqref{X} / \\Cref{X} / \\autoref{X} become
    <<XREF:X>>. Math-mode \\eqref/\\ref are LEFT ALONE (Phase 6 handles them
    via MyST `{eq}` role).

3d. Named-condition placeholder emission. Text-mode \\GIC, \\PFGIC, \\FHWC,
    \\FVAC, \\RIC, \\WRIC become <<NAMED:GIC>> etc. Math-mode occurrences are
    preserved raw (the macro is rendered by KaTeX via econark-math-macros.tex).

Also handles:
- `drop_macros`: silently delete \\subname{...}, \\authNum{...}, \\inframe{...}.
- `rename_macros`: \\labelsafe{X} → \\label{X}.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, config_path, read_text, write_text  # noqa: E402
from lib.tex_strip import find_balanced_brace_block  # noqa: E402
from lib.tex_tokenize import iter_segments  # noqa: E402


# ---------------------------------------------------------------------------
# 3a. Generic-text macro substitution
# ---------------------------------------------------------------------------

GENERIC_TEXT_MACROS = {
    r"\REMARK":      "REMARK",
    r"\ARKurl":      "Econ-ARK",
    r"\owner":       "llorracc",
    r"\texname":     "BufferStockTheory",
    r"\bibfilesfound": "",
    r"\BySame":      "———",
    r"\TH":          "Þ",
}

DROP_MACROS = (
    r"\subname",
    r"\authNum",
    r"\inframe",
    r"\providecmd",
    r"\appendixpage",
    r"\hypersetup",
)

RENAME_MACROS = {
    r"\labelsafe": r"\label",
    r"\refsafe":   r"\ref",
}

# KaTeX-specific text rewrites applied to math content. These are character
# sequences that pandoc passes through as-is but that the KaTeX renderer
# bundled with mystmd 1.8.x cannot handle.
#
# 1. `\colon=` and `\coloneqq` both expand in this KaTeX version through
#    `\html@mathml{\@binrel{...}...}`, which triggers
#    "Can't use function '\\@binrel' in text mode" on every use.
#    Substitute the literal two-character sequence `:=`.
#
# 2. `\BSTcondref{X}{Y}` is the canonical way the paper writes named-condition
#    references. KaTeX's macro engine doesn't handle 2-arg macros where only
#    one of the args appears in the body — and `#2`-only bodies render the
#    placeholder literally. Rewrite the call site directly to its expansion
#    `\textsf{\textrm{Y}}`. Same shim semantics as in @local/local.sty.
KATEX_TEXT_REWRITES = [
    (re.compile(r"\\colon\s*="), r":="),
    (re.compile(r"\\coloneqq\b"), r":="),
]


_MATH_ENV_NAMES = (
    "equation", "equation*",
    "aligned", "align", "align*",
    "gather", "gather*", "gathered",
    "eqnarray", "eqnarray*",
    "multline", "multline*",
    "displaymath",
)
_MATH_ENV_BEGIN_RE = re.compile(
    r"\\begin\{(" + "|".join(re.escape(n) for n in _MATH_ENV_NAMES) + r")\}"
)


def _collapse_blank_lines_in_math(text: str) -> str:
    r"""Drop blank lines from inside math environments.

    LaTeX silently tolerates blank lines inside `\begin{equation}` /
    `\begin{aligned}` / etc. but Pandoc converts them to markdown
    `$$...$$` blocks where a blank line *terminates* the math block —
    causing KaTeX to misparse everything after it ("Can't use function
    '$' in math mode" when the next inline math is encountered).

    This function scans for `\begin{ENV}...\end{ENV}` (matching the
    longest such region — math environments may be deeply nested,
    e.g. `equation > gathered > aligned`) and replaces blank lines
    inside with a single space.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        m = _MATH_ENV_BEGIN_RE.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        env = m.group(1)
        end_pat = r"\end{" + env + r"}"
        end_idx = text.find(end_pat, m.end())
        if end_idx == -1:
            out.append(text[m.start():])
            break
        body = text[m.start():end_idx + len(end_pat)]
        # Collapse blank-line gaps to a single newline. (Single newlines
        # are preserved — pandoc treats them as soft breaks inside math.)
        body = re.sub(r"\n[ \t]*\n+", "\n", body)
        out.append(body)
        i = end_idx + len(end_pat)
    return "".join(out)


def _rewrite_bstcondref(text: str) -> str:
    """Replace every `\\BSTcondref{X}{Y}` with `\\textsf{\\textrm{Y}}`.

    Uses balanced-brace scanning so `Y` may contain `{...}` (e.g. when
    a condition macro nests styled fragments). Matches the runtime
    behaviour of the LaTeX shim defined in ``@local/local.sty``.
    """
    needle = r"\BSTcondref{"
    out: list[str] = []
    i = 0
    n = len(text)
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
                    cursor += 1
                    break
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            # malformed call; emit verbatim and move on
            out.append(text[idx:cursor])
            i = cursor
            continue
        cursor += 1
        arg2_start = cursor
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
        arg2 = text[arg2_start:cursor]
        out.append(r"\textsf{\textrm{" + arg2 + "}}")
        i = cursor + 1
    return "".join(out)


def substitute_generic_text(text: str) -> str:
    out = text
    for macro, repl in GENERIC_TEXT_MACROS.items():
        # Word-boundary-aware replacement.
        pat = re.compile(re.escape(macro) + r"(?![A-Za-z@])")
        out = pat.sub(repl, out)
    return out


def drop_braced_macros(text: str, macros) -> str:
    """For each macro `\\X` in `macros`, remove `\\X{anything}` (one arg)."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        consumed = False
        for macro in macros:
            if text.startswith(macro, i):
                end_idx = i + len(macro)
                if end_idx < n and (text[end_idx].isalpha() or text[end_idx] == "@"):
                    continue
                cursor = end_idx
                while cursor < n and text[cursor].isspace():
                    cursor += 1
                if cursor < n and text[cursor] == "{":
                    try:
                        end = find_balanced_brace_block(text, cursor)
                        i = end
                        consumed = True
                        break
                    except ValueError:
                        pass
                # Bare control sequence with no arg — also drop it.
                i = end_idx
                consumed = True
                break
        if not consumed:
            out.append(text[i])
            i += 1
    return "".join(out)


def rename_macros(text: str, mapping: dict) -> str:
    out = text
    for old, new in mapping.items():
        pat = re.compile(re.escape(old) + r"(?![A-Za-z@])")
        # Use a lambda so backslashes in `new` are not interpreted as regex
        # backreferences (e.g. `\label` would otherwise raise "bad escape \l").
        out = pat.sub(lambda _m, _r=new: _r, out)
    return out


# ---------------------------------------------------------------------------
# 3b. Citation placeholder emission
# ---------------------------------------------------------------------------

# Maps source command → encoded style.
CITE_STYLES = {
    r"\cite":         "p",  # default (\cite ≅ \citep in econark style)
    r"\citep":        "p",
    r"\citet":        "t",
    r"\citeauthor":   "a",
    r"\citeyear":     "y",
    r"\citeyearpar":  "yp",
    r"\citealp":      "alp",
    r"\citealt":      "alt",
    r"\Citep":        "P",
    r"\Citet":        "T",
}

# Sort longest-first so \citeyearpar matches before \citeyear.
_CITE_NAMES_SORTED = sorted(CITE_STYLES.keys(), key=len, reverse=True)


def encode_cite_placeholder(text: str) -> str:
    """Turn LaTeX cite calls into `<<CITE:STYLE:opt|key1,key2>>` placeholders.

    Format:
        <<CITE:STYLE:keys>>           when there is no \\cite[opt]{...}
        <<CITE:STYLE/opt:keys>>       when an optional [opt] argument is present
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        matched = None
        for name in _CITE_NAMES_SORTED:
            if text.startswith(name, i):
                end_idx = i + len(name)
                if end_idx < n and (text[end_idx].isalpha() or text[end_idx] == "@"):
                    continue
                matched = name
                break
        if not matched:
            out.append(c)
            i += 1
            continue
        cursor = i + len(matched)
        # Optional [opt]
        opt = ""
        while cursor < n and text[cursor].isspace():
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
                        opt = text[cursor + 1:j]
                        cursor = j + 1
                        break
                j += 1
        while cursor < n and text[cursor].isspace():
            cursor += 1
        # Required {keys}
        if cursor >= n or text[cursor] != "{":
            out.append(text[i:cursor])
            i = cursor
            continue
        try:
            end = find_balanced_brace_block(text, cursor)
        except ValueError:
            out.append(text[i:cursor])
            i = cursor
            continue
        keys = text[cursor + 1:end - 1].strip()
        style = CITE_STYLES[matched]
        if opt:
            out.append(f"<<CITE:{style}/{opt}:{keys}>>")
        else:
            out.append(f"<<CITE:{style}:{keys}>>")
        i = end
    return "".join(out)


# ---------------------------------------------------------------------------
# 3c. Cross-reference placeholder emission (text-mode only)
# ---------------------------------------------------------------------------

LABEL_RE       = re.compile(r"\\label\{([^}]+)\}")
REF_RE         = re.compile(r"\\(?:ref|autoref)\{([^}]+)\}")
EQREF_RE       = re.compile(r"\\eqref\{([^}]+)\}")
CREF_RE        = re.compile(r"\\(?:Cref|cref)\{([^}]+)\}")
NAMEREF_RE     = re.compile(r"\\nameref\{([^}]+)\}")


def _replace_two_braced(text: str, command: str, format_fn) -> str:
    """Replace `\\command{a}{b}` with `format_fn(a, b)` using balanced-brace parsing.

    Handles bodies that themselves contain braces (e.g. `\\phantom{...}`).
    """
    out: list[str] = []
    i = 0
    n = len(text)
    needle = "\\" + command
    while i < n:
        idx = text.find(needle, i)
        if idx == -1:
            out.append(text[i:])
            break
        end_name = idx + len(needle)
        if end_name < n and (text[end_name].isalpha() or text[end_name] == "@"):
            out.append(text[i:end_name])
            i = end_name
            continue
        out.append(text[i:idx])
        cursor = end_name
        # Skip whitespace before first {.
        while cursor < n and text[cursor].isspace():
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            out.append(text[idx:cursor])
            i = cursor
            continue
        try:
            end1 = find_balanced_brace_block(text, cursor)
        except ValueError:
            out.append(text[idx:cursor])
            i = cursor
            continue
        a = text[cursor + 1:end1 - 1]
        cursor = end1
        while cursor < n and text[cursor].isspace():
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            out.append(text[idx:cursor])
            i = cursor
            continue
        try:
            end2 = find_balanced_brace_block(text, cursor)
        except ValueError:
            out.append(text[idx:cursor])
            i = cursor
            continue
        b = text[cursor + 1:end2 - 1]
        out.append(format_fn(a, b))
        i = end2
    return "".join(out)


def emit_xref_placeholders(text: str) -> str:
    """Convert text-mode hyper-/label-/ref-style commands to placeholders.

    `\\hypertarget` and `\\hyperlink` use balanced-brace parsing because their
    visible bodies can contain other LaTeX commands with their own braces
    (e.g. `\\phantom{...}`).
    """

    def _hypertarget(label, body):
        return f"<<ANCHOR:{label.strip()}>>{body}"

    def _hyperlink(target, body):
        # Pipe-separator: collapse any literal `|` in body to avoid colliding
        # with our `<<XREF:target|body>>` separator.
        body = body.strip().replace("|", "\u2502")
        return f"<<XREF:{target.strip()}|{body}>>"

    def _label(m):
        return f"<<ANCHOR:{m.group(1).strip()}>>"

    def _ref(m):
        return f"<<XREF:{m.group(1).strip()}>>"

    def _eqref(m):
        return f"<<EQREF:{m.group(1).strip()}>>"

    def _cref(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        return f"<<CREF:{','.join(keys)}>>"

    def _nameref(m):
        return f"<<NAMEREF:{m.group(1).strip()}>>"

    out = text
    out = _replace_two_braced(out, "hypertarget", _hypertarget)
    out = _replace_two_braced(out, "hyperlink",   _hyperlink)
    out = LABEL_RE.sub(_label, out)
    out = REF_RE.sub(_ref, out)
    out = EQREF_RE.sub(_eqref, out)
    out = CREF_RE.sub(_cref, out)
    out = NAMEREF_RE.sub(_nameref, out)
    return out


# ---------------------------------------------------------------------------
# 3d. Named-condition placeholder emission (text-mode only)
# ---------------------------------------------------------------------------

def emit_named_condition_placeholders(text: str, names: list[str]) -> str:
    """In text-mode segments only, turn `\\GIC` (etc.) into `<<NAMED:GIC>>`."""
    sorted_names = sorted(names, key=len, reverse=True)
    pat = re.compile(
        r"\\(" + "|".join(re.escape(n) for n in sorted_names) + r")(?![A-Za-z@])"
    )
    out: list[str] = []
    for mode, seg in iter_segments(text):
        if mode != "text":
            out.append(seg)
            continue
        out.append(pat.sub(lambda m: f"<<NAMED:{m.group(1)}>>", seg))
    return "".join(out)


# ---------------------------------------------------------------------------
# 3e. Theorem-environment sentinels (pre-pandoc)
# ---------------------------------------------------------------------------
# We replace `\begin{KIND}...\end{KIND}` with sentinel paragraphs that pandoc
# passes through as plain text. Phase 7 picks these up and emits MyST
# `:::{prf:KIND}` directives in their place.
#
# Sentinel format (pipe-delimited, single-line):
#     PRFBEGIN|kind|label|title
#     ... body content (untouched) ...
#     PRFEND
#
# `kind` is a config key from theorem-mapping.yml (theorem, proposition, ...);
# `label` is the value extracted from a `<<ANCHOR:...>>` placeholder
# immediately after `\begin{KIND}` (may be empty);
# `title` is extracted from an inline `(Title)` or `[Title]` decorator
# immediately after `\begin{KIND}` (may be empty).

THEOREM_KINDS = (
    "theorem", "proposition", "corollary", "lemma", "definition",
    "assumption", "conjecture", "remark", "example", "property",
    "claim", "fact", "proof",
    # Paper-specific assumption environments from @local/local.sty.
    # All three are aliases for "assumption" (see theorem-mapping.yml);
    # listing them here makes Phase 03 wrap them with PRFBEGIN/PRFEND
    # sentinels so Phase 07 can rewrite them to MyST directives.
    "assumL", "assumS", "assumI",
)

_BEGIN_RE = re.compile(
    r"\\begin\{(" + "|".join(THEOREM_KINDS) + r")\}"
)
_INLINE_ANCHOR_RE = re.compile(r"<<ANCHOR:([^>]*)>>")


def _consume_balanced(text: str, start: int, opener: str, closer: str) -> tuple[str, int] | None:
    """If text[start] == opener, consume balanced opener/closer pair.

    Returns (inner_content, end_index_after_closer) or None if no match.
    """
    if start >= len(text) or text[start] != opener:
        return None
    depth = 0
    i = start
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            i += 2
            continue
        if c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None


def convert_theorem_envs(text: str) -> str:
    """Wrap each `\\begin{KIND} ... \\end{KIND}` (KIND in THEOREM_KINDS) with
    sentinel paragraphs so pandoc preserves the boundary information.

    Handles decorations in any order:
        \\begin{theorem}(Title)\\n<<ANCHOR:label>>\\n body
        \\begin{theorem}<<ANCHOR:label>>(Title)body
        \\begin{proof}[Custom Title]body
    Plus bare `\\begin{theorem}\\nbody`.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        m = _BEGIN_RE.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        kind = m.group(1)
        cursor = m.end()
        title = ""
        label = ""
        # Consume any combination of [opt], (title), <<ANCHOR:label>>, and
        # whitespace, in any order, immediately following \begin{KIND}.
        progress = True
        while progress:
            progress = False
            # Skip horizontal whitespace and at most one newline after the begin.
            while cursor < n and text[cursor] in " \t":
                cursor += 1
            # [optional Title]
            if cursor < n and text[cursor] == "[":
                got = _consume_balanced(text, cursor, "[", "]")
                if got is not None:
                    if not title:
                        title = got[0].strip()
                    cursor = got[1]
                    progress = True
                    continue
            # (Title)
            if cursor < n and text[cursor] == "(":
                got = _consume_balanced(text, cursor, "(", ")")
                if got is not None:
                    if not title:
                        title = got[0].strip()
                    cursor = got[1]
                    # Eat a trailing period that often follows.
                    if cursor < n and text[cursor] == ".":
                        cursor += 1
                    progress = True
                    continue
            # <<ANCHOR:label>>
            am = _INLINE_ANCHOR_RE.match(text, cursor)
            if am:
                if not label:
                    label = am.group(1).strip()
                cursor = am.end()
                progress = True
                continue
            # Lone newline between decorators
            if cursor < n and text[cursor] == "\n":
                # Lookahead: if next non-whitespace is another decorator, eat newline.
                k = cursor + 1
                while k < n and text[k] in " \t":
                    k += 1
                if k < n and text[k] in "([<" or _INLINE_ANCHOR_RE.match(text, k):
                    cursor = k
                    progress = True
                    continue

        # Sanitize title and label for sentinel format.
        title_safe = title.replace("|", "\u2502").replace("\n", " ").strip()
        label_safe = label.replace("|", "").strip()

        out.append(f"\n\nPRFBEGIN|{kind}|{label_safe}|{title_safe}\n\n")

        end_pat = "\\end{" + kind + "}"
        end_idx = text.find(end_pat, cursor)
        if end_idx == -1:
            out.append(text[cursor:])
            i = n
            break
        out.append(text[cursor:end_idx])
        out.append("\n\nPRFEND\n\n")
        i = end_idx + len(end_pat)
    return "".join(out)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    src_path = build_path("02_stripped.tex")
    out_path = build_path("03_normalized.tex")

    raw = read_text(src_path)

    # Order matters: kill noise → emit placeholders.
    body = drop_braced_macros(raw, DROP_MACROS)
    body = rename_macros(body, RENAME_MACROS)
    body = substitute_generic_text(body)
    # KaTeX-specific math rewrites (apply before pandoc so the rewritten
    # text appears in math contexts in the .md output).
    for pat, repl in KATEX_TEXT_REWRITES:
        body = pat.sub(repl, body)
    body = _rewrite_bstcondref(body)
    body = _collapse_blank_lines_in_math(body)

    body = encode_cite_placeholder(body)
    body = emit_xref_placeholders(body)

    # Load named-conditions list from config.
    named_yml = yaml.safe_load(read_text(config_path("named-conditions.yml")))
    named_names = list(named_yml.keys())
    body = emit_named_condition_placeholders(body, named_names)

    # Wrap theorem-like environments with sentinel paragraphs so pandoc
    # preserves their boundaries for Phase 7.
    body = convert_theorem_envs(body)

    write_text(out_path, body)

    cite_count = body.count("<<CITE:")
    anchor_count = body.count("<<ANCHOR:")
    xref_count = body.count("<<XREF:")
    eqref_count = body.count("<<EQREF:")
    cref_count = body.count("<<CREF:")
    named_count = body.count("<<NAMED:")
    print(f"  normalized tex:  {out_path}")
    print(f"  placeholders:    cite={cite_count}  anchor={anchor_count}  "
          f"xref={xref_count}  eqref={eqref_count}  cref={cref_count}  named={named_count}")


if __name__ == "__main__":
    main()
