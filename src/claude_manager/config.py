"""Resolved paths to well-known Claude Code directories."""

from pathlib import Path


def claude_dir() -> Path:
    return Path.home() / ".claude"


def memory_dir(project_path: Path | None = None) -> Path:
    if project_path:
        slug = str(project_path).replace("/", "-").lstrip("-")
        return claude_dir() / "projects" / slug / "memory"
    return claude_dir() / "projects"


def skills_dir() -> Path:
    return claude_dir() / "skills"


def agents_dir() -> Path:
    return claude_dir() / "agents"


def settings_path() -> Path:
    return claude_dir() / "settings.json"
