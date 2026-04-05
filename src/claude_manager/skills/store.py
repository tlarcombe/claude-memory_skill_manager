"""Read skills from the Claude Code skills directory."""

import re
from pathlib import Path

from claude_manager.config import skills_dir
from claude_manager.skills.models import Skill

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)


def _parse_skill_meta(path: Path) -> dict[str, str]:
    try:
        text = path.read_text()
    except OSError:
        return {}
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    return dict(_FIELD_RE.findall(m.group(1)))


def list_skills() -> list[Skill]:
    base = skills_dir()
    if not base.exists():
        return []
    skills = []
    for md in sorted(base.rglob("*.md")):
        meta = _parse_skill_meta(md)
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
