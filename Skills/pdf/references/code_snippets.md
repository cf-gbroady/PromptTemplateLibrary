# PDF Code Snippets

These copy-and-run Python patterns are intended for environments where Code Interpreter cannot access repository helper files. Mandatory runtime behavior is duplicated in the `pdf` skill; this page is supplementary reference material.

## Profile a PDF

```python
from pypdf import PdfReader

reader = PdfReader("/mnt/data/input.pdf")
print({"pages": len(reader.pages), "encrypted": reader.is_encrypted})
for number, page in enumerate(reader.pages[:3], start=1):
    print(number, len(page.extract_text() or ""))
```

## Extract with page labels

```python
from pypdf import PdfReader

for page_number, page in enumerate(PdfReader("/mnt/data/input.pdf").pages, start=1):
    print(f"[Page {page_number}]\n{page.extract_text() or ''}")
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

For layout-sensitive table extraction, use `pdfplumber` if it is installed; otherwise describe the limitation rather than claiming table fidelity.
