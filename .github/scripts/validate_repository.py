#!/usr/bin/env python3
"""Validate Axiom Lab's publishable repository structure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / ".agents" / "skills" / "solve-math-modeling-competition"
MIRROR = ROOT / "Skill"
SYNC_PATHS = ("SKILL.md", "agents", "references", "scripts", "assets")
REQUIRED_ROOT = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "requirements.txt",
    ".gitignore",
    ".gitattributes",
)
MAX_GITHUB_FILE_SIZE = 100 * 1024 * 1024


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def files_under(root: Path) -> dict[str, Path]:
    if root.is_file():
        return {root.name: root}
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def validate_skill() -> None:
    skill_file = CANONICAL / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise AssertionError("SKILL.md frontmatter is malformed")
    metadata = yaml.safe_load(parts[1])
    if set(metadata) != {"name", "description"}:
        raise AssertionError("SKILL.md frontmatter must contain only name and description")
    if metadata["name"] != "solve-math-modeling-competition":
        raise AssertionError("Unexpected skill name")

    openai_yaml = yaml.safe_load((CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    prompt = openai_yaml["interface"]["default_prompt"]
    if "$solve-math-modeling-competition" not in prompt:
        raise AssertionError("Default prompt does not invoke the skill")

    for script in (CANONICAL / "scripts").glob("*.py"):
        compile(script.read_text(encoding="utf-8"), str(script), "exec")


def validate_mirror() -> None:
    for relative in SYNC_PATHS:
        canonical_files = files_under(CANONICAL / relative)
        mirror_files = files_under(MIRROR / relative)
        if canonical_files.keys() != mirror_files.keys():
            raise AssertionError(f"Skill mirror file set differs under {relative}")
        for name in canonical_files:
            if sha256(canonical_files[name]) != sha256(mirror_files[name]):
                raise AssertionError(f"Skill mirror differs: {relative}/{name}")


def validate_algorithm_metadata() -> None:
    required = {
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
    for metadata_path in (ROOT / "算法").rglob("metadata.json"):
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        missing = required - data.keys()
        if missing:
            raise AssertionError(f"{metadata_path}: missing {sorted(missing)}")
        for name in (str(data["entrypoint"]), "最小示例.py", "测试.py"):
            if not (metadata_path.parent / name).is_file():
                raise AssertionError(f"{metadata_path}: missing package file {name}")


def validate_publishability() -> None:
    missing = [name for name in REQUIRED_ROOT if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"Missing root files: {missing}")
    oversized = [path for path in ROOT.rglob("*") if path.is_file() and path.stat().st_size >= MAX_GITHUB_FILE_SIZE]
    if oversized:
        raise AssertionError(f"Files exceed GitHub's 100 MiB limit: {oversized}")


def main() -> int:
    validate_skill()
    validate_mirror()
    validate_algorithm_metadata()
    validate_publishability()
    print("Axiom Lab repository checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
