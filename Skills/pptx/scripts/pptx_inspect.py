#!/usr/bin/env python3
"""Inspect a PowerPoint .pptx package and report structure, text, media, and warnings.

This script is read-only and uses only Python's standard library. It is intended as
an efficient first pass before creating, editing, extracting, or accessibility-checking
PowerPoint files.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
}


def _xml_from_zip(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except Exception:
        return None


def _slide_sort_key(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 10**9


def _text_from_tree(root: ET.Element) -> list[str]:
    out: list[str] = []
    for node in root.findall(".//a:t", NS):
        if node.text and node.text.strip():
            out.append(node.text.strip())
    return out


def _shape_info(root: ET.Element) -> list[dict[str, Any]]:
    shapes: list[dict[str, Any]] = []
    for c_nv_pr in root.findall(".//p:cNvPr", NS):
        name = c_nv_pr.attrib.get("name", "")
        descr = c_nv_pr.attrib.get("descr", "")
        title = c_nv_pr.attrib.get("title", "")
        shapes.append({"name": name, "alt_text": descr or title})
    return shapes


def _core_properties(zf: zipfile.ZipFile) -> dict[str, str]:
    root = _xml_from_zip(zf, "docProps/core.xml")
    if root is None:
        return {}
    props: dict[str, str] = {}
    for key, path in {
        "title": "dc:title",
        "subject": "dc:subject",
        "creator": "dc:creator",
        "description": "dc:description",
        "keywords": "cp:keywords",
        "modified": "dcterms:modified",
        "created": "dcterms:created",
    }.items():
        node = root.find(path, NS)
        if node is not None and node.text:
            props[key] = node.text
    return props


def inspect_pptx(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".pptx":
        raise ValueError(f"Expected a .pptx file, got: {path}")

    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        slide_names = sorted(
            [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=_slide_sort_key,
        )
        media = [n for n in names if n.startswith("ppt/media/")]
        notes = [n for n in names if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)]
        masters = [n for n in names if re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", n)]
        layouts = [n for n in names if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)]
        slides = []
        title_counts: dict[str, int] = {}

        for idx, slide_name in enumerate(slide_names, start=1):
            root = _xml_from_zip(zf, slide_name)
            if root is None:
                slides.append({"index": idx, "path": slide_name, "error": "Could not parse XML"})
                continue
            texts = _text_from_tree(root)
            shapes = _shape_info(root)
            title = texts[0] if texts else ""
            if title:
                title_counts[title] = title_counts.get(title, 0) + 1
            picture_count = len(root.findall(".//p:pic", NS))
            graphic_frame_count = len(root.findall(".//p:graphicFrame", NS))
            slide_notes_name = f"ppt/notesSlides/notesSlide{idx}.xml"
            slides.append(
                {
                    "index": idx,
                    "path": slide_name,
                    "title_guess": title,
                    "text_count": len(texts),
                    "text_preview": texts[:12],
                    "shape_count": len(shapes),
                    "picture_count": picture_count,
                    "graphic_frame_count": graphic_frame_count,
                    "has_notes_xml": slide_notes_name in names,
                    "shapes": shapes[:30],
                }
            )

        warnings: list[str] = []
        missing_titles = [s["index"] for s in slides if not s.get("title_guess")]
        if missing_titles:
            warnings.append(f"Slides without title-like first text: {missing_titles}")
        duplicate_titles = sorted([title for title, count in title_counts.items() if count > 1])
        if duplicate_titles:
            warnings.append(f"Duplicate title-like first text values: {duplicate_titles}")
        slides_with_images = [s["index"] for s in slides if s.get("picture_count", 0) > 0]
        if slides_with_images:
            warnings.append(
                "Slides with images need alt-text/manual accessibility review: "
                + ", ".join(map(str, slides_with_images))
            )
        if any(s.get("graphic_frame_count", 0) > 0 for s in slides):
            warnings.append("Slides with tables/charts/graphics need simple structure, labels, and reading-order review.")

        return {
            "file": str(path),
            "size_bytes": path.stat().st_size,
            "slide_count": len(slide_names),
            "layout_count": len(layouts),
            "master_count": len(masters),
            "media_count": len(media),
            "notes_slide_count": len(notes),
            "core_properties": _core_properties(zf),
            "slides": slides,
            "warnings": warnings,
        }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PPTX Inspection Report",
        "",
        f"- File: `{report['file']}`",
        f"- Size: {report['size_bytes']} bytes",
        f"- Slides: {report['slide_count']}",
        f"- Layouts: {report['layout_count']}",
        f"- Masters: {report['master_count']}",
        f"- Media files: {report['media_count']}",
        f"- Notes slides: {report['notes_slide_count']}",
        "",
        "## Core Properties",
    ]
    props = report.get("core_properties") or {}
    if props:
        for key, value in props.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No core properties found.")
    lines += ["", "## Slides"]
    for slide in report["slides"]:
        title = slide.get("title_guess") or "(no title-like text found)"
        lines.append(f"### Slide {slide['index']}: {title}")
        lines.append(f"- Text runs: {slide.get('text_count', 0)}")
        lines.append(f"- Pictures: {slide.get('picture_count', 0)}")
        lines.append(f"- Graphic frames: {slide.get('graphic_frame_count', 0)}")
        lines.append(f"- Notes XML: {slide.get('has_notes_xml', False)}")
        preview = slide.get("text_preview") or []
        if preview:
            lines.append("- Text preview:")
            for item in preview[:8]:
                lines.append(f"  - {item}")
        lines.append("")
    lines.append("## Warnings / Manual Checks")
    warnings = report.get("warnings") or []
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- No structural warnings from this first-pass inspection.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect a .pptx file without modifying it.")
    parser.add_argument("pptx", type=Path, help="Path to .pptx file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true", help="Write JSON report")
    group.add_argument("--markdown", action="store_true", help="Write Markdown report")
    parser.add_argument("--output", "-o", type=Path, help="Optional output path")
    args = parser.parse_args(argv)

    try:
        report = inspect_pptx(args.pptx)
        if args.markdown:
            text = to_markdown(report)
        else:
            text = json.dumps(report, indent=2, ensure_ascii=False)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text)
        return 0
    except Exception as exc:
        print(f"pptx_inspect.py: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
