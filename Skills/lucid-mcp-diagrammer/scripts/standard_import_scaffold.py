"""
standard_import_scaffold.py

Build a minimal, valid Lucid Standard Import JSON payload from a flat list of
nodes and edges. Pass the resulting dict to the Lucid MCP
"Create Lucid Diagram from Specification" tool.

Pure-stdlib. No third-party dependencies. Code Interpreter friendly.

Usage:
    from standard_import_scaffold import build_standard_import

    nodes = [
        {"id": "s1", "text": "Customer submits refund",  "type": "rectangle"},
        {"id": "s2", "text": "Eligible?",                "type": "diamond"},
        {"id": "s3", "text": "Issue refund",             "type": "rectangle"},
        {"id": "s4", "text": "Reject",                   "type": "rectangle"},
    ]
    edges = [
        {"from": "s1", "to": "s2"},
        {"from": "s2", "to": "s3", "text": "Yes"},
        {"from": "s2", "to": "s4", "text": "No"},
    ]
    payload = build_standard_import(
        title="Customer Refund Process",
        nodes=nodes,
        edges=edges,
        product="lucidchart",
        auto_layout=True,
    )

CLI:
    python standard_import_scaffold.py nodes.json edges.json --title "My Diagram"
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

ALLOWED_PRODUCTS = {"lucidchart", "lucidspark"}
DEFAULT_SHAPE_TYPE = "rectangle"


def build_standard_import(
    title: str,
    nodes: Iterable[dict],
    edges: Iterable[dict],
    product: str = "lucidchart",
    auto_layout: bool = True,
    page_title: str = "Page 1",
) -> dict:
    """Return a Standard Import payload as a Python dict."""
    if product not in ALLOWED_PRODUCTS:
        raise ValueError(f"product must be one of {sorted(ALLOWED_PRODUCTS)}")

    shapes = []
    seen_ids: set[str] = set()
    for n in nodes:
        if "id" not in n:
            raise ValueError(f"node missing 'id': {n}")
        if n["id"] in seen_ids:
            raise ValueError(f"duplicate node id: {n['id']}")
        seen_ids.add(n["id"])
        shape = {
            "id": str(n["id"]),
            "type": n.get("type", DEFAULT_SHAPE_TYPE),
            "text": n.get("text", ""),
        }
        if "boundingBox" in n:
            shape["boundingBox"] = n["boundingBox"]
        if "style" in n:
            shape["style"] = n["style"]
        if "data" in n:
            shape["data"] = n["data"]
        shapes.append(shape)

    lines = []
    for e in edges:
        if "from" not in e or "to" not in e:
            raise ValueError(f"edge missing 'from' or 'to': {e}")
        if e["from"] not in seen_ids or e["to"] not in seen_ids:
            raise ValueError(f"edge references unknown node id: {e}")
        line = {
            "endpoint1": {"shapeId": str(e["from"])},
            "endpoint2": {"shapeId": str(e["to"])},
        }
        if "text" in e:
            line["text"] = e["text"]
        if "lineType" in e:
            line["lineType"] = e["lineType"]
        if "style" in e:
            line["style"] = e["style"]
        lines.append(line)

    return {
        "title": title,
        "product": product,
        "autoLayout": bool(auto_layout),
        "pages": [
            {
                "id": "p1",
                "title": page_title,
                "shapes": shapes,
                "lines": lines,
            }
        ],
    }


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build a Lucid Standard Import payload.")
    p.add_argument("nodes_json", help="Path to JSON file with a list of node objects.")
    p.add_argument("edges_json", help="Path to JSON file with a list of edge objects.")
    p.add_argument("--title", default="Untitled Diagram")
    p.add_argument("--product", default="lucidchart", choices=sorted(ALLOWED_PRODUCTS))
    p.add_argument("--no-auto-layout", action="store_true")
    p.add_argument("--out", default="-", help="Output path, or '-' for stdout.")
    args = p.parse_args(argv)

    with open(args.nodes_json, "r", encoding="utf-8") as f:
        nodes = json.load(f)
    with open(args.edges_json, "r", encoding="utf-8") as f:
        edges = json.load(f)

    payload = build_standard_import(
        title=args.title,
        nodes=nodes,
        edges=edges,
        product=args.product,
        auto_layout=not args.no_auto_layout,
    )
    text = json.dumps(payload, indent=2)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
