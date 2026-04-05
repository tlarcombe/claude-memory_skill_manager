"""Tests for MCP store parsing."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from claude_manager.mcp.store import list_global_servers, list_project_servers


def test_list_global_servers_empty_when_no_settings(tmp_path: Path) -> None:
    with patch("claude_manager.mcp.store.global_settings_path", return_value=tmp_path / "missing.json"):
        result = list_global_servers()
    assert result == []


def test_list_global_servers_empty_when_no_mcp_key(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({}))
    with patch("claude_manager.mcp.store.global_settings_path", return_value=settings):
        result = list_global_servers()
    assert result == []


def test_list_global_servers_parses_entries(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps({
            "mcpServers": {
                "my-server": {
                    "command": "npx",
                    "args": ["-y", "my-mcp-server"],
                    "env": {"API_KEY": "secret"},
                }
            }
        })
    )
    with patch("claude_manager.mcp.store.global_settings_path", return_value=settings):
        result = list_global_servers()
    assert len(result) == 1
    assert result[0].name == "my-server"
    assert result[0].command == "npx"
    assert result[0].args == ["-y", "my-mcp-server"]
    assert result[0].env == {"API_KEY": "secret"}


def test_list_project_servers_reads_project_settings(tmp_path: Path) -> None:
    project = tmp_path / "myproject"
    project.mkdir()
    claude_dir = project / ".claude"
    claude_dir.mkdir()
    settings = claude_dir / "settings.json"
    settings.write_text(json.dumps({
        "mcpServers": {
            "local-server": {"command": "python", "args": ["-m", "local_mcp"]}
        }
    }))

    result = list_project_servers(project)
    assert len(result) == 1
    assert result[0].name == "local-server"
    assert result[0].scope == str(project)
