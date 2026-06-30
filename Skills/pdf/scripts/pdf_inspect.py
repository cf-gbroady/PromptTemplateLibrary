#!/usr/bin/env python3
"""Inspect a PDF and emit a compact JSON profile.

The helper prefers pypdf when installed and degrades gracefully when optional PDF
libraries are unavailable. It never sends file contents to a network service.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def inspect_with_pypdf(path: Path, max_pages: int, extract_text: bool) -> dict[str, Any]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(path), strict=False)
    encrypted = bool(getattr(reader, "is_encrypted", False))
    result: dict[str, Any] = {
        "file": str(path),
        "library": "pypdf",
        "page_count": len(reader.pages),
        "encrypted": encrypted,
        "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
        "outline_count": 0,
        "pages": [],
        "warnings": [],
    }

    try:
        outline = getattr(reader, "outline", [])
        result["outline_count"] = len(outline) if isinstance(outline, list) else 0
    except Exception:
        result["warnings"].append("Unable to inspect outline/bookmarks.")

    if encrypted:
        result["warnings"].append("PDF is encrypted; extraction may require a password.")
        return result

    limit = min(max_pages, len(reader.pages))
    for page_index in range(limit):
        page = reader.pages[page_index]
        page_info: dict[str, Any] = {
            "page_number": page_index + 1,
            "mediabox": [float(x) for x in page.mediabox],
            "rotation": int(page.get("/Rotate", 0) or 0),
        }
        if extract_text:
            try:
                text = page.extract_text() or ""
                page_info["text_chars"] = len(text)
                page_info["text_preview"] = text[:500]
            except Exception as exc:  # noqa: BLE001
                page_info["text_error"] = str(exc)
        result["pages"].append(page_info)

    if len(reader.pages) > max_pages:
        result["warnings"].append(f"Only first {max_pages} pages inspected; rerun with --max-pages for more.")
    return result


def inspect_with_pdfplumber(path: Path, max_pages: int, extract_text: bool) -> dict[str, Any]:
    import pdfplumber  # type: ignore

    with pdfplumber.open(str(path)) as pdf:
        result: dict[str, Any] = {
            "file": str(path),
            "library": "pdfplumber",
            "page_count": len(pdf.pages),
            "metadata": dict(pdf.metadata or {}),
            "pages": [],
            "warnings": [],
        }
        for page in pdf.pages[:max_pages]:
            page_info: dict[str, Any] = {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "char_count": len(page.chars),
                "image_count": len(page.images),
                "line_count": len(page.lines),
                "rect_count": len(page.rects),
            }
            if extract_text:
                text = page.extract_text() or ""
                page_info["text_chars"] = len(text)
                page_info["text_preview"] = text[:500]
            try:
                page_info["table_count"] = len(page.find_tables())
            except Exception:
                page_info["table_count"] = None
            result["pages"].append(page_info)
        if len(pdf.pages) > max_pages:
            result["warnings"].append(f"Only first {max_pages} pages inspected; rerun with --max-pages for more.")
        return result


def inspect_pdf(path: Path, max_pages: int, extract_text: bool, prefer: str) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".pdf":
        raise ValueError("Expected a .pdf file")

    if prefer == "pdfplumber":
        attempts = ["pdfplumber", "pypdf"]
    elif prefer == "pypdf":
        attempts = ["pypdf", "pdfplumber"]
    else:
        attempts = ["pypdf", "pdfplumber"]

    errors: dict[str, str] = {}
    for lib in attempts:
        try:
            if lib == "pypdf":
                return inspect_with_pypdf(path, max_pages, extract_text)
            return inspect_with_pdfplumber(path, max_pages, extract_text)
        except ModuleNotFoundError as exc:
            errors[lib] = f"not installed: {exc.name}"
        except Exception as exc:  # noqa: BLE001
            errors[lib] = str(exc)

    return {
        "file": str(path),
        "error": "No supported PDF library succeeded.",
        "attempts": errors,
        "install_hint": "Install pypdf for splitting/merging/metadata, or pdfplumber for extraction/table/layout analysis.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a PDF and emit JSON metadata.")
    parser.add_argument("pdf", type=Path, help="Path to .pdf file")
    parser.add_argument("--out", type=Path, help="Optional JSON output path")
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum pages to inspect")
    parser.add_argument("--extract-text", action="store_true", help="Include short text previews")
    parser.add_argument("--prefer", choices=["pypdf", "pdfplumber", "auto"], default="auto")
    args = parser.parse_args()

    try:
        result = inspect_pdf(args.pdf, max(1, args.max_pages), args.extract_text, args.prefer)
    except Exception as exc:  # noqa: BLE001 - CLI should return clear JSON on failure
        result = {"file": str(args.pdf), "error": str(exc)}
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if "error" not in result else 2


if __name__ == "__main__":
    raise SystemExit(main())
