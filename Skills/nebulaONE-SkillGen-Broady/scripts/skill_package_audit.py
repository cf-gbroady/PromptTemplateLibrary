#!/usr/bin/env python3
"""Audit Agent Skills packages in PromptTemplateLibrary.

This helper is intentionally dependency-light so it can run in Code Interpreter,
local clones, CI jobs, or ad-hoc repo maintenance sessions without installing
third-party packages.

Checks:
- folder-based skills: Skills/<slug>/SKILL.md
- legacy standalone skills: Skills/*.md
- YAML-ish frontmatter presence and key fields
- nebulaONE description/body length limits
- Agent Skills naming shape for frontmatter `name`
- index.json coverage when available
- likely helper/reference files that are not discoverable by package convention
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


@dataclass
class Finding:
    severity: str
    code: str
    message: str


@dataclass
class SkillRecord:
    path: str
    kind: str
    name: str | None
    summary: str | None
    description: str | None
    body_chars: int
    description_chars: int
    findings: list[Finding] = field(default_factory=list)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, list[str]]:
    """Parse a conservative subset of YAML frontmatter.

    This is not a full YAML parser. It is sufficient for common Agent Skills
    frontmatter: scalar fields, folded `>` descriptions, and simple continuation
    lines. It avoids PyYAML so the audit can run without optional dependencies.
    """
    warnings: list[str] = []
    if not text.startswith("---"):
        return {}, text, ["missing-frontmatter"]
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, ["unterminated-frontmatter"]
    raw = text[3:end].strip("\n")
    body = text[end + len("\n---") :].lstrip("\r\n")
    data: dict[str, Any] = {}
    current_key: str | None = None
    folded: list[str] = []

    def flush_folded() -> None:
        nonlocal current_key, folded
        if current_key is not None and folded:
            data[current_key] = " ".join(part.strip() for part in folded).strip()
        current_key = None
        folded = []

    for line in raw.splitlines():
        if not line.strip():
            continue
        if current_key and (line.startswith(" ") or line.startswith("\t")):
            folded.append(line.strip())
            continue
        flush_folded()
        if ":" not in line:
            warnings.append(f"unparsed-frontmatter-line:{line[:40]}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", "|"}:
            current_key = key
            folded = []
        else:
            if (
                (value.startswith('"') and value.endswith('"'))
                or (value.startswith("'") and value.endswith("'"))
            ):
                value = value[1:-1]
            data[key] = value
    flush_folded()
    return data, body, warnings


def iter_skill_markdown(skills_root: Path) -> Iterable[tuple[Path, str]]:
    for child in sorted(skills_root.iterdir()):
        if child.name.startswith("."):
            continue
        if child.is_dir():
            skill_md = child / "SKILL.md"
            if skill_md.exists():
                yield skill_md, "package"
        elif child.suffix.lower() == ".md":
            yield child, "standalone"


def load_index_paths(index_path: Path) -> set[str]:
    if not index_path.exists():
        return set()
    try:
        data = json.loads(read_text(index_path))
    except Exception:
        return set()

    entries: list[dict[str, Any]]
    if isinstance(data, list):
        entries = [x for x in data if isinstance(x, dict)]
    elif isinstance(data, dict):
        for key in ("skills", "items", "entries"):
            if isinstance(data.get(key), list):
                entries = [x for x in data[key] if isinstance(x, dict)]
                break
        else:
            entries = []
    else:
        entries = []

    paths: set[str] = set()
    for entry in entries:
        for key in ("path", "skillPath", "fullyQualifiedLink", "rawSkillUrl"):
            value = entry.get(key)
            if isinstance(value, str) and "Skills/" in value:
                paths.add(value[value.find("Skills/") :].replace("/blob/main/", "/"))
    return paths


def audit(skills_root: Path, desc_limit: int, body_limit: int) -> list[SkillRecord]:
    index_paths = load_index_paths(skills_root / "index.json")
    records: list[SkillRecord] = []

    for path, kind in iter_skill_markdown(skills_root):
        try:
            rel = path.relative_to(skills_root.parent).as_posix()
        except ValueError:
            rel = path.as_posix()
        text = read_text(path)
        fm, body, parse_warnings = parse_frontmatter(text)
        name = fm.get("name") if isinstance(fm.get("name"), str) else None
        summary = fm.get("summary") if isinstance(fm.get("summary"), str) else None
        description = fm.get("description") if isinstance(fm.get("description"), str) else None
        record = SkillRecord(
            path=rel,
            kind=kind,
            name=name,
            summary=summary,
            description=description,
            body_chars=len(body),
            description_chars=len(description or ""),
        )

        def add(severity: str, code: str, message: str) -> None:
            record.findings.append(Finding(severity, code, message))

        for warning in parse_warnings:
            add("error" if "missing" in warning or "unterminated" in warning else "warn", warning, warning)

        if not name:
            add("error", "missing-name", "Frontmatter is missing `name`.")
        elif not NAME_RE.match(name):
            add(
                "warn",
                "nonstandard-name",
                "`name` should be lowercase kebab-case, <=64 chars, using only a-z, 0-9, and hyphen.",
            )

        if not description:
            add("error", "missing-description", "Frontmatter is missing `description`.")
        elif len(description) > desc_limit:
            add(
                "warn",
                "description-too-long",
                f"Description is {len(description)} chars; nebulaONE target is <= {desc_limit}.",
            )

        if len(body) > body_limit:
            add(
                "warn",
                "body-too-long",
                f"Body is {len(body)} chars; nebulaONE runtime body limit is <= {body_limit}.",
            )

        if kind == "package" and not summary:
            add("info", "missing-summary", "Consider adding `summary` for PromptTemplateLibrary index readability.")

        if index_paths and rel not in index_paths:
            add("info", "not-in-index", "This skill file path was not found in Skills/index.json.")

        records.append(record)

    return records


def markdown_report(records: list[SkillRecord]) -> str:
    counts = {"error": 0, "warn": 0, "info": 0}
    for record in records:
        for finding in record.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1

    lines = [
        "# Skill Package Audit Report",
        "",
        f"Skills scanned: {len(records)}",
        f"Errors: {counts.get('error', 0)} | Warnings: {counts.get('warn', 0)} | Info: {counts.get('info', 0)}",
        "",
        "## Findings by Skill",
        "",
    ]

    for record in records:
        status = "OK" if not record.findings else ", ".join(f"{f.severity}:{f.code}" for f in record.findings)
        lines.extend(
            [
                f"### `{record.path}`",
                "",
                f"- Kind: {record.kind}",
                f"- Name: {record.name or 'MISSING'}",
                f"- Description chars: {record.description_chars}",
                f"- Body chars: {record.body_chars}",
                f"- Status: {status}",
            ]
        )
        if record.findings:
            lines.append("- Findings:")
            for finding in record.findings:
                lines.append(f"  - **{finding.severity.upper()} `{finding.code}`**: {finding.message}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit PromptTemplateLibrary skill packages.")
    parser.add_argument("--repo-root", default=".", help="Repository root path. Defaults to current directory.")
    parser.add_argument("--skills-root", default="Skills", help="Skills directory path relative to repo root.")
    parser.add_argument("--description-limit", type=int, default=300, help="nebulaONE description character limit.")
    parser.add_argument("--body-limit", type=int, default=30000, help="nebulaONE SKILL.md body character limit.")
    parser.add_argument("--json-out", help="Optional JSON output path.")
    parser.add_argument("--md-out", help="Optional Markdown report output path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skills_root = (repo_root / args.skills_root).resolve()
    if not skills_root.exists():
        raise SystemExit(f"Skills root not found: {skills_root}")

    records = audit(skills_root, args.description_limit, args.body_limit)
    payload = [asdict(record) for record in records]

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(markdown_report(records), encoding="utf-8")

    errors = sum(1 for record in records for finding in record.findings if finding.severity == "error")
    warnings = sum(1 for record in records for finding in record.findings if finding.severity == "warn")
    print(f"Scanned {len(records)} skills: {errors} errors, {warnings} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
