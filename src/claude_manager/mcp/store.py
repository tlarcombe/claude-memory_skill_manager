"""Read MCP server configuration from Claude Code settings.json."""

import json

from claude_manager.config import settings_path
from claude_manager.mcp.models import McpServer


def list_servers() -> list[McpServer]:
    path = settings_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return []
    raw = data.get("mcpServers", {})
    servers = []
    for name, cfg in raw.items():
        servers.append(
            McpServer(
                name=name,
                command=cfg.get("command", ""),
                args=cfg.get("args", []),
                env=cfg.get("env", {}),
            )
        )
    return servers
