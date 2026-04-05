"""Read agents from the Claude Code agents directory."""

import re
from pathlib import Path

from claude_manager.agents.models import Agent
from claude_manager.config import agents_dir

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)
_LIST_FIELD_RE = re.compile(r"^(\w+):\s*\n((?:\s+-\s+.+\n?)+)", re.MULTILINE)
_LIST_ITEM_RE = re.compile(r"^\s+-\s+(.+)$", re.MULTILINE)


def _parse_agent_meta(path: Path) -> dict[str, str | list[str]]:
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


def list_agents() -> list[Agent]:
    base = agents_dir()
    if not base.exists():
        return []
    result = []
    for md in sorted(base.glob("*.md")):
        meta = _parse_agent_meta(md)
        tools_raw = meta.get("tools", [])
        tools = tools_raw if isinstance(tools_raw, list) else [tools_raw]
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
