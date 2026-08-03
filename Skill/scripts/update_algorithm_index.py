#!/usr/bin/env python3
"""Generate 算法索引.md from validated algorithm metadata.json files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "name",
    "category",
    "problem_types",
    "entrypoint",
    "dependencies",
    "source_urls",
    "license",
    "validated_metrics",
    "validated_at",
    "promoted_from",
}

REQUIRED_PACKAGE_FILES = ("最小示例.py", "测试.py")
NONEMPTY_FIELDS = REQUIRED_FIELDS - {"dependencies"}


def escape_cell(value: object) -> str:
    if isinstance(value, list):
        text = "、".join(str(item) for item in value)
    elif isinstance(value, dict):
        text = "；".join(f"{key}={val}" for key, val in value.items())
    else:
        text = str(value or "")
    return text.replace("|", "\\|").replace("\n", " ")


def load_entries(root: Path) -> list[tuple[Path, dict[str, object]]]:
    entries: list[tuple[Path, dict[str, object]]] = []
    errors: list[str] = []
    for metadata_path in sorted(root.rglob("metadata.json")):
        try:
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{metadata_path}: {exc}")
            continue
        missing = sorted(REQUIRED_FIELDS - data.keys())
        if missing:
            errors.append(f"{metadata_path}: missing {', '.join(missing)}")
            continue
        empty = sorted(field for field in NONEMPTY_FIELDS if data[field] in (None, "", [], {}))
        if empty:
            errors.append(f"{metadata_path}: empty {', '.join(empty)}")
            continue
        entrypoint = metadata_path.parent / str(data["entrypoint"])
        if not entrypoint.is_file():
            errors.append(f"{metadata_path}: entrypoint not found: {entrypoint.name}")
            continue
        missing_files = [name for name in REQUIRED_PACKAGE_FILES if not (metadata_path.parent / name).is_file()]
        if missing_files:
            errors.append(f"{metadata_path}: package files not found: {', '.join(missing_files)}")
            continue
        entries.append((metadata_path, data))
    if errors:
        raise SystemExit("Invalid algorithm metadata:\n" + "\n".join(errors))
    return entries


def render_index(root: Path, entries: list[tuple[Path, dict[str, object]]]) -> str:
    lines = [
        "# 算法索引",
        "",
        "> 此文件由 `update_algorithm_index.py` 根据各算法包的 `metadata.json` 生成。",
        "",
        "| 算法 | 分类 | 问题类型 | 入口 | 验证指标 | 验证日期 | 来源与许可证 |",
        "|---|---|---|---|---|---|---|",
    ]
    for metadata_path, data in sorted(
        entries, key=lambda item: (str(item[1]["category"]), str(item[1]["name"]))
    ):
        package = metadata_path.parent.relative_to(root).as_posix()
        source_license = (
            f"{escape_cell(data.get('source_urls', []))}；{escape_cell(data.get('license', ''))}"
        )
        lines.append(
            "| {name} | {category} | {types} | `{package}/{entrypoint}` | "
            "{metrics} | {date} | {source_license} |".format(
                name=escape_cell(data["name"]),
                category=escape_cell(data["category"]),
                types=escape_cell(data["problem_types"]),
                package=package,
                entrypoint=escape_cell(data["entrypoint"]),
                metrics=escape_cell(data.get("validated_metrics", {})),
                date=escape_cell(data["validated_at"]),
                source_license=source_license,
            )
        )
    if not entries:
        lines.append("| 暂无已验证条目 | — | — | — | — | — | — |")
    lines.extend(["", f"共 {len(entries)} 个已验证算法条目。", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild 算法索引.md from metadata.json files")
    parser.add_argument("algorithm_library", type=Path, help="算法库根目录")
    args = parser.parse_args()

    root = args.algorithm_library.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Algorithm library not found: {root}")
    entries = load_entries(root)
    output = root / "算法索引.md"
    output.write_text(render_index(root, entries), encoding="utf-8")
    print(f"Generated {output} with {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
