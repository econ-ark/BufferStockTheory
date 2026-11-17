"""Adjacent-label cluster detection and reference rewriting.

When LaTeX source places multiple ``\\hypertarget{X}{}`` / ``\\label{X}``
calls right next to a theorem-like environment, they all anchor at the
same target block. mystmd 1.8.x then "auto-collapses" them to a single
canonical name (typically the shortest), silently leaving the others
without HTML ids — and every cross-reference to a dropped name becomes
a dead link.

This module implements the same collapse mystmd does, but BEFORE it does
— and rewrites all cross-references to use the canonical name. Result:
no dead in-page links in the rendered HTML.

Algorithm:

  1. Walk the markdown line-by-line. Track "clusters" of label lines
     (``(X)=`` and ``:label: X``) connected only by transparent lines:
     blank lines, MyST directive opener / closer lines (``:::{...}`` /
     ``:::``).
  2. A non-transparent, non-label line ends the cluster.
  3. For each cluster of size > 1, pick the canonical name the same
     way mystmd does: **first occurrence wins** in document order.
     (Empirically derived from the reproduction warnings — e.g.
     `(FVAC)=` followed by `:label: ass-FVAC` keeps `FVAC` because
     it appeared first; `(Sufficient-Conditions...)= ` followed by
     `:label: thm-convgtobellman` keeps the long name because it
     appeared first.)
  4. Build an alias map ``{non_canonical: canonical}``.
  5. Rewrite every ``[](#non_canonical)`` reference in the text.

The duplicate label LINES themselves are left in place — mystmd will
collapse them at render time. We only fix the references.
"""

from __future__ import annotations

import re

_ANCHOR_LINE_RE = re.compile(r"^[ \t]*\(([A-Za-z0-9_.\-]+)\)=\s*$")
_LABEL_DIRECTIVE_LINE_RE = re.compile(r"^[ \t]*:label:\s+([A-Za-z0-9_.\-]+)\s*$")


def _is_transparent(line: str) -> bool:
    """Return True for lines that don't break a label cluster."""
    s = line.strip()
    if s == "":
        return True
    # MyST directive opener / closer / inner attribute lines that are
    # not real content. ``:::{prf:foo} Title`` is treated as transparent
    # since the directive is itself the cluster's target block.
    if s.startswith(":::"):
        return True
    return False


# Label prefixes that have meaningful semantics — we never drop a label
# bearing one of these prefixes during cluster collapse. This keeps
# `eq-foo`, `thm-foo`, `lemm-foo`, etc. anchors intact even when an
# adjacent unprefixed hypertarget is the cluster's canonical.
_PREFERRED_PREFIXES = ("eq-", "thm-", "lemm-", "lemma-", "prop-", "claim-",
                       "fact-", "fig-", "def-", "ass-")


def _has_preferred_prefix(name: str) -> bool:
    return any(name.startswith(p) for p in _PREFERRED_PREFIXES)


def merge_adjacent_label_clusters(text: str) -> tuple[str, dict[str, str]]:
    """Return (rewritten_text, aliases). Rewrites all ``[](#X)`` so that
    references use the canonical (first-in-order) name within each
    cluster of adjacent labels.

    Also drops redundant `(label)=` anchor LINES from each cluster when
    the canonical is a section/concept name and the cluster contains
    *only* anchor-form labels with no preferred prefix (`eq-`, `thm-`,
    etc.). This is what makes plain markdown tables get an HTML id —
    mystmd's auto-collapse otherwise leaves none of the cluster's
    labels emitted as ids when there are several stacked above a
    table. ``:label:`` directive lines and labels with preferred
    prefixes are always kept (dropping them would orphan a directive
    or fail Phase 11's equation-parity check).
    """
    lines = text.split("\n")
    n = len(lines)

    aliases: dict[str, str] = {}
    drop_lines: set[int] = set()

    i = 0
    while i < n:
        line = lines[i]
        m_a = _ANCHOR_LINE_RE.match(line)
        m_d = _LABEL_DIRECTIVE_LINE_RE.match(line)
        if not m_a and not m_d:
            i += 1
            continue
        # cluster: list of (line_index, name, is_directive_label)
        cluster: list[tuple[int, str, bool]] = [(i, (m_a or m_d).group(1), bool(m_d))]
        j = i + 1
        while j < n:
            nxt = lines[j]
            n_a = _ANCHOR_LINE_RE.match(nxt)
            n_d = _LABEL_DIRECTIVE_LINE_RE.match(nxt)
            if n_a or n_d:
                cluster.append((j, (n_a or n_d).group(1), bool(n_d)))
                j += 1
                continue
            if _is_transparent(nxt):
                j += 1
                continue
            break
        # Preserve document order; dedupe in-cluster while keeping order.
        seen_in_cluster: set[str] = set()
        ordered_unique: list[str] = []
        for _, name, _ in cluster:
            if name not in seen_in_cluster:
                seen_in_cluster.add(name)
                ordered_unique.append(name)
        if len(ordered_unique) > 1:
            canonical = ordered_unique[0]  # first wins (matches mystmd)
            for other in ordered_unique[1:]:
                if other not in aliases:
                    aliases[other] = canonical
            # Drop non-canonical anchor-form labels that don't have a
            # preferred prefix. Keep all `:label:` directive lines and
            # all labels bearing a preferred prefix.
            for (line_idx, name, is_dir) in cluster:
                if name == canonical:
                    continue
                if is_dir:
                    continue
                if _has_preferred_prefix(name):
                    continue
                drop_lines.add(line_idx)
        i = j if j > i else i + 1

    if drop_lines:
        kept = [ln for idx, ln in enumerate(lines) if idx not in drop_lines]
        text = "\n".join(kept)

    if not aliases:
        return text, aliases

    def _resolve(m: re.Match) -> str:
        target = m.group(1)
        return f"](#{aliases[target]})" if target in aliases else m.group(0)

    text = re.sub(r"\]\(#([A-Za-z0-9_.\-]+)\)", _resolve, text)
    return text, aliases


_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_CAPTION_RE = re.compile(r"^\s*:\s+(.+?)\s*$")


def wrap_labelled_tables_in_directives(text: str) -> tuple[str, int]:
    """Wrap label-prefixed markdown tables in ``:::{table}`` directives so
    mystmd emits an HTML id for the canonical label.

    mystmd 1.8.x does NOT attach ``(label)=`` anchors to subsequent plain
    markdown tables — the label gets recorded internally but no
    ``id="label"`` is emitted in the rendered HTML, so every reference
    is a dead link. The fix is to use the proper directive form, which
    DOES accept ``:label:`` and ``:name:`` and emits the id.

    Pattern detected:
        (X)=
        (newline)
        | header | header |
        |--------|--------|
        | row    | row    |
        (newline)
        : caption text                    (optional)

    Becomes:
        :::{table} caption text
        :label: X
        :name: X

        | header | header |
        |--------|--------|
        | row    | row    |

        :::

    Returns ``(text, n_wrapped)``.
    """
    lines = text.split("\n")
    n = len(lines)
    out: list[str] = []
    i = 0
    n_wrapped = 0
    while i < n:
        line = lines[i]
        m = _ANCHOR_LINE_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue
        # Look ahead: optional blank, then a markdown table.
        j = i + 1
        while j < n and lines[j].strip() == "":
            j += 1
        if j >= n or not _TABLE_ROW_RE.match(lines[j]):
            # No table follows; not the pattern we're after.
            out.append(line)
            i += 1
            continue
        # Found a table starting at j. Find the table's last row.
        k = j
        while k < n and _TABLE_ROW_RE.match(lines[k]):
            k += 1
        # Optional caption line directly after the table (after blank).
        capt_idx = k
        while capt_idx < n and lines[capt_idx].strip() == "":
            capt_idx += 1
        caption = ""
        post_idx = k
        if capt_idx < n:
            cap_m = _TABLE_CAPTION_RE.match(lines[capt_idx])
            if cap_m:
                caption = cap_m.group(1).strip()
                post_idx = capt_idx + 1
        # Build the directive. mystmd's :::{table} directive wants
        # `:name:`, not `:label:`, for the cross-ref id (mystmd 1.8.x
        # warns "option 'label' used instead of 'name'").
        label_name = m.group(1)
        directive_open = f":::{{table}} {caption}" if caption else ":::{table}"
        out.append(directive_open)
        out.append(f":name: {label_name}")
        out.append("")
        out.extend(lines[j:k])
        out.append("")
        out.append(":::")
        out.append("")
        n_wrapped += 1
        i = post_idx
    return "\n".join(out), n_wrapped


def dedent_indented_label_lines(text: str) -> int:
    """Dedent ``(label)=`` and ``:label:`` lines that have leading whitespace.

    Pandoc emits indented `(label)=` when a `\\label{...}` lives inside a
    numbered list item or otherwise indented context. mystmd 1.8.x
    does not register indented labels — `[](#label)` references then
    fail with "No target for internal reference '#label' was found".
    Dedenting moves the label to the document level where it picks up
    its target normally; the surrounding list/directive structure is
    unaffected because the label is itself a zero-width element.

    Returns the number of label lines that were dedented.
    """
    n_dedented = [0]

    def _dedent(m: re.Match) -> str:
        body = m.group(2)
        if m.group(1):
            n_dedented[0] += 1
        return body

    # Match labels with optional leading whitespace, then dedent.
    text_new = re.sub(
        r"^( +)((?:\([A-Za-z0-9_.\-]+\)=|:label:\s+[A-Za-z0-9_.\-]+))\s*$",
        _dedent,
        text,
        flags=re.MULTILINE,
    )
    return text_new, n_dedented[0]


def case_normalize_references(text: str) -> tuple[str, dict[str, str]]:
    """Rewrite `[](#X)` references to match the case of the actual anchor
    they target.

    mystmd lowercases anchor ids when it emits HTML (e.g. `(Calibration)=`
    becomes `id="calibration"`), but it does NOT lowercase href targets
    in the same source-rewriting pass — so `[](#calibration)` references
    written in lowercase fail to match `id="calibration"` which only
    exists if the source had `(calibration)=` exactly. By contrast, a
    href to `[](#Calibration)` would lowercase-match the id.

    This pass scans every label defined in the document, builds a
    case-insensitive map ``{lowercase_name: actual_case_name}``, and
    rewrites references whose target matches an existing anchor only
    case-insensitively to use the actual-case form.

    Run AFTER ``merge_adjacent_label_clusters`` so we operate on the
    already-canonicalised set of labels.
    """
    # Collect the ACTUAL labels defined in the markdown.
    actual_labels: set[str] = set()
    for m in _ANCHOR_LINE_RE.finditer(text):
        actual_labels.add(m.group(1))
    for m in _LABEL_DIRECTIVE_LINE_RE.finditer(text):
        actual_labels.add(m.group(1))
    # Use multiline mode for both (matches start-of-line anchors).
    actual_labels |= set(re.findall(
        r"^[ \t]*\(([A-Za-z0-9_.\-]+)\)=\s*$", text, flags=re.MULTILINE,
    ))
    actual_labels |= set(re.findall(
        r"^[ \t]*:label:\s+([A-Za-z0-9_.\-]+)\s*$", text, flags=re.MULTILINE,
    ))

    # Lowercase → first-seen actual-case mapping.
    lower_to_actual: dict[str, str] = {}
    for label in actual_labels:
        lower_to_actual.setdefault(label.lower(), label)

    case_aliases: dict[str, str] = {}

    def _resolve(m: re.Match) -> str:
        target = m.group(1)
        if target in actual_labels:
            return m.group(0)  # exact match, no rewrite needed
        actual = lower_to_actual.get(target.lower())
        if actual is None:
            return m.group(0)  # unknown target, leave alone
        case_aliases[target] = actual
        return f"](#{actual})"

    text = re.sub(r"\]\(#([A-Za-z0-9_.\-]+)\)", _resolve, text)
    return text, case_aliases
