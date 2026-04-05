"""Read memory entries from Claude Code's project memory store."""

from __future__ import annotations

import re
from pathlib import Path

from claude_manager.config import memory_store_dir
from claude_manager.memory.models import MemoryEntry, MemoryType

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)", re.DOTALL)
_FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fields = dict(_FIELD_RE.findall(m.group(1)))
    return fields, m.group(2).strip()


def load_entry(path: Path, project: str | None = None) -> MemoryEntry | None:
    try:
        text = path.read_text()
    except OSError:
        return None
    meta, body = _parse_frontmatter(text)
    if not meta.get("name") or not meta.get("type"):
        return None
    try:
        mem_type = MemoryType(meta["type"])
    except ValueError:
        return None
    return MemoryEntry(
        name=meta["name"],
        description=meta.get("description", ""),
        type=mem_type,
        body=body,
        path=path,
        project=project,
    )


def list_entries(project: Path) -> list[MemoryEntry]:
    """List all memory entries for a specific project."""
    base = memory_store_dir(project)
    if not base.exists():
        return []
    entries = []
    for md in sorted(base.glob("*.md")):
        if md.name == "MEMORY.md":
            continue
        entry = load_entry(md, project=str(project))
        if entry:
            entries.append(entry)
    return entries
