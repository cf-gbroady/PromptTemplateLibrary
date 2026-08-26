# PDF Inspection Helper Patterns

This Markdown reference replaces the runtime assumption that `pdf_inspect.py` can be downloaded or imported. Copy only the relevant Python block into the active Code Interpreter session. The authoritative operating rules are in [`../SKILL.md`](../SKILL.md).

## Inspect a PDF

```python
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
    raise PermissionError("PDF is encrypted; request an authorized password before proceeding.")

samples = []
for page_number, page in enumerate(reader.pages[:3], start=1):
    text = page.extract_text() or ""
    samples.append({"page": page_number, "characters": len(text), "preview": text[:300]})
profile["text_sample"] = samples
profile["likely_image_only"] = bool(reader.pages) and all(s["characters"] == 0 for s in samples)
print(profile)
```

## Extract text with page labels

```python
from pypdf import PdfReader

for page_number, page in enumerate(PdfReader("/mnt/data/input.pdf").pages, start=1):
    text = (page.extract_text() or "").strip()
    if text:
        print(f"[Page {page_number}]\n{text}\n")
```

## Validate a generated PDF

```python
from pypdf import PdfReader

output = "/mnt/data/output.pdf"
reader = PdfReader(output)
assert not reader.is_encrypted
assert len(reader.pages) > 0
print(f"Validated {output}: {len(reader.pages)} pages")
```

A zero-text sample is a triage signal, not conclusive evidence that the full file needs OCR. For table or layout-sensitive extraction, use `pdfplumber` if it is available and describe any remaining fidelity limitation.