"""Helpers for emitting MyST Markdown directives, anchors, and roles."""

from __future__ import annotations

from typing import Iterable, Optional


def anchor(label: str) -> str:
    """`(label)=` MyST target anchor on its own line."""
    return f"({label})="


def directive(name: str, *, arg: str = "", options: Optional[dict] = None,
              body: str = "") -> str:
    """Emit a MyST `:::{name} arg ... :::` block.

    Triple-colon form is used (matches `mystmd` defaults). Options are emitted
    as `:key: value` lines. Body is included verbatim and indented zero levels.
    """
    lines = []
    head = f":::{{{name}}}"
    if arg:
        head += f" {arg}"
    lines.append(head)
    if options:
        for k, v in options.items():
            if v is None or v == "":
                continue
            lines.append(f":{k}: {v}")
    if options:
        lines.append("")  # blank line between options and body
    if body:
        lines.append(body.rstrip())
    lines.append(":::")
    return "\n".join(lines)


def cite_role(role: str, keys: Iterable[str]) -> str:
    """Emit a MyST citation role like `{cite:p}`​\\``key1, key2``​\\`.

    Note: this plan resolves citations inline rather than as roles, so this
    helper is provided for completeness / future use.
    """
    keylist = ", ".join(k.strip() for k in keys)
    return "{" + role + "}`" + keylist + "`"


def eq_ref(label: str) -> str:
    return "{eq}`" + label + "`"


def num_ref(label: str) -> str:
    return "{numref}`" + label + "`"


def md_link(text: str, target: str) -> str:
    """Markdown link `[text](#target)`."""
    return f"[{text}](#{target})"


def proof_directive(kind: str, *, name: str = "", label: str = "",
                    body: str = "") -> str:
    """Emit a sphinx-proof directive: `:::{prf:theorem} Optional Name ... :::`.

    `kind` is one of theorem|proposition|corollary|lemma|definition|remark|
    example|property|assumption|proof.
    """
    options = {}
    if label:
        options["label"] = label
    return directive(f"prf:{kind}", arg=name, options=options, body=body)


def figure_directive(image: str, *, label: str = "", caption: str = "",
                     width: str = "", alt: str = "") -> str:
    options = {}
    if label:
        options["label"] = label
    if width:
        options["width"] = width
    if alt:
        options["alt"] = alt
    body = caption or ""
    return directive("figure", arg=image, options=options, body=body)
