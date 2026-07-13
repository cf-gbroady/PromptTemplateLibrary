import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "skills_proprietary_scan.py"
SPEC = importlib.util.spec_from_file_location("skills_proprietary_scan", SCRIPT_PATH)
scanner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = scanner
SPEC.loader.exec_module(scanner)


class ProprietaryScanTests(unittest.TestCase):
    def policy(self):
        return {
            "include_globs": ["**/*"],
            "exclude_globs": [],
            "extensions": [".md", ".py"],
            "patterns": [
                {
                    "id": "brand",
                    "category": "organization_brand",
                    "severity": "medium",
                    "regex": r"\bCloudforce\b",
                    "message": "Review brand."
                },
                {
                    "id": "private-key",
                    "category": "credential",
                    "severity": "critical",
                    "regex": r"-----BEGIN PRIVATE KEY-----",
                    "message": "Private key."
                }
            ],
            "allowlist": []
        }

    def test_detects_unsuppressed_brand(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skill.md").write_text("Cloudforce default", encoding="utf-8")
            findings = scanner.scan(root, self.policy())
            self.assertEqual(1, len(findings))
            self.assertFalse(findings[0].suppressed)
            self.assertEqual("medium", findings[0].severity)

    def test_allowlist_suppresses_reviewed_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Cloudforce default", encoding="utf-8")
            policy = self.policy()
            policy["allowlist"] = [
                {
                    "path_glob": "README.md",
                    "pattern_id": "brand",
                    "reason": "Reviewed baseline."
                }
            ]
            finding = scanner.scan(root, policy)[0]
            self.assertTrue(finding.suppressed)
            self.assertEqual("Reviewed baseline.", finding.suppression_reason)

    def test_critical_finding_fails_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "secret.md").write_text("-----BEGIN PRIVATE KEY-----", encoding="utf-8")
            findings = scanner.scan(root, self.policy())
            self.assertTrue(scanner.should_fail(findings, "high"))

    def test_reports_are_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skill.md").write_text("Cloudforce default", encoding="utf-8")
            findings = scanner.scan(root, self.policy())
            json_path = root / "report.json"
            markdown_path = root / "report.md"
            scanner.write_json(json_path, root, root / "policy.json", findings)
            scanner.write_markdown(markdown_path, findings)
            data = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(1, data["summary"]["unsuppressed"])
            self.assertIn("Unsuppressed findings", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
