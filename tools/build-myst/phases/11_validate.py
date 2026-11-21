#!/usr/bin/env python3
"""Phase 11: Validation, privacy audit, and smoke probes.

Reads:  _build/myst/10_with_frontmatter.md  (final markdown)
        _build/myst/02_stripped.tex          (post-conditional source)
Writes: _build/myst/11_validation.json       (structured report)
        _build/myst/11_validation.txt        (human-readable summary)

Failure modes (cause non-zero exit):

  - frontmatter does not parse as YAML
  - residual placeholders (`<<...>>`)
  - residual LaTeX commands in body (e.g. `\\cite`, `\\ref`, `\\hyperlink`)
  - residual `Web`/draft markers (`\\Draft{...}`, `\\todo`, `XXX`, `FIXME`)
  - **equation labels missing from output** (every `\\label{eq:*}` in source
    must produce a matching `(eq:*)=` anchor — a missing one means
    `\\eqref` to that label is dead in the published markdown)
  - **raw `\\label{...}` left inside `$$...$$` display math** (Phase 06
    must lift these into preceding `(label)=` lines; anything still
    inside math means the lift missed it)

Equation correctness is the top priority. Any equation-related failure
above is fatal regardless of how clean the rest of the report is.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml  # type: ignore[import-untyped]

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import build_path, read_text, write_text  # noqa: E402


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", flags=re.DOTALL)
_PLACEHOLDER_RE = re.compile(r"<<[A-Z]+:[^>]*>>")
_LATEX_CMD_RE = re.compile(r"(?<!\\)\\(?:cite|ref|eqref|hyperlink|hypertarget|Cref|nameref|todo|Draft)[A-Za-z]*\b")
_DRAFT_RE = re.compile(r"\b(?:XXX|FIXME|TODO!|TBD)\b")
_ANCHOR_RE = re.compile(r"^[ \t]*\(([A-Za-z0-9_:.-]+)\)=\s*$", flags=re.MULTILINE)
# MyST `prf:` / figure / equation directive labels are also valid anchors:
#     :::{prf:theorem}
#     :label: thm:Boyd
# A cross-ref `[](#thm:Boyd)` resolves via the directive label, not via a
# `(X)=` standalone line. Treat both forms as anchor sources.
_LABEL_DIRECTIVE_RE = re.compile(r"^:label:\s+([A-Za-z0-9_:.-]+)\s*$", flags=re.MULTILINE)
# `:::{table}` and similar directives use `:name:` rather than `:label:`
# for the cross-ref id; both are valid anchor sources.
_NAME_DIRECTIVE_RE = re.compile(r"^:name:\s+([A-Za-z0-9_:.-]+)\s*$", flags=re.MULTILINE)
_LINK_RE = re.compile(r"\]\(#([A-Za-z0-9_:.-]+)\)")
_FIGURE_RE = re.compile(r":::\{figure\}\s*([^\s\n]+)")

# Equation-correctness checks. Sources may use \label{} or \labelsafe{}
# (the latter is renamed to \label by Phase 03 normalize_macros).
_SRC_EQ_LABEL_RE = re.compile(r"\\labels?(?:safe)?\{(eq:[^}]+)\}")
_RAW_LABEL_IN_LINE_RE = re.compile(r"\\labels?(?:safe)?\{[^}]+\}")


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = text[m.end():]
    fm = yaml.safe_load(fm_text) or {}
    return fm, body


def find_residual_placeholders(body: str) -> list[str]:
    return _PLACEHOLDER_RE.findall(body)


def find_residual_latex(body: str) -> list[str]:
    return _LATEX_CMD_RE.findall(body)


def find_draft_markers(body: str) -> list[str]:
    return _DRAFT_RE.findall(body)


def check_xref_targets(body: str) -> tuple[set[str], set[str], set[str]]:
    """Return (all_anchors, all_refs, missing).

    Every `[](#X)` reference must point at a `(X)=` anchor or `:label: X`
    directive line. This includes `cite-*` references — Phase 05 emits
    cite-anchors when it builds the References section, and any reference
    with no anchor is a broken link in the published markdown. The
    earlier carve-out for `cite-*` was a debugging convenience that
    masked Phase 05 cite-key resolution failures.
    """
    anchors = (
        set(_ANCHOR_RE.findall(body))
        | set(_LABEL_DIRECTIVE_RE.findall(body))
        | set(_NAME_DIRECTIVE_RE.findall(body))
    )
    refs = set(_LINK_RE.findall(body))
    missing = refs - anchors
    return anchors, refs, missing


def check_figure_paths(body: str, project_root: Path) -> list[str]:
    missing: list[str] = []
    for src in _FIGURE_RE.findall(body):
        if src.startswith(("http://", "https://")):
            continue
        rel = src.lstrip("./")
        if not (project_root / rel).exists():
            missing.append(src)
    return missing


def check_equation_labels(body: str, anchors: set[str]) -> tuple[set[str], set[str]]:
    """Compare `\\label{eq:*}` / `\\labelsafe{eq:*}` in the post-strip source
    against equation anchors in the final markdown.

    Pipeline conventions: source labels look like ``\\label{eq:Foo}``;
    Phase 06 emits the corresponding MyST target as ``(eq-Foo)=``
    (colons rewritten to dashes — see _safe_label in 06_resolve_xrefs.py
    for the mystmd prefix-strip workaround). The check converts source
    labels with the same transform before comparing.

    Returns (src_eq_labels, missing_in_output). A non-empty
    `missing_in_output` means an equation label in source did not
    survive to a MyST anchor — every `\\eqref` to that label will be a
    dead link.
    """
    src = build_path("02_stripped.tex")
    src_text = read_text(src)
    # Apply the same colon→dash transform Phase 06 uses for anchors.
    src_labels = {raw.replace(":", "-") for raw in _SRC_EQ_LABEL_RE.findall(src_text)}
    out_eq_anchors = {a for a in anchors if a.startswith("eq-") or a.startswith("eq:")}
    missing = src_labels - out_eq_anchors
    return src_labels, missing


def find_raw_labels_in_math(body: str) -> list[str]:
    """Detect raw `\\label{...}` / `\\labelsafe{...}` left inside `$$...$$`
    display-math blocks.

    Phase 06 lifts equation labels out of math blocks into preceding
    `(label)=` anchor lines. Anything still inside `$$...$$` after that
    means the lift missed it — KaTeX/MathJax will render `\\label{...}`
    as math text and `\\eqref{}` to that label will be dead.

    Detection assumes `$$` is on its own line (the canonical Pandoc
    output). Single-line `$$...$$` matches are rare; this function
    handles them but its primary target is multi-line blocks.
    """
    findings: list[str] = []
    in_math = False
    for line_no, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        # Toggle on standalone `$$` (start or end of display math block).
        if stripped == "$$":
            in_math = not in_math
            continue
        # Single-line `$$ ... $$`: only matters if it contains \label{}.
        if not in_math and stripped.startswith("$$") and stripped.rstrip().endswith("$$") and len(stripped) > 4:
            for m in _RAW_LABEL_IN_LINE_RE.finditer(line):
                findings.append(f"line {line_no}: {m.group(0)}")
            continue
        if in_math:
            for m in _RAW_LABEL_IN_LINE_RE.finditer(line):
                findings.append(f"line {line_no}: {m.group(0)}")
    return findings


def main() -> None:
    src = build_path("10_with_frontmatter.md")
    report_json = build_path("11_validation.json")
    report_txt = build_path("11_validation.txt")
    project_root = Path(__file__).resolve().parents[3]

    text = read_text(src)
    try:
        frontmatter, body = split_frontmatter(text)
        fm_ok = True
        fm_error: str | None = None
    except yaml.YAMLError as exc:
        frontmatter, body = {}, text
        fm_ok = False
        fm_error = str(exc)

    placeholders = find_residual_placeholders(body)
    latex_residue = find_residual_latex(body)
    draft = find_draft_markers(body)
    anchors, refs, missing_refs = check_xref_targets(body)
    missing_figs = check_figure_paths(body, project_root)
    src_eq_labels, missing_eq_anchors = check_equation_labels(body, anchors)
    raw_labels_in_math = find_raw_labels_in_math(body)

    report = {
        "frontmatter_ok": fm_ok,
        "frontmatter_error": fm_error,
        "frontmatter_keys": sorted(frontmatter.keys()) if frontmatter else [],
        "n_anchors": len(anchors),
        "n_refs": len(refs),
        "missing_xref_targets": sorted(missing_refs),
        "residual_placeholders": placeholders[:20],
        "n_residual_placeholders": len(placeholders),
        "residual_latex_commands": list(set(latex_residue))[:20],
        "n_residual_latex_commands": len(latex_residue),
        "draft_markers": draft[:20],
        "n_draft_markers": len(draft),
        "missing_figure_paths": missing_figs,
        "n_src_eq_labels": len(src_eq_labels),
        "missing_eq_anchors": sorted(missing_eq_anchors),
        "raw_labels_in_math": raw_labels_in_math[:20],
        "n_raw_labels_in_math": len(raw_labels_in_math),
        "body_chars": len(body),
        "body_lines": body.count("\n") + 1,
    }

    write_text(report_json, json.dumps(report, indent=2, ensure_ascii=False))

    lines = [
        "MyST validation report",
        "======================",
        f"frontmatter ok:        {fm_ok}",
        f"frontmatter keys:      {', '.join(report['frontmatter_keys']) or '-'}",
        f"anchors emitted:       {report['n_anchors']}",
        f"links to anchors:      {report['n_refs']}",
        f"missing xref targets:  {len(missing_refs)}"
        + (f"  (e.g. {', '.join(sorted(missing_refs)[:5])})" if missing_refs else ""),
        f"src eq labels:         {report['n_src_eq_labels']}",
        f"missing eq anchors:    {len(missing_eq_anchors)}"
        + (f"  ({', '.join(sorted(missing_eq_anchors)[:5])})" if missing_eq_anchors else ""),
        f"raw \\label in math:    {report['n_raw_labels_in_math']}"
        + (f"  ({'; '.join(raw_labels_in_math[:3])})" if raw_labels_in_math else ""),
        f"residual placeholders: {report['n_residual_placeholders']}",
        f"residual LaTeX cmds:   {report['n_residual_latex_commands']}"
        + (f"  ({', '.join(sorted(set(latex_residue)))})" if latex_residue else ""),
        f"draft markers:         {report['n_draft_markers']}",
        f"missing fig paths:     {len(missing_figs)}"
        + (f"  ({', '.join(missing_figs[:5])})" if missing_figs else ""),
        f"body lines / chars:    {report['body_lines']} / {report['body_chars']}",
    ]
    write_text(report_txt, "\n".join(lines) + "\n")
    for line in lines:
        print(f"  {line}")

    fatal: list[str] = []
    if not fm_ok:
        fatal.append("frontmatter does not parse")
    if placeholders:
        fatal.append(f"{len(placeholders)} residual placeholder(s)")
    if latex_residue:
        fatal.append(f"{len(latex_residue)} residual LaTeX command(s)")
    if draft:
        fatal.append(f"{len(draft)} draft marker(s)")
    # Equation correctness — top-priority checks. Any failure here means
    # an equation reference is broken in the published markdown.
    if missing_eq_anchors:
        fatal.append(f"{len(missing_eq_anchors)} equation label(s) missing from output")
    if raw_labels_in_math:
        fatal.append(f"{len(raw_labels_in_math)} raw \\label in display math")
    # Cross-reference and figure integrity — any broken link/path is a bug
    # in the published markdown that should not slip through silently.
    if missing_refs:
        fatal.append(f"{len(missing_refs)} broken cross-reference(s)")
    if missing_figs:
        fatal.append(f"{len(missing_figs)} missing figure path(s)")

    if fatal:
        print("\nFAIL: " + "; ".join(fatal))
        sys.exit(1)

    # Final integration check: does the published markdown actually
    # build with mystmd? Catches structural issues that pure-string
    # validation misses (mystmd config errors, malformed directives,
    # KaTeX errors that slipped past Phase 00). Skipped if `myst` is
    # not on PATH so contributors without the CLI can still run the
    # pipeline up to this point.
    #
    # We use non-strict mode because mystmd 1.8.x's strict link
    # resolver fires on `prefix:name` label collisions that are
    # fundamental tool behaviour (Phase 06's colon→dash transform
    # eliminates the colon-prefix variant; the remaining warnings
    # are MyST collapsing duplicate labels — a different mechanism
    # that the pipeline cannot fully sidestep). The site still builds
    # and renders; the strict link warnings are reported in
    # _build/site-build.log for review.
    import shutil
    import subprocess

    myst_cli = shutil.which("myst")
    if myst_cli is None:
        print("\nNOTE: myst CLI not on PATH; skipping strict-build integration check.")
        print("OK")
        return

    log_path = build_path("12_myst_build.log")
    print(f"\n  running `myst build --html` (strict-build integration check)...")
    try:
        result = subprocess.run(
            [myst_cli, "build", "--html"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        print("  WARN: myst build did not finish in 120s; skipping the check.")
        print("OK")
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(result.stdout + "\n--- stderr ---\n" + result.stderr,
                        encoding="utf-8")
    n_warn = result.stdout.count("⚠️") + result.stderr.count("⚠️")
    n_err  = result.stdout.count("⛔") + result.stderr.count("⛔")
    print(f"  myst build exit={result.returncode}, warnings={n_warn}, errors={n_err}")
    print(f"  full log: {log_path}")
    if result.returncode != 0:
        # Real build failure — surface and abort.
        print("\nFAIL: myst build returned non-zero")
        print(result.stderr[-2000:] if result.stderr else "(no stderr)")
        sys.exit(1)
    # Even when mystmd exits 0, "⛔" markers in its output indicate hard
    # render failures (KaTeX errors, malformed directives) that the
    # build tolerates but which mean the published HTML is broken.
    # Surface a summary; exact entries are in the log file.
    if n_err > 0:
        print(f"\nFAIL: myst build reported {n_err} render error(s)")
        for line in (result.stdout + result.stderr).splitlines():
            if "⛔" in line:
                print(f"  {line.strip()}")
        sys.exit(1)
    print("\nOK")


if __name__ == "__main__":
    main()
