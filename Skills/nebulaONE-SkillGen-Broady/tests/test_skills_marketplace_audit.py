import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "skills_marketplace_audit.py"
SPEC = importlib.util.spec_from_file_location("skills_marketplace_audit", SCRIPT)
audit_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = audit_module
SPEC.loader.exec_module(audit_module)


class MarketplaceAuditTests(unittest.TestCase):
    def policy(self):
        return {
            "policy_version": 1,
            "marketplace_adapter": "portable-agent-skills",
            "repository": "example/repo",
            "index_path": "Skills/index.json",
            "required_index_fields": ["id", "name", "path", "description"],
            "recommended_index_fields": ["tags"],
            "limits": {
                "name_characters": 64,
                "description_characters": 300,
                "body_characters": 30000,
            },
            "exclude_globs": [],
            "fail_at_severity": "high",
        }

    def write_index(self, root: Path, entries):
        path = root / "Skills" / "index.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(entries), encoding="utf-8")

    def write_skill(self, root: Path, name="sample-skill", description="Use for sample tasks."):
        path = root / "Skills" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# Sample\n\nFollow the workflow.\n",
            encoding="utf-8",
        )
        return path

    def entry(self, name="sample-skill", path="Skills/sample-skill/SKILL.md"):
        return {
            "id": name,
            "name": name,
            "title": "Sample Skill",
            "summary": "Sample workflow",
            "path": path,
            "fullyQualifiedLink": f"https://github.com/example/repo/tree/main/{path}",
            "rawSkillUrl": f"https://raw.githubusercontent.com/example/repo/main/{path}",
            "description": "Use for sample tasks.",
            "triggers": ["sample"],
            "tags": ["example"],
        }

    def test_valid_package_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_skill(root)
            self.write_index(root, [self.entry()])
            report = audit_module.audit(root, self.policy())
            self.assertFalse(report["failed"])
            self.assertEqual(report["summary"]["ready_packages"], 1)

    def test_legacy_path_requires_migration_without_failing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            legacy = root / "Skills" / "skills-old.md"
            legacy.parent.mkdir(parents=True, exist_ok=True)
            legacy.write_text("---\nname: old\ndescription: old\n---\n", encoding="utf-8")
            self.write_index(root, [self.entry("old", "Skills/skills-old.md")])
            report = audit_module.audit(root, self.policy())
            self.assertFalse(report["failed"])
            self.assertEqual(report["summary"]["migration_needed"], 1)
            self.assertTrue(any(item["code"] == "legacy-index-path" for item in report["findings"]))

    def test_unindexed_package_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_skill(root, "orphan")
            self.write_index(root, [])
            report = audit_module.audit(root, self.policy())
            self.assertTrue(report["failed"])
            self.assertTrue(any(item["code"] == "package-not-indexed" for item in report["findings"]))

    def test_name_folder_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "Skills" / "folder-name" / "SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "---\nname: different-name\ndescription: Use for testing.\n---\n# Test\n",
                encoding="utf-8",
            )
            self.write_index(root, [self.entry("folder-name", "Skills/folder-name/SKILL.md")])
            report = audit_module.audit(root, self.policy())
            self.assertTrue(report["failed"])
            self.assertTrue(any(item["code"] == "name-folder-mismatch" for item in report["findings"]))

    def test_report_writers(self):
        report = audit_module.summarize([], [], self.policy())
        markdown = audit_module.to_markdown(report)
        self.assertIn("Skills Marketplace Readiness Report", markdown)
        self.assertFalse(report["failed"])


if __name__ == "__main__":
    unittest.main()
