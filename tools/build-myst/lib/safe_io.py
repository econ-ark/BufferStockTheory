"""Idempotent read/write helpers with per-input sha256 caching.

Each phase writes its output atomically and stores a sidecar `.sha256` file
recording the hash of the *input* it processed. On the next run, if the input
hash matches, the phase can short-circuit and re-emit the cached output.

Usage:

    from lib.safe_io import read_text, write_text, input_changed, mark_processed

    src = read_text("_build/myst/01_flat.tex")
    out_path = "_build/myst/02_stripped.tex"
    if not input_changed(src, out_path):
        return  # cache hit
    result = transform(src)
    write_text(out_path, result)
    mark_processed(src, out_path)
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Union

PathLike = Union[str, os.PathLike]


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: PathLike) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: PathLike, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def sidecar_path(output_path: PathLike) -> Path:
    p = Path(output_path)
    return p.with_suffix(p.suffix + ".sha256")


def input_changed(input_text: str, output_path: PathLike) -> bool:
    """Return True if output is missing OR sidecar hash differs from input hash."""
    out = Path(output_path)
    side = sidecar_path(output_path)
    if not out.exists() or not side.exists():
        return True
    try:
        cached = side.read_text(encoding="utf-8").strip()
    except OSError:
        return True
    return cached != _hash(input_text)


def mark_processed(input_text: str, output_path: PathLike) -> None:
    """Record the input hash next to the output."""
    sidecar_path(output_path).write_text(_hash(input_text), encoding="utf-8")


def repo_root() -> Path:
    """Locate the BufferStockTheory repo root.

    Strategy: walk up from this file's location until a `.git` directory is
    found. Falls back to the cwd of the calling process.
    """
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".git").exists():
            return parent
    return Path.cwd()


def build_path(name: str) -> Path:
    """Resolve a filename inside `_build/myst/` relative to the repo root."""
    return repo_root() / "_build" / "myst" / name


def config_path(name: str) -> Path:
    """Resolve a filename inside `tools/build-myst/config/` relative to repo root."""
    return repo_root() / "tools" / "build-myst" / "config" / name
