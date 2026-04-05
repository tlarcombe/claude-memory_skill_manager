"""fzf subprocess wrapper — matches the claude++/claude-project-chooser aesthetic."""

from __future__ import annotations

import subprocess
import sys
from typing import NamedTuple

# Catppuccin Mocha — identical to claude++ / claude-project-chooser
FZF_COLORS = (
    "bg+:#313244,hl:#89b4fa,hl+:#89b4fa,"
    "pointer:#f38ba8,prompt:#cba6f7,"
    "marker:#a6e3a1,header:#89dceb,border:#585b70"
)

# ANSI colour helpers
BOLD_CYAN = "\033[1;36m"
BOLD_GREEN = "\033[1;32m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


class FzfResult(NamedTuple):
    key: str        # the data key (left of \t)
    pressed: str    # the key that triggered selection ("" = Enter)


_NO_RESULT = FzfResult("", "")


def fzf(
    items: list[tuple[str, str]],
    header: str,
    prompt: str = "  ",
    expect: list[str] | None = None,
    preview_cmd: str | None = None,
    preview_window: str = "right:45%:wrap:border-left:hidden",
    bind_toggle_preview: bool = True,
) -> FzfResult:
    """Run fzf on items (list of (key, display_line) tuples).

    Returns FzfResult(key, pressed_key), or _NO_RESULT on Esc/Ctrl-C.
    """
    if not items:
        return _NO_RESULT

    input_text = "\n".join(f"{k}\t{d}" for k, d in items)

    args = [
        "fzf",
        "--ansi",
        "--delimiter=\t",
        "--with-nth=2",
        "--header", header,
        "--header-first",
        "--no-sort",
        "--reverse",
        "--height=100%",
        "--border=rounded",
        "--prompt", prompt,
        "--pointer=▶",
        "--marker=✓",
        f"--color={FZF_COLORS}",
    ]

    if expect:
        args += ["--expect", ",".join(expect)]

    if preview_cmd:
        args += ["--preview", preview_cmd, "--preview-window", preview_window]
        if bind_toggle_preview:
            args += ["--bind", "ctrl-/:toggle-preview"]

    try:
        result = subprocess.run(
            args,
            input=input_text,
            text=True,
            capture_output=False,
            stdout=subprocess.PIPE,
        )
    except FileNotFoundError:
        print("Error: fzf not found. Install with: sudo pacman -S fzf", file=sys.stderr)
        sys.exit(1)

    if result.returncode not in (0, 1):
        return _NO_RESULT  # Esc or Ctrl-C

    lines = result.stdout.strip().splitlines()
    if not lines:
        return _NO_RESULT

    if expect:
        pressed = lines[0] if lines else ""
        raw = lines[1] if len(lines) > 1 else ""
    else:
        pressed = ""
        raw = lines[0] if lines else ""

    if not raw:
        return _NO_RESULT

    key = raw.split("\t")[0]
    return FzfResult(key, pressed)


def set_title(title: str) -> None:
    print(f"\033]2;{title}\007", end="", flush=True)
