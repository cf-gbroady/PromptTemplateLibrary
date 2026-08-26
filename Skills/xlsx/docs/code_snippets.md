# XLSX Code Snippets

These are copy-and-run Python patterns for environments where Code Interpreter cannot download or import repository helper files. The `xlsx` skill contains the mandatory runtime guidance; this document is supplementary reference material for repository readers.

## Inspect workbook structure

```python
from openpyxl import load_workbook

wb = load_workbook("/mnt/data/input.xlsx", data_only=False)
for ws in wb.worksheets:
    print(ws.title, ws.max_row, ws.max_column, ws.sheet_state)
```

## Check cached formula errors

```python
from openpyxl import load_workbook

errors = {"#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NUM!", "#NULL!"}
wb = load_workbook("/mnt/data/output.xlsx", data_only=True, read_only=True)
hits = [
    f"{ws.title}!{cell.coordinate}: {cell.value}"
    for ws in wb.worksheets
    for row in ws.iter_rows()
    for cell in row
    if cell.value in errors
]
print("No blocking errors" if not hits else "\n".join(hits))
```

Use LibreOffice headless recalculation before this check when it is available. When it is not available, disclose that cached results may be stale and Excel should recalculate on open.
