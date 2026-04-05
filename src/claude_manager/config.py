"""Resolved paths to Claude Code directories — global and project-scoped."""

from __future__ import annotations

import re
from pathlib import Path

USER_PROJECTS_DIR = Path.home() / "projects"

# Registry — companion repo used for browsing and installing addons
REGISTRY_REPO_URL = "https://github.com/tlarcombe/claude-addons"
REGISTRY_JSON_URL = "https://raw.githubusercontent.com/tlarcombe/claude-addons/main/REGISTRY.json"
REGISTRY_LOCAL_PATH = Path.home() / "projects" / "claude-addons"


# ── Core paths ────────────────────────────────────────────────────────────────

def claude_dir() -> Path:
    return Path.home() / ".claude"


def _encode_path(path: Path) -> str:
    """Encode a filesystem path to the Claude Code project slug format."""
    return re.sub(r"[^a-zA-Z0-9]", "-", str(path))


# ── Global tool paths ─────────────────────────────────────────────────────────

def global_skills_dir() -> Path:
    return claude_dir() / "skills"


def global_agents_dir() -> Path:
    return claude_dir() / "agents"


def global_settings_path() -> Path:
    return claude_dir() / "settings.json"


# ── Project-local tool paths ──────────────────────────────────────────────────

def project_claude_dir(project: Path) -> Path:
    return project / ".claude"


def project_skills_dir(project: Path) -> Path:
    return project_claude_dir(project) / "skills"


def project_agents_dir(project: Path) -> Path:
    return project_claude_dir(project) / "agents"


def project_settings_path(project: Path) -> Path:
    return project_claude_dir(project) / "settings.json"


# ── Memory (always project-scoped via Claude Code's internal store) ───────────

def memory_store_dir(project: Path) -> Path:
    """~/.claude/projects/<slug>/memory/ — Claude Code's memory for a project."""
    return claude_dir() / "projects" / _encode_path(project) / "memory"


def all_memory_project_slugs() -> list[str]:
    base = claude_dir() / "projects"
    if not base.exists():
        return []
    return sorted(p.name for p in base.iterdir() if (p / "memory").is_dir())


# ── Project discovery ─────────────────────────────────────────────────────────

def list_known_projects() -> list[Path]:
    """Return all project directories under ~/projects, sorted by name."""
    if not USER_PROJECTS_DIR.exists():
        return []
    return sorted(
        [p for p in USER_PROJECTS_DIR.iterdir() if p.is_dir()],
        key=lambda p: p.name.lower(),
    )
