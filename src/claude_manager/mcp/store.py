"""Read MCP server configuration from global or project-local settings.json."""

from __future__ import annotations

import json
from pathlib import Path

from claude_manager.config import global_settings_path, project_settings_path
from claude_manager.mcp.models import McpServer


def _load_from_settings(path: Path, scope: str = "global") -> list[McpServer]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return []
    raw = data.get("mcpServers", {})
    return [
        McpServer(
            name=name,
            command=cfg.get("command", ""),
            args=cfg.get("args", []),
            env=cfg.get("env", {}),
            scope=scope,
        )
        for name, cfg in raw.items()
    ]


def list_global_servers() -> list[McpServer]:
    return _load_from_settings(global_settings_path(), scope="global")


def list_project_servers(project: Path) -> list[McpServer]:
    return _load_from_settings(project_settings_path(project), scope=str(project))


def list_servers(project: Path | None = None) -> list[McpServer]:
    """Global MCP servers. If project given, project-local servers only."""
    if project is not None:
        return list_project_servers(project)
    return list_global_servers()
