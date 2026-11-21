"""Phase 01 implementation: recursive \\input{} / \\subfile{} expansion.

Drives `01_resolve_inputs.sh`. Splits out so we can write tests and keep the
shell script thin.

Behaviour:

- Reads the master TeX file.
- Substitutes econark path macros inside \\input{...}/\\subfile{...} arguments
  (\\ApndxDir → Appendices, \\econtexRoot/X → X, etc.).
- Replaces \\subfile{X} with \\input{X} so the same expander handles both.
- Recursively expands \\input{X} by reading X.tex (or X if the literal name
  has an extension) from the repo root.
- Skips paths starting with `@resources/` or `@local/` since these point at
  texmf-local content that pandoc can't use anyway; logs a warning.
- Strips `\\documentclass...{subfiles}` and the surrounding `\\begin{document}`/
  `\\end{document}` from inlined subfile content (a no-op once flattened).
- Detects cycles by tracking the inclusion stack.
- Hard-caps recursion depth (safety net).

Output: a single flattened .tex file with the resolved bibliography appended
between fence comments.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Set


PATH_SUBSTITUTIONS = [
    (r"\ApndxDir",       "Appendices"),
    (r"\EqDir",          "Equations"),
    (r"\TableDir",       "Tables"),
    (r"\FigDir",         "Figures"),
    (r"\ResourcesDir",   "@resources"),
    (r"\LaTeXGenerated", "."),
    (r"\LtxDir",         ""),
    (r"\econtexRoot/",   ""),
    (r"\econtexRoot",    "."),
]

INPUT_OR_SUBFILE_RE = re.compile(r"\\(?:input|subfile)\{([^}]+)\}")

DOCCLASS_RE = re.compile(
    r"\\documentclass\s*(?:\[[^\]]*\])?\s*\{[^}]*\}", re.DOTALL
)

# In an inlined subfile, also drop the document-environment wrappers and any
# trailing `\endinput`. These are preamble/finalisation noise once flattened.
SUBFILE_NOISE_RES = [
    re.compile(r"\\begin\{document\}"),
    re.compile(r"\\end\{document\}\\?endinput?"),
    re.compile(r"\\end\{document\}"),
    re.compile(r"\\endinput\b"),
    re.compile(r"\\sloppy\b"),
]

# Subfile-inclusion hooks consume one or two BALANCED braced groups, which
# may contain nested braces (e.g. `\notinsubfile{\captionsetup[fig]{list=no}}`).
# Handled separately via balanced-brace skipping.
SUBFILE_BRACED_HOOKS_1ARG = [
    "notinsubfile",
    "compilingassubfile",
    "onlyinsubfile",
]
SUBFILE_BRACED_HOOKS_2ARG = [
    "ifSubfilesClassLoaded",
]


def substitute_path_macros(arg: str) -> str:
    out = arg
    for macro, repl in PATH_SUBSTITUTIONS:
        out = out.replace(macro, repl)
    return out


def is_skippable(arg: str) -> bool:
    """Return True for paths we deliberately do NOT try to resolve.

    Resources and local-only files live outside the repo's tracked content.
    Their absence does not break the conversion — they are preamble-shaped
    and Phase 2 strips that anyway.
    """
    return arg.startswith("@resources/") or arg.startswith("@local/") or arg.startswith(".econtexRoot")


def find_tex_file(root: Path, name: str) -> Optional[Path]:
    """Locate a .tex file referenced by `\\input{name}`.

    Handles the common cases:
    - name has no extension → try name.tex
    - name has a .tex extension → use as-is
    - name otherwise → try as-is, then with .tex
    """
    candidates: List[Path] = []
    p = (root / name)
    if p.suffix == ".tex":
        candidates.append(p)
    else:
        candidates.append(p.with_suffix(".tex"))
        candidates.append(p)
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    return None


def _balanced_close(text: str, start: int) -> int:
    """Given text[start] == '{', return index after matching '}'. Raises if unbalanced."""
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
    raise ValueError("unbalanced")


def _drop_command_with_braced_args(text: str, name: str, n_args: int) -> str:
    needle = "\\" + name
    out: list[str] = []
    i = 0
    n = len(text)
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
        groups = 0
        while groups < n_args:
            while cursor < n and text[cursor] in (" ", "\t", "\n"):
                cursor += 1
            if cursor >= n or text[cursor] != "{":
                break
            try:
                end = _balanced_close(text, cursor)
            except ValueError:
                break
            cursor = end
            groups += 1
        if groups < n_args:
            i = cursor
            continue
        i = cursor
    return "".join(out)


_FIGMACRO_RENEW_RE = re.compile(
    r"\\renewcommand\{\\(figName|figFile)\}\{([^{}]*)\}"
)


def substitute_figname(text: str) -> str:
    r"""Substitute `\figName` / `\figFile` macro uses with their literal values.

    The source uses a pattern like:
        \renewcommand{\figName}{RelatePFGICFHWCRICPFFVAC}
        \hypertarget{\figName}{}
        \input{\FigDir/\figName}
    LaTeX expands `\figName` at use-time, but our static expander cannot.
    Walk the text linearly, tracking the most recent `\renewcommand{\figName}{X}`
    and `\renewcommand{\figFile}{X}`, and rewrite any subsequent occurrence of
    `\figName` / `\figFile` (followed by a non-letter token boundary) with the
    literal value, until the next `\renewcommand` updates state.

    Out of scope: macros declared via `\newcommand` (which only fire once) and
    macros assigned conditionally. The pattern this fixes is the simple
    sequential `\renewcommand` + use that body files use for figure inclusion.
    """
    state: dict[str, str] = {}
    out: List[str] = []
    i = 0
    n = len(text)
    pat = re.compile(
        r"\\renewcommand\{\\(figName|figFile)\}\{([^{}]*)\}"
        r"|"
        r"\\(figName|figFile)(?=[^A-Za-z]|$)"
    )
    while i < n:
        m = pat.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        if m.group(1) is not None:
            # \renewcommand{\figXxx}{value}: record state, emit verbatim.
            state[m.group(1)] = m.group(2)
            out.append(m.group(0))
        else:
            # bare \figName or \figFile: substitute if state is known, else leave.
            name = m.group(3)
            if name in state:
                out.append(state[name])
            else:
                out.append(m.group(0))
        i = m.end()
    return "".join(out)


def collapse_blank_lines_in_centerline(text: str) -> str:
    r"""Collapse paragraph-break blank lines inside `\centerline{...}` to a
    single space. LaTeX tolerates them (treats as a forced paragraph break);
    pandoc parses paragraph breaks inside braced macro args as terminators
    and chokes on the unmatched closing `}`.

    Body content uses this pattern in figure captions (e.g.
    `Figures/Inequalities.tex`): two sentences inside one `\centerline{}`
    separated by a blank line. The fix preserves the rendered output (both
    sentences flow together as a single line) while letting pandoc parse it.
    """
    out: List[str] = []
    i = 0
    n = len(text)
    needle = "\\centerline"
    while i < n:
        idx = text.find(needle, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        cursor = idx + len(needle)
        # Skip whitespace before the opening `{`.
        while cursor < n and text[cursor] in " \t\n":
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            # Not a `\centerline{...}` (could be `\centerlines` or similar).
            out.append(text[idx:cursor])
            i = cursor
            continue
        try:
            end = _balanced_close(text, cursor)
        except ValueError:
            out.append(text[idx:])
            i = n
            break
        body = text[cursor + 1:end - 1]
        body = re.sub(r"\n[ \t]*\n", " ", body)
        out.append("\\centerline{" + body + "}")
        i = end
    return "".join(out)


def strip_subfile_boilerplate(text: str) -> str:
    """Remove preamble + document-env wrappers that live in subfile sources.

    Subfiles look like:

        \\input{...resources}
        \\documentclass[Master]{subfiles}
        \\begin{document}
        ... real content ...
        \\end{document}\\endinput

    Once flattened, only the real content matters.
    """
    out = DOCCLASS_RE.sub("", text)
    for pat in SUBFILE_NOISE_RES:
        out = pat.sub("", out)
    for name in SUBFILE_BRACED_HOOKS_1ARG:
        out = _drop_command_with_braced_args(out, name, 1)
    for name in SUBFILE_BRACED_HOOKS_2ARG:
        out = _drop_command_with_braced_args(out, name, 2)
    return out


VERBATIMWRITE_RE = re.compile(
    r"\\begin\{verbatimwrite\}\{([^}]+)\}(.*?)\\end\{verbatimwrite\}",
    re.DOTALL,
)


def regenerate_verbatimwrite_targets(text: str, repo_root: Path, log) -> str:
    r"""Extract `\begin{verbatimwrite}{X}...\end{verbatimwrite}` blocks,
    write the contents to X (canonicalising path macros first), and remove
    the blocks from `text`.

    pdflatex's moreverb.verbatimwrite has the side-effect of writing the
    verbatim block to disk; the body that follows then `\input{X}`s the
    just-written file. The MyST pipeline cannot rely on pdflatex having
    run first (or having run with current sources), so we replicate the
    side effect here. Result: `Equations/X.tex` and `Tables/X.tex` files
    are guaranteed to be in sync with the master sources by the time
    Phase 01 reaches the matching `\input{}`.
    """
    out: List[str] = []
    last = 0
    for m in VERBATIMWRITE_RE.finditer(text):
        out.append(text[last:m.start()])
        target_arg = substitute_path_macros(m.group(1).strip())
        content = m.group(2)
        if content.startswith("\n"):
            content = content[1:]
        target_path = repo_root / target_arg
        if target_path.suffix != ".tex":
            target_path = target_path.with_suffix(".tex")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
        try:
            rel = target_path.relative_to(repo_root)
        except ValueError:
            rel = target_path
        log.write(f"  verbatimwrite: regenerated {rel}\n")
        last = m.end()
    out.append(text[last:])
    return "".join(out)


class UnresolvedInputError(RuntimeError):
    """Raised when \\input{} / \\subfile{} cannot be located on disk.

    Treated as fatal — silently dropping a missing input would mean an
    entire section of the paper goes missing from the MyST output with
    no other warning to the user.
    """


def expand(
    file_path: Path,
    repo_root: Path,
    seen: Set[Path],
    log,
    depth: int = 0,
    max_depth: int = 32,
) -> str:
    """Recursively expand \\input{}/\\subfile{} occurrences in file_path."""
    if depth > max_depth:
        log.write(f"WARN max recursion depth at {file_path}\n")
        return ""

    real = file_path.resolve()
    if real in seen:
        log.write(f"WARN cycle: skipping re-include of {real}\n")
        return ""
    seen.add(real)

    raw = file_path.read_text(encoding="utf-8", errors="replace")
    if depth > 0:
        raw = strip_subfile_boilerplate(raw)
    # Regenerate \verbatimwrite targets before resolving \input{}, so any
    # subsequent \input{Equations/X} reads fresh content.
    raw = regenerate_verbatimwrite_targets(raw, repo_root, log)
    raw = substitute_figname(raw)
    raw = collapse_blank_lines_in_centerline(raw)

    out: List[str] = []
    last = 0
    for m in INPUT_OR_SUBFILE_RE.finditer(raw):
        out.append(raw[last:m.start()])
        arg = substitute_path_macros(m.group(1).strip())
        if is_skippable(arg):
            log.write(f"WARN skipping unresolvable: {m.group(0)} -> {arg}\n")
            last = m.end()
            continue
        located = find_tex_file(repo_root, arg)
        if located is None:
            # Fatal: unresolved \input means content is silently missing
            # from the MyST output. Caller (main) prints to stderr.
            log.write(f"ERROR cannot find: {m.group(0)} -> {arg} (in {file_path})\n")
            raise UnresolvedInputError(
                f"\\input{{{arg}}} (referenced in {file_path}) does not "
                f"resolve to a file on disk"
            )
        log.write(f"  inlining ({depth}): {m.group(0)} -> {located.relative_to(repo_root)}\n")
        out.append(expand(located, repo_root, seen, log, depth + 1, max_depth))
        last = m.end()
    out.append(raw[last:])
    return "".join(out)


def strip_line_comments(text: str) -> str:
    r"""Remove `% ... \n` comments while preserving escaped \%."""
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", required=True)
    ap.add_argument("--bbl", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--log", required=True)
    args = ap.parse_args()

    repo_root = Path.cwd()
    master = Path(args.master)
    bbl = Path(args.bbl)
    output = Path(args.output)
    log_path = Path(args.log)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as log:
        log.write(f"# Phase 01 expand log\n")
        log.write(f"# repo_root: {repo_root}\n")
        log.write(f"# master: {master}\n")
        try:
            body = expand(master, repo_root, set(), log)
        except UnresolvedInputError as exc:
            print(f"Phase 01 ERROR: {exc}", file=sys.stderr)
            print(f"  see {log_path} for the full expansion trace", file=sys.stderr)
            sys.exit(1)
        body = strip_line_comments(body)

        bbl_text = bbl.read_text(encoding="utf-8", errors="replace")

        with open(output, "w", encoding="utf-8") as f:
            f.write(body)
            f.write("\n\n")
            f.write(f"% --- begin inlined bibliography (from {bbl}) ---\n")
            f.write(bbl_text)
            if not bbl_text.endswith("\n"):
                f.write("\n")
            f.write(f"% --- end inlined bibliography ---\n")

        log.write(f"# wrote: {output}\n")


if __name__ == "__main__":
    main()
