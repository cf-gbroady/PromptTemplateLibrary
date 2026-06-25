"""
plantuml_sequence_builder.py

Build PlantUML sequence-diagram markup from structured participants and
messages. Pass the result to the Lucid MCP "Create UML Sequence Diagram"
tool.

Pure-stdlib. Code Interpreter friendly.

Participant kinds supported by the Lucid MCP tool:
    participant, actor, boundary, control, entity, database

Arrow styles:
    "sync"   -> "->"
    "reply"  -> "-->"
    "async"  -> "->>"

Group kinds supported:
    alt, else, loop, opt, par, critical, group, note_over, note_left, note_right

Usage:
    from plantuml_sequence_builder import build_plantuml

    participants = [
        {"name": "User",       "kind": "actor"},
        {"name": "Web App",    "kind": "participant", "alias": "App"},
        {"name": "DB",         "kind": "database"},
    ]
    messages = [
        {"from": "User", "to": "App", "text": "Submit form", "arrow": "sync"},
        {"from": "App",  "to": "DB",  "text": "INSERT row",  "arrow": "sync"},
        {"from": "DB",   "to": "App", "text": "OK",          "arrow": "reply"},
        {"from": "App",  "to": "User","text": "Confirmation","arrow": "reply"},
    ]
    print(build_plantuml(participants, messages))
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

VALID_KINDS = {"participant", "actor", "boundary", "control", "entity", "database"}
ARROWS = {"sync": "->", "reply": "-->", "async": "->>"}


def _quote(name: str) -> str:
    return f'"{name}"' if any(c.isspace() for c in name) else name


def build_plantuml(
    participants: Iterable[dict],
    messages: Iterable[dict],
    title: str | None = None,
) -> str:
    lines: list[str] = ["@startuml"]
    if title:
        lines.append(f"title {title}")

    name_to_ref: dict[str, str] = {}
    for p in participants:
        kind = p.get("kind", "participant")
        if kind not in VALID_KINDS:
            raise ValueError(f"invalid participant kind '{kind}'")
        name = p["name"]
        alias = p.get("alias")
        if alias:
            lines.append(f"{kind} {_quote(name)} as {alias}")
            name_to_ref[name] = alias
            name_to_ref[alias] = alias
        else:
            lines.append(f"{kind} {_quote(name)}")
            name_to_ref[name] = _quote(name)

    for m in messages:
        kind = m.get("kind")
        if kind in {"alt", "loop", "opt", "par", "critical", "group"}:
            lines.append(f"{kind} {m.get('label','')}".rstrip())
            continue
        if kind == "else":
            lines.append(f"else {m.get('label','')}".rstrip())
            continue
        if kind == "end":
            lines.append("end")
            continue
        if kind in {"note_over", "note_left", "note_right"}:
            keyword = kind.replace("_", " ")
            target = m.get("target", "")
            text = m.get("text", "")
            lines.append(f"{keyword} {target} : {text}".rstrip())
            continue

        arrow = ARROWS.get(m.get("arrow", "sync"))
        if arrow is None:
            raise ValueError(f"invalid arrow '{m.get('arrow')}'")
        frm = name_to_ref.get(m["from"], _quote(m["from"]))
        to = name_to_ref.get(m["to"], _quote(m["to"]))
        text = m.get("text", "")
        lines.append(f"{frm} {arrow} {to} : {text}".rstrip())

    lines.append("@enduml")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build PlantUML sequence markup.")
    p.add_argument("participants_json", help="JSON file with a list of participants.")
    p.add_argument("messages_json", help="JSON file with a list of messages.")
    p.add_argument("--title", default=None)
    p.add_argument("--out", default="-")
    args = p.parse_args(argv)

    with open(args.participants_json, "r", encoding="utf-8") as f:
        participants = json.load(f)
    with open(args.messages_json, "r", encoding="utf-8") as f:
        messages = json.load(f)

    text = build_plantuml(participants, messages, title=args.title)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
