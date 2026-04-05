"""Data models for Claude Code skills."""

from pathlib import Path

from pydantic import BaseModel


class Skill(BaseModel):
    name: str
    description: str
    path: Path
    trigger: str | None = None
