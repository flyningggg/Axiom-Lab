#!/usr/bin/env python3
"""Initialize a mathematical-modeling competition workspace safely."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_missing(source: Path, destination: Path, force: bool) -> tuple[int, int]:
    copied = 0
    skipped = 0
    for item in source.rglob("*"):
        relative = item.relative_to(source)
        target = destination / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped += 1
            continue
        shutil.copy2(item, target)
        copied += 1
    return copied, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create 题目、数据、求解、论文 directories and copy the bundled paper template."
    )
    parser.add_argument("workspace", type=Path, help="Target competition workspace")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files (never deletes unrelated files)",
    )
    args = parser.parse_args()

    workspace = args.workspace.expanduser().resolve()
    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "论文模板"
    if not template_dir.is_dir():
        raise SystemExit(f"Bundled template not found: {template_dir}")

    for name in ("题目", "数据", "求解", "论文"):
        (workspace / name).mkdir(parents=True, exist_ok=True)

    copied, skipped = copy_missing(template_dir, workspace / "论文", args.force)
    print(f"Workspace: {workspace}")
    print(f"Template files copied: {copied}; existing files skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
