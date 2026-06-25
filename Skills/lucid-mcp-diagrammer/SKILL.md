---
name: lucid-mcp-diagrammer
summary: Drive the official Lucid MCP server to search, fetch, create, export, and share Lucid diagrams using the right tool for the job.
description: Use when the user asks to create, find, summarize, export, or share a Lucid document, Lucidchart diagram, Lucidspark board, org chart, mind map, UML sequence diagram, flowchart, BPMN, swim lane, or process map via the Lucid MCP server.
---

# Lucid MCP Diagrammer

## Purpose

Help an AI agent productively use the **official Lucid MCP server** (the OAuth-based Lucid connector enabled by Lucid admins, exposed to Claude, ChatGPT, Microsoft 365 Copilot, and other MCP clients). The skill teaches the agent which Lucid MCP tool to call for each user intent, how to shape the input correctly (especially the Standard Import format, org-chart node lists, mind-map node lists, and PlantUML sequence markup), how to respect Lucid's documented limits, and how to recover when a request does not map cleanly to a supported tool (e.g., Mermaid input).

This skill assumes the Lucid MCP server is already connected to the current agent and the user has authenticated via OAuth.

## When to Use

- The user asks to **find or summarize** a Lucid document, Lucidchart diagram, or Lucidspark board.
- The user asks to **create** a diagram in Lucid: flowchart, process diagram, architecture diagram, BPMN, swim lane, UML class, container, data-backed diagram, org chart, mind map, or UML sequence diagram.
- The user wants to **export** a Lucid page as an image (e.g., to embed in a doc or to let a vision model interpret it).
- The user wants to **share** a Lucid document or **create a share link** with specific permissions.
- The user provides a dataset (CSV, table, spreadsheet, JSON) and asks to turn it into a Lucid diagram.
- The user provides PlantUML, a sequence description, or a list of participants and messages.
- The user references a Lucid document URL or document ID.

## Do Not Use When

- The user wants to create a Mermaid diagram **inside chat** (not in Lucid). The Lucid MCP server does not import Mermaid; use a Mermaid skill instead.
- The user wants to edit shapes inside an existing Lucid document at the canvas level — the current Lucid MCP server creates new documents and surfaces metadata; it does not expose granular shape-by-shape edits.
- The user is on a non-MCP-aware client where the Lucid connector is not registered.

## Inputs to Consider

- User request text and intent (find vs. create vs. export vs. share).
- Attached datasets (CSV, XLSX, JSON, tables) the user wants visualized.
- Existing Lucid document IDs or URLs (the ID is the path segment, often followed by `/edit`).
- PlantUML markup or sequence descriptions.
- Org chart node lists (manager → report relationships).
- Mind map node lists (parent → child relationships).
- Sharing recipients (emails) and desired permission level.

## Available Lucid MCP Tools and When to Use Each

Use this routing table before calling a tool. Tool names in your client may vary slightly (verb-noun vs. snake_case); match by description.

| User intent | Correct tool | Notes |
|---|---|---|
| "Find / search my Lucid docs for X" | **Search Lucid Documents** | Max 200 results, query ≤400 chars. |
| "Summarize / read / what does this Lucid doc say" | **Fetch Lucid Document Content** | Returns full structure (shapes, lines, metadata). |
| "Create a flowchart / process diagram / architecture diagram / BPMN / swim lane / UML class / container / table / data-backed diagram" | **Create Lucid Diagram from Specification** | Uses Lucid's **Standard Import** JSON. See "Standard Import quick spec" below. |
| "Create an org chart" / "Build a reporting structure" | **Create Org Chart in Lucid** | Flat node list with manager-report relationships. Max 1000 nodes. Optional role and image URL per node. Lucidchart only. |
| "Create a mind map" / "Brainstorm topic tree" | **Create Mind Map in Lucid** | Flat node list with parent-child relationships. Max 1000 nodes. Lucidchart and Lucidspark. |
| "Create a UML sequence diagram" / "Show the message flow between A and B" | **Create UML Sequence Diagram in Lucid** | Takes **PlantUML** markup. Supports participant/actor/boundary/control/entity/database, alt/else, loop, opt, par, critical, group, notes. |
| "Export this page as PNG" / "Let me see the image" / "Analyze this diagram visually" | **Export Lucid Document as Image** | Returns base64 PNG. Page index is 1-based for multi-page docs. Pair with the session model's vision to interpret. |
| "Create a share link with X permission" | **Create Lucid Document Share Link** | Roles: view, comment, edit, edit and share. Supports expiration and anonymous-access control. |
| "Share this doc with alice@... and bob@..." | **Share Lucid Document with Collaborators** | Up to 100 emails per call. Roles: view, comment, edit, edit and share. |

## Workflow

1. **Classify intent.** Decide whether the user wants to search, fetch, create (and which creation tool), export, or share. If ambiguous, ask one focused clarifying question before calling a tool.
2. **Pick the most specific tool.** Prefer **Create Org Chart**, **Create Mind Map**, or **Create UML Sequence Diagram** over the generic **Create Diagram from Specification** whenever the intent matches — purpose-built tools produce better layouts and require less spec authoring.
3. **Shape the input.** For generic diagrams, draft a Standard Import JSON object (see quick spec). For org charts and mind maps, build the flat node list. For sequence diagrams, write PlantUML markup. For searches, keep the query ≤400 chars and choose specific keywords.
4. **Confirm destructive or wide-blast-radius actions before calling.** Sharing with collaborators and creating broadly-permissioned share links should be confirmed with the user (recipients, role, expiration) before the tool call.
5. **Call the tool.** Pass the smallest valid payload. Do not invent fields the tool does not document.
6. **Report the result.** Always return the **document title, document ID, and direct URL** for create/search calls. For export, return where the image was saved or display it. For share, return the recipients, role, and link.
7. **Handle failure or unsupported inputs.** If the user provides Mermaid, convert to Standard Import or PlantUML sequence markup and proceed, telling the user what you converted. If the request exceeds limits (e.g., 1500 org-chart nodes), split or trim and explain.

## Standard Import Quick Spec (for Create Diagram from Specification)

The **Standard Import** format is Lucid's JSON shape for declarative diagram creation. Key fields:

- `title` — the document title.
- `product` — `"lucidchart"` or `"lucidspark"`.
- `pages` — array of page objects, each with `id`, `title`, `shapes`, `lines`, optional `groups`, `layers`, `containers`, `swimLanes`, `tables`.
- `shapes` — each shape has `id`, `type` (e.g., `rectangle`, `ellipse`, `diamond`, `cylinder`, `bpmn_*`, `uml_class`), `boundingBox` (`{x, y, w, h}`), and optional `text`, `style`, `data`.
- `lines` — each line connects two shape `id`s with `endpoint1` and `endpoint2`, optional `text`, `style`, `lineType` (`straight`, `elbow`, `curved`).
- `autoLayout` — set to `true` to let Lucid place shapes; recommended unless coordinates are deliberate.

Minimal viable Standard Import payload for a 3-node flow:

```json
{
  "title": "Customer Refund Process",
  "product": "lucidchart",
  "autoLayout": true,
  "pages": [{
    "id": "p1",
    "title": "Flow",
    "shapes": [
      {"id": "s1", "type": "rectangle", "text": "Customer submits refund"},
      {"id": "s2", "type": "diamond",   "text": "Eligible?"},
      {"id": "s3", "type": "rectangle", "text": "Issue refund"}
    ],
    "lines": [
      {"endpoint1": {"shapeId": "s1"}, "endpoint2": {"shapeId": "s2"}},
      {"endpoint1": {"shapeId": "s2"}, "endpoint2": {"shapeId": "s3"}, "text": "Yes"}
    ]
  }]
}
```

Authoring rules:

- Set `autoLayout: true` unless the user explicitly specifies coordinates.
- Use stable `id` values (`s1`, `s2`, ...) and reference them consistently in `lines`.
- For BPMN, use `bpmn_*` shape types (e.g., `bpmn_task`, `bpmn_gateway_exclusive`, `bpmn_event_start`).
- For swim lanes, declare a `swimLanes` array on the page with `lanes` and place shapes via `laneId`.
- For data-backed diagrams (tables), attach `data` rows to shapes — useful for architecture inventories.
- Keep one logical diagram per page; create additional pages for sub-flows.

Optional helper: `scripts/standard_import_scaffold.py` (in this skill folder) builds a valid Standard Import payload from a flat nodes/edges list. Use it when you have a clean source dataset and want to avoid hand-authoring JSON.

## Org Chart Input Shape (for Create Org Chart)

Flat list of nodes, each with:

- `id` — unique identifier (e.g., employee ID or email).
- `name` — display name.
- `role` *(optional)* — title shown under the name.
- `managerId` *(optional)* — `id` of the manager. Root nodes omit this.
- `imageUrl` *(optional)* — public URL to a headshot.

Limits: up to 1000 nodes per call. Lucidchart product only. If the user has >1000 employees, split by org unit and create multiple documents.

## Mind Map Input Shape (for Create Mind Map)

Flat list of nodes, each with:

- `id` — unique identifier.
- `text` — node label.
- `parentId` *(optional)* — `id` of the parent node. Root node omits this.

Limits: up to 1000 nodes. Works in Lucidchart and Lucidspark; ask the user which product they prefer if unclear.

## PlantUML Sequence Markup (for Create UML Sequence Diagram)

The Create UML Sequence Diagram tool accepts standard PlantUML between `@startuml` and `@enduml`. Supported elements:

- Participant kinds: `participant`, `actor`, `boundary`, `control`, `entity`, `database`.
- Arrow styles: `->` (sync), `-->` (reply/dashed), `->>` (async).
- Groups: `alt`/`else`/`end`, `loop`/`end`, `opt`/`end`, `par`/`end`, `critical`/`end`, `group`/`end`.
- Notes: `note over`, `note left of`, `note right of`.

Minimal example:

```
@startuml
actor User
participant "Web App" as App
database DB
User -> App : Submit form
App -> DB : INSERT row
DB --> App : OK
App --> User : Confirmation
@enduml
```

Optional helper: `scripts/plantuml_sequence_builder.py` (in this skill folder) generates PlantUML markup from a participants/messages list.

## Mermaid Fallback Protocol

The Lucid MCP server does not import Mermaid. If the user provides Mermaid:

- **Mermaid `flowchart` / `graph`** → translate nodes and edges into a Standard Import payload and call **Create Diagram from Specification**.
- **Mermaid `sequenceDiagram`** → translate into PlantUML markup and call **Create UML Sequence Diagram**.
- **Mermaid `mindmap`** → translate into the mind-map flat node list and call **Create Mind Map**.
- **Mermaid `classDiagram`** → translate into Standard Import with `uml_class` shapes.

Always tell the user you converted from Mermaid and offer to share the converted payload for review.

## Export-and-Read Protocol

When the user asks the agent to "read," "summarize," or "analyze" an existing Lucid document:

1. **Try Fetch first.** Call **Fetch Lucid Document Content** — it returns structured shapes, lines, and text and is cheaper than vision.
2. **Fall back to Export-as-Image** when Fetch returns mostly empty content (image-heavy diagrams, embedded sketches) or when the user explicitly asks for a visual interpretation.
3. Pass the exported base64 PNG to the session model's vision pathway and summarize what it shows.
4. Always cite the page index and the document URL in the summary.

## Sharing Guardrails

- Confirm recipients, role, and expiration **before** calling **Share Lucid Document with Collaborators** or **Create Lucid Document Share Link**.
- Default to the least-privileged role that satisfies the request (prefer `view` over `comment` over `edit`).
- Warn the user before creating an anonymous (link-anyone) share link, and prefer an expiration date.
- Never share documents whose contents you have not verified are appropriate for the requested audience.

## Rate Limits and Defensive Behavior

- Throttle: ~100 tool calls per 60 seconds across all Lucid MCP tools. Batch related operations and avoid tight loops.
- Search: ≤200 results, ≤400-char queries. If the user query is broader, narrow it with the user before calling.
- Org chart / mind map: ≤1000 nodes per document.
- Share collaborators: ≤100 emails per call.
- Document IDs are stable — cache them in the conversation when working with the same document across turns.

## Output Format

For every successful Lucid MCP action, return:

- **What you did** in one sentence ("Created a Lucidchart flowchart titled 'Customer Refund Process'.").
- **Document title**, **document ID**, and **direct URL** (for create/search/fetch).
- **Any conversions** you applied (e.g., "Converted your Mermaid `flowchart` to Standard Import").
- **Next-step suggestions** when relevant ("Want me to add a swim lane for Finance?").

For exports, embed or describe the image and cite the page index.

For failures, return the failed tool name, the input you sent (redacted as needed), and a clear next step.

## Examples

**Example 1 — generic flowchart from a dataset**

User: "Here's our refund process steps as a CSV. Make it a Lucid flowchart."
Assistant: Build a Standard Import JSON with rectangles for steps and diamonds for decisions, `autoLayout: true`, and call **Create Diagram from Specification**. Return title, ID, URL.

**Example 2 — org chart**

User: "Build an org chart for my engineering team from this spreadsheet."
Assistant: Parse the spreadsheet into the org-chart node list with `id`, `name`, `role`, `managerId`. Call **Create Org Chart in Lucid**. Return URL and confirm node count.

**Example 3 — Mermaid sequence diagram**

User pastes a Mermaid `sequenceDiagram`.
Assistant: Translate to PlantUML markup, call **Create UML Sequence Diagram in Lucid**, and tell the user the conversion was applied. Return URL.

**Example 4 — read an existing diagram**

User: "What does this Lucid doc show? <URL>"
Assistant: Extract the document ID from the URL. Call **Fetch Lucid Document Content** first. If shapes/text are sparse, fall back to **Export Lucid Document as Image** and pass through vision. Summarize with page citations.

**Example 5 — share with confirmation**

User: "Share that doc with my team."
Assistant: Ask for the specific emails, the role, and whether a share link or per-user invite is preferred. Then call **Share Lucid Document with Collaborators** with role defaulting to `view`.

**Example 6 — out of scope**

User: "Move the 'Approve' shape 100 pixels to the right."
Assistant: Explain that the Lucid MCP server creates new documents but does not expose granular shape edits. Offer to regenerate the page with the new layout instead.
