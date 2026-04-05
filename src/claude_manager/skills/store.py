"""Read skills from global or project-local skills directories."""

from __future__ import annotations

import re
from pathlib import Path

from claude_manager.config import global_skills_dir, project_skills_dir
from claude_manager.skills.models import Skill

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)


def _parse_meta(path: Path) -> dict[str, str]:
    try:
        text = path.read_text()
    except OSError:
        return {}
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    return dict(_FIELD_RE.findall(m.group(1)))


def _load_from_dir(directory: Path) -> list[Skill]:
    if not directory.exists():
        return []
    skills = []
    for md in sorted(directory.rglob("*.md")):
        meta = _parse_meta(md)
        name = meta.get("name") or md.stem
        skills.append(
            Skill(
                name=name,
                description=meta.get("description", ""),
                path=md,
                trigger=meta.get("trigger"),
            )
        )
    return skills


def list_global_skills() -> list[Skill]:
    return _load_from_dir(global_skills_dir())


def list_project_skills(project: Path) -> list[Skill]:
    return _load_from_dir(project_skills_dir(project))


def list_skills(project: Path | None = None) -> list[Skill]:
    """Global skills. If project given, project-local skills only."""
    if project is not None:
        return list_project_skills(project)
    return list_global_skills()
