"""Read agents from global or project-local agent directories."""

from __future__ import annotations

import re
from pathlib import Path

from claude_manager.agents.models import Agent
from claude_manager.config import global_agents_dir, project_agents_dir

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)
_LIST_FIELD_RE = re.compile(r"^(\w+):\s*\n((?:\s+-\s+.+\n?)+)", re.MULTILINE)
_LIST_ITEM_RE = re.compile(r"^\s+-\s+(.+)$", re.MULTILINE)


def _parse_meta(path: Path) -> dict[str, str | list[str]]:
    try:
        text = path.read_text()
    except OSError:
        return {}
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    meta: dict[str, str | list[str]] = dict(_FIELD_RE.findall(block))
    for lm in _LIST_FIELD_RE.finditer(block):
        meta[lm.group(1)] = _LIST_ITEM_RE.findall(lm.group(2))
    return meta


def _load_from_dir(directory: Path) -> list[Agent]:
    if not directory.exists():
        return []
    result = []
    for md in sorted(directory.glob("*.md")):
        meta = _parse_meta(md)
        tools_raw = meta.get("tools", [])
        tools = tools_raw if isinstance(tools_raw, list) else [str(tools_raw)]
        result.append(
            Agent(
                name=str(meta.get("name", md.stem)),
                description=str(meta.get("description", "")),
                path=md,
                model=str(meta["model"]) if "model" in meta else None,
                tools=tools,
            )
        )
    return result


def list_global_agents() -> list[Agent]:
    return _load_from_dir(global_agents_dir())


def list_project_agents(project: Path) -> list[Agent]:
    return _load_from_dir(project_agents_dir(project))


def list_agents(project: Path | None = None) -> list[Agent]:
    """Global agents. If project given, project-local agents only."""
    if project is not None:
        return list_project_agents(project)
    return list_global_agents()
