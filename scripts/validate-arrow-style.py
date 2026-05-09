#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message):
    raise AssertionError(message)


def main():
    for template in sorted((ROOT / "templates").glob("*.excalidraw")):
        data = json.loads(template.read_text())
        for element in data.get("elements", []):
            if element.get("type") != "arrow":
                continue
            if element.get("roundness") == {"type": 2}:
                fail(f"{template.name}:{element['id']} uses curved arrow roundness")

    skill_text = (ROOT / "SKILL.md").read_text()
    required_skill_phrases = [
        "Prefer elbow arrows for multi-direction connectors",
        "Use curved arrows only when an elbow or straight connector would be less readable",
    ]
    for phrase in required_skill_phrases:
        if phrase not in skill_text:
            fail(f"SKILL.md missing required arrow style guidance: {phrase}")

    add_arrow_text = (ROOT / "scripts" / "add-arrow.py").read_text()
    if '"roundness": None' not in add_arrow_text:
        fail("add-arrow.py must default generated arrows to non-curved roundness")


if __name__ == "__main__":
    main()
