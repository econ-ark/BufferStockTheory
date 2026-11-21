"""Extract and KaTeX-normalise math macros from the econark shortcuts source.

The canonical source of paper math macros is
`@resources/markdown/econark-shortcuts.md`, a Jekyll-flavoured markdown file
holding ~307 `\\newcommand` definitions. The MyST pipeline needs them as a
YAML map under `project.math:` in `myst.yml` (or in a file referenced via
`extends:`) so KaTeX can resolve them when rendering equations.

Two transforms happen here:

1. **Parse** balanced-brace `\\newcommand{\\NAME}[N]{BODY}` blocks. The source
   uses `{% raw %}` Jekyll fences and sometimes ends a body with an extra `}`
   to avoid `}}` colliding with Liquid template delimiters; strip those.

2. **Rewrite for KaTeX.** A handful of LaTeX commands have no KaTeX
   counterpart and would error if a macro body uses them. Per the project's
   "robustness > fidelity" mandate, we substitute the closest KaTeX-renderable
   shape (visual aesthetic may shift; meaning survives):

   - ``\\hyperlink{X}{Y}`` → ``\\textsf{Y}``  (drops the link, keeps styled text)
   - ``\\href{X}{Y}``      → ``Y``            (drops link entirely)
   - ``\\unicode{NNNN}``   → the literal Unicode character at codepoint NNNN

   Unrewritten macros that still contain KaTeX-incompatible commands will
   surface as `myst build --strict` errors downstream — that's OK; the
   strict-build check in Phase 11 catches them.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator


# Match \newcommand, \providecommand, and \renewcommand. All three share
# the syntax `\X{\NAME}[N]{BODY}` OR the brace-less variant `\X\NAME[N]{BODY}`
# that some TeX sources (notably the econark shortcuts markdown) use for
# redefinitions. We parse both identically and let the "last definition
# wins" rule in parse_newcommands sort out duplicates.
_NEWCOMMAND_RE = re.compile(
    r"\\(?:new|provide|renew)command"
    r"(?:\{\\([A-Za-z]+)\}|\\([A-Za-z]+))"
    r"(?:\[(\d+)\])?\{"
)
_UNICODE_RE = re.compile(r"\\unicode\{(\d+)\}")


def _balanced_close(text: str, start: int) -> int:
    """Index just past the `}` that matches the `{` immediately before `start`.

    `start` is the position right after the opening brace; the function
    walks forward, tracking depth, and returns the index after the
    matching closing brace.
    """
    depth = 1
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
    raise ValueError(f"unbalanced braces from offset {start}")


_TEX_COMMENT_RE = re.compile(r"(?<!\\)%[^\n]*")


def _strip_tex_comments_and_collapse(body: str) -> str:
    """Drop `% ... \\n` TeX comments and collapse remaining whitespace.

    TeX comments hide the rest of the line *and* the following newline,
    which body-spanning macros rely on to chain across lines. After
    stripping comments we collapse all whitespace to single spaces so
    the body fits on one YAML line.
    """
    out = _TEX_COMMENT_RE.sub("", body)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def parse_newcommands(text: str) -> dict[str, tuple[int | None, str]]:
    """Extract every `\\newcommand{\\NAME}[N]{BODY}` (or providecommand /
    renewcommand) from `text`.

    Returns ``{name: (nargs_or_None, body)}``. Last definition wins if a
    macro is repeated (matches LaTeX's behaviour with `\\renewcommand`-
    style overrides, though `\\newcommand` itself errors on redefinition;
    the source file mostly uses `\\newcommand` once per name anyway).

    Bodies are post-processed: TeX `% ...` comments are stripped, and
    whitespace (including embedded newlines from multi-line macro
    definitions) is collapsed to single spaces. This makes them safe
    for single-line YAML emission.

    Empty bodies are kept — for some macros the empty expansion IS the
    intended behaviour (e.g. our katex-shims override of `\\WebOnly` is
    `\\renewcommand{\\WebOnly}[1]{}` to drop Web-only content). Pure
    forward-declaration "empty stubs" in the source are caught by the
    later-source-wins ordering in extract_to_yaml.
    """
    out: dict[str, tuple[int | None, str]] = {}
    for m in _NEWCOMMAND_RE.finditer(text):
        name = m.group(1) or m.group(2)
        nargs = int(m.group(3)) if m.group(3) else None
        try:
            end = _balanced_close(text, m.end())
        except ValueError:
            continue
        body = text[m.end():end - 1]
        # Jekyll source escapes some `}}` collisions with an extra `}`;
        # the parsed body then has more `}` than `{`. Trim trailing `}`
        # until balanced (or empty).
        while body.endswith("}") and body.count("{") < body.count("}"):
            body = body[:-1]
        body = _strip_tex_comments_and_collapse(body)
        out[name] = (nargs, body)
    return out


def _rewrite_two_arg(body: str, name: str, replace: callable) -> str:
    """Locate every `\\name{ARG1}{ARG2}` in `body` (with brace-balanced ARGs,
    possibly nested) and replace each with `replace(arg1, arg2)`.

    Necessary because `\\hyperlink{X}{Y}` and `\\href{X}{Y}` may have ARG2
    contents like `\\textrm{APF}` that contain nested braces, which a
    naive `[^{}]*` regex cannot match.
    """
    needle = "\\" + name + "{"
    out: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        idx = body.find(needle, i)
        if idx == -1:
            out.append(body[i:])
            break
        out.append(body[i:idx])
        try:
            arg1_end = _balanced_close(body, idx + len(needle))
        except ValueError:
            out.append(body[idx:])
            break
        if arg1_end >= n or body[arg1_end] != "{":
            out.append(body[idx:arg1_end])
            i = arg1_end
            continue
        try:
            arg2_end = _balanced_close(body, arg1_end + 1)
        except ValueError:
            out.append(body[idx:])
            break
        arg1 = body[idx + len(needle):arg1_end - 1]
        arg2 = body[arg1_end + 1:arg2_end - 1]
        out.append(replace(arg1, arg2))
        i = arg2_end
    return "".join(out)


def katex_safe(body: str) -> str:
    """Rewrite `body` to use only KaTeX-supported commands.

    See module docstring for the rewrite list. This is purely textual; it
    does not attempt to verify that the output is a complete, parseable
    macro body — the strict-build check in Phase 11 is the integration
    test.
    """
    out = _rewrite_two_arg(body, "hyperlink",  lambda _a, b: r"\textsf{" + b + "}")
    out = _rewrite_two_arg(out,  "href",       lambda _a, b: b)
    # \BSTcondref{X}{Y} is the paper's named-condition shim. mystmd 1.8.x's
    # KaTeX cannot evaluate two-arg macro bodies that reference only #2
    # (the placeholder leaks through literally). Pre-expand each call site
    # to its PDF-mode rendering: \textsf{\textrm{Y}}.
    out = _rewrite_two_arg(out,  "BSTcondref", lambda _a, b: r"\textsf{\textrm{" + b + "}}")
    out = _UNICODE_RE.sub(lambda m: chr(int(m.group(1))), out)
    return out


def to_macro_map(macros: dict[str, tuple[int | None, str]]) -> dict[str, str]:
    """Produce the `name -> body` map suitable for YAML emission.

    All macros emit as plain strings; KaTeX's macro engine infers the
    argument count from the highest `#N` placeholder in the body. This
    matches the format used by mystmd's `project.math:` resolver.
    """
    out: dict[str, str] = {}
    for name in sorted(macros):
        nargs, body = macros[name]
        body_safe = katex_safe(body)
        key = "\\" + name
        out[key] = body_safe
    return out


def render_yaml(mac_map: dict[str, object], header_comment: str = "") -> str:
    """Emit the macro map as a complete mystmd config with `project.math:`.

    Output shape (required by mystmd's `extends:` resolver, which expects
    each extended file to be itself a valid mystmd config file):

        version: 1
        project:
          math:
            '\\Foo': '\\bar'
            ...

    Hand-rolled rather than `yaml.safe_dump` so we can keep keys
    single-quoted (preserves backslashes literally without YAML
    escaping ambiguity) and group output predictably.
    """
    lines: list[str] = []
    if header_comment:
        for h in header_comment.splitlines():
            lines.append(f"# {h}" if h else "#")
        lines.append("")
    lines.append("version: 1")
    lines.append("project:")
    lines.append("  math:")
    for key in mac_map:  # already sorted by to_macro_map
        val = mac_map[key]
        # Single-quote both key and value; double single-quotes inside.
        key_escaped = key.replace("'", "''")
        val_escaped = val.replace("'", "''")
        lines.append(f"    '{key_escaped}': '{val_escaped}'")
    return "\n".join(lines) + "\n"


def extract_to_yaml(*sources: Path, header_comment: str = "") -> str:
    """One-shot: read each source file in order, parse, normalise, emit YAML.

    Multiple sources are concatenated so later definitions override
    earlier ones. The expected use is

        extract_to_yaml(econark_shortcuts_md, local_sty,
                        local_tikz_sty, ...)

    where the markdown shortcut file holds the broad pool of econark
    macros and the .sty files contribute paper-specific overrides
    (e.g. condition macros redefined to use \\BSTcondref-style
    fallbacks).
    """
    parts: list[str] = []
    for src in sources:
        if src.exists():
            parts.append(src.read_text(encoding="utf-8"))
    text = "\n".join(parts)
    macros = parse_newcommands(text)
    mac_map = to_macro_map(macros)
    return render_yaml(mac_map, header_comment=header_comment)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Usage:  python -m lib.math_macros <output.yml> <source1> [<source2> ...]

    Reads ``\\newcommand`` / ``\\providecommand`` / ``\\renewcommand``
    definitions from each source file in order, rewrites bodies for
    KaTeX, and writes a single YAML config to ``<output.yml>``. Later
    sources override earlier ones (matches LaTeX's renewcommand
    semantics).
    """
    import sys
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 2:
        print(
            "usage: math_macros.py <output.yml> <source1> [<source2> ...]",
            file=sys.stderr,
        )
        return 64
    out_path = Path(args[0])
    sources = [Path(s) for s in args[1:]]
    missing = [s for s in sources if not s.exists()]
    if missing:
        for s in missing:
            print(f"ERROR: source not found: {s}", file=sys.stderr)
        return 1
    src_list = "\n  - " + "\n  - ".join(str(s) for s in sources)
    header = (
        "Auto-generated by tools/build-myst/lib/math_macros.py from:"
        + src_list + "\n"
        "DO NOT EDIT BY HAND — your changes will be overwritten on the\n"
        "next pipeline run.  Edit the source files instead, then re-run\n"
        "`bash tools/build-myst/build.sh` (which calls Phase 00)."
    )
    yaml_text = extract_to_yaml(*sources, header_comment=header)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml_text, encoding="utf-8")
    print(f"  wrote {out_path}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
