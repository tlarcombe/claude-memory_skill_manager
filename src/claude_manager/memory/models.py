"""Data models for Claude Code memory entries."""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel


class MemoryType(str, Enum):
    user = "user"
    feedback = "feedback"
    project = "project"
    reference = "reference"


class MemoryEntry(BaseModel):
    name: str
    description: str
    type: MemoryType
    body: str
    path: Path
    project: str | None = None
