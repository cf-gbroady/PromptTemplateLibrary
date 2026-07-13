#!/usr/bin/env python3
"""Scan a skill library for secret-like and proprietary-information patterns.

Standard-library only. Findings are controlled by a JSON policy with regex patterns
and narrowly scoped allowlist rules. Reports can be emitted as JSON and Markdown.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
DEFAULT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".toml"}


@dataclass
class Finding:
    fingerprint: str
    path: str
    line: int
    category: str
    severity: str
    pattern_id: str
    message: str
    excerpt: str
    suppressed: bool = False
    suppression_reason: str | None = None


def load_policy(path: Path) -> dict:
    policy = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(policy.get("patterns"), list):
        raise ValueError("Policy must contain a 'patterns' array.")
    for item in policy["patterns"]:
        for required in ("id", "category", "severity", "regex", "message"):
            if required not in item:
                raise ValueError(f"Pattern is missing required field '{required}'.")
        if item["severity"] not in SEVERITY_ORDER:
            raise ValueError(f"Unknown severity: {item['severity']}")
        re.compile(item["regex"], re.IGNORECASE | re.MULTILINE)
    return policy


def glob_matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatch(path, pattern) or (
        pattern.startswith("**/") and fnmatch.fnmatch(path, pattern[3:])
    )


def iter_files(root: Path, policy: dict) -> Iterable[Path]:
    extensions = set(policy.get("extensions", DEFAULT_EXTENSIONS))
    exclude = policy.get("exclude_globs", [])
    include = policy.get("include_globs", ["**/*"])
    max_bytes = int(policy.get("max_file_bytes", 1_000_000))

    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() not in extensions:
            continue
        if path.stat().st_size > max_bytes:
            continue
        if any(glob_matches(rel, pattern) for pattern in exclude):
            continue
        if not any(glob_matches(rel, pattern) for pattern in include):
            continue
        yield path


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def excerpt_for(text: str, start: int, end: int, radius: int = 90) -> str:
    snippet = text[max(0, start - radius):min(len(text), end + radius)]
    return " ".join(snippet.replace("\r", " ").replace("\n", " ").split())[:260]


def fingerprint(path: str, pattern_id: str, line: int, matched: str) -> str:
    payload = f"{path}\0{pattern_id}\0{line}\0{matched}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:20]


def matching_allowlist(finding: Finding, allowlist: list[dict]) -> str | None:
    for rule in allowlist:
        if not glob_matches(finding.path, rule.get("path_glob", "*")):
            continue
        if rule.get("pattern_id") and rule["pattern_id"] != finding.pattern_id:
            continue
        if rule.get("category") and rule["category"] != finding.category:
            continue
        if rule.get("line") and int(rule["line"]) != finding.line:
            continue
        return rule.get("reason", "Allowed by policy.")
    return None


def scan(root: Path, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    allowlist = policy.get("allowlist", [])
    compiled = [(item, re.compile(item["regex"], re.IGNORECASE | re.MULTILINE)) for item in policy["patterns"]]

    for path in iter_files(root, policy):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for item, regex in compiled:
            for match in regex.finditer(text):
                line = line_number(text, match.start())
                finding = Finding(
                    fingerprint=fingerprint(rel, item["id"], line, match.group(0)),
                    path=rel,
                    line=line,
                    category=item["category"],
                    severity=item["severity"],
                    pattern_id=item["id"],
                    message=item["message"],
                    excerpt=excerpt_for(text, match.start(), match.end()),
                )
                reason = matching_allowlist(finding, allowlist)
                if reason:
                    finding.suppressed = True
                    finding.suppression_reason = reason
                findings.append(finding)
    return findings


def summary(findings: list[Finding]) -> dict:
    unsuppressed = [finding for finding in findings if not finding.suppressed]
    by_severity = {name: 0 for name in SEVERITY_ORDER}
    by_category: dict[str, int] = {}
    for finding in unsuppressed:
        by_severity[finding.severity] += 1
        by_category[finding.category] = by_category.get(finding.category, 0) + 1
    return {
        "total": len(findings),
        "unsuppressed": len(unsuppressed),
        "suppressed": len(findings) - len(unsuppressed),
        "by_severity": by_severity,
        "by_category": dict(sorted(by_category.items())),
    }


def write_json(path: Path, root: Path, policy_path: Path, findings: list[Finding]) -> None:
    payload = {
        "scanner": "skills_proprietary_scan",
        "root": root.as_posix(),
        "policy": policy_path.as_posix(),
        "summary": summary(findings),
        "findings": [asdict(finding) for finding in findings],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, findings: list[Finding]) -> None:
    stats = summary(findings)
    lines = [
        "# Skills Proprietary-Information Scan",
        "",
        f"- Findings: **{stats['total']}**",
        f"- Unsuppressed: **{stats['unsuppressed']}**",
        f"- Suppressed by reviewed policy: **{stats['suppressed']}**",
        "",
        "## Unsuppressed findings",
        "",
    ]
    active = [finding for finding in findings if not finding.suppressed]
    if not active:
        lines.append("No unsuppressed findings.")
    else:
        lines.extend(["| Severity | Category | File | Line | Message |", "|---|---|---|---:|---|"])
        for finding in active:
            lines.append(f"| {finding.severity} | {finding.category} | `{finding.path}` | {finding.line} | {finding.message} |")
    lines.extend(["", "## Suppressed findings", ""])
    suppressed = [finding for finding in findings if finding.suppressed]
    if not suppressed:
        lines.append("No suppressed findings.")
    else:
        lines.extend(["| Category | File | Line | Reason |", "|---|---|---:|---|"])
        for finding in suppressed:
            lines.append(f"| {finding.category} | `{finding.path}` | {finding.line} | {finding.suppression_reason} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def should_fail(findings: list[Finding], threshold: str) -> bool:
    minimum = SEVERITY_ORDER[threshold]
    return any(not finding.suppressed and SEVERITY_ORDER[finding.severity] >= minimum for finding in findings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository or subtree to scan.")
    parser.add_argument("--policy", type=Path, required=True, help="JSON scan policy.")
    parser.add_argument("--json-out", type=Path, help="Write a machine-readable JSON report.")
    parser.add_argument("--markdown-out", type=Path, help="Write a Markdown report.")
    parser.add_argument("--fail-on", choices=tuple(SEVERITY_ORDER), default="high")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    policy_path = args.policy.resolve()
    try:
        policy = load_policy(policy_path)
        findings = scan(root, policy)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"scan error: {exc}", file=sys.stderr)
        return 2

    if args.json_out:
        write_json(args.json_out, root, policy_path, findings)
    if args.markdown_out:
        write_markdown(args.markdown_out, findings)

    print(json.dumps(summary(findings), indent=2))
    return 1 if should_fail(findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
