"""Data models for Claude Code agents."""

from pathlib import Path

from pydantic import BaseModel


class Agent(BaseModel):
    name: str
    description: str
    path: Path
    model: str | None = None
    tools: list[str] = []
