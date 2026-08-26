# XLSX Helper Patterns

This Markdown reference replaces the runtime assumption that `xlsx_tools.py` can be downloaded or imported. Copy only the relevant Python block into the active Code Interpreter session. The authoritative operating rules are in [`../SKILL.md`](../SKILL.md).

## Inspect structure

```python
from openpyxl import load_workbook

input_path = "/mnt/data/input.xlsx"
wb = load_workbook(input_path, data_only=False)
for ws in wb.worksheets:
    print({"sheet": ws.title, "rows": ws.max_row, "columns": ws.max_column, "state": ws.sheet_state})
```

## Recalculate, when LibreOffice is available

```python
from pathlib import Path
import shutil
import subprocess

source = Path("/mnt/data/output.xlsx")
recalc_dir = Path("/mnt/data/recalculated")
recalc_dir.mkdir(exist_ok=True)
soffice = shutil.which("soffice") or shutil.which("libreoffice")
if not soffice:
    raise RuntimeError("LibreOffice is unavailable; disclose that Excel should recalculate on open.")

subprocess.run(
    [soffice, "--headless", "--convert-to", "xlsx", "--outdir", str(recalc_dir), str(source)],
    check=True,
    capture_output=True,
    text=True,
)
recalculated = recalc_dir / source.name
if not recalculated.exists():
    raise FileNotFoundError(f"Expected recalculated workbook at {recalculated}")
print(recalculated)
```

## Validate cached formula errors

```python
from openpyxl import load_workbook

ERRORS = {"#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NUM!", "#NULL!"}

def find_formula_errors(path):
    wb = load_workbook(path, data_only=True, read_only=True)
    return [
        f"{ws.title}!{cell.coordinate}: {cell.value}"
        for ws in wb.worksheets
        for row in ws.iter_rows()
        for cell in row
        if cell.value in ERRORS
    ]

errors = find_formula_errors("/mnt/data/recalculated/output.xlsx")
if errors:
    raise ValueError("Blocking formula errors found:\n" + "\n".join(errors))
print("Validation passed: no blocking cached formula errors found.")
```

Do not save a workbook loaded with `data_only=True`; it reads cached values and does not preserve formula logic.