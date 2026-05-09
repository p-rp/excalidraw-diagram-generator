#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "flowchart-template.excalidraw"
SKILL = ROOT / "SKILL.md"


def fail(message):
    raise AssertionError(message)


def main():
    data = json.loads(TEMPLATE.read_text())
    elements = data["elements"]
    by_id = {element["id"]: element for element in elements}

    ids = set(by_id)
    required_ids = {
        "start-shopping",
        "add-item-decision",
        "view-cart",
        "enter-details",
        "process-payment",
        "order-confirmed",
        "order-completed",
        "payment-error",
    }
    missing = required_ids - ids
    if missing:
        fail(f"flowchart template missing required process/decision nodes: {sorted(missing)}")

    for node_id in ["add-item-decision", "process-payment"]:
        if by_id[node_id]["type"] != "diamond":
            fail(f"{node_id} must be a diamond")

    for element in elements:
        if element["type"] not in {"rectangle", "ellipse", "diamond", "arrow"}:
            continue

        bound_text_ids = [
            item["id"]
            for item in element.get("boundElements", [])
            if item.get("type") == "text"
        ]

        if element["type"] in {"rectangle", "ellipse", "diamond"} and not bound_text_ids:
            fail(f"shape {element['id']} has no bound text")

        for text_id in bound_text_ids:
            text = by_id.get(text_id)
            if not text:
                fail(f"{element['id']} references missing bound text {text_id}")
            if text.get("containerId") != element["id"]:
                fail(f"text {text_id} is not bound back to {element['id']}")
            if text.get("fontFamily") != 5:
                fail(f"text {text_id} does not use Excalifont")

            if element["type"] in {"rectangle", "ellipse", "diamond"}:
                if not (element["x"] <= text["x"] <= element["x"] + element["width"]):
                    fail(f"text {text_id} is horizontally outside {element['id']}")
                if not (element["y"] <= text["y"] <= element["y"] + element["height"]):
                    fail(f"text {text_id} is vertically outside {element['id']}")

    labeled_arrows = [
        element
        for element in elements
        if element["type"] == "arrow"
        and any(item.get("type") == "text" for item in element.get("boundElements", []))
    ]
    if len(labeled_arrows) < 2:
        fail("decision flow must include at least two arrows with bound labels")

    for arrow in [element for element in elements if element["type"] == "arrow"]:
        start_id = arrow.get("startBinding", {}).get("elementId")
        end_id = arrow.get("endBinding", {}).get("elementId")
        if not start_id or not end_id:
            fail(f"arrow {arrow['id']} must bind to both source and target shapes")
        for shape_id in [start_id, end_id]:
            shape = by_id.get(shape_id)
            if not shape:
                fail(f"arrow {arrow['id']} binds to missing shape {shape_id}")
            if not any(item.get("id") == arrow["id"] for item in shape.get("boundElements", [])):
                fail(f"shape {shape_id} does not bind back to arrow {arrow['id']}")

    skill_text = SKILL.read_text()
    required_phrases = [
        "Process flowcharts should use a guided start-to-end layout",
        "Decision flowcharts should use diamond decision nodes",
        "All visible labels must be bound text elements",
        "Arrow labels must be bound to the arrow container itself",
        "Arrows connecting shapes must bind to both shapes",
    ]
    for phrase in required_phrases:
        if phrase not in skill_text:
            fail(f"SKILL.md missing required guidance: {phrase}")


if __name__ == "__main__":
    main()
