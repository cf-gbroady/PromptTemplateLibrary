# Microsoft 365 Skill Routing Hygiene Plan

Date: 2026-07-13
Repository: cf-gbroady/PromptTemplateLibrary
Branch: repair/m365-routing-hygiene

## Purpose

This document captures the post-repair routing plan for the Microsoft 365 standalone skills after the individual guardrail updates for Outlook, OneDrive, SharePoint, and Teams.

The prior repair sequence modernized the skill bodies with nebulaONE frontmatter, trigger descriptions under 300 characters, access modes, least-privilege guidance, permission transparency, sensitive-data minimization, confirmation-before-mutation rules, and tenant-policy boundaries.

This PR intentionally does not rewrite `Skills/index.json` yet. Instead, it provides a safe routing plan and machine-readable recommended registry entries so the next PR can update the index and README with a small, auditable diff.

## Canonical Skill Paths

| Product surface | Canonical path | Status |
|---|---|---|
| Outlook | `Skills/skill_outlook_productivity.md` | Repaired and ready for registry hygiene |
| OneDrive | `Skills/skill_onedrive_file_intelligence.md` | Repaired and ready for registry hygiene |
| SharePoint | `Skills/skill_sharepoint_knowledge_collaboration.md` | Repaired and ready for registry hygiene |
| Teams | `Skills/skill_teams_productivity.md` | Repaired and ready for registry hygiene |

## Routing Goals

1. Ensure each Microsoft 365 skill has a clear index entry.
2. Keep descriptions under 300 characters.
3. Use descriptions as trigger text, not as long implementation summaries.
4. Include common user intents in `triggers` where supported by the existing `Skills/index.json` schema.
5. Tag all four skills consistently with `microsoft-365`, `m365`, `enterprise-collaboration`, and the product name.
6. Avoid claiming live Microsoft Graph access in registry text; the skills themselves distinguish user-provided content, tool-authorized content, and no-access scenarios.

## Recommended Description Text

| Skill | Recommended description |
|---|---|
| Outlook Productivity | Use for Outlook email, calendar, inbox triage, meeting prep, follow-ups, and productivity workflows with permission-aware Microsoft 365 guardrails. |
| OneDrive File Intelligence | Use for OneDrive file triage, organization, sharing-risk review, version analysis, and file workflow planning with permission-aware M365 guardrails. |
| SharePoint Knowledge Collaboration | Use for SharePoint knowledge organization, site/library planning, sharing review, page/list guidance, and governance with M365 guardrails. |
| Teams Productivity | Use for Teams meetings, chats, channels, collaboration hygiene, guest/app governance, and productivity workflows with M365 guardrails. |

## Recommended Trigger Phrases

### Outlook

- outlook productivity
- email triage
- inbox cleanup
- calendar planning
- meeting follow ups
- draft email
- schedule meeting

### OneDrive

- onedrive file intelligence
- organize files
- file sharing review
- duplicate file review
- version analysis
- folder structure
- permission risk review

### SharePoint

- sharepoint knowledge collaboration
- sharepoint site planning
- document library governance
- page planning
- list planning
- sharing risk review
- knowledge base organization

### Teams

- teams productivity
- meeting hygiene
- channel architecture
- chat summary
- guest access review
- teams governance
- app and tab planning

## Recommended Tags

All four skills should include:

- `microsoft-365`
- `m365`
- `enterprise-collaboration`
- `guardrails`

Product-specific tags should include:

- Outlook: `outlook`, `email`, `calendar`
- OneDrive: `onedrive`, `files`, `sharing`
- SharePoint: `sharepoint`, `knowledge-management`, `governance`
- Teams: `teams`, `meetings`, `channels`

## Index Update Guidance

When updating `Skills/index.json`, preserve the existing schema and ordering convention. If an entry already exists for a Microsoft 365 skill, update it in place. If missing, add a new entry with the same field shape used by neighboring standalone skill entries.

Recommended fields when supported by the schema:

```json
{
  "id": "m365-outlook-productivity",
  "name": "Outlook Productivity",
  "title": "Outlook Productivity",
  "summary": "Permission-aware Outlook email, calendar, and productivity workflow support.",
  "repositoryPrefix": "https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/",
  "path": "Skills/skill_outlook_productivity.md",
  "fullyQualifiedLink": "https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/Skills/skill_outlook_productivity.md",
  "rawSkillUrl": "https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/skill_outlook_productivity.md",
  "description": "Use for Outlook email, calendar, inbox triage, meeting prep, follow-ups, and productivity workflows with permission-aware Microsoft 365 guardrails.",
  "triggers": [],
  "tags": []
}
```

Use the companion JSON recommendation file for all four entries.

## README Update Guidance

`Skills/README.md` should add a Microsoft 365 section or table that lists the four canonical skill paths. This makes the repaired skills discoverable outside of `Skills/index.json`.

Suggested table:

| Skill | Path | Use when |
|---|---|---|
| Outlook Productivity | `Skills/skill_outlook_productivity.md` | Email, calendar, inbox triage, meeting prep, follow-ups |
| OneDrive File Intelligence | `Skills/skill_onedrive_file_intelligence.md` | File triage, organization, sharing review, version/file workflow analysis |
| SharePoint Knowledge Collaboration | `Skills/skill_sharepoint_knowledge_collaboration.md` | Site/library/page/list planning, governance, knowledge organization |
| Teams Productivity | `Skills/skill_teams_productivity.md` | Meetings, chats, channels, collaboration hygiene, guest/app governance |

## Validation Checklist for the Next PR

- `Skills/index.json` remains valid JSON.
- Every M365 index entry points to an existing file.
- Every recommended description is under 300 characters.
- README paths match repository paths exactly.
- No registry text claims live access to Outlook, OneDrive, SharePoint, Teams, or Microsoft Graph.
- Tags and triggers improve routing without over-triggering unrelated Microsoft 365 tasks.

## Follow-up

After this routing plan is merged, the next PR should update `Skills/index.json` and `Skills/README.md` directly, then proceed to the next audit area: safety/meta skills such as citations/grounding, compliance/privacy, and web research.
