# PDF Workflows

## Inspection and Triage

1. Confirm the user’s goal: summarize, extract, manipulate, create, or remediate.
2. Run `scripts/pdf_inspect.py input.pdf --extract-text --out profile.json`.
3. Review:
   - page count,
   - encryption/password status,
   - metadata,
   - outline/bookmark count,
   - text availability by page,
   - image/table indicators if `pdfplumber` is available.
4. Classify the PDF:
   - **digital text PDF**: text extraction should work.
   - **scanned/image PDF**: OCR is needed.
   - **hybrid PDF**: extract text where possible; OCR image-only pages if required.
   - **form PDF**: inspect fields separately if needed.
   - **complex layout PDF**: use layout-aware extraction and verify manually.

## Extraction Workflow

For text:
1. Prefer `pdfplumber` for layout-sensitive extraction from machine-generated PDFs.
2. Use `pypdf` for quick text extraction or when page operations are already needed.
3. Preserve page numbers in extracted output.
4. For summaries, cite page ranges or page numbers.
5. If extraction quality is poor, inspect page images or request OCR.

For tables:
1. Use `pdfplumber` table extraction first.
2. Crop to table regions when needed.
3. Try both line-based and text-based strategies for difficult tables.
4. Validate row/column alignment before using extracted values in analysis.
5. Export tables to CSV/XLSX only after checking obvious header and row alignment issues.

## Page Operations

Use `pypdf` for:
- split by page range,
- merge multiple PDFs,
- rotate pages,
- crop pages,
- add metadata,
- inspect encryption,
- add watermarks/stamps when supported.

Always:
- write a new output file,
- preserve source page order unless requested otherwise,
- re-open the generated PDF,
- report output page count.

## PDF Creation

When creating a PDF from scratch:
1. Prefer generating from a structured source such as HTML, Markdown, DOCX, or report content.
2. Use semantic source structure before export: headings, lists, tables, captions, alt text guidance.
3. If the output must be accessible, fix structure in the source document before PDF export whenever possible.
4. Validate the generated file by opening/reading page count.

## Forms

PDF forms may store values separately from visible page text. If the user asks about form fields:
- inspect AcroForm fields when the library supports it,
- report field names and current values separately from visible text,
- avoid flattening or filling forms unless the user explicitly requests it,
- keep a copy of the unmodified source.

## OCR Escalation

Escalate to OCR when:
- text extraction returns little or no text,
- pages are image-heavy scans,
- the user needs searchable text from scanned pages.

Report OCR limitations:
- handwriting, low resolution, skew, and complex forms can reduce accuracy,
- OCR output requires manual verification for legal, financial, medical, or compliance use.
