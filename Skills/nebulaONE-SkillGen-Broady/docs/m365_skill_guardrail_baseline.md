# Microsoft 365 Skill Guardrail Baseline

Date: 2026-07-13  
Branch: `repair/m365-guardrail-baseline`  
Scope: Outlook, OneDrive, SharePoint, and Teams root-level Microsoft 365 skills.

## Purpose

This repair establishes a shared guardrail baseline for Microsoft 365 skills before rewriting individual skill bodies. The goal is to make the next repair PRs safer and easier to review by defining the mandatory rules each Microsoft 365 skill should include.

## Skills in Scope

| Skill file | Product surface | Repair priority |
|---|---|---|
| `Skills/skill_outlook_productivity.md` | Outlook mail, calendar, contacts, and tasks | P1 |
| `Skills/skill_onedrive_file_intelligence.md` | OneDrive files and file intelligence | P1 |
| `Skills/skill_sharepoint_knowledge_collaboration.md` | SharePoint sites, files, pages, and lists | P1 |
| `Skills/skill_teams_productivity.md` | Teams chats, channels, meetings, and collaboration | P1 |

## Standards Source

This baseline is grounded in Microsoft Graph and Microsoft identity platform guidance:

- Microsoft Graph supports delegated access, where an app acts on behalf of a signed-in user, and app-only access, where an app acts with its own identity without a signed-in user.
- Delegated permissions are constrained by both the app's granted scopes and the signed-in user's own permissions.
- Application permissions can access data associated with the granted permission without a signed-in user and normally require administrator consent.
- Microsoft recommends least-privilege permission selection and warns that over-privileged permissions increase exposure to unauthorized or unintended access.
- Tenant-wide admin consent is a sensitive operation that can give an application broad access to organizational data or privileged operations; permissions should be carefully reviewed before consent.

## Mandatory Guardrails for Microsoft 365 Skills

Each Microsoft 365 skill should include the following runtime rules directly in its `SKILL.md` or root Markdown body.

### 1. Permission and Access Boundary

- Do not claim access to Outlook, OneDrive, SharePoint, Teams, or Graph data unless the user has provided it in chat, uploaded it, or the runtime has an authorized connector/tool.
- Treat Microsoft 365 data as permission-scoped: only access or reason over resources the signed-in user or configured app is allowed to access.
- If access depends on Microsoft Graph, identify whether the scenario is delegated/user-context or application/app-only before recommending permissions.
- Prefer delegated/user-context access for interactive user tasks.
- Prefer app-only/application access only for unattended automation, background services, tenant-level reporting, or scenarios that cannot be scoped to one signed-in user.

### 2. Least-Privilege Rule

- Recommend the narrowest permission that supports the task.
- Prefer read-only permissions for analysis and summarization.
- Avoid broad `.All`, tenant-wide, write, delete, send, or full-control permissions unless the task explicitly requires them.
- When a broad permission is necessary, state why narrower alternatives are insufficient.
- Do not recommend `Directory.*`, `Sites.FullControl.All`, `Mail.ReadWrite.All`, `Files.ReadWrite.All`, or comparable high-impact permissions without a clear justification and admin review note.

### 3. Confirmation Before User-Impacting Actions

Require explicit user confirmation before:

- Sending email, meeting invitations, Teams messages, or notifications.
- Creating, updating, moving, deleting, sharing, publishing, or permissioning files, folders, pages, lists, sites, teams, channels, chats, or calendar items.
- Exporting or summarizing sensitive, personal, HR, legal, financial, regulated, or cross-user content.
- Running bulk operations or changes affecting multiple users, groups, sites, teams, mailboxes, or documents.
- Granting, requesting, or recommending tenant-wide admin consent.

### 4. Privacy and Sensitive Data Handling

- Minimize collection and display of personal, confidential, or regulated data.
- Summarize instead of quoting sensitive content unless exact wording is necessary.
- Do not expose hidden, private, restricted, or unrelated content discovered through broad access.
- Respect retention, legal hold, DLP, sensitivity labels, and organization policy constraints when known.
- If the user asks for content outside their apparent authorization scope, refuse or ask them to provide authorized source material.

### 5. Tool and API Claims

- Do not imply direct Microsoft Graph, Outlook, OneDrive, SharePoint, or Teams API access unless such a connector/tool is available in the runtime.
- If no connector is available, provide steps, scripts, or instructions rather than claiming completion.
- If proposing Graph calls, include the endpoint intent and permission class at a high level, but avoid fabricating tenant IDs, app IDs, URLs, tokens, or resource identifiers.
- Never ask users to paste secrets, refresh tokens, client secrets, private keys, or admin credentials into chat.

### 6. Output Requirements

For Microsoft 365 tasks, each skill should clearly report:

- What data source was used.
- Whether actions were performed or only recommended.
- Any assumptions about permissions or access.
- Any required admin consent or tenant policy dependency.
- Any privacy or compliance caveats.
- Next safe action for the user.

## Product-Specific Repair Notes

### Outlook

Add explicit confirmation before sending mail, replying, forwarding, deleting, moving messages, creating calendar events, changing contacts, or modifying tasks. Recommend read-only mail/calendar permissions unless the task requires write/send operations.

### OneDrive

Add explicit confirmation before sharing, deleting, moving, renaming, or changing permissions on files/folders. Prefer selected-file or delegated access where possible and avoid broad tenant file permissions unless an admin automation scenario requires it.

### SharePoint

Add explicit confirmation before changing sites, pages, lists, permissions, metadata, or publishing content. Prefer site-selected or scoped access patterns when possible and avoid full-control permissions unless necessary.

### Teams

Add explicit confirmation before sending messages, creating channels/teams, changing membership, installing apps, or accessing meeting artifacts. Treat chat, transcript, recording, and call data as sensitive.

## Recommended Next PRs

1. **Outlook guardrail rewrite** — add the shared baseline plus Outlook-specific confirmation rules.
2. **OneDrive guardrail rewrite** — add file access, sharing, and permission safeguards.
3. **SharePoint guardrail rewrite** — add site/list/page permission and publishing safeguards.
4. **Teams guardrail rewrite** — add chat/channel/meeting artifact safeguards.
5. **Index hygiene pass** — verify the `Skills/index.json` entries for Microsoft 365 skills describe the new boundaries and triggers.

## Validation Checklist for Future M365 Skill Repairs

- [ ] Description remains under 300 characters.
- [ ] Body remains under 30,000 characters.
- [ ] Skill includes permission/access boundaries.
- [ ] Skill distinguishes delegated vs app-only access where Graph is mentioned.
- [ ] Skill includes explicit confirmation rules for user-impacting actions.
- [ ] Skill includes privacy and sensitive-data minimization rules.
- [ ] Skill does not claim unavailable connector/API access.
- [ ] Skill does not ask for secrets or credentials.
- [ ] Skill reports assumptions, caveats, and next safe action.
