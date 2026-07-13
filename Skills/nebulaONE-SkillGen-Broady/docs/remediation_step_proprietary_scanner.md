# Remediation Step: Local Proprietary-Information Scanner

This change converts the merged proprietary-information audit into a repeatable validation control.

## Added

- A standard-library scanner for credential-like values, organization identifiers, platform architecture/compliance claims, and fixed brand defaults.
- A versioned JSON policy with narrowly scoped, reasoned allowlist entries.
- Unit tests covering detection, suppression, threshold failure, and report generation.
- Operating guidance for local execution and future remediation work.

## Scope decisions

- Existing nebulaONE-specific packages remain intact.
- Known branding and architecture references are allowlisted only where the audit already identified and reviewed them.
- Allowlisted items remain remediation backlog entries rather than being treated as permanently safe.
- The scanner fails on unsuppressed `high` or `critical` findings by default.

## Next remediation

Use the scanner to support a separate, focused PR that splits public/general authoring defaults from intentionally platform-specific defaults and removes temporary allowlist entries as each file is neutralized.
