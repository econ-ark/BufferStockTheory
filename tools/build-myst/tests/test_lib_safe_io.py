"""Unit tests for `lib.safe_io`."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.safe_io import (  # noqa: E402
    build_path,
    config_path,
    input_changed,
    mark_processed,
    read_text,
    repo_root,
    sidecar_path,
    write_text,
)


def test_write_then_read_roundtrip(tmp_path: Path) -> None:
    target = tmp_path / "subdir" / "out.txt"
    write_text(target, "hello")
    assert read_text(target) == "hello"


def test_write_atomic_replaces(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"
    write_text(target, "v1")
    write_text(target, "v2")
    assert read_text(target) == "v2"


def test_input_changed_when_no_sidecar(tmp_path: Path) -> None:
    target = tmp_path / "out.md"
    write_text(target, "anything")
    assert input_changed("any input", target) is True


def test_input_changed_after_mark(tmp_path: Path) -> None:
    target = tmp_path / "out.md"
    src = "the source text"
    write_text(target, "transformed")
    mark_processed(src, target)
    assert input_changed(src, target) is False
    assert input_changed("different source", target) is True


def test_sidecar_path_naming(tmp_path: Path) -> None:
    target = tmp_path / "data.json"
    side = sidecar_path(target)
    assert side.name == "data.json.sha256"


def test_repo_root_resolves() -> None:
    root = repo_root()
    assert (root / ".git").exists()


def test_build_path_inside_repo() -> None:
    p = build_path("99_test.txt")
    assert "_build/myst/" in str(p)


def test_config_path_inside_repo() -> None:
    p = config_path("pipeline.yml")
    assert "tools/build-myst/config" in str(p)
