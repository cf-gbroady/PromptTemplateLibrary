# DOCX Workflows

## New Document Workflow

1. Confirm the requested document type, audience, required sections, tone, and output filename.
2. Create a structured outline before generating content.
3. Use semantic Word structures:
   - Title for document title.
   - Heading 1/2/3 styles for hierarchy.
   - Built-in list styles for ordered and unordered lists.
   - Real Word tables for tabular data.
4. Set core properties when useful: title, subject, author/department, category, keywords, comments, and language when supported.
5. Add images only when the user provided or requested them. Preserve aspect ratio.
6. Save to a new file path.
7. Re-open or inspect the output and report validation.

## Existing Document Edit Workflow

1. Preserve the original file. Create a versioned output filename.
2. Run `scripts/docx_inspect.py input.docx --out profile.json`.
3. Read the profile:
   - heading levels and skipped heading levels,
   - paragraph/table/image counts,
   - hyperlinks and comments,
   - core properties,
   - package warnings.
4. Make the smallest edit that satisfies the request.
5. Re-open the edited document and compare high-level structure with the original.
6. Report what changed and what was intentionally preserved.

## Inspection and Extraction

Use inspection for questions like “what is in this document,” “extract the tables,” or “check the metadata.”

Recommended checks:
- Paragraph and heading counts.
- Heading hierarchy.
- Tables and likely table-header needs.
- Images and likely alt-text needs.
- Hyperlinks and external targets.
- Comments.
- Core properties.
- Presence of numbering and styles parts.

When extracting content, preserve order where possible. If tables and paragraphs must remain interleaved, inspect `word/document.xml` document order instead of relying only on `document.paragraphs` and `document.tables`.

## OOXML Fallbacks

Use direct OpenXML package access only when normal libraries are insufficient or unavailable:
- `.docx` files are ZIP packages.
- Main text lives in `word/document.xml`.
- Relationships live in `word/_rels/document.xml.rels`.
- Styles live in `word/styles.xml`.
- Numbering lives in `word/numbering.xml`.
- Core properties live in `docProps/core.xml`.

Fallback rules:
- Treat direct XML editing as higher risk than `python-docx`.
- Edit only known, narrow structures.
- Validate the ZIP package and XML parseability after changes.
- Prefer read-only inspection for complex features such as tracked changes, content controls, macros, embedded OLE objects, SmartArt, or custom XML.

## Common Task Patterns

### Add or Update Metadata

Use `doc.core_properties` when `python-docx` is available. Keep metadata professional and minimal. Avoid adding sensitive or private information.

### Add Comments

Use supported comment APIs when available. Anchor comments to real runs of text. If comments cannot be created reliably in the runtime, provide a reviewer note instead of pretending comments were inserted.

### Tables

Use real Word tables. For accessibility and readability:
- Keep tables simple.
- Include a clear header row.
- Avoid merged cells unless necessary.
- Add a short caption or lead-in sentence for complex tables.

### Images

Preserve aspect ratio. Verify file exists before insertion. Provide alt text guidance in the response if the runtime cannot set image alt text reliably.

### Versioned Outputs

If editing `report.docx`, use `report_v2.docx` unless the user requested a different filename. If the file already ends in `_vN`, increment N.
