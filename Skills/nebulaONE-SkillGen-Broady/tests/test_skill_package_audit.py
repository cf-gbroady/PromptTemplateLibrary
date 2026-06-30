#!/usr/bin/env python3
"""Smoke tests for skill_package_audit.py.

Run from a checkout with:
python Skills/nebulaONE-SkillGen-Broady/tests/test_skill_package_audit.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    audit_script = repo_root / "Skills" / "nebulaONE-SkillGen-Broady" / "scripts" / "skill_package_audit.py"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        skills = tmp / "Skills"
        (skills / "valid-skill").mkdir(parents=True)
        (skills / "valid-skill" / "SKILL.md").write_text(
            """---
name: valid-skill
summary: Valid skill.
description: Use when validating the audit helper.
---
# Valid Skill

Do the work.
""",
            encoding="utf-8",
        )
        (skills / "invalid.md").write_text("# Missing frontmatter\n", encoding="utf-8")

        json_out = tmp / "audit.json"
        md_out = tmp / "audit.md"
        result = subprocess.run(
            [
                sys.executable,
                str(audit_script),
                "--repo-root",
                str(tmp),
                "--json-out",
                str(json_out),
                "--md-out",
                str(md_out),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        assert result.returncode == 1, result.stdout + result.stderr
        payload = json.loads(json_out.read_text(encoding="utf-8"))
        assert len(payload) == 2
        invalid = next(item for item in payload if item["path"] == "Skills/invalid.md")
        codes = {finding["code"] for finding in invalid["findings"]}
        assert {"missing-frontmatter", "missing-name", "missing-description"} <= codes
        assert "Skill Package Audit Report" in md_out.read_text(encoding="utf-8")

    print("skill_package_audit smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
