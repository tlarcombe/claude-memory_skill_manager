"""Tests for agents store."""

from __future__ import annotations

from pathlib import Path

from claude_manager.agents.store import list_project_agents


def test_list_project_agents_empty_when_no_dir(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    result = list_project_agents(project)
    assert result == []


def test_list_project_agents_parses_metadata(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    (project / ".claude" / "agents").mkdir(parents=True)
    agent_file = project / ".claude" / "agents" / "my-agent.md"
    agent_file.write_text(
        "---\n"
        "name: My Agent\n"
        "description: Does stuff\n"
        "model: claude-sonnet-4-6\n"
        "---\n"
        "Agent instructions here.\n"
    )

    result = list_project_agents(project)
    assert len(result) == 1
    assert result[0].name == "My Agent"
    assert result[0].description == "Does stuff"
    assert result[0].model == "claude-sonnet-4-6"


def test_list_project_agents_falls_back_to_stem(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    (project / ".claude" / "agents").mkdir(parents=True)
    (project / ".claude" / "agents" / "bare.md").write_text("No frontmatter.\n")

    result = list_project_agents(project)
    assert len(result) == 1
    assert result[0].name == "bare"
