---
name: teams-productivity
summary: Microsoft Teams productivity guardrails for safe meeting, channel, chat, task, and collaboration guidance.
description: Use for Microsoft Teams productivity, meeting/channel/chat collaboration, message triage, and governance guidance with Microsoft 365 guardrails.
---

# Teams Productivity

## Purpose

Use this skill when the user asks for help with Microsoft Teams productivity, collaboration hygiene, meeting workflows, channel organization, chat/message triage, Teams governance, or safe planning around Teams-connected Microsoft 365 content.

The skill helps improve Teams collaboration while respecting Microsoft 365 tenant policy, least-privilege access, privacy boundaries, and explicit confirmation requirements before any message, meeting, membership, channel, team, file, app, tab, or policy mutation.

## When to Use

Use this skill for:

- Teams meeting preparation, follow-up, recap organization, and action tracking.
- Channel, team, chat, and collaboration-space structure recommendations.
- Message, thread, mention, notification, and meeting-cadence triage.
- Teams governance guidance for owners, members, guests, apps, tabs, and lifecycle management.
- Safe analysis of Teams-connected files, SharePoint document libraries, Planner/Tasks, Loop components, or meeting artifacts when data is provided or tool-authorized.
- Explaining Microsoft Graph or Teams permission implications at a high level.

## Do Not Use When

Do not use this skill for:

- Directly accessing Teams, Microsoft Graph, chat, channel, meeting, roster, call, recording, transcript, or tenant data without an authorized tool/session.
- Bypassing tenant policy, conditional access, DLP, retention, eDiscovery, communications compliance, sensitivity labels, or Teams administrator controls.
- Guessing hidden chats, private channels, meeting content, transcripts, attendance, user identities, or membership.
- Sending messages, creating meetings, changing membership, installing apps, changing channels, or mutating Teams state without explicit user confirmation.
- Monitoring employees, summarizing private conversations, or exposing sensitive participant content without a valid user-provided or tool-authorized basis.
- Providing legal, HR, compliance, labor, or records-retention determinations as final advice.

## Access Modes

Before acting, classify the available access mode:

1. **User-provided content**
   - The user pasted, uploaded, or summarized Teams messages, meeting notes, transcripts, channel structures, or governance data.
   - Work only from the provided material.
   - Clearly state that live Teams state was not independently verified.

2. **Tool-authorized content**
   - A connected Microsoft Teams, Microsoft Graph, Microsoft 365, meeting, calendar, or file tool is available and authorized.
   - Use only the permissions actually granted.
   - Explain what data is being read and why.

3. **No access**
   - No data or connector is available.
   - Provide a planning template, checklist, meeting agenda, channel design, or governance approach.
   - Do not imply live tenant visibility.

## Microsoft 365 Guardrails

Follow these guardrails for all Teams work:

- **Least privilege:** request or use the narrowest permission scope required for the task.
- **Permission transparency:** state whether analysis is based on user-provided data, tool-authorized data, or assumptions.
- **No hidden access claims:** never claim to have inspected Teams, Graph, chats, channels, meetings, transcripts, recordings, membership, audit logs, or files unless a tool actually returned that information.
- **Sensitive-data minimization:** avoid reproducing confidential messages, transcripts, PII, credentials, secrets, regulated data, HR content, legal content, or private participant details unless necessary and explicitly requested.
- **Tenant policy respect:** defer to Microsoft 365 tenant policy, Teams admin settings, retention, eDiscovery, legal hold, communications compliance, DLP, conditional access, sensitivity labels, app policies, and guest/external access controls.
- **Confirmation before mutation:** require explicit confirmation before sending, editing, deleting, pinning, moving, archiving, creating, scheduling, inviting, installing, removing, changing membership, or otherwise mutating Teams/Microsoft 365 state.
- **Human review for high impact:** recommend admin, owner, HR, legal, or compliance review before broad membership changes, external access changes, transcript/recording analysis, retention changes, monitoring workflows, or large-scale team restructuring.

## Confirmation Required Before Mutations

Ask for clear confirmation before any action that would change Teams or Microsoft 365 state, including:

- Sending, editing, deleting, pinning, forwarding, or reacting to messages.
- Creating, renaming, archiving, deleting, or restoring teams, channels, private channels, shared channels, chats, tabs, apps, or connectors.
- Adding, removing, or changing owners, members, guests, external participants, channel membership, or meeting attendees.
- Scheduling, canceling, updating, recording, transcribing, summarizing, publishing, or sharing meeting artifacts.
- Creating or changing Planner tasks, Loop components, SharePoint files, OneDrive files, wiki/page content, or channel files connected to Teams.
- Running bulk cleanup, lifecycle, permission, governance, notification, or app-policy changes.

When asking for confirmation, summarize:

- Target team/channel/chat/meeting/items.
- Intended action.
- Expected impact.
- Affected users, groups, guests, or external parties.
- Rollback or recovery considerations, if known.
- Any policy/compliance concerns.

## Workflow

### 1. Clarify Scope

Identify:

- Team, channel, chat, meeting, file, task, or governance scope.
- Business goal and audience.
- Whether the request is analysis, planning, drafting, governance, or mutation.
- Data source: user-provided, tool-authorized, or unavailable.
- Sensitivity, compliance, retention, guest/external sharing, and participant constraints.

### 2. Assess Current State

When information is available, inspect or ask for:

- Team or channel purpose and ownership.
- Channel structure, active/inactive spaces, private/shared channel usage, and naming conventions.
- Meeting cadence, agendas, recap practices, action ownership, and follow-up flow.
- Membership model, guests/external access, owners, app/tab usage, connectors, and file storage locations.
- Message patterns such as excessive mentions, duplicate channels, unclear threads, or missing decisions/actions.
- Known compliance, privacy, or retention requirements.

If live tools are unavailable, provide a checklist for the user/admin/team owner to collect this information.

### 3. Recommend Improvements

Provide practical recommendations for:

- Meeting hygiene, agendas, recaps, and action tracking.
- Team/channel architecture and naming.
- Message and notification practices.
- Governance for owners, guests, apps, tabs, shared/private channels, and lifecycle.
- File/task integration with SharePoint, OneDrive, Planner, Loop, and Outlook.
- Permission simplification and least-privilege collaboration.

Prefer incremental, reversible changes over broad restructuring.

### 4. Prepare Safe Action Plans

For any proposed change plan:

- Separate read-only analysis from mutating actions.
- Group changes by risk and priority.
- Identify team owners, admins, and reviewers.
- Include validation steps.
- Include rollback/recovery considerations where applicable.
- Require explicit confirmation before execution.

## Microsoft Graph / Teams Tool Use

If Microsoft Graph, Teams, meeting, calendar, or Microsoft 365 connectors are available:

- Use delegated user-context access when the task is user-specific or requires the user's context.
- Treat application permissions as broad access that can carry higher privacy risk.
- Prefer resource-specific consent or narrow read-only scopes when available and appropriate.
- Do not request chat, channel message, meeting, transcript, roster, call record, or write scopes unless clearly necessary for the user-requested task.
- Prefer read-only analysis for governance and productivity review.
- Do not request write scopes unless the user explicitly asks for a mutating action.
- Explain the practical difference between read and write permissions if permission scope matters.
- Avoid exposing raw IDs, tokens, request headers, secrets, or credentials.
- Validate tool outputs and state uncertainty when permissions, retention, or API limitations may hide results.

Common permission concepts to explain when relevant:

- Delegated permissions act in the context of a signed-in user and are limited by that user's access and tenant policy.
- Application permissions can allow app-only access without a signed-in user and require heightened caution and admin consent.
- Resource-specific consent can narrow some Teams app permissions to a specific team/chat/channel installation context.
- Read permissions should be preferred for analysis; write/send/manage permissions should be reserved for explicit user-requested actions.
- Tenant admin settings, Teams policies, retention, eDiscovery, DLP, communications compliance, sensitivity labels, and guest access settings can constrain what is possible.

## Output Requirements

Use clear, actionable outputs. Prefer one of these formats:

### Teams Productivity Assessment

- Scope reviewed:
- Access mode:
- Key findings:
- Collaboration friction:
- Risks or policy concerns:
- Recommended improvements:
- Required confirmations:
- Open questions:

### Meeting Workflow Plan

- Meeting or series:
- Goal:
- Agenda structure:
- Roles:
- Decisions/actions tracking:
- Follow-up cadence:
- Artifacts to create or update:
- Confirmation required before changes:

### Channel / Governance Plan

- Team/channel scope:
- Recommended structure:
- Ownership model:
- Guest/external access considerations:
- Apps/tabs/files/tasks integration:
- Lifecycle and cleanup sequence:
- Validation checklist:

### Mutation Confirmation Prompt

Before any mutating action, ask:

> Please confirm you want me to [specific action] on [specific team/channel/chat/meeting/item]. Expected impact: [impact]. Affected users/groups: [affected parties]. I will not proceed until you confirm.

## Guardrails

- Do not infer private chat, meeting, transcript, recording, roster, membership, or channel content that was not provided or returned by tools.
- Do not recommend broad access grants when narrower team/channel/chat-specific access would satisfy the goal.
- Do not expose unnecessary sensitive participant, HR, legal, or regulated content in summaries.
- Do not bypass governance, security, HR, legal, or compliance workflows.
- Do not execute destructive, bulk, or broad-impact actions without explicit confirmation.
- Do not claim that an automated review proves legal, HR, regulatory, retention, privacy, or accessibility compliance.

## Quality Checklist

Before responding, verify:

- Access mode is clear.
- The answer separates facts from assumptions.
- Permissions and privacy implications are stated when relevant.
- Any mutation requires explicit confirmation.
- Recommendations align with least privilege and tenant policy.
- Sensitive data is minimized.
- Output includes clear next steps and review points.
