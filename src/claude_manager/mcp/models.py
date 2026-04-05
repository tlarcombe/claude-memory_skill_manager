"""Data models for MCP server entries."""

from pydantic import BaseModel


class McpServer(BaseModel):
    name: str
    command: str
    args: list[str] = []
    env: dict[str, str] = {}
    scope: str = "global"
