"""Tests for memory store parsing."""

from pathlib import Path

import pytest

from claude_manager.memory.models import MemoryType
from claude_manager.memory.store import load_entry


@pytest.fixture
def tmp_memory_file(tmp_path: Path) -> Path:
    f = tmp_path / "test_entry.md"
    f.write_text(
        "---\n"
        "name: Test Entry\n"
        "description: A test memory\n"
        "type: feedback\n"
        "---\n\n"
        "Do the thing.\n\n"
        "**Why:** Because tests.\n"
    )
    return f


def test_load_entry_parses_metadata(tmp_memory_file: Path) -> None:
    entry = load_entry(tmp_memory_file)
    assert entry is not None
    assert entry.name == "Test Entry"
    assert entry.description == "A test memory"
    assert entry.type == MemoryType.feedback


def test_load_entry_parses_body(tmp_memory_file: Path) -> None:
    entry = load_entry(tmp_memory_file)
    assert entry is not None
    assert "Do the thing." in entry.body


def test_load_entry_returns_none_for_missing_file(tmp_path: Path) -> None:
    result = load_entry(tmp_path / "nonexistent.md")
    assert result is None


def test_load_entry_returns_none_for_missing_frontmatter(tmp_path: Path) -> None:
    f = tmp_path / "bad.md"
    f.write_text("Just plain text, no frontmatter.\n")
    assert load_entry(f) is None
