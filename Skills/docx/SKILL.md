---
name: docx
summary: Create, edit, inspect, and quality-check Microsoft Word DOCX documents.
description: Use when creating, editing, inspecting, extracting, or quality-checking Microsoft Word .docx files, including reports, styled documents, tables, images, metadata, accessibility, and document automation.
---

# DOCX Skill

## Purpose

Create, edit, inspect, and quality-check Microsoft Word `.docx` files with reliable workflows, source-safe file handling, and accessibility-aware output.

## When to Use

Use this skill when the user asks to:
- Create or update a `.docx` file.
- Convert structured content into a Word report, memo, proposal, agenda, SOP, or brief.
- Inspect a Word document for text, headings, tables, images, comments, links, styles, or metadata.
- Apply formatting, page structure, sections, headers/footers, tables, images, comments, or core properties.
- Make a Word document more accessible or easier to navigate.

Do not use this skill for spreadsheets, slide decks, PDFs, or image-only documents unless the DOCX is the requested source or output. For PDF-specific work, use the `pdf` skill.

## Required Runtime Behavior

1. **Preserve originals.** Never overwrite an uploaded or repository source document. Create a new output file with a version suffix or a clearly distinct output path.
2. **Inspect before editing.** For existing documents, inspect structure first: headings, sections, tables, images, links, comments, and metadata.
3. **Choose the safest implementation.**
   - Use `python-docx` when available for normal creation/editing, paragraphs, tables, images, comments, and core properties.
   - Use direct OOXML package inspection only for read-only structure checks or features not exposed by `python-docx`.
   - Do not fake track changes, comments, alt text, accessibility tags, or metadata. State what was actually changed and what needs manual verification.
4. **Validate after editing.** Re-open the generated `.docx` when possible and confirm it is a valid ZIP/OpenXML package.
5. **Report clearly.** Summarize changed sections, generated file path, validation performed, and any limitations.

## Quick Start

For a read-only profile of a DOCX package, run:

```bash
python Skills/docx/scripts/docx_inspect.py input.docx --out docx_profile.json
```

Use the JSON output to decide whether the task needs creation, light editing, metadata cleanup, accessibility remediation, or manual Word review.

## Workflow Router

- **Create a new DOCX:** read `references/docx_workflows.md#new-document-workflow`.
- **Edit an existing DOCX:** read `references/docx_workflows.md#existing-document-edit-workflow`.
- **Inspect or extract:** run `scripts/docx_inspect.py`, then read `references/docx_workflows.md#inspection-and-extraction`.
- **Accessibility or quality review:** read `references/accessibility_quality.md`.
- **Advanced OOXML edge cases:** read `references/docx_workflows.md#ooxml-fallbacks`.

Keep references one level deep from this `SKILL.md`; do not add nested reference chains.

## Tool and Library Guidance

Preferred Python libraries:
- `python-docx` for Word creation and standard editing.
- Python standard library `zipfile` and `xml.etree.ElementTree` for read-only package inspection.
- `Pillow` only when image sizing or metadata inspection is needed and available.

If a dependency is unavailable, explain the limitation and provide the best available fallback. Do not attempt network installation unless the runtime explicitly allows it.

## Output Requirements

When producing a DOCX deliverable:
- Provide the output file path.
- State whether the file was created new or based on an existing document.
- State validation performed, such as “opened as DOCX package,” “reopened with python-docx,” or “inspected headings/tables/images.”
- Mention remaining manual checks, especially accessibility, alt text, complex tables, macros, or tracked changes.

## Guardrails

- Do not include secrets, hidden credentials, private keys, or unrelated personal data in document properties.
- Avoid destructive edits to source files.
- Do not claim full accessibility compliance from automated checks alone.
- Do not modify macros or embedded OLE objects unless explicitly requested and technically supported.
- Use forward-slash paths in examples and references.
