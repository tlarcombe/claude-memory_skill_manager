"""Tests for skills store."""

from __future__ import annotations

from pathlib import Path

from claude_manager.skills.store import list_project_skills


def test_list_project_skills_empty_when_no_dir(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    result = list_project_skills(project)
    assert result == []


def test_list_project_skills_finds_skill_files(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    (project / ".claude" / "skills").mkdir(parents=True)
    skill_file = project / ".claude" / "skills" / "my-skill.md"
    skill_file.write_text(
        "---\nname: My Skill\ndescription: Does a thing\n---\nBody here.\n"
    )

    result = list_project_skills(project)
    assert len(result) == 1
    assert result[0].name == "My Skill"
    assert result[0].description == "Does a thing"
    assert result[0].path == skill_file


def test_list_project_skills_falls_back_to_stem_name(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    (project / ".claude" / "skills").mkdir(parents=True)
    skill_file = project / ".claude" / "skills" / "unnamed.md"
    skill_file.write_text("No frontmatter here.\n")

    result = list_project_skills(project)
    assert len(result) == 1
    assert result[0].name == "unnamed"
