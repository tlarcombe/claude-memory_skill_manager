"""Tests for config path helpers."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from claude_manager.config import (
    list_known_projects,
    memory_store_dir,
    project_agents_dir,
    project_settings_path,
    project_skills_dir,
)


def test_project_skills_dir(tmp_path: Path) -> None:
    project = tmp_path / "myapp"
    assert project_skills_dir(project) == project / ".claude" / "skills"


def test_project_agents_dir(tmp_path: Path) -> None:
    project = tmp_path / "myapp"
    assert project_agents_dir(project) == project / ".claude" / "agents"


def test_project_settings_path(tmp_path: Path) -> None:
    project = tmp_path / "myapp"
    assert project_settings_path(project) == project / ".claude" / "settings.json"


def test_memory_store_dir_encodes_path() -> None:
    project = Path("/home/user/projects/my-app")
    result = memory_store_dir(project)
    # The slug should have non-alphanumeric chars replaced with hyphens
    assert "-home-user-projects-my-app" in str(result)


def test_list_known_projects_returns_sorted_dirs(tmp_path: Path) -> None:
    (tmp_path / "zebra").mkdir()
    (tmp_path / "alpha").mkdir()
    (tmp_path / "middle").mkdir()
    (tmp_path / "file.txt").write_text("not a dir")

    with patch("claude_manager.config.USER_PROJECTS_DIR", tmp_path):
        projects = list_known_projects()

    names = [p.name for p in projects]
    assert names == ["alpha", "middle", "zebra"]
    assert all(p.is_dir() for p in projects)


def test_list_known_projects_empty_when_no_dir(tmp_path: Path) -> None:
    missing = tmp_path / "nonexistent"
    with patch("claude_manager.config.USER_PROJECTS_DIR", missing):
        result = list_known_projects()
    assert result == []
