#!/usr/bin/env python3
"""Audit the Skills library for portable marketplace readiness.

This helper uses only the Python standard library. It reads repository files,
validates metadata and paths, and emits JSON and Markdown reports. It never
publishes, installs, or modifies skills.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str
    skill_id: str | None = None


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value[0:1] in {'"', "'"} and value[-1:] == value[0]:
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value.replace("'", '"'))
        except json.JSONDecodeError:
            return [item.strip() for item in value[1:-1].split(",") if item.strip()]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse the flat metadata fields used by repository SKILL.md files."""
    match = FRONTMATTER_RE.search(text.replace("\r\n", "\n"))
    if not match:
        return {}, text

    metadata: dict[str, Any] = {}
    active_list: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and active_list and line.lstrip().startswith("- "):
            metadata.setdefault(active_list, []).append(parse_scalar(line.lstrip()[2:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            metadata[key] = []
            active_list = key
        else:
            metadata[key] = parse_scalar(value)
            active_list = None
    return metadata, text[match.end():]


def index_entries(index_data: Any) -> list[dict[str, Any]]:
    if isinstance(index_data, list):
        return [item for item in index_data if isinstance(item, dict)]
    if isinstance(index_data, dict):
        for key in ("skills", "items", "entries"):
            value = index_data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise ValueError("Skills/index.json must be an array or contain a skills/items/entries array")


def excluded(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def audit(root: Path, policy: dict[str, Any]) -> dict[str, Any]:
    findings: list[Finding] = []
    limits = policy.get("limits", {})
    description_max = int(limits.get("description_characters", 300))
    body_max = int(limits.get("body_characters", 30000))
    name_max = int(limits.get("name_characters", 64))
    index_path = root / policy.get("index_path", "Skills/index.json")
    excluded_globs = policy.get("exclude_globs", [])

    try:
        entries = index_entries(load_json(index_path))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        findings.append(Finding("critical", "index-invalid", str(index_path.relative_to(root)), str(exc)))
        return summarize(findings, [], policy)

    required_fields = policy.get("required_index_fields", ["id", "name", "path", "description"])
    recommended_fields = policy.get("recommended_index_fields", ["title", "summary", "triggers", "tags"])
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    records: list[dict[str, Any]] = []

    for entry in entries:
        skill_id = str(entry.get("id") or entry.get("name") or "").strip()
        path_value = str(entry.get("path") or "").strip()
        record = {
            "id": skill_id or None,
            "path": path_value or None,
            "format": "unknown",
            "status": "not_ready",
            "description_characters": len(str(entry.get("description") or "")),
            "body_characters": None,
        }

        for field in required_fields:
            if entry.get(field) in (None, "", []):
                findings.append(Finding("high", "index-required-field", "Skills/index.json",
                                        f"Missing required index field: {field}", skill_id or None))
        for field in recommended_fields:
            if entry.get(field) in (None, "", []):
                findings.append(Finding("low", "index-recommended-field", "Skills/index.json",
                                        f"Missing recommended marketplace field: {field}", skill_id or None))

        if skill_id:
            if skill_id in seen_ids:
                findings.append(Finding("high", "duplicate-id", "Skills/index.json",
                                        f"Duplicate skill id: {skill_id}", skill_id))
            seen_ids.add(skill_id)
            if len(skill_id) > name_max or not NAME_RE.fullmatch(skill_id):
                findings.append(Finding("medium", "invalid-id", "Skills/index.json",
                                        "Skill id should be lowercase kebab-case and within the configured limit.", skill_id))

        if path_value:
            if path_value in seen_paths:
                findings.append(Finding("medium", "duplicate-path", "Skills/index.json",
                                        f"Multiple entries use path: {path_value}", skill_id or None))
            seen_paths.add(path_value)
            target = root / path_value
            if not target.is_file():
                findings.append(Finding("high", "missing-path", path_value,
                                        "Indexed skill path does not exist.", skill_id or None))
                records.append(record)
                continue

            if path_value.endswith("/SKILL.md"):
                record["format"] = "package"
                metadata, body = parse_frontmatter(target.read_text(encoding="utf-8"))
                record["body_characters"] = len(body)
                package_name = target.parent.name
                front_name = str(metadata.get("name") or "")
                front_description = str(metadata.get("description") or "")
                if not metadata:
                    findings.append(Finding("high", "frontmatter-missing", path_value,
                                            "Canonical package is missing YAML frontmatter.", skill_id or None))
                if front_name != package_name:
                    findings.append(Finding("high", "name-folder-mismatch", path_value,
                                            f"Frontmatter name '{front_name}' must match folder '{package_name}'.",
                                            skill_id or None))
                if skill_id and front_name and skill_id != front_name:
                    findings.append(Finding("medium", "index-name-mismatch", path_value,
                                            f"Index id '{skill_id}' differs from frontmatter name '{front_name}'.",
                                            skill_id))
                if not front_description:
                    findings.append(Finding("high", "description-missing", path_value,
                                            "Frontmatter description is required.", skill_id or None))
                elif len(front_description) > description_max:
                    findings.append(Finding("medium", "description-too-long", path_value,
                                            f"Description is {len(front_description)} characters; limit is {description_max}.",
                                            skill_id or None))
                if len(body) > body_max:
                    findings.append(Finding("medium", "body-too-long", path_value,
                                            f"Body is {len(body)} characters; limit is {body_max}.",
                                            skill_id or None))
                record["description_characters"] = len(front_description)
                record["status"] = "ready"
            else:
                record["format"] = "legacy"
                record["status"] = "migration_needed"
                findings.append(Finding("medium", "legacy-index-path", path_value,
                                        "Marketplace exports should use a folder containing SKILL.md; preserve this path only as a compatibility shim.",
                                        skill_id or None))

            expected_tree = f"https://github.com/{policy.get('repository', '')}/tree/main/{path_value}"
            expected_raw = f"https://raw.githubusercontent.com/{policy.get('repository', '')}/main/{path_value}"
            if entry.get("fullyQualifiedLink") and entry.get("fullyQualifiedLink") != expected_tree:
                findings.append(Finding("low", "tree-link-mismatch", "Skills/index.json",
                                        f"fullyQualifiedLink should resolve to {expected_tree}", skill_id or None))
            if entry.get("rawSkillUrl") and entry.get("rawSkillUrl") != expected_raw:
                findings.append(Finding("low", "raw-link-mismatch", "Skills/index.json",
                                        f"rawSkillUrl should resolve to {expected_raw}", skill_id or None))

        records.append(record)

    skills_root = root / "Skills"
    for skill_file in skills_root.glob("*/SKILL.md"):
        rel = skill_file.relative_to(root).as_posix()
        if excluded(rel, excluded_globs):
            continue
        if rel not in seen_paths:
            metadata, _ = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
            sid = str(metadata.get("name") or skill_file.parent.name)
            findings.append(Finding("high", "package-not-indexed", rel,
                                    "Canonical skill package is not represented in Skills/index.json.", sid))

    return summarize(findings, records, policy)


def summarize(findings: list[Finding], records: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    counts = {severity: 0 for severity in SEVERITY_ORDER}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    fail_at = policy.get("fail_at_severity", "high")
    threshold = SEVERITY_ORDER.get(fail_at, 3)
    failed = any(SEVERITY_ORDER.get(item.severity, 0) >= threshold for item in findings)
    return {
        "policy_version": policy.get("policy_version"),
        "marketplace_adapter": policy.get("marketplace_adapter", "portable-agent-skills"),
        "failed": failed,
        "summary": {
            "skills_indexed": len(records),
            "ready_packages": sum(item["status"] == "ready" for item in records),
            "migration_needed": sum(item["status"] == "migration_needed" for item in records),
            "findings": len(findings),
            "by_severity": counts,
        },
        "skills": records,
        "findings": [asdict(item) for item in sorted(
            findings,
            key=lambda item: (-SEVERITY_ORDER.get(item.severity, 0), item.path, item.code),
        )],
    }


def to_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Skills Marketplace Readiness Report",
        "",
        f"- Adapter: `{report['marketplace_adapter']}`",
        f"- Indexed skills: **{summary['skills_indexed']}**",
        f"- Ready packages: **{summary['ready_packages']}**",
        f"- Legacy migrations needed: **{summary['migration_needed']}**",
        f"- Findings: **{summary['findings']}**",
        f"- Validation result: **{'FAIL' if report['failed'] else 'PASS'}**",
        "",
        "## Skill status",
        "",
        "| Skill | Format | Status | Path |",
        "|---|---|---|---|",
    ]
    for item in report["skills"]:
        lines.append(f"| {item['id'] or '—'} | {item['format']} | {item['status']} | `{item['path'] or '—'}` |")
    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("No findings.")
    else:
        lines.extend(["| Severity | Code | Skill | Path | Message |", "|---|---|---|---|---|"])
        for item in report["findings"]:
            message = item["message"].replace("|", "\\|")
            lines.append(
                f"| {item['severity']} | `{item['code']}` | {item['skill_id'] or '—'} | "
                f"`{item['path']}` | {message} |"
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("Skills/nebulaONE-SkillGen-Broady/policies/marketplace_readiness_policy.json"),
    )
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    policy_path = args.policy if args.policy.is_absolute() else root / args.policy
    report = audit(root, load_json(policy_path))

    if args.json_output:
        output = args.json_output if args.json_output.is_absolute() else root / args.json_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        output = args.markdown_output if args.markdown_output.is_absolute() else root / args.markdown_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(to_markdown(report), encoding="utf-8")
    if not args.json_output and not args.markdown_output:
        print(json.dumps(report, indent=2))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
