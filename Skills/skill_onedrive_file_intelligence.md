---
name: onedrive-file-intelligence
summary: Analyze OneDrive file content, metadata, sharing context, and organization signals from user-provided or authorized files.
description: Use for OneDrive file intelligence, file triage, metadata review, sharing-risk summaries, version/change analysis, or folder/file organization when the user provides files or authorized Microsoft 365 access.
---

# OneDrive File Intelligence

## Purpose

Use this skill to help users understand, organize, summarize, compare, and reason about OneDrive files and folders when the relevant content, metadata, or tool-authorized Microsoft 365 access is available.

The skill supports:
- File and folder triage
- Metadata and sharing-context review
- Version, duplicate, and change analysis
- File organization recommendations
- Content summaries and extraction from user-provided or authorized OneDrive files
- Risk-aware review of sharing, sensitivity, retention, and ownership signals

## When to Use

Use this skill when the user asks to:
- Analyze OneDrive files, folders, links, sync state, file versions, or sharing settings
- Summarize or compare documents stored in OneDrive
- Identify duplicate, stale, risky, sensitive, or poorly organized files
- Build a file inventory, cleanup plan, or migration readiness summary
- Review OneDrive metadata exported from Microsoft 365, Graph, Purview, audit logs, or admin reports
- Explain which Microsoft Graph permissions or consent boundaries would be needed for a OneDrive workflow

## Do Not Use When

Do not use this skill for:
- General spreadsheet, DOCX, PDF, or PowerPoint editing when the task is only file-format transformation; use the relevant document skill instead
- SharePoint site governance that is not about OneDrive or files
- Outlook mailbox, calendar, or Teams productivity tasks
- Live Microsoft 365 access when the user has not provided a connector, token, uploaded export, or authorized tool context
- Bypassing tenant policy, retention, DLP, sharing restrictions, consent requirements, or user permissions

## Access Modes

Before analyzing or acting on OneDrive content, classify the access mode.

### 1. User-provided content

Use this mode when the user uploads files, pastes metadata, provides a CSV/export, or describes a folder structure.

You may analyze only what the user provided. Do not imply that you inspected the user's live OneDrive unless a tool actually did so.

### 2. Tool-authorized content

Use this mode when a Microsoft 365, OneDrive, SharePoint, Graph, Purview, or file connector is available and has been explicitly authorized.

Before using the tool:
- State what data you plan to access
- Use the narrowest available scope and filters
- Prefer read-only access for analysis
- Respect tenant and connector restrictions
- Report permission or consent limitations plainly

### 3. No access

Use this mode when the user asks about their OneDrive but has not provided files, exports, metadata, or an authorized tool.

In this mode:
- Ask for the needed file, export, folder listing, metadata, or authorized connector
- Provide a template for the information needed
- Do not claim to have inspected OneDrive content

## Microsoft 365 Guardrails

Follow these guardrails for all OneDrive and Microsoft Graph work.

### Permission transparency

When tools or APIs are involved, state the access assumption:
- Delegated access: actions happen in the signed-in user's context.
- Application access: app-only access can be broader and may require administrator consent.
- Unknown access: do not assume access exists; ask the user or inspect the tool state.

### Least privilege

Use the least privileged access that can satisfy the task:
- Prefer selected files, uploaded files, exported reports, or read-only metadata.
- Prefer `Files.Read` or equivalent read-only access for user-file analysis.
- Use broader scopes such as `Files.Read.All`, `Files.ReadWrite`, `Files.ReadWrite.All`, `Sites.Read.All`, or `Sites.ReadWrite.All` only when the task clearly requires them and the user has authorized them.
- Do not request write permissions for read-only analysis.

### Sensitive-data minimization

OneDrive files can contain confidential business data, personal data, financial data, legal content, health information, credentials, and regulated records.

When producing outputs:
- Summarize sensitive content instead of reproducing it unless the user explicitly needs exact text.
- Avoid unnecessary exposure of file paths, sharing links, external users, object IDs, and tenant identifiers.
- Flag suspected secrets, credentials, or regulated data and recommend safe handling.
- Do not generate public sharing links or broad-access recommendations unless the user explicitly asks and confirms the risk.

### Confirmation before mutations

Require explicit user confirmation before any action that would:
- Create, overwrite, move, rename, archive, restore, delete, or share a file or folder
- Change permissions, links, owners, labels, retention, or sensitivity metadata
- Sync, migrate, export, or bulk-download OneDrive content
- Grant, request, or elevate Microsoft Graph permissions
- Send file contents to external services or non-tenant destinations

Confirmation must summarize:
1. Target files/folders
2. Intended action
3. Expected permission level
4. Reversibility or recovery options
5. Known risks

### Tenant policy and compliance

Respect tenant configuration and governance:
- Do not recommend bypassing DLP, retention, sensitivity labels, eDiscovery holds, sharing restrictions, conditional access, or audit requirements.
- If the user requests an action that conflicts with policy, explain the conflict and suggest a compliant alternative.
- For compliance-sensitive analysis, recommend involving the appropriate Microsoft 365, Purview, legal, records, or security owner.

## OneDrive Workflow

### 1. Clarify the task

Determine:
- Files, folders, drive, site, or user scope
- Whether the user needs content analysis, metadata analysis, sharing analysis, or organization planning
- Whether the data is uploaded, exported, pasted, or accessible through tools
- Whether the output should be a summary, table, risk report, cleanup plan, migration plan, or action checklist

### 2. Establish access and boundaries

State what you can and cannot see.

Examples:
- "I can analyze the uploaded export, but I cannot inspect live OneDrive content."
- "I can use the authorized connector to read metadata for the selected folder only."
- "I do not have OneDrive access yet; upload the files or provide an export."

### 3. Inspect available data

Depending on the input, inspect:
- File name, extension, path, size, owner, created/modified dates
- Sharing links, external users, inherited permissions, anonymous links, and expiration dates
- Version history and recent activity when available
- Sensitivity labels, retention labels, DLP/audit signals, and compliance holds when available
- Content type, document summary, duplicates, stale files, and folder patterns

### 4. Analyze and prioritize

Organize findings by impact:
- **High risk:** externally shared sensitive files, anonymous links, broad write permissions, suspected secrets, regulated data exposure, deletion-risk changes
- **Medium risk:** stale external sharing, unclear ownership, unmanaged duplicates, missing labels, inconsistent folder structure
- **Low risk:** naming cleanup, archive candidates, metadata improvements, documentation gaps

### 5. Recommend safe actions

For every recommendation, include:
- Why it matters
- Required access or permission
- Whether confirmation is required
- Whether the change is reversible
- Suggested owner or reviewer

## Tool Use Rules

When using Microsoft 365, OneDrive, SharePoint, Graph, Purview, or connector tools:

- Read current metadata before recommending changes.
- Prefer scoped queries over tenant-wide queries.
- Prefer read-only operations unless a confirmed mutation is requested.
- Never claim a file was changed unless the tool confirms the change.
- If a tool returns limited or redacted information, say so and avoid filling gaps with guesses.
- If authorization fails, explain the likely permission boundary and ask for the needed export, file, or approved access path.
- Do not store, print, or expose access tokens, refresh tokens, cookies, client secrets, or authorization headers.

## Microsoft Graph Permission Notes

Use permission names carefully and avoid overclaiming.

Common OneDrive-related Graph concepts:
- `Files.Read`: read the signed-in user's files.
- `Files.Read.All`: read files the signed-in user can access, or app-level file access depending on grant type.
- `Files.ReadWrite`: read and write the signed-in user's files.
- `Files.ReadWrite.All`: read, create, update, and delete files the signed-in user or app can access, depending on grant type.
- `Sites.Read.All` and `Sites.ReadWrite.All`: broader SharePoint/OneDrive site collection access and often broader than needed for a single-user file task.
- Selected-file or selected-site approaches are preferable when available and suitable.

Do not recommend deprecated, preview, or limited-support permissions as a default. If a user asks about `Files.Read.Selected` or `Files.ReadWrite.Selected`, explain that selected-file permission behavior is limited and context-dependent, and verify current platform support before relying on it.

## Output Requirements

For file intelligence outputs, use the format that best fits the task.

### Risk report

Use:

```markdown
# OneDrive File Intelligence Report

## Scope
- Data source:
- Access mode:
- Files/folders reviewed:
- Limitations:

## Executive Summary
[Short summary]

## Key Findings
| Priority | Finding | Evidence | Risk | Recommended action |
|---|---|---|---|---|

## Permission / Access Notes
[Delegated/application/unknown access and least-privilege notes]

## Recommended Next Actions
1. [Action]
2. [Action]
3. [Action]

## Confirmation Needed
[List any mutations that require explicit user confirmation]
```

### Organization plan

Use:

```markdown
# OneDrive Organization Plan

## Current Structure
[Observed structure or limitations]

## Proposed Structure
[Folder/naming/metadata plan]

## Cleanup Candidates
| File/folder | Reason | Recommended action | Confirmation required |
|---|---|---|---|

## Governance Notes
[Sharing, labeling, retention, and owner recommendations]
```

### Permission explanation

Use:

```markdown
# OneDrive Access Recommendation

## Goal
[User goal]

## Minimum practical access
[Recommended least-privilege access]

## Avoid unless required
[Broader scopes or risky permissions]

## User/admin consent notes
[Consent and tenant policy considerations]

## Safe fallback
[Upload/export/manual workflow if live access is unavailable]
```

## Quality Checklist

Before finalizing:
- Identified access mode and limitations
- Used or recommended least-privilege access
- Avoided claiming live OneDrive access unless tool-confirmed
- Minimimized sensitive content exposure
- Flagged risky sharing, write, delete, export, or permission actions
- Required explicit confirmation for mutations
- Respected tenant policy and compliance boundaries
- Produced a clear table or prioritized action list when appropriate
