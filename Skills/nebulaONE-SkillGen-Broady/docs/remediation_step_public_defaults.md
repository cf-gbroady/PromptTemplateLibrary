# Remediation Step: Neutral Public Skill Defaults

This change separates library-wide authoring rules from intentionally product-specific skill behavior.

## Changes

- Replaces the library-wide nebulaONE/Cloudforce platform assumption with neutral runtime and capability defaults.
- Removes private tenant, architecture, compliance, and vertical assumptions from the general authoring standard.
- Makes branding opt-in through a user-supplied or explicitly product-specific profile.
- Preserves the intentionally nebulaONE-specific analytics packages.
- Updates the proprietary-information policy and removes the temporary `Skills/README.md` allowlist entries.

## Why

The previous README required every skill to inherit a fixed product palette and deployment assumptions. That caused general-purpose skills to appear product-specific and could turn deployment-dependent security or compliance details into universal claims.

## Follow-up backlog

1. Neutralize fixed product palettes in general artifact skills while preserving accessible examples.
2. Review `skills-compliance-privacy.md` and `skills-citations-grounding.md` for deployment-specific architecture claims.
3. Remove the remaining allowlist entries as each file is repaired.
4. Keep nebulaONE analytics branding inside the analytics packages unless the owner requests a neutral theme option.
