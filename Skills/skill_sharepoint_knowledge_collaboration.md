---
name: sharepoint-knowledge-collaboration
summary: Microsoft 365 SharePoint knowledge collaboration guardrails for safe site, library, page, and permission analysis.
description: Use for SharePoint knowledge collaboration, site/library/page planning, permission review, and governance guidance with Microsoft 365 guardrails.
---

# SharePoint Knowledge Collaboration

## Purpose

Use this skill when the user asks for help with SharePoint knowledge management, site organization, document library structure, page planning, metadata/taxonomy design, collaboration governance, or permission/sharing risk review.

The skill helps analyze and improve SharePoint collaboration patterns while respecting Microsoft 365 tenant policy, least-privilege access, privacy boundaries, and explicit confirmation requirements before any mutation.

## When to Use

Use this skill for:

- SharePoint site, hub, library, list, or page organization planning.
- Knowledge base and intranet content structure.
- Metadata, taxonomy, retention-label, and content-type planning.
- Permission and sharing-risk review for SharePoint sites, libraries, folders, files, or pages.
- Governance recommendations for collaboration spaces.
- Drafting safe SharePoint cleanup, migration, or information architecture plans.
- Explaining Microsoft Graph or SharePoint permission implications at a high level.

## Do Not Use When

Do not use this skill for:

- Directly accessing SharePoint, Microsoft Graph, or tenant data without an authorized tool/session.
- Bypassing tenant policy, conditional access, DLP, records management, retention, or eDiscovery controls.
- Guessing hidden site contents, permissions, sensitivity labels, or user identities.
- Making permission, sharing, page, list, site, or file changes without explicit user confirmation.
- Providing legal, compliance, or records-retention determinations as final advice.
- Extracting or exposing sensitive content beyond what is needed for the requested task.

## Access Modes

Before acting, classify the available access mode:

1. **User-provided content**
   - The user pasted, uploaded, or summarized site/page/library information.
   - Work only from that provided material.
   - Clearly state that live SharePoint state was not independently verified.

2. **Tool-authorized content**
   - A connected SharePoint, Microsoft Graph, or Microsoft 365 tool is available and authorized.
   - Use only the permissions actually granted.
   - Explain what data is being read and why.

3. **No access**
   - No data or connector is available.
   - Provide a planning template, checklist, or sample query approach.
   - Do not imply live tenant visibility.

## Microsoft 365 Guardrails

Follow these guardrails for all SharePoint work:

- **Least privilege:** request or use the narrowest permission scope required for the task.
- **Permission transparency:** state whether analysis is based on user-provided data, tool-authorized data, or assumptions.
- **No hidden access claims:** never claim to have inspected SharePoint, Graph, audit logs, permissions, or site content unless a tool actually returned that information.
- **Sensitive-data minimization:** avoid reproducing sensitive file contents, confidential page text, PII, credentials, secrets, or regulated data unless necessary and explicitly requested.
- **Tenant policy respect:** defer to Microsoft 365 tenant policy, sensitivity labels, DLP, retention, eDiscovery, legal hold, conditional access, and administrator controls.
- **Confirmation before mutation:** require explicit confirmation before creating, editing, deleting, publishing, sharing, moving, archiving, labeling, permission-changing, or site/list/library/page-mutating actions.
- **Human review for high impact:** recommend admin or compliance review before broad permission changes, external sharing changes, retention changes, site deletion, or large-scale restructuring.

## Confirmation Required Before Mutations

Ask for clear confirmation before any action that would change SharePoint or Microsoft 365 state, including:

- Creating, deleting, renaming, moving, archiving, publishing, or unpublishing sites, pages, lists, libraries, folders, or files.
- Adding, removing, or changing owners, members, visitors, groups, sharing links, or external access.
- Changing sensitivity labels, retention labels, metadata, content types, default views, navigation, or hub association.
- Sending notifications, comments, approvals, page posts, or news posts.
- Running bulk cleanup, migration, restructuring, or permission-remediation steps.

When asking for confirmation, summarize:

- Target site/library/page/items.
- Intended action.
- Expected impact.
- Rollback or recovery considerations, if known.
- Any users, groups, or external parties affected.

## Workflow

### 1. Clarify Scope

Identify:

- Site, hub, library, list, page, or folder scope.
- Business goal and audience.
- Whether the task is analysis, planning, drafting, governance, or mutation.
- Data source: user-provided, tool-authorized, or unavailable.
- Sensitivity, compliance, retention, and sharing constraints.

### 2. Assess Current State

When information is available, inspect or ask for:

- Site purpose and ownership.
- Library/list structure.
- Metadata, content types, and views.
- Page hierarchy and navigation.
- Permission inheritance, owners/members/visitors, sharing links, guests, and external access.
- Stale content, duplicate locations, broken ownership, or unclear accountability.
- Known compliance requirements.

If live tools are unavailable, provide a checklist for the user/admin to collect this information.

### 3. Recommend Improvements

Provide practical recommendations for:

- Information architecture.
- Library/list design.
- Metadata and taxonomy.
- Page and navigation layout.
- Permission simplification and least-privilege access.
- Governance, ownership, and lifecycle practices.
- Migration or cleanup sequencing.

Prefer incremental, reversible changes over broad restructuring.

### 4. Prepare Safe Action Plans

For any proposed change plan:

- Separate read-only analysis from mutating actions.
- Group changes by risk and priority.
- Identify owners and reviewers.
- Include validation steps.
- Include rollback/recovery considerations where applicable.
- Require explicit confirmation before execution.

## Microsoft Graph / SharePoint Tool Use

If Microsoft Graph, SharePoint REST, PnP, or a Microsoft 365 connector is available:

- Use delegated user-context access when the task is user-specific or requires the user's context.
- Treat application permissions as broad tenant-level access that requires heightened caution.
- Prefer read-only scopes for analysis tasks.
- Do not request write scopes unless the user explicitly asks for a mutating action.
- Explain the practical difference between read and write permissions if permission scope matters.
- Avoid exposing raw IDs, tokens, request headers, secrets, or credentials.
- Validate tool outputs and state uncertainty when permissions or API limitations may hide results.

Common permission concepts to explain when relevant:

- `Sites.Read.All` or equivalent read access can allow reading site content and metadata depending on tenant/admin consent.
- `Sites.ReadWrite.All` or equivalent write access can allow creating, updating, or deleting SharePoint content depending on grant type and policy.
- `Files.Read*` and `Files.ReadWrite*` scopes may apply to files stored in SharePoint-backed document libraries.
- Admin consent, conditional access, sensitivity labels, retention, DLP, and sharing policies can constrain what is possible.

## Output Requirements

Use clear, actionable outputs. Prefer one of these formats:

### SharePoint Assessment

- Scope reviewed:
- Access mode:
- Key findings:
- Risks:
- Recommended improvements:
- Required confirmations:
- Open questions:

### Permission / Sharing Risk Review

- Site/library/item:
- Current permission model, if known:
- Potential overexposure:
- External sharing considerations:
- Least-privilege recommendation:
- Admin/compliance review needed:
- Suggested next steps:

### Information Architecture Plan

- Goal:
- Recommended structure:
- Metadata/taxonomy:
- Navigation/page plan:
- Ownership/governance:
- Migration or cleanup sequence:
- Validation checklist:

### Mutation Confirmation Prompt

Before any mutating action, ask:

> Please confirm you want me to [specific action] on [specific target]. Expected impact: [impact]. Affected users/groups: [affected parties]. I will not proceed until you confirm.

## Guardrails

- Do not infer confidential site content or permissions that were not provided or returned by tools.
- Do not recommend broad permission grants when narrower access would satisfy the goal.
- Do not expose unnecessary sensitive content in summaries.
- Do not bypass governance, security, or compliance workflows.
- Do not execute destructive or broad-impact actions without explicit confirmation.
- Do not claim that an automated review proves legal, regulatory, or accessibility compliance.

## Quality Checklist

Before responding, verify:

- Access mode is clear.
- The answer separates facts from assumptions.
- Permissions and privacy implications are stated when relevant.
- Any mutation requires explicit confirmation.
- Recommendations align with least privilege and tenant policy.
- Sensitive data is minimized.
- Output includes clear next steps and review points.
