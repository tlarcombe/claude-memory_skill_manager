"""Tests for MCP store parsing."""

import json
from pathlib import Path
from unittest.mock import patch

from claude_manager.mcp.store import list_servers


def test_list_servers_empty_when_no_settings(tmp_path: Path) -> None:
    with patch("claude_manager.mcp.store.settings_path", return_value=tmp_path / "missing.json"):
        result = list_servers()
    assert result == []


def test_list_servers_empty_when_no_mcp_key(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({}))
    with patch("claude_manager.mcp.store.settings_path", return_value=settings):
        result = list_servers()
    assert result == []


def test_list_servers_parses_entries(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "my-server": {
                        "command": "npx",
                        "args": ["-y", "my-mcp-server"],
                        "env": {"API_KEY": "secret"},
                    }
                }
            }
        )
    )
    with patch("claude_manager.mcp.store.settings_path", return_value=settings):
        result = list_servers()
    assert len(result) == 1
    assert result[0].name == "my-server"
    assert result[0].command == "npx"
    assert result[0].args == ["-y", "my-mcp-server"]
    assert result[0].env == {"API_KEY": "secret"}
