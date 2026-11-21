#!/usr/bin/env python3
"""Phase 08a: Convert pandoc `<figure>` HTML blocks to MyST `:::{figure}`
directives, and substitute LaTeX path macros (`\\FigDir`, `\\TableDir`, ...)
to their resolved relative paths.

Reads:  _build/myst/07_theorems.md
Writes: _build/myst/08a_paragraphs_figs.md

Pandoc renders `\\begin{figure} \\includegraphics ... \\caption ... \\end{figure}`
as raw HTML (we asked for `markdown_strict` with `raw_attribute` ext):

    <figure>
    <img src="\\FigDir/cNrmTargetFig" style="width:80.0%" />
    <p>
    (fig:cNrmTargetFig)=
    </p>
    <figcaption>Buffer Stock Target and Pseudo-Target</figcaption>
    </figure>

We rewrite each block to:

    (fig:cNrmTargetFig)=

    :::{figure} Figures/cNrmTargetFig.png
    :name: fig:cNrmTargetFig
    :width: 80%

    Buffer Stock Target and Pseudo-Target
    :::

Path-macro substitutions used here are also applied to any image references
that happen to slip through outside <figure> blocks.

`\\paragraph{X}` headings were already converted by pandoc to `#### X` so we
do not touch headings here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, read_text, write_text  # noqa: E402


# Path macro → relative path.
PATH_MACROS = {
    r"\FigDir":   "Figures",
    r"\TableDir": "Tables",
    r"\EqDir":    "Equations",
    r"\ApndxDir": "Appendices",
}


_FIGURE_RE = re.compile(
    r"<figure>(?P<body>.*?)</figure>",
    flags=re.DOTALL,
)
_IMG_RE = re.compile(
    r'<img\s+src="(?P<src>[^"]+)"(?:\s+style="(?P<style>[^"]*)")?\s*/?>'
)
_FIGCAPTION_RE = re.compile(r"<figcaption>(?P<cap>.*?)</figcaption>", flags=re.DOTALL)
_INLINE_ANCHOR_RE = re.compile(r"\((?P<label>[^)]+?)\)=")
_WIDTH_PCT_RE = re.compile(r"width:\s*([\d.]+)%")
_WIDTH_IN_RE = re.compile(r"width:\s*([\d.]+)\s*in")


_FIG_EXT_PRIORITY = (".png", ".svg", ".jpg", ".jpeg", ".pdf")


def _resolve_path(src: str) -> str:
    """Substitute path macros and pick a real file on disk.

    LaTeX `\\includegraphics{Foo}` resolves to whichever extension exists
    in the project tree.  We prefer raster/web formats (`.png`, `.svg`)
    over `.pdf` since the latter does not render natively in MyST/HTML
    output.
    """
    for macro, repl in PATH_MACROS.items():
        src = re.sub(re.escape(macro) + r"(?![A-Za-z@])", repl, src)

    project_root = Path(__file__).resolve().parents[3]
    if re.search(r"\.[A-Za-z0-9]{2,4}$", src):
        rel = src.lstrip("./")
        if (project_root / rel).exists():
            return src
        # Try alternate extensions for the same stem.
        stem_path = Path(rel).with_suffix("")
        for ext in _FIG_EXT_PRIORITY:
            candidate = project_root / stem_path.with_suffix(ext)
            if candidate.exists():
                return str(stem_path.with_suffix(ext))
        return src

    rel = src.lstrip("./")
    for ext in _FIG_EXT_PRIORITY:
        if (project_root / (rel + ext)).exists():
            return rel + ext
    return src + ".png"


def _extract_width(style: str | None) -> str:
    if not style:
        return ""
    m = _WIDTH_PCT_RE.search(style)
    if m:
        # Render `80.0` as `80`, but keep `12.5` as `12.5`.
        val = m.group(1)
        if "." in val:
            val = val.rstrip("0").rstrip(".")
        return f"{val or '0'}%"
    m = _WIDTH_IN_RE.search(style)
    if m:
        return f"{m.group(1)}in"
    return ""


def _convert_figure(match: re.Match) -> str:
    body = match.group("body")
    img_m = _IMG_RE.search(body)
    if not img_m:
        return match.group(0)  # pass-through if malformed.
    src = _resolve_path(img_m.group("src").strip())
    width = _extract_width(img_m.group("style"))

    cap_m = _FIGCAPTION_RE.search(body)
    caption = cap_m.group("cap").strip() if cap_m else ""

    # Anchor placeholder may appear anywhere inside the figure body.
    anc_m = _INLINE_ANCHOR_RE.search(body)
    label = anc_m.group("label").strip() if anc_m else ""

    lines: list[str] = []
    if label:
        lines.append(f"({label})=")
        lines.append("")
    head = f":::{{figure}} {src}"
    directive_lines: list[str] = [head]
    if label:
        directive_lines.append(f":name: {label}")
    if width:
        directive_lines.append(f":width: {width}")
    if label or width:
        directive_lines.append("")
    if caption:
        directive_lines.append(caption)
    directive_lines.append(":::")
    lines.append("\n".join(directive_lines))
    return "\n".join(lines)


def convert_figures(text: str) -> tuple[str, int]:
    n = 0

    def _sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        return _convert_figure(m)

    return _FIGURE_RE.sub(_sub, text), n


def resolve_remaining_paths(text: str) -> str:
    """Substitute path macros that appear outside of <figure> blocks (e.g. in
    raw markdown image references that slipped past pandoc).
    """
    for macro, repl in PATH_MACROS.items():
        text = re.sub(re.escape(macro) + r"(?![A-Za-z@])", repl, text)
    return text


def main() -> None:
    src = build_path("07_theorems.md")
    dst = build_path("08a_paragraphs_figs.md")

    text = read_text(src)
    text, n_figs = convert_figures(text)
    text = resolve_remaining_paths(text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    write_text(dst, text)
    print(f"  paragraphs/figs md: {dst}")
    print(f"  figures converted:  {n_figs}")


if __name__ == "__main__":
    main()
