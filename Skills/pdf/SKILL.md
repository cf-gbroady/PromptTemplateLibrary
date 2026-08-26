---
name: pdf
summary: Inspect, extract, create, edit, validate, and assess PDF files.
description: Use when the user asks to inspect, summarize, extract, split, merge, crop, watermark, create, validate, or assess accessibility of a PDF, including PDF text, tables, forms, metadata, page-level content, scans, or OCR needs.
---

# PDF Skill

## Purpose

Work with PDF files safely and transparently: inspect structure, extract text and tables, split or merge pages, create reports, and identify accessibility or source-quality limitations.

## When to use

Use this skill to inspect, summarize, extract, split, merge, rotate, crop, watermark, create, validate, or assess a PDF. Use it when the user needs text, tables, form fields, metadata, links, outlines, page-level information, scan/OCR triage, or accessibility guidance.

## Runtime model

This skill is self-contained: its required instructions and minimal Python patterns are in this file. Do not depend on a repository `.py` helper being mounted, downloadable, or importable in Code Interpreter. The companion reference at `Skills/pdf/references/code_snippets.md` supports repository readers and public browsing; it is not a runtime dependency.

## Required behavior

1. Inspect before acting. Identify page count, encryption, metadata, text extractability, image-heavy/scanned characteristics, tables, and OCR need.
2. Preserve source PDFs. Create a new versioned output file for every edit.
3. Use `pypdf` for splitting, merging, page manipulation, metadata, outlines, encryption checks, and basic extraction. Use `pdfplumber` for layout-aware text/table extraction and page-object inspection when it is available.
4. Cite page numbers or page ranges when reporting extracted or summarized content.
5. Re-open every generated PDF and report its page count plus validation performed.
6. State extraction, OCR, encryption, and accessibility limitations precisely. Automated checks can identify likely issues; they do not certify PDF/UA or WCAG compliance.

## Workflow

1. Profile the PDF with the inline inspection pattern below.
2. Choose the narrowest suitable operation and library.
3. For scans or image-only documents, determine whether OCR is available before claiming searchable text.
4. Write to a new versioned output path.
5. Re-open the output and verify the intended pages, page count, and basic readability.
6. Report inputs, outputs, pages processed, tool/library, validation, and limitations.

## Inline Python patterns

### Compact inspection profile

~~~python
from pathlib import Path
from pypdf import PdfReader

path = Path("/mnt/data/input.pdf")
reader = PdfReader(path)
profile = {
    "path": str(path),
    "pages": len(reader.pages),
    "encrypted": reader.is_encrypted,
    "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
}
if reader.is_encrypted:
    print(profile)
    raise PermissionError("PDF is encrypted; request an authorized password before extraction or editing.")

sample = []
for page_number, page in enumerate(reader.pages[:3], start=1):
    text = page.extract_text() or ""
    sample.append({"page": page_number, "characters": len(text), "preview": text[:300]})
profile["text_sample"] = sample
profile["likely_image_only"] = bool(reader.pages) and all(item["characters"] == 0 for item in sample)
print(profile)
~~~

A zero-text sample is a triage signal, not proof that every page requires OCR. Inspect representative pages visually or with `pdfplumber` where available.

### Extract text with page citations

~~~python
from pypdf import PdfReader

reader = PdfReader("/mnt/data/input.pdf")
for page_number, page in enumerate(reader.pages, start=1):
    text = (page.extract_text() or "").strip()
    if text:
        print(f"[Page {page_number}]\n{text}\n")
~~~

### Split a selected page range without overwriting the original

~~~python
from pypdf import PdfReader, PdfWriter

source = "/mnt/data/input.pdf"
output = "/mnt/data/input_v2_pages_3_to_5.pdf"
start_page, end_page = 3, 5  # human page numbers, inclusive
reader = PdfReader(source)
writer = PdfWriter()
for index in range(start_page - 1, end_page):
    writer.add_page(reader.pages[index])
with open(output, "wb") as stream:
    writer.write(stream)

check = PdfReader(output)
assert len(check.pages) == end_page - start_page + 1
print(f"Created {output} with {len(check.pages)} pages")
~~~

### Layout-aware table/text extraction when available

~~~python
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

if pdfplumber is None:
    print("pdfplumber is unavailable; use pypdf text extraction and state the table-fidelity limitation.")
else:
    with pdfplumber.open("/mnt/data/input.pdf") as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            print({"page": page_number, "tables_found": len(tables)})
~~~

## Output requirements

Report the input and output paths, page count and range processed, library or tool used, validation performed, and limitations involving extraction order, tables, OCR, passwords, or accessibility.

## Guardrails

- Do not overwrite source PDFs.
- Do not send PDF contents to an external service unless the user expressly authorizes it and the environment permits it.
- Treat PDF text order and table reconstruction as layout-sensitive; verify against page images when accuracy matters.
- For accessibility requests, distinguish an automated review from human accessibility remediation and conformance validation.

## Failure handling

If the PDF is encrypted, request an authorized password or a decrypted copy. If OCR tooling is unavailable for a scan, explain that limitation and provide the options available in the current environment. Ask a focused question before applying a destructive-looking page operation when the requested pages or output naming is ambiguous.
