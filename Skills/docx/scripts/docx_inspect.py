#!/usr/bin/env python3
"""Inspect a .docx package and emit a compact JSON profile.

This helper intentionally uses only the Python standard library so it works in
restricted Code Interpreter environments. It does not edit documents.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def parse_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML in {name}: {exc}") from exc


def text_of(el: ET.Element) -> str:
    return "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip()


def style_of(paragraph: ET.Element) -> str | None:
    val = paragraph.find("./w:pPr/w:pStyle", NS)
    return val.get(f"{{{NS['w']}}}val") if val is not None else None


def heading_level(style: str | None) -> int | None:
    if not style:
        return None
    match = re.search(r"Heading\s*([1-9])|Heading([1-9])", style, re.I)
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def rels_by_id(root: ET.Element | None) -> dict[str, dict[str, str]]:
    if root is None:
        return {}
    out: dict[str, dict[str, str]] = {}
    for rel in root.findall(".//rel:Relationship", NS):
        rel_id = rel.get("Id")
        if rel_id:
            out[rel_id] = {
                "type": rel.get("Type", ""),
                "target": rel.get("Target", ""),
                "mode": rel.get("TargetMode", ""),
            }
    return out


def core_properties(zf: zipfile.ZipFile) -> dict[str, str]:
    root = parse_xml(zf, "docProps/core.xml")
    if root is None:
        return {}
    props: dict[str, str] = {}
    for child in root:
        tag = child.tag.split("}", 1)[-1]
        props[tag] = child.text or ""
    return props


def quality_warnings(headings: list[dict[str, Any]], paragraph_count: int, table_count: int, image_count: int) -> list[str]:
    warnings: list[str] = []
    if paragraph_count and not headings:
        warnings.append("No styled headings detected; use Word heading styles for navigability.")
    previous = 0
    for heading in headings:
        level = int(heading["level"])
        if previous and level > previous + 1:
            warnings.append(f"Heading level jumps from H{previous} to H{level} near: {heading['text']!r}")
        previous = level
    if table_count:
        warnings.append("Tables detected; verify header rows and accessibility semantics in Word.")
    if image_count:
        warnings.append("Images detected; verify alt text in the source document.")
    return warnings


def inspect_docx(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".docx":
        raise ValueError("Expected a .docx file")

    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        document = parse_xml(zf, "word/document.xml")
        rels = rels_by_id(parse_xml(zf, "word/_rels/document.xml.rels"))

        if document is None:
            raise ValueError("word/document.xml not found; this is not a valid .docx package")

        paragraphs = document.findall(".//w:p", NS)
        tables = document.findall(".//w:tbl", NS)
        styles = [style_of(p) for p in paragraphs if style_of(p)]
        style_counts = Counter(styles)

        headings = []
        for idx, p in enumerate(paragraphs, start=1):
            style = style_of(p)
            level = heading_level(style)
            if level is not None:
                headings.append({
                    "paragraph_index": idx,
                    "level": level,
                    "style": style,
                    "text": text_of(p)[:200],
                })

        hyperlink_ids = [
            h.get(f"{{{NS['r']}}}id")
            for h in document.findall(".//w:hyperlink", NS)
            if h.get(f"{{{NS['r']}}}id")
        ]
        hyperlinks = [
            {
                "relationship_id": rid,
                "target": rels.get(rid, {}).get("target", ""),
                "mode": rels.get(rid, {}).get("mode", ""),
            }
            for rid in hyperlink_ids
        ]

        media = sorted(n for n in names if n.startswith("word/media/"))
        comments = parse_xml(zf, "word/comments.xml")
        comment_count = 0 if comments is None else len(comments.findall(".//w:comment", NS))

        return {
            "file": str(path),
            "valid_zip_package": True,
            "paragraph_count": len(paragraphs),
            "table_count": len(tables),
            "heading_count": len(headings),
            "headings": headings[:50],
            "style_counts": dict(style_counts.most_common(30)),
            "image_count": len(media),
            "media_files": media[:50],
            "hyperlink_count": len(hyperlinks),
            "hyperlinks": hyperlinks[:50],
            "comment_count": comment_count,
            "core_properties": core_properties(zf),
            "has_numbering": "word/numbering.xml" in names,
            "has_styles": "word/styles.xml" in names,
            "has_comments": "word/comments.xml" in names,
            "warnings": quality_warnings(headings, len(paragraphs), len(tables), len(media)),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a DOCX file and emit JSON metadata.")
    parser.add_argument("docx", type=Path, help="Path to .docx file")
    parser.add_argument("--out", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    try:
        result = inspect_docx(args.docx)
    except Exception as exc:  # noqa: BLE001 - CLI should return clear JSON on failure
        result = {"file": str(args.docx), "error": str(exc)}
        text = json.dumps(result, indent=2, ensure_ascii=False)
        if args.out:
            args.out.write_text(text + "\n", encoding="utf-8")
        print(text)
        return 2

    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
