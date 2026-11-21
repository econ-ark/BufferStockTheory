#!/usr/bin/env python3
"""Phase 02: Strip preamble noise, web-only conditionals, and verbose blocks.

Reads:  _build/myst/01_flat.tex
Writes: _build/myst/02_stripped.tex
        _build/myst/02_metadata.json   (title, authors, abstract — for Phase 10)

Operations performed (in order):

1. Extract metadata fields from the master preamble (\\title, \\author, \\date,
   \\begin{abstract}...\\end{abstract}) into 02_metadata.json.
2. Drop the master preamble: anything before the first \\begin{document}.
3. Drop the master closing: \\bibliography{...} \\end{document} \\endinput line
   (the actual bibliography content is appended below as `\\harvarditem` block
   and is preserved).
4. Strip \\ifthenelse{\\boolean{Web}}{web}{print} keeping the print branch only.
5. Strip \\begin{comment}...\\end{comment} blocks.
6. Drop standalone frontmatter machinery (\\maketitle, \\tableofcontents, etc.).
7. Drop arg-killer commands (\\hypersetup{...}, \\setcounter{...}{...},
   \\renewcommand{...}{...}, \\providecommand{...}{...}, \\thispagestyle{...},
   \\pagestyle{...}, \\addcontentsline{...}{...}{...}, etc.).
8. Drop residual \\input{...} (anything Phase 1 could not resolve).
9. Drop the previously-extracted \\title/\\author/\\date/abstract content from
   the body so it doesn't appear twice in the output.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Ensure `lib/` is importable when this script is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, read_text, write_text  # noqa: E402
from lib.tex_strip import (  # noqa: E402
    resolve_box_macros,
    strip_argkill_commands,
    strip_comment_envs,
    strip_deprecated_line_cmds,
    strip_ifthenelse_web,
    strip_let_assignments,
)


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------

def _balanced(s: str, start: int, opener: str = "{", closer: str = "}") -> int:
    depth = 0
    i = start
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            i += 2
            continue
        if c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced")


def extract_braced_arg(text: str, command: str) -> str | None:
    """Return the {...} body of the FIRST occurrence of `\\command{...}`."""
    idx = text.find(command)
    while idx != -1:
        cursor = idx + len(command)
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor < len(text) and text[cursor] == "{":
            end = _balanced(text, cursor)
            return text[cursor + 1:end - 1].strip()
        idx = text.find(command, idx + len(command))
    return None


def extract_abstract(text: str) -> str | None:
    m = re.search(r"\\begin\{abstract\}", text)
    if not m:
        return None
    end_marker = "\\end{abstract}"
    end = text.find(end_marker, m.end())
    if end == -1:
        return None
    return text[m.end():end].strip()


def extract_metadata(preamble_plus_body: str) -> dict:
    return {
        "title":    extract_braced_arg(preamble_plus_body, r"\title"),
        "authors":  extract_braced_arg(preamble_plus_body, r"\author"),
        "date":     extract_braced_arg(preamble_plus_body, r"\date"),
        "keywords": extract_braced_arg(preamble_plus_body, r"\keywords"),
        "jelclass": extract_braced_arg(preamble_plus_body, r"\jelclass"),
        "abstract": extract_abstract(preamble_plus_body),
    }


# ---------------------------------------------------------------------------
# Body extraction & cleanup
# ---------------------------------------------------------------------------

PREAMBLE_END_RE = re.compile(r"\\begin\{document\}")

# After removing preamble, drop the master closing line which contains
# \bibliography{}\sloppy\end{document}\endinput. The bbl content was appended
# below this line by Phase 1 and is preserved.
MASTER_END_RE = re.compile(
    r"\\bibliography\{[^}]*\}\\sloppy\\end\{document\}\\endinput"
)

# Already-extracted blocks we now want to remove from the body.
TITLE_RE   = re.compile(r"\\title\s*\{")
AUTHOR_RE  = re.compile(r"\\author\s*\{")
DATE_RE    = re.compile(r"\\date\s*\{")
KEYWORDS_RE = re.compile(r"\\keywords\s*\{")
JELCLASS_RE = re.compile(r"\\jelclass\s*\{")

ABSTRACT_BLOCK_RE = re.compile(
    r"\\begin\{abstract\}.*?\\end\{abstract\}",
    flags=re.DOTALL,
)

# Residual unresolved \input{...} from Phase 1 (path macros that didn't expand).
UNRESOLVED_INPUT_RE = re.compile(r"\\input\s*\{[^}]*\}")


def remove_braced(text: str, regex: re.Pattern) -> str:
    """Remove every match of `\\cmd{` (regex) plus its balanced `{...}` body."""
    out: list[str] = []
    last = 0
    for m in regex.finditer(text):
        out.append(text[last:m.start()])
        # Locate the opening brace this regex landed on (or just after).
        cursor = m.end() - 1
        if cursor < len(text) and text[cursor] != "{":
            cursor = text.find("{", cursor)
            if cursor == -1:
                last = m.end()
                continue
        try:
            end = _balanced(text, cursor)
        except ValueError:
            last = m.end()
            continue
        last = end
    out.append(text[last:])
    return "".join(out)


def main() -> None:
    src_path = build_path("01_flat.tex")
    out_path = build_path("02_stripped.tex")
    meta_path = build_path("02_metadata.json")

    raw = read_text(src_path)

    metadata = extract_metadata(raw)

    # Body = everything starting at first \begin{document}, EXCLUDING the
    # \begin{document} marker itself.
    m = PREAMBLE_END_RE.search(raw)
    if m is None:
        body = raw
    else:
        body = raw[m.end():]

    body = MASTER_END_RE.sub("", body)
    body = strip_ifthenelse_web(body)
    body = strip_comment_envs(body)
    body = resolve_box_macros(body)
    # Arg-killers FIRST: they consume balanced {...} blocks, atomically removing
    # any deprecated commands nested inside (e.g. \typeout{after \\tableofcontents}).
    body = strip_argkill_commands(body)
    body = strip_let_assignments(body)
    body = strip_deprecated_line_cmds(body)

    body = remove_braced(body, TITLE_RE)
    body = remove_braced(body, AUTHOR_RE)
    body = remove_braced(body, DATE_RE)
    body = remove_braced(body, KEYWORDS_RE)
    body = remove_braced(body, JELCLASS_RE)
    body = ABSTRACT_BLOCK_RE.sub("", body)

    body = UNRESOLVED_INPUT_RE.sub("", body)

    body = re.sub(r"\n{3,}", "\n\n", body)

    write_text(out_path, body)
    write_text(meta_path, json.dumps(metadata, indent=2, ensure_ascii=False))

    # Stats
    n_lines = body.count("\n") + 1
    print(f"  stripped tex: {out_path} ({n_lines} lines)")
    print(f"  metadata:     {meta_path}")


if __name__ == "__main__":
    main()
