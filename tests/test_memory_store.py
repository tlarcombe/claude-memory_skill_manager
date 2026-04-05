"""Tests for memory store parsing."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from claude_manager.memory.models import MemoryType
from claude_manager.memory.store import list_entries, load_entry


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


def test_list_entries_skips_memory_index(tmp_path: Path) -> None:
    project = tmp_path / "myproject"
    project.mkdir()

    # Patch memory_store_dir to point to our tmp directory
    mem_dir = tmp_path / "mem"
    mem_dir.mkdir()

    # Add MEMORY.md (should be skipped)
    (mem_dir / "MEMORY.md").write_text("# Index\n")

    # Add a valid entry
    (mem_dir / "user_role.md").write_text(
        "---\nname: Role\ndescription: Test\ntype: user\n---\nBody.\n"
    )

    with patch("claude_manager.memory.store.memory_store_dir", return_value=mem_dir):
        entries = list_entries(project)

    assert len(entries) == 1
    assert entries[0].name == "Role"
