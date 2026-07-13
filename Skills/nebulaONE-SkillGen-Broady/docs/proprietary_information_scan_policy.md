# Proprietary-Information Scan Policy

Use the local scanner before publishing or materially changing skills. It detects likely credentials, organization-specific identifiers, platform architecture/compliance claims, and fixed product-brand defaults. It supplements—rather than replaces—GitHub secret scanning.

## Operating rules

- Run the scanner from the repository root so policy paths remain stable.
- Treat `critical` and `high` unsuppressed findings as blockers.
- Review `medium` and `low` findings for scope, wording, and intended audience.
- Allowlist only a specific path plus a pattern ID or category, with a concrete reason.
- Do not allowlist a credential finding.
- Existing reviewed exceptions are baselines, not permanent approval; remove them as related files are neutralized.
- Keep output reports out of the committed tree unless they are deliberately retained as audit evidence.

## Command

```bash
python Skills/nebulaONE-SkillGen-Broady/scripts/skills_proprietary_scan.py \
  --root . \
  --policy Skills/nebulaONE-SkillGen-Broady/policies/proprietary_information_scan_policy.json \
  --json-out /tmp/skills-proprietary-scan.json \
  --markdown-out /tmp/skills-proprietary-scan.md \
  --fail-on high
```

The scanner uses only the Python standard library and does not require network access. Exit codes are `0` for no findings at or above the failure threshold, `1` for blocking findings, and `2` for invalid policy or runtime errors.

## Relationship to GitHub controls

GitHub Secret Protection remains preferred for provider-token coverage and push protection when enabled. This local control adds repository-specific checks and provides a fallback where Advanced Security is unavailable.
