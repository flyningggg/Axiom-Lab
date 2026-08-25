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


def write_missing(path: Path, content: str, encoding: str = "utf-8") -> bool:
    """Create one control file without overwriting user work."""
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    return True


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
    innovation_matrix = (
        "创新ID,核心问题,基线局限,创新类型,最近方法,核心差异,作用机制,最小实现,"
        "比较对象,消融项,主要指标,成功标准,失败条件,计算预算,状态,结果路径,结论\n"
    )
    innovation_report = """# 创新性审查报告

> 在稳定基线与创新实验完成后更新。只把有可核查实验和消融证据的项目写成论文创新点。

## 总体结论

待执行。

## 逐项审查

按创新 ID 记录最近方法、核心差异、实验路径、成功标准、实际结果、结论、适用边界和论文允许表述。
"""
    paper_blueprint = """# 论文论证蓝图

> 本文件把内部求解过程映射为正式论文的数学论证。建模与正式结果确定后补全，写作前不得保留关键空项。

## 全文统一主线

- 研究对象：
- 四问递进关系：
- 统一建模思想：
- 结论边界：

## 问题一

- 题目任务与核心难点：
- 建模动机：
- 决策或状态变量：
- 参数、集合与单位：
- 目标函数或学习目标：
- 约束、边界条件或数据生成假设：
- 模型性质与适用边界：
- 求解原理：
- 算法输入、输出、关键步骤、可行性处理与停止条件：
- 关键定量结果：
- 数值—现象—原因—意义：
- 验证方式与证据路径：
- 论文允许表述：

> 根据问题数量复制“问题一”部分；不适用的字段说明替代结构，不机械留空。
"""
    controls = {
        "创新实验矩阵.csv": write_missing(
            workspace / "求解" / "创新实验矩阵.csv",
            innovation_matrix,
            encoding="utf-8-sig",
        ),
        "创新性审查报告.md": write_missing(
            workspace / "求解" / "创新性审查报告.md",
            innovation_report,
        ),
        "论文论证蓝图.md": write_missing(
            workspace / "求解" / "论文论证蓝图.md",
            paper_blueprint,
        ),
    }
    print(f"Workspace: {workspace}")
    print(f"Template files copied: {copied}; existing files skipped: {skipped}")
    created = [name for name, was_created in controls.items() if was_created]
    preserved = [name for name, was_created in controls.items() if not was_created]
    print(f"Control files created: {created or 'none'}")
    print(f"Existing control files preserved: {preserved or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
